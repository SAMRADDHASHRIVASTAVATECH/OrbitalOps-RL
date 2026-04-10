"""
client.py — Environment Client for Remote/Local Interaction
============================================================
"""

import requests
import subprocess
import time
from typing import Optional, Dict, Any
from contextlib import contextmanager

from models import SpaceMissionAction, ResetResponse, StepResponse, ObservationResponse


class SpaceMissionClient:
    """Client for interacting with Space Mission RL environment"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
    
    def reset(self, task_id: Optional[str] = None) -> ResetResponse:
        """Reset environment"""
        response = self.session.post(
            f"{self.base_url}/reset",
            json={"task_id": task_id}
        )
        response.raise_for_status()
        return ResetResponse(**response.json())
    
    def step(self, action: SpaceMissionAction) -> StepResponse:
        """Execute action"""
        # Convert action to indices
        from server.space_mission_environment import SpaceMissionEnv
        category_idx = SpaceMissionEnv.CATEGORIES.index(action.category)
        priority_idx = SpaceMissionEnv.PRIORITIES.index(action.priority)
        decision_idx = SpaceMissionEnv.DECISIONS.index(action.decision)
        
        response = self.session.post(
            f"{self.base_url}/step",
            json={"action": [category_idx, priority_idx, decision_idx]}
        )
        response.raise_for_status()
        return StepResponse(**response.json())
    
    @contextmanager
    def sync(self):
        """Context manager for session management"""
        try:
            yield self
        finally:
            self.session.close()
    
    @classmethod
    def from_docker_image(cls, image_name: str, task: Optional[str] = None, port: int = 8000):
        """Launch environment from Docker image and return client"""
        container_name = f"space-mission-env-{int(time.time())}"
        
        subprocess.run([
            "docker", "run", "-d",
            "--name", container_name,
            "-p", f"{port}:7860",
            image_name
        ], check=True)
        
        # Wait for server to be ready
        time.sleep(5)
        
        client = cls(base_url=f"http://localhost:{port}")
        return client