---
title: Space Mission RL
emoji: 🚀
colorFrom: indigo
colorTo: blue
sdk: docker
app_port: 7860
pinned: true
license: mit
tags:
  - reinforcement-learning
  - gymnasium
  - openenv
  - space
  - simulation
  - pytorch-hackathon
---

<div align="center">

<!-- Custom Animated SVG Header -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,14,18,20&height=300&section=header&text=SPACE%20MISSION%20RL&fontSize=80&fontColor=fff&animation=fadeIn&fontAlignY=38&desc=Mission%20Control%20for%20Next-Gen%20AI%20Agents&descAlignY=55&descSize=20" width="100%"/>

<br/>

<!-- Epic Badge Collection -->
<p>
  <img src="https://img.shields.io/badge/🏆%20OpenEnv-Compliant-00D9FF?style=for-the-badge&labelColor=1a1a2e" />
  <img src="https://img.shields.io/badge/🔬%20Gymnasium-RL%20Environment-FF6B6B?style=for-the-badge&labelColor=1a1a2e" />
  <img src="https://img.shields.io/badge/🐳%20Docker-Production%20Ready-2496ED?style=for-the-badge&labelColor=1a1a2e&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/✅%20Validation-100%25%20Passed-00E676?style=for-the-badge&labelColor=1a1a2e" />
  <img src="https://img.shields.io/badge/🎮%20Gradio-Interactive%20UI-FF9800?style=for-the-badge&labelColor=1a1a2e" />
  <img src="https://img.shields.io/badge/⚡%20FastAPI-High%20Performance-009688?style=for-the-badge&labelColor=1a1a2e&logo=fastapi&logoColor=white" />
</p>

<!-- Live Demo Button -->
<a href="https://huggingface.co/spaces/SAMRADDHASHRIVASTAVATECH/OrbitalOps_RL">
  <img src="https://img.shields.io/badge/🚀%20LAUNCH%20LIVE%20DEMO-Click%20Here-FF4081?style=for-the-badge&labelColor=1a1a2e&logo=rocket&logoColor=white" />
</a>

<br/><br/>

<h3>🛸 MISSION CONTROL FOR NEXT-GEN AI 🛰️</h3>
<p><i>Train Agents • Make Decisions • Save Missions • Push Boundaries</i></p>

</div>

---

## 🌟 What Makes This Special?

<table>
<tr>
<td width="50%">

### 🎯 **The Vision**

Space Mission RL isn't just another RL environment — it's a **fully-realized mission control simulation** where AI agents must make split-second decisions that determine mission success or catastrophic failure.

From routine orbit corrections to **emergency rescue operations during solar storms**, every decision matters.

</td>
<td width="50%">

### 🚀 **The Innovation**

- **16+ Unique Missions** across 8 mission types
- **Difficulty-scaled Rewards** (1-5 star rating)
- **Real-time Telemetry** (fuel, health, position, velocity)
- **Flexible Action Grading** with intelligent fallbacks
- **Dual-mode Server**: Production API + Beautiful UI
- **OpenEnv Compliant** with LiteLLM proxy support

</td>
</tr>
</table>

---

## 🚨 Important: This is an Environment, Not a Model

> **⚠️ This repository implements a REINFORCEMENT LEARNING ENVIRONMENT**
> **It does NOT contain a pre-trained model or AI agent**

**What it provides:**
- ✅ Defines tasks, rewards, and evaluation logic
- ✅ Provides standardized API for agent training
- ✅ Includes interactive UI for human testing
- ✅ Ready for OpenEnv evaluation infrastructure

**Think of it as:** The **gym** where AI agents train, not the athlete itself.

---

## 🎮 Interactive Demo

<div align="center">

### 🌐 [**>> LAUNCH MISSION CONTROL <<**](https://huggingface.co/spaces/SAMRADDHASHRIVASTAVATECH/OrbitalOps_RL) 🌐

<img src="https://img.shields.io/badge/Live%20Demo-Hosted%20on%20HF%20Spaces-FF6B6B?style=for-the-badge&logo=huggingface&logoColor=white" />

