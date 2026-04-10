from typing import Literal, Optional, List, Tuple
from pydantic import BaseModel, Field


class SpacecraftState(BaseModel):
    """Real-time spacecraft telemetry"""
    position: Tuple[float, float, float] = Field(description="[x, y, z] coordinates in km")
    velocity: Tuple[float, float, float] = Field(description="[vx, vy, vz] in km/s")
    fuel: float = Field(ge=0.0, le=1.0, description="Fuel percentage (0.0 to 1.0)")
    orientation: Tuple[float, float, float] = Field(description="[pitch, yaw, roll] in degrees")
    system_health: float = Field(ge=0.0, le=1.0, description="Overall system health (0.0 to 1.0)")


class MissionConfig(BaseModel):
    """Mission parameters and constraints"""
    mission_type: Literal[
        "orbit_stabilization",
        "lunar_landing",
        "docking_procedure",
        "emergency_rescue",
        "asteroid_mining",
        "solar_storm_evasion",
        "satellite_repair",
        "mars_transfer",
    ]
    difficulty: Literal[1, 2, 3, 4, 5] = Field(description="1=Easy, 5=Extreme")
    time_limit: int = Field(gt=0, description="Mission time limit in seconds")
    fuel_budget: float = Field(ge=0.0, le=1.0, description="Initial fuel allocation")
    success_criteria: str = Field(description="Mission success conditions")


class SpaceMissionAction(BaseModel):
    """Agent decision components"""
    category: Literal["system_failure", "navigation", "resource_management"]
    priority: Literal["low", "medium", "high"]
    decision: Literal["continue", "adjust", "abort"]


class ObservationResponse(BaseModel):
    """Environment observation returned to agent"""
    mission_type: str
    difficulty: int
    fuel_remaining: float
    position: List[float]
    velocity: List[float]
    system_health: float
    text: str = Field(description="Natural language mission briefing")


class StepResponse(BaseModel):
    """Response from environment.step()"""
    observation: ObservationResponse
    reward: float
    done: bool
    info: dict = Field(default_factory=dict)


class ResetResponse(BaseModel):
    """Response from environment.reset()"""
    observation: ObservationResponse
    info: dict = Field(default_factory=dict)