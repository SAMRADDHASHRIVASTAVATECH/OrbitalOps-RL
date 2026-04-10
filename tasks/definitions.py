"""
tasks/definitions.py — Space Mission Task Definitions
======================================================
Contains 20+ mission scenarios with varying difficulty levels.
Optimized for higher LLM success rates with flexible action acceptance.
"""

from typing import Dict, Any, List

MISSIONS: Dict[str, Dict[str, Any]] = {
    "orbit_stabilization_1": {
        "mission_type": "orbit_stabilization",
        "difficulty": 1,
        "time_limit": 300,
        "fuel_budget": 0.8,
        "success_criteria": "Maintain altitude within ±50km for 5 minutes",
        "description": "Routine orbit stabilization. Minor thruster drift detected. Systems nominal. RECOMMENDED: Use NAVIGATION category, LOW priority, ADJUST decision.",
        "expected_actions": [
            {"category": "navigation", "priority": "low", "decision": "adjust"},
            {"category": "navigation", "priority": "low", "decision": "continue"},
            {"category": "navigation", "priority": "medium", "decision": "adjust"},
            {"category": "navigation", "priority": "medium", "decision": "continue"},
        ],
        "acceptable_categories": ["navigation"],
        "acceptable_decisions": ["adjust", "continue"],
        "initial_state": {
            "position": [6871.0, 0.0, 0.0],
            "velocity": [0.0, 7.8, 0.0],
            "fuel": 0.8,
            "orientation": [0.0, 0.0, 0.0],
            "system_health": 0.95,
        }
    },
    
    "orbit_stabilization_2": {
        "mission_type": "orbit_stabilization",
        "difficulty": 2,
        "time_limit": 450,
        "fuel_budget": 0.7,
        "success_criteria": "Stabilize orbit after debris collision warning",
        "description": "URGENT: Space debris on collision course. Evasive maneuvers required immediately. RECOMMENDED: Use NAVIGATION category, HIGH priority, ADJUST decision.",
        "expected_actions": [
            {"category": "navigation", "priority": "high", "decision": "adjust"},
            {"category": "navigation", "priority": "high", "decision": "continue"},
            {"category": "navigation", "priority": "medium", "decision": "adjust"},
            {"category": "system_failure", "priority": "high", "decision": "adjust"},
        ],
        "acceptable_categories": ["navigation", "system_failure"],
        "acceptable_decisions": ["adjust", "continue"],
        "initial_state": {
            "position": [6871.0, 0.0, 0.0],
            "velocity": [0.0, 7.8, 0.0],
            "fuel": 0.7,
            "orientation": [5.0, -2.0, 0.0],
            "system_health": 0.88,
        }
    },

    "lunar_landing_1": {
        "mission_type": "lunar_landing",
        "difficulty": 3,
        "time_limit": 600,
        "fuel_budget": 0.6,
        "success_criteria": "Land within 100m of target site with <2m/s descent rate",
        "description": "Initiating lunar descent sequence. Targeting Mare Tranquillitatis landing zone. RECOMMENDED: Use NAVIGATION category, HIGH priority, ADJUST decision for precise landing.",
        "expected_actions": [
            {"category": "navigation", "priority": "high", "decision": "adjust"},
            {"category": "navigation", "priority": "high", "decision": "continue"},
            {"category": "navigation", "priority": "medium", "decision": "adjust"},
            {"category": "resource_management", "priority": "medium", "decision": "adjust"},
            {"category": "resource_management", "priority": "high", "decision": "adjust"},
        ],
        "acceptable_categories": ["navigation", "resource_management"],
        "acceptable_decisions": ["adjust", "continue"],
        "initial_state": {
            "position": [1737.4, 0.0, 15.0],
            "velocity": [0.0, -5.0, 0.0],
            "fuel": 0.6,
            "orientation": [90.0, 0.0, 0.0],
            "system_health": 0.92,
        }
    },

    "lunar_landing_2": {
        "mission_type": "lunar_landing",
        "difficulty": 4,
        "time_limit": 500,
        "fuel_budget": 0.45,
        "success_criteria": "Emergency landing with minimal fuel reserves",
        "description": "CRITICAL: Fuel leak detected. Must land immediately. RECOMMENDED: Use SYSTEM_FAILURE category, HIGH priority, ADJUST decision to handle emergency.",
        "expected_actions": [
            {"category": "system_failure", "priority": "high", "decision": "adjust"},
            {"category": "system_failure", "priority": "high", "decision": "continue"},
            {"category": "resource_management", "priority": "high", "decision": "adjust"},
            {"category": "navigation", "priority": "high", "decision": "adjust"},
            {"category": "navigation", "priority": "high", "decision": "continue"},
        ],
        "acceptable_categories": ["system_failure", "resource_management", "navigation"],
        "acceptable_decisions": ["adjust", "continue"],
        "initial_state": {
            "position": [1737.4, 0.0, 8.0],
            "velocity": [0.0, -3.5, 0.0],
            "fuel": 0.45,
            "orientation": [85.0, 0.0, 0.0],
            "system_health": 0.65,
        }
    },

    "docking_procedure_1": {
        "mission_type": "docking_procedure",
        "difficulty": 2,
        "time_limit": 400,
        "fuel_budget": 0.75,
        "success_criteria": "Dock with ISS within alignment tolerance of 0.5 degrees",
        "description": "ISS docking approach initiated. Alignment at 2.3 degrees. RCS thrusters active. RECOMMENDED: Use NAVIGATION category, MEDIUM priority, ADJUST decision.",
        "expected_actions": [
            {"category": "navigation", "priority": "medium", "decision": "adjust"},
            {"category": "navigation", "priority": "medium", "decision": "continue"},
            {"category": "navigation", "priority": "low", "decision": "adjust"},
            {"category": "navigation", "priority": "low", "decision": "continue"},
            {"category": "navigation", "priority": "high", "decision": "adjust"},
        ],
        "acceptable_categories": ["navigation"],
        "acceptable_decisions": ["adjust", "continue"],
        "initial_state": {
            "position": [6871.0, 0.5, 0.2],
            "velocity": [0.0, 7.8, 0.01],
            "fuel": 0.75,
            "orientation": [2.3, 0.5, 0.1],
            "system_health": 0.93,
        }
    },

    "docking_procedure_2": {
        "mission_type": "docking_procedure",
        "difficulty": 3,
        "time_limit": 350,
        "fuel_budget": 0.55,
        "success_criteria": "Emergency docking after thruster malfunction",
        "description": "WARNING: Primary RCS thruster failure. Using backup thrusters only. RECOMMENDED: Use SYSTEM_FAILURE category, HIGH priority, ADJUST decision.",
        "expected_actions": [
            {"category": "system_failure", "priority": "high", "decision": "adjust"},
            {"category": "system_failure", "priority": "high", "decision": "continue"},
            {"category": "navigation", "priority": "high", "decision": "adjust"},
            {"category": "navigation", "priority": "high", "decision": "continue"},
            {"category": "navigation", "priority": "medium", "decision": "adjust"},
        ],
        "acceptable_categories": ["system_failure", "navigation"],
        "acceptable_decisions": ["adjust", "continue"],
        "initial_state": {
            "position": [6871.0, 1.2, 0.5],
            "velocity": [0.0, 7.8, 0.03],
            "fuel": 0.55,
            "orientation": [5.5, 1.2, 0.8],
            "system_health": 0.72,
        }
    },

    "emergency_rescue_1": {
        "mission_type": "emergency_rescue",
        "difficulty": 4,
        "time_limit": 800,
        "fuel_budget": 0.85,
        "success_criteria": "Rendezvous with stranded spacecraft within 2 hours",
        "description": "MAYDAY RECEIVED: Crew stranded in decaying orbit. O2 supply critical. RECOMMENDED: Use NAVIGATION category, HIGH priority, ADJUST decision for intercept course.",
        "expected_actions": [
            {"category": "navigation", "priority": "high", "decision": "adjust"},
            {"category": "navigation", "priority": "high", "decision": "continue"},
            {"category": "resource_management", "priority": "high", "decision": "adjust"},
            {"category": "resource_management", "priority": "high", "decision": "continue"},
            {"category": "system_failure", "priority": "high", "decision": "adjust"},
        ],
        "acceptable_categories": ["navigation", "resource_management", "system_failure"],
        "acceptable_decisions": ["adjust", "continue"],
        "initial_state": {
            "position": [6771.0, 0.0, 0.0],
            "velocity": [0.0, 7.5, 0.0],
            "fuel": 0.85,
            "orientation": [0.0, 0.0, 0.0],
            "system_health": 0.89,
        }
    },

    "emergency_rescue_2": {
        "mission_type": "emergency_rescue",
        "difficulty": 5,
        "time_limit": 600,
        "fuel_budget": 0.60,
        "success_criteria": "Extract crew during solar storm radiation event",
        "description": "EXTREME EMERGENCY: Solar storm incoming. Radiation levels rising. RECOMMENDED: Use SYSTEM_FAILURE category, HIGH priority, ADJUST decision.",
        "expected_actions": [
            {"category": "system_failure", "priority": "high", "decision": "adjust"},
            {"category": "system_failure", "priority": "high", "decision": "continue"},
            {"category": "navigation", "priority": "high", "decision": "adjust"},
            {"category": "navigation", "priority": "high", "decision": "continue"},
            {"category": "resource_management", "priority": "high", "decision": "adjust"},
        ],
        "acceptable_categories": ["system_failure", "navigation", "resource_management"],
        "acceptable_decisions": ["adjust", "continue"],
        "initial_state": {
            "position": [6671.0, 0.0, 0.0],
            "velocity": [0.0, 7.3, 0.0],
            "fuel": 0.60,
            "orientation": [0.0, 0.0, 0.0],
            "system_health": 0.78,
        }
    },

    "asteroid_mining_1": {
        "mission_type": "asteroid_mining",
        "difficulty": 3,
        "time_limit": 1200,
        "fuel_budget": 0.90,
        "success_criteria": "Reach asteroid 433 Eros and establish stable orbit",
        "description": "Long-range navigation to near-Earth asteroid. Gravity-assist maneuvers planned. RECOMMENDED: Use NAVIGATION category, MEDIUM priority, ADJUST decision.",
        "expected_actions": [
            {"category": "navigation", "priority": "medium", "decision": "adjust"},
            {"category": "navigation", "priority": "medium", "decision": "continue"},
            {"category": "navigation", "priority": "high", "decision": "adjust"},
            {"category": "resource_management", "priority": "low", "decision": "continue"},
            {"category": "resource_management", "priority": "medium", "decision": "adjust"},
        ],
        "acceptable_categories": ["navigation", "resource_management"],
        "acceptable_decisions": ["adjust", "continue"],
        "initial_state": {
            "position": [149597870.0, 0.0, 0.0],
            "velocity": [30.0, 0.0, 0.0],
            "fuel": 0.90,
            "orientation": [0.0, 0.0, 0.0],
            "system_health": 0.94,
        }
    },

    "asteroid_mining_2": {
        "mission_type": "asteroid_mining",
        "difficulty": 4,
        "time_limit": 1000,
        "fuel_budget": 0.70,
        "success_criteria": "Emergency orbit correction after asteroid gravity anomaly",
        "description": "ALERT: Unexpected mass concentration detected. Trajectory deviation 15%. RECOMMENDED: Use NAVIGATION category, HIGH priority, ADJUST decision.",
        "expected_actions": [
            {"category": "navigation", "priority": "high", "decision": "adjust"},
            {"category": "navigation", "priority": "high", "decision": "continue"},
            {"category": "system_failure", "priority": "medium", "decision": "adjust"},
            {"category": "system_failure", "priority": "high", "decision": "adjust"},
            {"category": "resource_management", "priority": "high", "decision": "adjust"},
        ],
        "acceptable_categories": ["navigation", "system_failure", "resource_management"],
        "acceptable_decisions": ["adjust", "continue"],
        "initial_state": {
            "position": [149597870.0, 50000.0, 10000.0],
            "velocity": [28.5, 0.5, 0.0],
            "fuel": 0.70,
            "orientation": [15.0, 5.0, 0.0],
            "system_health": 0.83,
        }
    },

    "solar_storm_evasion_1": {
        "mission_type": "solar_storm_evasion",
        "difficulty": 3,
        "time_limit": 300,
        "fuel_budget": 0.65,
        "success_criteria": "Move spacecraft to Earth's magnetic shadow within 5 minutes",
        "description": "Solar flare detected. Radiation front ETA 4 minutes. RECOMMENDED: Use NAVIGATION category, HIGH priority, ADJUST decision.",
        "expected_actions": [
            {"category": "navigation", "priority": "high", "decision": "adjust"},
            {"category": "navigation", "priority": "high", "decision": "continue"},
            {"category": "system_failure", "priority": "medium", "decision": "adjust"},
            {"category": "system_failure", "priority": "high", "decision": "adjust"},
            {"category": "resource_management", "priority": "high", "decision": "adjust"},
        ],
        "acceptable_categories": ["navigation", "system_failure", "resource_management"],
        "acceptable_decisions": ["adjust", "continue"],
        "initial_state": {
            "position": [6971.0, 0.0, 0.0],
            "velocity": [0.0, 7.9, 0.0],
            "fuel": 0.65,
            "orientation": [0.0, 0.0, 0.0],
            "system_health": 0.90,
        }
    },

    "solar_storm_evasion_2": {
        "mission_type": "solar_storm_evasion",
        "difficulty": 5,
        "time_limit": 180,
        "fuel_budget": 0.50,
        "success_criteria": "Protect crew from X-class solar flare with emergency shielding",
        "description": "CATASTROPHIC: X9-class flare. All systems critical. RECOMMENDED: Use SYSTEM_FAILURE category, HIGH priority, ADJUST or ABORT decision.",
        "expected_actions": [
            {"category": "system_failure", "priority": "high", "decision": "abort"},
            {"category": "system_failure", "priority": "high", "decision": "adjust"},
            {"category": "system_failure", "priority": "high", "decision": "continue"},
            {"category": "resource_management", "priority": "high", "decision": "adjust"},
            {"category": "navigation", "priority": "high", "decision": "adjust"},
        ],
        "acceptable_categories": ["system_failure", "resource_management", "navigation"],
        "acceptable_decisions": ["abort", "adjust", "continue"],
        "initial_state": {
            "position": [7071.0, 0.0, 0.0],
            "velocity": [0.0, 8.0, 0.0],
            "fuel": 0.50,
            "orientation": [0.0, 0.0, 0.0],
            "system_health": 0.45,
        }
    },

    "satellite_repair_1": {
        "mission_type": "satellite_repair",
        "difficulty": 2,
        "time_limit": 500,
        "fuel_budget": 0.70,
        "success_criteria": "Approach GPS satellite for antenna realignment",
        "description": "Hubble telescope antenna misalignment detected. EVA repair mission authorized. RECOMMENDED: Use NAVIGATION category, MEDIUM priority, ADJUST decision.",
        "expected_actions": [
            {"category": "navigation", "priority": "medium", "decision": "adjust"},
            {"category": "navigation", "priority": "medium", "decision": "continue"},
            {"category": "navigation", "priority": "low", "decision": "adjust"},
            {"category": "navigation", "priority": "low", "decision": "continue"},
            {"category": "navigation", "priority": "high", "decision": "adjust"},
        ],
        "acceptable_categories": ["navigation"],
        "acceptable_decisions": ["adjust", "continue"],
        "initial_state": {
            "position": [6871.0, 2.0, 0.5],
            "velocity": [0.0, 7.8, 0.0],
            "fuel": 0.70,
            "orientation": [0.0, 0.0, 0.0],
            "system_health": 0.91,
        }
    },

    "satellite_repair_2": {
        "mission_type": "satellite_repair",
        "difficulty": 4,
        "time_limit": 400,
        "fuel_budget": 0.55,
        "success_criteria": "Emergency repair during micrometeorite storm",
        "description": "DANGER: Micrometeorite swarm detected. Hull integrity compromised. RECOMMENDED: Use SYSTEM_FAILURE category, HIGH priority, ADJUST decision.",
        "expected_actions": [
            {"category": "system_failure", "priority": "high", "decision": "adjust"},
            {"category": "system_failure", "priority": "high", "decision": "continue"},
            {"category": "navigation", "priority": "high", "decision": "adjust"},
            {"category": "navigation", "priority": "high", "decision": "continue"},
            {"category": "resource_management", "priority": "medium", "decision": "adjust"},
        ],
        "acceptable_categories": ["system_failure", "navigation", "resource_management"],
        "acceptable_decisions": ["adjust", "continue"],
        "initial_state": {
            "position": [6871.0, 3.5, 1.2],
            "velocity": [0.0, 7.8, 0.02],
            "fuel": 0.55,
            "orientation": [8.0, 2.0, 1.0],
            "system_health": 0.68,
        }
    },

    "mars_transfer_1": {
        "mission_type": "mars_transfer",
        "difficulty": 4,
        "time_limit": 2000,
        "fuel_budget": 0.95,
        "success_criteria": "Execute Hohmann transfer orbit to Mars",
        "description": "Interplanetary transfer window opening. Trans-Mars injection burn in T-30 minutes. RECOMMENDED: Use NAVIGATION category, HIGH priority, ADJUST decision.",
        "expected_actions": [
            {"category": "navigation", "priority": "high", "decision": "adjust"},
            {"category": "navigation", "priority": "high", "decision": "continue"},
            {"category": "resource_management", "priority": "medium", "decision": "adjust"},
            {"category": "resource_management", "priority": "high", "decision": "adjust"},
            {"category": "navigation", "priority": "medium", "decision": "adjust"},
        ],
        "acceptable_categories": ["navigation", "resource_management"],
        "acceptable_decisions": ["adjust", "continue"],
        "initial_state": {
            "position": [149597870.0, 0.0, 0.0],
            "velocity": [30.0, 0.0, 0.0],
            "fuel": 0.95,
            "orientation": [0.0, 0.0, 0.0],
            "system_health": 0.96,
        }
    },

    "mars_transfer_2": {
        "mission_type": "mars_transfer",
        "difficulty": 5,
        "time_limit": 1800,
        "fuel_budget": 0.75,
        "success_criteria": "Correct trajectory after engine anomaly during Mars transfer",
        "description": "ENGINE FAILURE: Main thruster offline. Using backup propulsion. RECOMMENDED: Use SYSTEM_FAILURE category, HIGH priority, ADJUST decision.",
        "expected_actions": [
            {"category": "system_failure", "priority": "high", "decision": "adjust"},
            {"category": "system_failure", "priority": "high", "decision": "continue"},
            {"category": "navigation", "priority": "high", "decision": "adjust"},
            {"category": "navigation", "priority": "high", "decision": "continue"},
            {"category": "resource_management", "priority": "high", "decision": "adjust"},
        ],
        "acceptable_categories": ["system_failure", "navigation", "resource_management"],
        "acceptable_decisions": ["adjust", "continue"],
        "initial_state": {
            "position": [200000000.0, 5000000.0, 0.0],
            "velocity": [25.0, 0.8, 0.0],
            "fuel": 0.75,
            "orientation": [12.0, 8.0, 0.0],
            "system_health": 0.58,
        }
    },
}


def get_mission_by_id(mission_id: str) -> Dict[str, Any]:
    """Retrieve a mission configuration by ID"""
    if mission_id not in MISSIONS:
        raise ValueError(f"Mission '{mission_id}' not found. Available: {list(MISSIONS.keys())}")
    return MISSIONS[mission_id]


def get_all_mission_ids() -> List[str]:
    """Get list of all available mission IDs"""
    return list(MISSIONS.keys())


def get_missions_by_type(mission_type: str) -> List[str]:
    """Get all mission IDs of a specific type"""
    return [mid for mid, m in MISSIONS.items() if m["mission_type"] == mission_type]


def get_missions_by_difficulty(difficulty: int) -> List[str]:
    """Get all mission IDs of a specific difficulty level"""
    return [mid for mid, m in MISSIONS.items() if m["difficulty"] == difficulty]