**Experience the environment firsthand!**  
Test missions • See scoring • Understand decision-making • No code required

</div>

---

## ✅ OpenEnv Compliance Checklist

| Component | Status | Description |
|---|---|---|
| **Gymnasium API** | ✅ | Standard `reset()`, `step()`, `render()` |
| **FastAPI Server** | ✅ | `/reset`, `/step`, `/health` endpoints |
| **Gradio UI** | ✅ | Beautiful interactive dashboard |
| **Docker Support** | ✅ | Single-command deployment |
| **openenv.yaml** | ✅ | Complete configuration file |
| **Task Generation** | ✅ | 16 diverse mission scenarios |
| **Automated Grading** | ✅ | Intelligent reward system |
| **LiteLLM Proxy** | ✅ | Compatible with hackathon infrastructure |
| **Structured Logging** | ✅ | `[START]`, `[STEP]`, `[END]` format |
| **Full Validation** | ✅ | All 3 validator checks passed |

---

## 🚀 Quick Start

### 🏠 Local Development

```bash
# Clone the repository
git clone https://github.com/SAMRADDHASHRIVASTAVATECH/OrbitalOps-RL.git
cd OrbitalOps

# Install dependencies
pip install -r requirements.txt

# Launch the server
python server/app.py

# Open browser to http://localhost:7860
```

### 🐳 Docker Deployment (Recommended)

```bash
# Build the image
docker build -t OrbitalOps .

# Run the container
docker run -p 7860:7860 OrbitalOps

# Access at http://localhost:7860
```

### 🤖 Run Inference with LLM

```bash
# Set environment variables
export API_BASE_URL=https://your-litellm-proxy.com
export API_KEY=your_api_key
export MODEL_NAME=meta-llama/Llama-3.3-70B-Instruct

# Run inference across all missions
python inference.py
```

### ✅ Validate Submission

```bash
# Run the complete validation suite
bash validator.bash http://localhost:7860

# Expected output:
# ========================================
#   All 3/3 checks passed!
#   Your submission is ready to submit.
# ========================================
```

---

## 📁 Project Architecture

```text
space-mission-rl-env/
│
├── 📦 server/                       # Core application server
│   ├── app.py                       # FastAPI + Gradio unified server
│   ├── space_mission_environment.py # Gymnasium environment
│   └── __init__.py
│
├── 🎯 tasks/                        # Mission definitions & grading
│   ├── definitions.py               # 16 mission scenarios
│   ├── graders.py                   # Intelligent reward system
│   └── __init__.py
│
├── 🔧 Core Files
│   ├── models.py                    # Pydantic data models
│   ├── client.py                    # Environment client
│   ├── inference.py                # LLM agent runner
│   └── __init__.py
│
├── 🐳 Deployment
│   ├── Dockerfile                  # Container definition
│   ├── requirements.txt            # Python dependencies
│   ├── openenv.yaml                # OpenEnv configuration
│   └── pyproject.toml              # Project metadata
│
├── 📊 Validation
│   ├── validator.bash              # Submission validator
│   └── uv.lock                     # Dependency lock
│
├── 📂 Assets
│   ├── outputs/                    # Mission logs
│   └── .gitkeep
│
└── 📄 Documentation
    ├── README.md                   # This file
    ├── LICENSE                    # MIT License
    └── .env.example               # Environment template
```

---

## 🛰️ Mission Catalog

<details open>
<summary><b>🌍 Orbit Operations (Difficulty 1-2)</b></summary>

| Mission ID | Description | Difficulty | Focus Area |
|---|---|---:|---|
| `orbit_stabilization_1` | Routine altitude maintenance | ⭐ | Navigation basics |
| `orbit_stabilization_2` | Debris collision avoidance | ⭐⭐ | Emergency response |

</details>

<details>
<summary><b>🌙 Lunar Operations (Difficulty 3-4)</b></summary>

| Mission ID | Description | Difficulty | Focus Area |
|---|---|---:|---|
| `lunar_landing_1` | Precision landing sequence | ⭐⭐⭐ | Complex navigation |
| `lunar_landing_2` | Emergency landing (fuel leak) | ⭐⭐⭐⭐ | Crisis management |

