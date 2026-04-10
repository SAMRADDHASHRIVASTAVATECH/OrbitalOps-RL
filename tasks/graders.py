"""
tasks/graders.py — Space Mission Action Grading
================================================
Evaluates agent actions against expected mission responses.
"""

from typing import Dict, Any
from models import SpaceMissionAction


def grade_action(
    action: SpaceMissionAction,
    expected_actions: list[Dict[str, str]],
    step: int,
    difficulty: int
) -> float:
    """
    Grade an agent's action against expected responses.
    
    Returns a score from 0.0 to 1.0 based on:
    - Perfect match: 1.0
    - Partial match (2/3 components): 0.6
    - Weak match (1/3 components): 0.3
    - Complete mismatch: 0.0
    
    Score is then multiplied by difficulty factor.
    """
    if step >= len(expected_actions):
        # No expected action for this step - evaluate based on general safety
        return evaluate_safety_heuristic(action, difficulty)
    
    expected = expected_actions[step]
    matches = 0
    
    if action.category == expected.get("category"):
        matches += 1
    if action.priority == expected.get("priority"):
        matches += 1
    if action.decision == expected.get("decision"):
        matches += 1
    
    # Base score
    if matches == 3:
        base_score = 1.0  # Perfect
    elif matches == 2:
        base_score = 0.6  # Partial
    elif matches == 1:
        base_score = 0.3  # Weak
    else:
        base_score = 0.0  # Mismatch
    
    # Apply difficulty multiplier
    difficulty_factor = 1.0 + (difficulty - 1) * 0.1  # 1.0 to 1.4
    final_score = base_score * difficulty_factor
    
    return min(final_score, 1.0)


def evaluate_safety_heuristic(action: SpaceMissionAction, difficulty: int) -> float:
    """
    Safety-based evaluation when no expected action exists.
    Penalizes risky decisions in high-difficulty scenarios.
    """
    safety_scores = {
        "abort": 0.5,      # Safe but mission failure
        "continue": 0.7,   # Moderate risk
        "adjust": 0.9,     # Active problem-solving
    }
    
    priority_bonus = {
        "low": 0.0,
        "medium": 0.05,
        "high": 0.1,
    }
    
    base_score = safety_scores.get(action.decision, 0.5)
    bonus = priority_bonus.get(action.priority, 0.0)
    
    # In high-difficulty missions, penalize passive actions
    if difficulty >= 4 and action.decision == "continue":
        base_score *= 0.7
    
    return min(base_score + bonus, 1.0)


def calculate_mission_score(rewards: list[float]) -> float:
    """Calculate final mission score from step rewards"""
    if not rewards:
        return 0.0
    
    # Average reward with slight bonus for consistency
    avg_reward = sum(rewards) / len(rewards)
    consistency_bonus = 0.0
    
    # Bonus if most rewards are above 0.5
    high_quality_steps = sum(1 for r in rewards if r >= 0.5)
    if high_quality_steps >= len(rewards) * 0.7:
        consistency_bonus = 0.1
    
    return min(avg_reward + consistency_bonus, 1.0)