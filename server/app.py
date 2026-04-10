"""
server/app.py — FastAPI + Gradio Unified Server
================================================
Serves both the OpenEnv API and interactive Gradio UI.
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contextlib import asynccontextmanager
from typing import Optional

import gradio as gr
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Now these imports will work
from server.space_mission_environment import SpaceMissionEnv
from models import SpaceMissionAction, ObservationResponse, ResetResponse, StepResponse
from tasks.definitions import get_all_mission_ids


# ========== FastAPI Setup ==========

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic"""
    print("🚀 Space Mission RL Environment - Server Starting")
    yield
    print("🛑 Server Shutting Down")


app = FastAPI(
    title="Space Mission RL Environment",
    description="OpenEnv-compliant RL environment for space mission control",
    version="1.0.0",
    lifespan=lifespan,
)

# Global environment instance (stateful for session)
env_instance: Optional[SpaceMissionEnv] = None


class ResetRequest(BaseModel):
    task_id: Optional[str] = None


class StepRequest(BaseModel):
    action: list[int]  # [category_idx, priority_idx, decision_idx]


@app.post("/reset", response_model=ResetResponse)
async def reset(request: ResetRequest = ResetRequest()):
    """Reset the environment and start a new mission"""
    global env_instance
    
    env_instance = SpaceMissionEnv(task_id=request.task_id)
    obs, info = env_instance.reset()
    
    return ResetResponse(observation=obs, info=info)


@app.post("/step", response_model=StepResponse)
async def step(request: StepRequest):
    """Execute one step in the environment"""
    global env_instance
    
    if env_instance is None:
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")
    
    try:
        action_array = np.array(request.action, dtype=np.int32)
        obs, reward, done, truncated, info = env_instance.step(action_array)
        
        return StepResponse(
            observation=obs,
            reward=reward,
            done=done,
            info=info,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "operational", "missions_available": len(get_all_mission_ids())}


# ========== Gradio UI ==========

def gradio_reset(mission_id: str):
    """Gradio wrapper for reset"""
    global env_instance
    env_instance = SpaceMissionEnv(task_id=mission_id if mission_id else None)
    obs, info = env_instance.reset()
    
    return (
        f"**Mission:** {obs.mission_type}\n"
        f"**Difficulty:** {obs.difficulty}/5\n"
        f"**Briefing:** {obs.text}\n\n"
        f"**Success Criteria:** {info['success_criteria']}"
    )


def gradio_step(category: str, priority: str, decision: str):
    """Gradio wrapper for step"""
    global env_instance
    
    if env_instance is None:
        return "❌ Please reset the environment first!", 0.0, False
    
    category_idx = SpaceMissionEnv.CATEGORIES.index(category)
    priority_idx = SpaceMissionEnv.PRIORITIES.index(priority)
    decision_idx = SpaceMissionEnv.DECISIONS.index(decision)
    
    action = np.array([category_idx, priority_idx, decision_idx])
    obs, reward, done, truncated, info = env_instance.step(action)
    
    result = (
        f"**Step {info['step']}**\n"
        f"Reward: {reward:.2f}\n"
        f"Cumulative: {info['cumulative_reward']:.2f}\n"
        f"Status: {obs.text}\n"
        f"Fuel: {obs.fuel_remaining:.1%} | Health: {obs.system_health:.1%}"
    )
    
    return result, info['cumulative_reward'], done


with gr.Blocks(title="🚀 Space Mission Control") as demo:
    gr.Markdown("# 🚀 Space Mission Control RL Environment")
    gr.Markdown("Test mission scenarios and see how your decisions affect outcomes.")
    
    with gr.Row():
        mission_dropdown = gr.Dropdown(
            choices=get_all_mission_ids(),
            label="Select Mission",
            value=get_all_mission_ids()[0]
        )
        reset_btn = gr.Button("🔄 Start Mission", variant="primary")
    
    mission_status = gr.Markdown("Click 'Start Mission' to begin")
    
    with gr.Row():
        category = gr.Radio(
            choices=SpaceMissionEnv.CATEGORIES,
            label="Category",
            value="navigation"
        )
        priority = gr.Radio(
            choices=SpaceMissionEnv.PRIORITIES,
            label="Priority",
            value="medium"
        )
        decision = gr.Radio(
            choices=SpaceMissionEnv.DECISIONS,
            label="Decision",
            value="continue"
        )
    
    execute_btn = gr.Button("Execute Action", variant="secondary")
    
    step_result = gr.Markdown()
    score_display = gr.Number(label="Cumulative Score", value=0)
    done_status = gr.Checkbox(label="Mission Complete", value=False)
    
    reset_btn.click(
        fn=gradio_reset,
        inputs=[mission_dropdown],
        outputs=[mission_status]
    )
    
    execute_btn.click(
        fn=gradio_step,
        inputs=[category, priority, decision],
        outputs=[step_result, score_display, done_status]
    )


# ========== Mount Gradio to FastAPI ==========

app = gr.mount_gradio_app(app, demo, path="/")


# ========== Main Entry Point ==========

def main():
    """Main entry point for the server"""
    import uvicorn
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()