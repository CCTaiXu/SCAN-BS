from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, constr

from backend.app.auth import (
    create_user,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from backend.app.inference import VulnDetector, ModelLoadError
from backend.app.preprocess import solidity_to_graph

app = FastAPI(title="Smart Contract Vulnerability Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

detector = VulnDetector()


class RegisterRequest(BaseModel):
    username: constr(min_length=3, max_length=32)
    password: constr(min_length=6, max_length=64)


class LoginRequest(BaseModel):
    username: constr(min_length=3, max_length=32)
    password: constr(min_length=6, max_length=64)


@app.post("/api/auth/register")
async def register(payload: RegisterRequest):
    user = create_user(payload.username, payload.password)
    token = create_access_token({"sub": payload.username})
    return {"user": user, "access_token": token, "token_type": "bearer"}


@app.post("/api/auth/login")
async def login(payload: LoginRequest):
    user = authenticate_user(payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    token = create_access_token({"sub": payload.username})
    return {"user": user, "access_token": token, "token_type": "bearer"}


@app.get("/api/auth/me")
async def me(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}


@app.post("/api/detect")
async def detect_vuln(
    code: str = Form(None),
    file: UploadFile = File(None),
    current_user: dict = Depends(get_current_user),
):
    if file is not None:
        content = await file.read()
        solidity_code = content.decode("utf-8")
    elif code is not None:
        solidity_code = code
    else:
        return {"error": "No Solidity code provided."}

    graph_data = solidity_to_graph(solidity_code)

    try:
        pred, prob = detector.predict(graph_data)
    except ModelLoadError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Inference failed: {exc}") from exc

    label_map = {
        0: "No Vulnerability",
        1: "Vulnerable",
    }

    # Calculate confidence
    # prob is [P(Vulnerable), P(Safe)] based on inference.py: return pred, [prob, 1.0 - prob]
    # If pred == 1 (Vulnerable), confidence is prob[0]
    # If pred == 0 (Safe), confidence is prob[1]
    
    confidence = 0.0
    if isinstance(prob, list) or isinstance(prob, tuple):
        # prob[0] is P(Vulnerable), prob[1] is P(Safe)
        if pred == 1:
            confidence = prob[0]
        else:
            confidence = prob[1]
    else:
        # If prob is a single float, it's P(Vulnerable)
        if pred == 1:
            confidence = prob
        else:
            confidence = 1.0 - prob

    result = {
        "prediction": label_map.get(pred, str(pred)),
        "raw_pred": int(pred),
        "probabilities": float(prob) if isinstance(prob, (float, int)) else [float(p) for p in prob],
        "confidence": float(confidence),
        "vulnerabilities": []
    }

    if pred == 1:
        result["vulnerabilities"].append({
            "type": "Reentrancy",
            "description": "Detected potential reentrancy vulnerability. The contract performs an external call before updating its state, which violates the Checks-Effects-Interactions pattern.",
            "severity": "High"
        })

    return result
