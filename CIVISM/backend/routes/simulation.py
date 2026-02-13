"""
Simulation API Routes
"""

from fastapi import APIRouter

from schemas import PolicyInput
from simulation import SimulationEngine

router = APIRouter(tags=["Simulation"])

# Initialize simulation engine
engine = SimulationEngine()


@router.post("/simulate")
def simulate(policy: PolicyInput):
    """
    Run simulation with given policy parameters.
    Compares policy results against baseline scenario.
    """
    # Run baseline scenario
    baseline_results = engine.run_scenario(
        night_shifts=False,
        safety_level="standard",
        urgency="standard",
        labor="standard",
        traffic="basic"
    )
    
    # Run policy scenario
    policy_results = engine.run_scenario(
        night_shifts=policy.night_shifts,
        safety_level=policy.safety_level,
        urgency=policy.urgency,
        labor=policy.labor,
        traffic=policy.traffic,
    )
    
    # Generate explanation
    explanation = engine.generate_explanation(
        baseline_results["metrics"],
        policy_results["metrics"],
        policy.dict()
    )
    
    return {
        "baseline": baseline_results,
        "policy": policy_results,
        "analysis": explanation
    }
