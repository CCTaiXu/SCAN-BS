import sys
from typing import Dict, Any, Optional

import numpy as np
import tensorflow as tf

from backend.app.config import GNN_CORE_DIR, MODEL_PATH

# Ensure gnn_core is importable
if GNN_CORE_DIR not in sys.path:
    sys.path.insert(0, GNN_CORE_DIR)

try:
    from GNNSCModel import GNNSCModel
except ImportError as exc:
    raise ImportError(
        "Cannot import GNNSCModel from gnn_core. Check that the repository is present and sys.path is set correctly."
    ) from exc


class ModelLoadError(RuntimeError):
    """Raised when model weights cannot be loaded."""


class VulnDetector:
    """Wrap GNNSCModel (TensorFlow 1.x) for inference."""

    def __init__(self):
        self.model: Optional[GNNSCModel] = None
        self.load_error: Optional[BaseException] = None

    def _build_model(self):
        # Minimal arg set to instantiate GNNSCModel; adjust if you customize config.
        args: Dict[str, Any] = {
            '--config-file': None,
            '--config': None,
            '--log_dir': '.',
            '--data_dir': GNN_CORE_DIR,
            '--random_seed': 9930,
            '--thresholds': 0.3,
            '--restore': MODEL_PATH,
            '--restrict_data': None,
            '--freeze-graph-model': False,
        }
        model = GNNSCModel(args)
        # GNNSCModel.__init__ will call restore_model if --restore is provided.
        return model

    def load(self) -> GNNSCModel:
        """Lazy-load the model so the API can start even if weights are missing."""
        if self.model is None and self.load_error is None:
            try:
                self.model = self._build_model()
            except Exception as exc:  # noqa: BLE001
                self.load_error = exc
        if self.load_error is not None:
            raise ModelLoadError(f"Failed to load model from {MODEL_PATH}: {self.load_error}") from self.load_error
        return self.model

    def predict(self, raw_graph: Dict[str, Any]):
        """
        raw_graph: dict with keys graph, node_features, targets, contract_name
        (same structure as entries in train_data/*.json).
        """
        model = self.load()

        # Convert raw graph to model-ready structures
        processed_graphs, _ = model.process_raw_graphs([raw_graph], is_training_data=False)
        batch_iter = model.make_minibatch_iterator(processed_graphs, is_training=False)
        batch = next(batch_iter)
        batch[model.placeholders['out_layer_dropout_keep_prob']] = 1.0

        # Run sigmoid outputs
        fetch = [model.ops['new_computed_values']]  # sigmoid(logits)
        probs = model.sess.run(fetch, feed_dict=batch)[0]
        prob = float(np.squeeze(probs)) if probs.size == 1 else float(np.mean(probs))
        pred = 1 if prob >= model.threshold else 0
        return pred, [prob, 1.0 - prob]
