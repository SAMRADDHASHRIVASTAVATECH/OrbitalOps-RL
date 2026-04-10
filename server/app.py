"""
server/app.py — FastAPI + Gradio Unified Server
================================================
Serves both the OpenEnv API and interactive Gradio UI.
Modern, feature-rich interface for Space Mission Control.
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contextlib import asynccontextmanager
from typing import Optional, Dict, Any
from datetime import datetime

import gradio as gr
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Now these imports will work
from server.space_mission_environment import SpaceMissionEnv
from models import SpaceMissionAction, ObservationResponse, ResetResponse, StepResponse
from tasks.definitions import get_all_mission_ids, get_mission_by_id, MISSIONS


# ========== FastAPI Setup ==========

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic"""
    print("=" * 60)
    print("🚀 SPACE MISSION RL ENVIRONMENT")
    print("=" * 60)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Missions available: {len(get_all_mission_ids())}")
    print(f"🌐 Server running on port: {os.getenv('PORT', 7860)}")
    print("=" * 60)
    yield
    print("\n🛑 Server Shutting Down")
    print(f"📅 Stopped at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


app = FastAPI(
    title="🚀 Space Mission RL Environment",
    description="OpenEnv-compliant Reinforcement Learning environment for space mission control. Train AI agents to make critical decisions in space!",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global environment instance (stateful for session)
env_instance: Optional[SpaceMissionEnv] = None
session_stats: Dict[str, Any] = {
    "total_steps": 0,
    "total_rewards": 0.0,
    "missions_completed": 0,
    "missions_succeeded": 0,
}


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
    global env_instance, session_stats
    
    if env_instance is None:
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")
    
    try:
        action_array = np.array(request.action, dtype=np.int32)
        obs, reward, done, truncated, info = env_instance.step(action_array)
        
        # Update session stats
        session_stats["total_steps"] += 1
        session_stats["total_rewards"] += reward
        
        if done:
            session_stats["missions_completed"] += 1
            if info.get("cumulative_reward", 0) >= 0.6:
                session_stats["missions_succeeded"] += 1
        
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
    return {
        "status": "operational",
        "missions_available": len(get_all_mission_ids()),
        "version": "1.0.0",
        "session_stats": session_stats,
    }


@app.get("/missions")
async def list_missions():
    """List all available missions"""
    missions_list = []
    for mid in get_all_mission_ids():
        mission = get_mission_by_id(mid)
        missions_list.append({
            "id": mid,
            "type": mission["mission_type"],
            "difficulty": mission["difficulty"],
            "description": mission["description"][:100] + "...",
        })
    return {"missions": missions_list, "total": len(missions_list)}


@app.get("/stats")
async def get_stats():
    """Get session statistics"""
    return session_stats


# ========== Custom CSS for Modern UI ==========

CUSTOM_CSS = """
/* Modern Dark Theme */
.gradio-container {
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
}

/* Header Styling */
.header-title {
    text-align: center;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    border: 1px solid #e94560;
    box-shadow: 0 4px 15px rgba(233, 69, 96, 0.3);
}

/* Mission Cards */
.mission-card {
    background: linear-gradient(145deg, #1a1a2e, #16213e);
    border: 1px solid #e94560;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
}

/* Status Indicators */
.status-operational {
    color: #00ff88;
    font-weight: bold;
}

.status-warning {
    color: #ffaa00;
    font-weight: bold;
}

.status-critical {
    color: #ff4444;
    font-weight: bold;
}

/* Buttons */
.primary-btn {
    background: linear-gradient(135deg, #e94560, #ff6b6b) !important;
    border: none !important;
    font-weight: bold !important;
}

.secondary-btn {
    background: linear-gradient(135deg, #0f3460, #16213e) !important;
    border: 1px solid #e94560 !important;
}

/* Score Display */
.score-display {
    font-size: 2em;
    font-weight: bold;
    text-align: center;
    color: #00ff88;
}

/* Telemetry Panel */
.telemetry-panel {
    background: rgba(15, 52, 96, 0.5);
    border: 1px solid #e94560;
    border-radius: 8px;
    padding: 10px;
    font-family: 'Courier New', monospace;
}

/* Animation for active mission */
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 5px #e94560; }
    50% { box-shadow: 0 0 20px #e94560, 0 0 30px #ff6b6b; }
}

.active-mission {
    animation: pulse 2s infinite;
}
"""


# ========== Gradio UI Functions ==========

def get_difficulty_stars(difficulty: int) -> str:
    """Convert difficulty to star rating"""
    filled = "⭐" * difficulty
    empty = "☆" * (5 - difficulty)
    return filled + empty


def get_health_bar(value: float) -> str:
    """Create a visual health bar"""
    filled = int(value * 10)
    bar = "█" * filled + "░" * (10 - filled)
    color = "🟢" if value > 0.7 else "🟡" if value > 0.4 else "🔴"
    return f"{color} [{bar}] {value:.0%}"


def get_fuel_bar(value: float) -> str:
    """Create a visual fuel bar"""
    filled = int(value * 10)
    bar = "█" * filled + "░" * (10 - filled)
    color = "⛽" if value > 0.5 else "⚠️" if value > 0.2 else "🚨"
    return f"{color} [{bar}] {value:.0%}"


def format_mission_briefing(obs, info) -> str:
    """Format mission briefing with rich details"""
    mission_type_icons = {
        "orbit_stabilization": "🛰️",
        "lunar_landing": "🌙",
        "docking_procedure": "🔗",
        "emergency_rescue": "🆘",
        "asteroid_mining": "☄️",
        "solar_storm_evasion": "☀️",
        "satellite_repair": "🔧",
        "mars_transfer": "🔴",
    }
    
    icon = mission_type_icons.get(obs.mission_type, "🚀")
    stars = get_difficulty_stars(obs.difficulty)
    
    briefing = f"""
## {icon} MISSION BRIEFING

### Mission Type: **{obs.mission_type.replace('_', ' ').title()}**

### Difficulty: {stars}

---

### 📋 Objective
{info.get('success_criteria', 'Complete the mission successfully')}

---

### 📡 Current Status
{obs.text}

---

### 📊 Telemetry
| Parameter | Status |
|-----------|--------|
| **Fuel** | {get_fuel_bar(obs.fuel_remaining)} |
| **Health** | {get_health_bar(obs.system_health)} |
| **Position** | `{obs.position}` |
| **Velocity** | `{obs.velocity}` |

---

⚡ **Mission Active - Awaiting Your Command**
"""
    return briefing


def format_step_result(obs, reward: float, done: bool, info: dict) -> str:
    """Format step result with visual feedback"""
    
    # Reward indicator
    if reward >= 0.8:
        reward_icon = "🎯 EXCELLENT"
        reward_color = "green"
    elif reward >= 0.6:
        reward_icon = "✅ GOOD"
        reward_color = "lime"
    elif reward >= 0.4:
        reward_icon = "⚠️ ACCEPTABLE"
        reward_color = "yellow"
    else:
        reward_icon = "❌ POOR"
        reward_color = "red"
    
    # Mission status
    if done:
        cumulative = info.get('cumulative_reward', 0)
        if cumulative >= 0.6:
            status = "## 🎉 MISSION SUCCESSFUL!"
            status_detail = "Excellent work, Commander! Mission objectives achieved."
        else:
            status = "## ⚠️ MISSION COMPLETE"
            status_detail = "Mission ended. Review your decisions for improvement."
    else:
        status = "## 🔄 MISSION IN PROGRESS"
        status_detail = "Awaiting next command..."
    
    result = f"""
{status}

---

### 📊 Action Result

| Metric | Value |
|--------|-------|
| **Step** | {info.get('step', '?')} |
| **Reward** | {reward_icon} ({reward:.2f}) |
| **Cumulative Score** | **{info.get('cumulative_reward', 0):.2f}** |

---

### 📡 Updated Telemetry
| Parameter | Status |
|-----------|--------|
| **Fuel** | {get_fuel_bar(obs.fuel_remaining)} |
| **Health** | {get_health_bar(obs.system_health)} |

---

### 📝 Status Update
{obs.text}

---

{status_detail}
"""
    return result


def gradio_reset(mission_id: str):
    """Gradio wrapper for reset with enhanced output"""
    global env_instance
    
    try:
        env_instance = SpaceMissionEnv(task_id=mission_id if mission_id else None)
        obs, info = env_instance.reset()
        
        briefing = format_mission_briefing(obs, info)
        
        return (
            briefing,
            0.0,
            False,
            "🟢 Mission initialized. Ready for commands.",
            f"Mission: {mission_id}"
        )
    except Exception as e:
        return (
            f"## ❌ Error\n\n{str(e)}",
            0.0,
            False,
            f"🔴 Error: {str(e)}",
            "Error"
        )


def gradio_step(category: str, priority: str, decision: str):
    """Gradio wrapper for step with enhanced output"""
    global env_instance
    
    if env_instance is None:
        return (
            "## ❌ No Active Mission\n\nPlease start a mission first by clicking **🚀 Launch Mission**",
            0.0,
            False,
            "🔴 No active mission",
            "N/A"
        )
    
    try:
        category_idx = SpaceMissionEnv.CATEGORIES.index(category)
        priority_idx = SpaceMissionEnv.PRIORITIES.index(priority)
        decision_idx = SpaceMissionEnv.DECISIONS.index(decision)
        
        action = np.array([category_idx, priority_idx, decision_idx])
        obs, reward, done, truncated, info = env_instance.step(action)
        
        result = format_step_result(obs, reward, done, info)
        
        status_emoji = "🎉" if done and info.get('cumulative_reward', 0) >= 0.6 else "🔄" if not done else "⚠️"
        status_text = f"{status_emoji} Step {info.get('step', '?')} | Reward: {reward:.2f}"
        
        action_text = f"{category}/{priority}/{decision}"
        
        return (
            result,
            info.get('cumulative_reward', 0),
            done,
            status_text,
            action_text
        )
    except Exception as e:
        return (
            f"## ❌ Error\n\n{str(e)}",
            0.0,
            True,
            f"🔴 Error: {str(e)}",
            "Error"
        )


def get_mission_info(mission_id: str) -> str:
    """Get detailed mission information"""
    if not mission_id:
        return "Select a mission to see details."
    
    try:
        mission = get_mission_by_id(mission_id)
        stars = get_difficulty_stars(mission["difficulty"])
        
        return f"""
### 📋 Mission Details

**Type:** {mission["mission_type"].replace('_', ' ').title()}

**Difficulty:** {stars}

**Time Limit:** {mission["time_limit"]}s

**Fuel Budget:** {mission["fuel_budget"]:.0%}

**Success Criteria:**
{mission["success_criteria"]}

---

**Description:**
{mission["description"]}
"""
    except:
        return "Mission details not available."


# ========== Build Gradio Interface ==========

with gr.Blocks(
    title="🚀 Space Mission Control",
    theme=gr.themes.Soft(
        primary_hue="red",
        secondary_hue="blue",
        neutral_hue="slate",
    ),
    css=CUSTOM_CSS,
) as demo:
    
    # Header
    gr.Markdown("""
    <div class="header-title">
    <h1>🚀 SPACE MISSION CONTROL</h1>
    <p>OpenEnv Reinforcement Learning Environment</p>
    <p><em>Make critical decisions. Save the mission. Train AI agents.</em></p>
    </div>
    """)
    
    with gr.Tabs():
        # Main Mission Tab
        with gr.TabItem("🎮 Mission Control", id=1):
            with gr.Row():
                # Left Panel - Mission Selection
                with gr.Column(scale=1):
                    gr.Markdown("### 🎯 Mission Selection")
                    
                    mission_dropdown = gr.Dropdown(
                        choices=get_all_mission_ids(),
                        label="Select Mission",
                        value=get_all_mission_ids()[0],
                        interactive=True,
                    )
                    
                    mission_info = gr.Markdown(
                        value=get_mission_info(get_all_mission_ids()[0]),
                        label="Mission Info"
                    )
                    
                    launch_btn = gr.Button(
                        "🚀 Launch Mission",
                        variant="primary",
                        size="lg",
                    )
                    
                    gr.Markdown("---")
                    
                    # Action Controls
                    gr.Markdown("### 🎛️ Command Interface")
                    
                    category = gr.Radio(
                        choices=SpaceMissionEnv.CATEGORIES,
                        label="📂 Category",
                        value="navigation",
                        info="What type of action to take"
                    )
                    
                    priority = gr.Radio(
                        choices=SpaceMissionEnv.PRIORITIES,
                        label="⚡ Priority",
                        value="medium",
                        info="Urgency level of the action"
                    )
                    
                    decision = gr.Radio(
                        choices=SpaceMissionEnv.DECISIONS,
                        label="🎯 Decision",
                        value="adjust",
                        info="What action to execute"
                    )
                    
                    execute_btn = gr.Button(
                        "⚡ Execute Command",
                        variant="secondary",
                        size="lg",
                    )
                
                # Right Panel - Mission Display
                with gr.Column(scale=2):
                    gr.Markdown("### 📡 Mission Status")
                    
                    status_bar = gr.Textbox(
                        label="Status",
                        value="🟡 Awaiting mission launch...",
                        interactive=False,
                    )
                    
                    last_action = gr.Textbox(
                        label="Last Action",
                        value="N/A",
                        interactive=False,
                    )
                    
                    mission_display = gr.Markdown(
                        value="## 🛸 Welcome, Commander!\n\nSelect a mission and click **🚀 Launch Mission** to begin.\n\n*Your decisions will determine the fate of the crew and spacecraft.*",
                        label="Mission Briefing"
                    )
                    
                    with gr.Row():
                        score_display = gr.Number(
                            label="📊 Cumulative Score",
                            value=0,
                            interactive=False,
                        )
                        done_status = gr.Checkbox(
                            label="✅ Mission Complete",
                            value=False,
                            interactive=False,
                        )
        
        # Missions Catalog Tab
        with gr.TabItem("📚 Mission Catalog", id=2):
            gr.Markdown("## 📚 Available Missions")
            gr.Markdown("Browse all available mission scenarios and their difficulty levels.")
            
            missions_data = []
            for mid in get_all_mission_ids():
                m = get_mission_by_id(mid)
                missions_data.append([
                    mid,
                    m["mission_type"].replace("_", " ").title(),
                    get_difficulty_stars(m["difficulty"]),
                    m["description"][:80] + "...",
                ])
            
            gr.Dataframe(
                headers=["Mission ID", "Type", "Difficulty", "Description"],
                value=missions_data,
                label="All Missions",
            )
        
        # Help Tab
        with gr.TabItem("❓ Help", id=3):
            gr.Markdown("""
## 📖 How to Play

### 🎯 Objective
You are the Mission Control operator. Make critical decisions to ensure mission success and crew safety.

### 🎛️ Controls

**Categories:**
- `system_failure` - Handle malfunctions and emergencies
- `navigation` - Course corrections and positioning
- `resource_management` - Fuel and power management

**Priority Levels:**
- `low` - Routine operations
- `medium` - Standard priority
- `high` - Urgent action required

**Decisions:**
- `continue` - Maintain current operations
- `adjust` - Make corrections
- `abort` - Emergency abort (use sparingly!)

### 📊 Scoring

| Score | Meaning |
|-------|---------|
| 0.8+ | 🎯 Excellent - Perfect execution |
| 0.6+ | ✅ Good - Mission success |
| 0.4+ | ⚠️ Acceptable - Room for improvement |
| <0.4 | ❌ Poor - Critical errors |

### 💡 Tips
1. Read the mission briefing carefully
2. Match your actions to the situation
3. High priority for emergencies
4. Adjust is usually better than continue
5. Abort only in extreme emergencies

---

**Built for the OpenEnv Hackathon** 🚀
""")
    
    # Event Handlers
    mission_dropdown.change(
        fn=get_mission_info,
        inputs=[mission_dropdown],
        outputs=[mission_info],
    )
    
    launch_btn.click(
        fn=gradio_reset,
        inputs=[mission_dropdown],
        outputs=[mission_display, score_display, done_status, status_bar, last_action],
    )
    
    execute_btn.click(
        fn=gradio_step,
        inputs=[category, priority, decision],
        outputs=[mission_display, score_display, done_status, status_bar, last_action],
    )


# ========== Mount Gradio to FastAPI ==========

app = gr.mount_gradio_app(app, demo, path="/")


# ========== Main Entry Point ==========

def main():
    """Main entry point for the server"""
    import uvicorn
    port = int(os.getenv("PORT", 7860))
    print(f"\n🌐 Starting server on http://0.0.0.0:{port}")
    print(f"📚 API Docs available at http://0.0.0.0:{port}/docs")
    print(f"🎮 Gradio UI available at http://0.0.0.0:{port}/\n")
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
