import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
GNN_CORE_DIR = os.path.join(PROJECT_ROOT, "gnn_core")
# GNNSCModel expects a pickle checkpoint. You can override via env MODEL_PATH.
MODEL_PATH = os.environ.get(
	"MODEL_PATH",
	os.path.join(GNN_CORE_DIR, "saved_models", "model_best.pickle"),
)
TMP_DIR = os.path.join(PROJECT_ROOT, "tmp")
os.makedirs(TMP_DIR, exist_ok=True)

# Auth / storage
DB_PATH = os.environ.get("AUTH_DB_PATH", os.path.join(PROJECT_ROOT, "users.db"))
JWT_SECRET = os.environ.get("JWT_SECRET", "dev-secret-change-me")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(os.environ.get("JWT_EXPIRE_MINUTES", "720"))
