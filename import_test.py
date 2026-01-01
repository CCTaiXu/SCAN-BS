import sys, traceback
from backend.app.config import GNN_CORE_DIR
print("GNN_CORE_DIR:", GNN_CORE_DIR)
sys.path.insert(0, GNN_CORE_DIR)
try:
    from tools.reentrancy.AutoExtractGraph import generate_graph
    print("IMPORT_OK")
except Exception:
    traceback.print_exc()
