"""
server/space_mission_environment.py — Space Mission Gymnasium Environment
==========================================================================
Core RL environment implementing OpenAI Gym interface.
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import Dict, Any, Optional, Tuple, List

from models import SpaceMissionAction, ObservationResponse, SpacecraftState
from tasks.definitions import get_mission_by_id, get_all_mission_ids
from tasks.graders import grade_action


class SpaceMissionEnv(gym.Env):
    """
    Space Mission Control RL Environment
    
    Observation Space:
        Dict with mission telemetry and text description
    
    Action Space:
        MultiDiscrete([3, 3, 3]) representing:
        - category: [system_failure, navigation, resource_management]
        - priority: [low, medium, high]
        - decision: [continue, adjust, abort]
    
    Reward:
        0.0 to 1.0 based on action quality and mission difficulty
    """
    
    metadata = {"render_modes": ["human", "rgb_array"]}
    
    CATEGORIES = ["system_failure", "navigation", "resource_management"]
    PRIORITIES = ["low", "medium", "high"]
    DECISIONS = ["continue", "adjust", "abort"]
    
    def __init__(self, task_id: Optional[str] = None):
        super().__init__()
        
        self.action_space = spaces.MultiDiscrete([3, 3, 3])
        self.observation_space = spaces.Dict({
            "difficulty": spaces.Discrete(5, start=1),
            "fuel_remaining": spaces.Box(0.0, 1.0, shape=(), dtype=np.float32),
            "system_health": spaces.Box(0.0, 1.0, shape=(), dtype=np.float32),
        })
        
        self.current_mission: Optional[Dict[str, Any]] = None
        self.current_step: int = 0
        self.max_steps: int = 10
        self.step_rewards: List[float] = []
        self.task_id = task_id
    
    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
    ) -> Tuple[ObservationResponse, dict]:
        """Reset environment and load a new mission"""
        super().reset(seed=seed)
        
        # Select mission
        if self.task_id:
            mission_id = self.task_id
        elif options and "task_id" in options:
            mission_id = options["task_id"]
        else:
            all_missions = get_all_mission_ids()
            mission_id = self.np_random.choice(all_missions)
        
        self.current_mission = get_mission_by_id(mission_id)
        self.current_step = 0
        self.step_rewards = []
        
        # Build observation
        initial_state = self.current_mission["initial_state"]
        obs = ObservationResponse(
            mission_type=self.current_mission["mission_type"],
            difficulty=self.current_mission["difficulty"],
            fuel_remaining=initial_state["fuel"],
            position=list(initial_state["position"]),
            velocity=list(initial_state["velocity"]),
            system_health=initial_state["system_health"],
            text=self.current_mission["description"],
        )
        
        info = {
            "mission_id": mission_id,
            "success_criteria": self.current_mission["success_criteria"],
            "time_limit": self.current_mission["time_limit"],
        }
        
        return obs, info
    
    def step(self, action: np.ndarray) -> Tuple[ObservationResponse, float, bool, bool, dict]:
        """Execute one step in the environment"""
        if self.current_mission is None:
            raise RuntimeError("Environment not initialized. Call reset() first.")
        
        # Parse action
        category_idx, priority_idx, decision_idx = action
        space_action = SpaceMissionAction(
            category=self.CATEGORIES[category_idx],
            priority=self.PRIORITIES[priority_idx],
            decision=self.DECISIONS[decision_idx],
        )
        
        # Grade action
        expected_actions = self.current_mission.get("expected_actions", [])
        reward = grade_action(
            space_action,
            expected_actions,
            self.current_step,
            self.current_mission["difficulty"]
        )
        
        self.step_rewards.append(reward)
        self.current_step += 1
        
        # Check termination
        done = (
            self.current_step >= self.max_steps or
            space_action.decision == "abort" or
            self.current_step >= len(expected_actions)
        )
        
        # Update observation
        current_state = self.current_mission["initial_state"]
        obs = ObservationResponse(
            mission_type=self.current_mission["mission_type"],
            difficulty=self.current_mission["difficulty"],
            fuel_remaining=max(0.0, current_state["fuel"] - 0.05 * self.current_step),
            position=list(current_state["position"]),
            velocity=list(current_state["velocity"]),
            system_health=max(0.0, current_state["system_health"] - 0.02 * self.current_step),
            text=f"Step {self.current_step}: Action {space_action.decision} executed.",
        )
        
        info = {
            "step": self.current_step,
            "action_taken": space_action.model_dump(),
            "cumulative_reward": sum(self.step_rewards),
        }
        
        return obs, reward, done, False, info
    
    def render(self):
        """Render the environment (optional)"""
        if self.current_mission:
            print(f"Mission: {self.current_mission['mission_type']}")
            print(f"Step: {self.current_step}/{self.max_steps}")
            print(f"Cumulative Reward: {sum(self.step_rewards):.2f}")
    
    def close(self):
        """Clean up resources"""
        pass