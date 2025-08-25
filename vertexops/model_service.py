import uuid
import json
import time
import threading
from typing import Dict, Any
from pathlib import Path

MODELS_FILE = Path("vertexops/models.json")

class ModelService:
    def __init__(self):
        self._lock = threading.Lock()
        # Load or init
        if MODELS_FILE.exists():
            try:
                self._models = json.loads(MODELS_FILE.read_text())
            except Exception:
                self._models = {}
        else:
            self._models = {}
            self._persist()

    def _persist(self):
        with self._lock:
            MODELS_FILE.write_text(json.dumps(self._models, indent=2))

    def deploy_model(self, model_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
        model_id = f"model-{uuid.uuid4().hex[:8]}"
        entry = {
            "model_id": model_id,
            "model_type": model_type,
            "config": config,
            "status": "deploying",
            "created_at": time.time(),
            "message": "Starting deployment"
        }
        with self._lock:
            self._models[model_id] = entry
            self._persist()

        # Simulate async deployment in background
        threading.Thread(target=self._finish_deploy, args=(model_id,), daemon=True).start()
        return entry

    def _finish_deploy(self, model_id):
        time.sleep(2)  # simulate some work
        with self._lock:
            if model_id in self._models:
                self._models[model_id]["status"] = "deployed"
                self._models[model_id]["message"] = "Deployment succeeded (simulated)"
                self._persist()

    def get_status(self, model_id: str):
        with self._lock:
            return self._models.get(model_id)

    def fine_tune(self, model_id: str, dataset_uri: str) -> Dict[str, Any]:
        job_id = f"finetune-{uuid.uuid4().hex[:8]}"
        job = {"job_id": job_id, "model_id": model_id, "dataset_uri": dataset_uri, "status": "running", "started_at": time.time()}
        # store job under model if needed
        def _run():
            time.sleep(3)
            with self._lock:
                if model_id in self._models:
                    ver = self._models[model_id].get("version", 0) + 1
                    self._models[model_id]["version"] = ver
                    self._models[model_id]["status"] = "deployed"
                    self._models[model_id]["last_finetune_job"] = job_id
                    self._persist()
            job["status"] = "succeeded"
        threading.Thread(target=_run, daemon=True).start()
        return job
