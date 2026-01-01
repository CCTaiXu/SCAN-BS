import os
import sys
import tempfile
from typing import Any, Dict

# Ensure gnn_core is importable
from backend.app.config import GNN_CORE_DIR

# Ensure both gnn_core and its tools/ subdir are importable for graph2vec's absolute imports
if GNN_CORE_DIR not in sys.path:
    sys.path.insert(0, GNN_CORE_DIR)
TOOLS_DIR = os.path.join(GNN_CORE_DIR, "tools")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

try:
    from tools.reentrancy.AutoExtractGraph import generate_graph
    from tools.reentrancy.graph2vec import (
        extract_node_features,
        elimination_node,
        embedding_node,
        elimination_edge,
        embedding_edge,
        construct_vec,
    )
except ImportError as exc:
    raise ImportError(
        "Cannot import preprocessing modules from gnn_core/tools. Check that the repository exists and sys.path is set."
    ) from exc


def solidity_to_graph(solidity_code: str, contract_name: str = "temp.sol") -> Dict[str, Any]:
    """Run gnn_core's preprocessing to turn Solidity source into a GNNSCModel sample dict."""
    with tempfile.TemporaryDirectory() as tmpdir:
        sol_path = os.path.join(tmpdir, contract_name)
        with open(sol_path, "w", encoding="utf-8") as f:
            f.write(solidity_code)

        # 1) Extract node/edge info from Solidity source
        node_feature, edge_feature = generate_graph(sol_path)
        node_feature = sorted(node_feature, key=lambda x: x[0])
        edge_feature = sorted(edge_feature, key=lambda x: (x[2], x[3]))

        # 2) Persist to temp files so graph2vec helpers can reuse their loaders
        node_file = os.path.join(tmpdir, "node.txt")
        edge_file = os.path.join(tmpdir, "edge.txt")
        with open(node_file, "w", encoding="utf-8") as nf:
            for row in node_feature:
                # Fix: Convert lists to comma-separated strings to avoid "['NULL']" format
                formatted_row = []
                for item in row:
                    if isinstance(item, list):
                        formatted_row.append(",".join(map(str, item)))
                    else:
                        formatted_row.append(str(item))
                nf.write(" ".join(formatted_row) + "\n")
        with open(edge_file, "w", encoding="utf-8") as ef:
            for row in edge_feature:
                ef.write(" ".join(map(str, row)) + "\n")

        # 3) graph2vec pipeline to get graph adjacency and node feature vectors
        _, _, node_attr_list = extract_node_features(node_file)
        node_attr_list, _ = elimination_node(node_attr_list)
        _, _, node_embedding, var_embedding = embedding_node(node_attr_list)
        edge_list, _ = elimination_edge(edge_file)
        edge_encode, edge_embedding = embedding_edge(edge_list)
        node_vec, graph_edge = construct_vec(edge_list, node_embedding, var_embedding, edge_embedding, edge_encode)

        corenodes_feature_list = [vec for _, vec in node_vec]

        graph_dict = {
            "targets": "0",  # dummy label; GNNSCModel ignores it during inference
            "graph": graph_edge,
            "contract_name": os.path.basename(contract_name),
            "node_features": corenodes_feature_list,
        }

        return graph_dict
