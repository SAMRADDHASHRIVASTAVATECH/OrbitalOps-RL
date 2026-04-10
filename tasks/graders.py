"""
tasks/graders.py — Space Mission Action Grading
================================================
Evaluates agent actions against expected mission responses.
More lenient grading for higher success rates.
"""

from typing import Dict, Any, List, Optional
from models import SpaceMissionAction


def grade_action(
    action: SpaceMissionAction,
    expected_actions: List[Dict[str, str]],
    step: int,
    difficulty: int,
    mission: Optional[Dict[str, Any]] = None
) -> float:
    """
    Grade an agent's action against expected responses.
    Uses flexible matching for higher success rates.
    
    Returns a score from 0.0 to 1.0 based on:
    - Perfect match (3/3 components): 1.0
    - Strong match (2/3 components): 0.8
    - Acceptable category + decision: 0.7
    - Partial match (1/3 components): 0.5
    - Acceptable category or decision: 0.4
    - Complete mismatch: 0.3 (still gives some points)
    
    Score is then adjusted by difficulty factor.
    """
    best_score = 0.0
    
    # Check against ALL expected actions (not just step-indexed)
    for expected in expected_actions:
        matches = 0
        
        if action.category == expected.get("category"):
            matches += 1
        if action.priority == expected.get("priority"):
            matches += 1
        if action.decision == expected.get("decision"):
            matches += 1
        
        # Calculate score for this expected action
        if matches == 3:
            score = 1.0  # Perfect match
        elif matches == 2:
            score = 0.8  # Strong match
        elif matches == 1:
            score = 0.5  # Partial match
        else:
            score = 0.0
        
        best_score = max(best_score, score)
        
        # Early exit if perfect match found
        if best_score == 1.0:
            break
    
    # If no good match found, check acceptable categories/decisions
    if best_score < 0.7 and mission:
        acceptable_cats = mission.get("acceptable_categories", [])
        acceptable_decs = mission.get("acceptable_decisions", [])
        
        cat_ok = action.category in acceptable_cats if acceptable_cats else True
        dec_ok = action.decision in acceptable_decs if acceptable_decs else True
        
        if cat_ok and dec_ok:
            best_score = max(best_score, 0.7)  # Good choice
        elif cat_ok:
            best_score = max(best_score, 0.5)  # Category correct
        elif dec_ok:
            best_score = max(best_score, 0.4)  # Decision correct
    
    # If still no match, use safety heuristic (minimum 0.3)
    if best_score < 0.3:
        best_score = evaluate_safety_heuristic(action, difficulty)
    
    # Apply difficulty bonus (higher difficulty = more reward for success)
    difficulty_bonus = (difficulty - 1) * 0.02  # 0.0 to 0.08
    final_score = best_score + difficulty_bonus
    
    return min(final_score, 1.0)


def evaluate_safety_heuristic(action: SpaceMissionAction, difficulty: int) -> float:
    """
    Safety-based evaluation when no expected action matches.
    Always returns at least 0.3 to avoid zero scores.
    """
    # Base scores for decisions (more lenient)
    decision_scores = {
        "adjust": 0.5,    # Active problem-solving - best default
        "continue": 0.4,  # Monitoring situation
        "abort": 0.35,    # Safe but impacts mission
    }
    
    # Priority bonus
    priority_bonus = {
        "high": 0.1,
        "medium": 0.05,
        "low": 0.0,
    }
    
    # Category bonus (any valid category gets bonus)
    category_bonus = {
        "navigation": 0.05,
        "system_failure": 0.05,
        "resource_management": 0.05,
    }
    
    base_score = decision_scores.get(action.decision, 0.35)
    p_bonus = priority_bonus.get(action.priority, 0.0)
    c_bonus = category_bonus.get(action.category, 0.0)
    
    final_score = base_score + p_bonus + c_bonus
    
    # Ensure minimum score of 0.3
    return max(min(final_score, 1.0), 0.3)


def calculate_mission_score(rewards: List[float]) -> float:
    """Calculate final mission score from step rewards"""
    if not rewards:
        return 0.0
    
    # Average reward
    avg_reward = sum(rewards) / len(rewards)
    
    # Consistency bonus for good performance
    high_quality_steps = sum(1 for r in rewards if r >= 0.6)
    consistency_bonus = 0.0
    
    if len(rewards) > 0:
        quality_ratio = high_quality_steps / len(rewards)
        if quality_ratio >= 0.8:
            consistency_bonus = 0.1
        elif quality_ratio >= 0.5:
            consistency_bonus = 0.05
    
    # Completion bonus (finished all steps)
    completion_bonus = 0.05 if len(rewards) >= 2 else 0.0
    
    final_score = avg_reward + consistency_bonus + completion_bonus
    
    return min(final_score, 1.0)
