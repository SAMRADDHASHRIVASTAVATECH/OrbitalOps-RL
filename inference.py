#!/usr/bin/env python3
"""
inference.py — Space Mission OpenEnv Agent
===========================================
Runs an LLM agent through space mission tasks and emits structured stdout logs.

Required environment variables:
    API_BASE_URL      LLM API endpoint
    MODEL_NAME        Model identifier
    HF_TOKEN          HuggingFace / API key
    LOCAL_IMAGE_NAME  (optional) Docker image to launch as env server

Stdout format (must not deviate):
    [START] task=<task> env=space_mission model=<model>
    [STEP]  step=<n> action=<action> reward=<0.00> done=<true|false> error=<msg|null>
    [END]   success=<true|false> steps=<n> score=<0.000> rewards=<r1,r2,...>
"""

import os
import textwrap
from typing import List, Optional

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

from models import SpaceMissionAction
from client import SpaceMissionClient
from tasks.definitions import get_all_mission_ids

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

IMAGE_NAME   = os.getenv("LOCAL_IMAGE_NAME")
API_KEY      = os.getenv("HF_TOKEN") or os.getenv("API_KEY")

API_BASE_URL = os.getenv("API_BASE_URL", "https://api-inference.huggingface.co/v1")
MODEL_NAME   = os.getenv("MODEL_NAME",   "Qwen/Qwen2.5-72B-Instruct")
ENV_BASE_URL = os.getenv("ENV_BASE_URL", "http://localhost:8000")
BENCHMARK    = "space_mission"

MAX_STEPS              = 10
SUCCESS_SCORE_THRESHOLD = 0.6
TEMPERATURE            = 0.3
MAX_TOKENS             = 1024

TASKS = get_all_mission_ids()[:8]  # Run first 8 missions

SYSTEM_PROMPT = textwrap.dedent("""
    You are Mission Control for a spacecraft. You receive telemetry and must make critical decisions.
    
    Choose ONE action from these components:
    
    CATEGORY: system_failure | navigation | resource_management
    PRIORITY: low | medium | high
    DECISION: continue | adjust | abort
    
    Reply in this EXACT format:
    category: <choice>
    priority: <choice>
    decision: <choice>
    
    No other text. No explanation.
""").strip()

# ---------------------------------------------------------------------------
# Logging helpers
# ---------------------------------------------------------------------------

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val  = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True,
    )

# ---------------------------------------------------------------------------
# LLM call
# ---------------------------------------------------------------------------

def get_model_action(
    client: OpenAI,
    observation: str,
    history: List[str],
) -> SpaceMissionAction:
    """Ask LLM to decide action"""
    history_block = "\n".join(history[-3:]) if history else "None"
    user_prompt = (
        f"Mission status:\n{observation}\n\n"
        f"Previous actions:\n{history_block}\n\n"
        f"Your decision:"
    )
    
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        
        text = (completion.choices[0].message.content or "").strip().lower()
        
        # Parse response
        lines = [l.strip() for l in text.split("\n") if ":" in l]
        parsed = {}
        for line in lines:
            key, val = line.split(":", 1)
            parsed[key.strip()] = val.strip()
        
        return SpaceMissionAction(
            category=parsed.get("category", "navigation"),
            priority=parsed.get("priority", "medium"),
            decision=parsed.get("decision", "continue"),
        )
    
    except Exception as exc:
        print(f"[DEBUG] Model error: {exc}", flush=True)
        return SpaceMissionAction(
            category="navigation",
            priority="medium",
            decision="continue"
        )

# ---------------------------------------------------------------------------
# Single task runner
# ---------------------------------------------------------------------------

def run_task(client: OpenAI, task_name: str) -> None:
    """Run one full episode"""
    
    if IMAGE_NAME:
        env_instance = SpaceMissionClient.from_docker_image(IMAGE_NAME, task=task_name)
    else:
        env_instance = SpaceMissionClient(base_url=ENV_BASE_URL)
    
    history: List[str] = []
    rewards: List[float] = []
    steps_taken   = 0
    score         = 0.0
    success       = False
    last_error: Optional[str] = None
    
    log_start(task=task_name, env=BENCHMARK, model=MODEL_NAME)
    
    try:
        with env_instance.sync() as env:
            if not IMAGE_NAME:
                result = env.reset(task_id=task_name)
            else:
                result = env.reset()
            
            observation = result.observation
            done = False
            
            for step in range(1, MAX_STEPS + 1):
                if done:
                    break
                
                action = get_model_action(client, observation.text, history)
                
                try:
                    result = env.step(action)
                    last_error = None
                except Exception as exc:
                    last_error = str(exc)
                    done = True
                    result.reward = 0.0
                
                reward = result.reward or 0.0
                done = result.done
                
                rewards.append(reward)
                steps_taken = step
                
                action_str = f"{action.category}/{action.priority}/{action.decision}"
                log_step(step=step, action=action_str, reward=reward, done=done, error=last_error)
                history.append(f"Step {step}: {action_str} → {reward:.2f}")
                
                observation = result.observation
        
        score = sum(rewards) / len(rewards) if rewards else 0.0
        score = max(0.001, min(score, 0.999))
        success = score >= SUCCESS_SCORE_THRESHOLD
    
    except Exception as exc:
        print(f"[DEBUG] Task {task_name} error: {exc}", flush=True)
        last_error = str(exc)
    
    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    for task_name in TASKS:
        run_task(client, task_name)


if __name__ == "__main__":
    main()