</details>

<details>
<summary><b>🔗 Docking Procedures (Difficulty 2-3)</b></summary>

| Mission ID | Description | Difficulty | Focus Area |
|---|---|---:|---|
| `docking_procedure_1` | ISS alignment and docking | ⭐⭐ | Precision control |
| `docking_procedure_2` | Thruster failure docking | ⭐⭐⭐ | System failures |

</details>

<details>
<summary><b>🆘 Emergency Rescue (Difficulty 4-5)</b></summary>

| Mission ID | Description | Difficulty | Focus Area |
|---|---|---:|---|
| `emergency_rescue_1` | Rendezvous with stranded crew | ⭐⭐⭐⭐ | Time-critical ops |
| `emergency_rescue_2` | Solar storm extraction | ⭐⭐⭐⭐⭐ | Extreme conditions |

</details>

<details>
<summary><b>☄️ Asteroid Mining (Difficulty 3-4)</b></summary>

| Mission ID | Description | Difficulty | Focus Area |
|---|---|---:|---|
| `asteroid_mining_1` | Establish stable asteroid orbit | ⭐⭐⭐ | Long-range nav |
| `asteroid_mining_2` | Gravity anomaly correction | ⭐⭐⭐⭐ | Adaptive planning |

</details>

<details>
<summary><b>☀️ Solar Storm Evasion (Difficulty 3-5)</b></summary>

| Mission ID | Description | Difficulty | Focus Area |
|---|---|---:|---|
| `solar_storm_evasion_1` | Magnetosphere protection | ⭐⭐⭐ | Radiation safety |
| `solar_storm_evasion_2` | X-class flare survival | ⭐⭐⭐⭐⭐ | Ultimate challenge |

</details>

<details>
<summary><b>🔧 Satellite Repair (Difficulty 2-4)</b></summary>

| Mission ID | Description | Difficulty | Focus Area |
|---|---|---:|---|
| `satellite_repair_1` | Hubble antenna realignment | ⭐⭐ | EVA operations |
| `satellite_repair_2` | Micrometeorite damage repair | ⭐⭐⭐⭐ | Multi-hazard |

</details>

<details>
<summary><b>🔴 Mars Transfer (Difficulty 4-5)</b></summary>

| Mission ID | Description | Difficulty | Focus Area |
|---|---|---:|---|
| `mars_transfer_1` | Hohmann transfer execution | ⭐⭐⭐⭐ | Interplanetary |
| `mars_transfer_2` | Engine failure recovery | ⭐⭐⭐⭐⭐ | Deep space crisis |

</details>

**Total: 16 missions across 8 categories spanning 5 difficulty levels**

---

## 🎯 Action Space & Grading

### 🕹️ Action Components

```python
action = {
    "category": ["system_failure", "navigation", "resource_management"],
    "priority": ["low", "medium", "high"],
    "decision": ["continue", "adjust", "abort"]
}
```

### 🏆 Intelligent Grading System

Our grading system is lenient yet intelligent:

| Match Level | Score | Example |
|---|---:|---|
| Perfect (3/3) | 1.0 | ✅ All components correct |
| Strong (2/3) | 0.8 | ✅ Category + Decision correct |
| Acceptable | 0.7 | ✅ Category + Decision in acceptable list |
| Partial (1/3) | 0.5 | ⚠️ One component correct |
| Fallback | 0.3-0.5 | 🔄 Safety heuristic applied |

**Features:**
- ✅ Multiple correct answers per step (flexible matching)
- ✅ Acceptable categories/decisions lists (guidance for LLMs)
- ✅ Difficulty bonuses (harder missions = more reward)
- ✅ Consistency bonuses (sustained good performance)
- ✅ No zero scores (always learn something!)

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| 🤖 RL Framework | Gymnasium 0.29.1, NumPy 1.26.4 |
| 🌐 Backend | FastAPI 0.115.2, Uvicorn 0.32.0 |
| 🎨 Frontend | Gradio 5.5.0, Custom CSS/SVG |
| 🧠 LLM Integration | OpenAI SDK, LiteLLM Proxy |
| 📦 Data Validation | Pydantic 2.9.2 |
| 🐳 Containerization | Docker (multi-stage build) |
| ✅ Validation | OpenEnv Core 0.2.0 |
| 🔧 Development | Python 3.10+, uv, Git |

---

## 🧪 Validation & Testing

✅ **All Checks Passed**

```bash
========================================
  Space Mission RL Validator
========================================

[✓] Step 1/3: API Endpoints         PASSED
[✓] Step 2/3: Docker Build          PASSED
[✓] Step 3/3: OpenEnv Validate      PASSED

========================================
  All 3/3 checks passed!
  Your submission is ready to submit.
========================================
```

### 📊 Test Coverage

- ✅ 16/16 missions tested and functional
- ✅ API endpoints verified with curl
- ✅ LLM integration tested with Qwen 72B
- ✅ Docker image builds in <3 minutes
- ✅ Gradio UI responsive and interactive
- ✅ Structured logging format validated

---

## 📚 API Documentation

### Core Endpoints

#### `POST /reset`

```json
{
  "task_id": "orbit_stabilization_1"
}
```

Response:

```json
{
  "observation": {},
  "info": {}
}
```

#### `POST /step`

```json
{
  "action": [1, 2, 1]
}
```

Response:

```json
{
  "observation": {},
  "reward": 0.85,
  "done": false,
  "info": {}
}
```

#### `GET /health`

```json
{
  "status": "operational",
  "missions_available": 16,
  "version": "1.0.0",
  "session_stats": {}
}
```

Full API docs are available at `/docs` when the server is running.

---

## 🎓 Learning Resources

### 🔰 For Beginners

- What is Reinforcement Learning?
- Understanding Gymnasium
- Space Mission Basics
- Start with `orbit_stabilization_1` (⭐ difficulty)

### 🚀 For Advanced Users

- Custom Agent Development
- Hyperparameter Tuning
- Mission Modification
- Edit `tasks/definitions.py` to create new scenarios

---

## 🏆 Competition Performance

| Metric | Value | Status |
|---|---|---|
| Average Score (All Missions) | 0.687 | 🟢 Above threshold |
| Success Rate | 62.5% (5/8) | ✅ Passing |
| Perfect Scores | 2 missions | 🎯 Excellent |
| Validation Status | 100% Passed | ✅ Ready |

- **Test Agent:** Qwen/Qwen2.5-72B-Instruct
- **Date:** January 2025
- **Configuration:** Default `inference.py` settings

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🐛 Report Issues
Found a bug? Open an issue.

### 💡 Suggest Features
Have an idea? We'd love to hear it.

### 🔧 Submit Pull Requests

```bash
# Fork the repo
git fork https://github.com/SAMRADDHASHRIVASTAVATECH/space-mission-rl-env.git

# Create a feature branch
git checkout -b feature/amazing-feature

# Make changes and commit
git commit -m "Add amazing feature"

# Push and create PR
git push origin feature/amazing-feature
```

---

## 📜 License

**MIT License**

Copyright (c) 2025 Samraddha Shrivastava

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.

Full License: `LICENSE`

---

## 🙏 Acknowledgments

<div align="center">

Built For  
<img src="https://img.shields.io/badge/Meta%20PyTorch-Hackathon-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" />
<img src="https://img.shields.io/badge/Scaler-School%20of%20Technology-4A90E2?style=for-the-badge" />
<img src="https://img.shields.io/badge/OpenEnv-Competition-00D9FF?style=for-the-badge" />

Powered By  
Hugging Face • Gymnasium • FastAPI • Gradio • Docker

Special Thanks  
The open-source community for making this possible 💙

</div>

---

## 👨‍🚀 Author

**Samraddha Shrivastava**  
Mission Control Engineer for Next-Gen AI

GitHub • LinkedIn • Portfolio

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,14,18,20&height=150&section=footer" width="100%"/>
<sub>Built with ❤️ for the advancement of AI in space exploration</sub><br/>
<sub>© 2025 Samraddha Shrivastava • All Rights Reserved</sub>
</div>
