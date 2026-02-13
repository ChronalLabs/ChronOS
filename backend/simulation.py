from typing import Any, Dict, List
import random


class SimulationEngine:
    """Lightweight rule engine for construction policy scenarios."""

    def __init__(self) -> None:
        self._baseline_duration: float = 180.0  # days
        self._baseline_risk: float = 45.0  # risk score out of 100
        self._baseline_disruption: float = 55.0  # disruption index out of 100

        self._safety_modifiers: Dict[str, Dict[str, float]] = {
            "low": {"risk_score": 18.0, "disruption_index": -6.0, "duration": -12.0},
            "standard": {"risk_score": 0.0, "disruption_index": 0.0, "duration": 0.0},
            "high": {"risk_score": -15.0, "disruption_index": 10.0, "duration": 18.0},
        }

        self._urgency_modifiers: Dict[str, Dict[str, float]] = {
            "standard": {"duration": 0.0, "risk_score": 0.0, "disruption_index": 0.0},
            "high": {"duration": -25.0, "risk_score": 9.0, "disruption_index": 6.0},
        }

        self._labor_modifiers: Dict[str, Dict[str, float]] = {
            "standard": {"duration": 0.0, "risk_score": 0.0, "disruption_index": 0.0},
            "increased": {"duration": -18.0, "risk_score": 6.0, "disruption_index": 5.0},
        }

        self._traffic_modifiers: Dict[str, Dict[str, float]] = {
            "basic": {"duration": 0.0, "risk_score": 0.0, "disruption_index": 0.0},
            "advanced": {"duration": 6.0, "risk_score": -4.0, "disruption_index": -12.0},
        }

    def run_scenario(
        self,
        night_shifts: bool,
        safety_level: str,
        urgency: str,
        labor: str,
        traffic: str,
    ) -> Dict[str, Any]:
        """Return metrics and timeline for the requested policy scenario."""

        duration = self._baseline_duration
        risk_score = self._baseline_risk
        disruption_index = self._baseline_disruption

        if night_shifts:
            duration -= 28.0
            disruption_index += 14.0
            risk_score += 7.0

        safety = self._safety_modifiers.get(safety_level, self._safety_modifiers["standard"])
        duration += safety.get("duration", 0.0)
        risk_score += safety.get("risk_score", 0.0)
        disruption_index += safety.get("disruption_index", 0.0)

        urgency_mod = self._urgency_modifiers.get(urgency, self._urgency_modifiers["standard"])
        duration += urgency_mod.get("duration", 0.0)
        risk_score += urgency_mod.get("risk_score", 0.0)
        disruption_index += urgency_mod.get("disruption_index", 0.0)

        labor_mod = self._labor_modifiers.get(labor, self._labor_modifiers["standard"])
        duration += labor_mod.get("duration", 0.0)
        risk_score += labor_mod.get("risk_score", 0.0)
        disruption_index += labor_mod.get("disruption_index", 0.0)

        traffic_mod = self._traffic_modifiers.get(traffic, self._traffic_modifiers["basic"])
        duration += traffic_mod.get("duration", 0.0)
        risk_score += traffic_mod.get("risk_score", 0.0)
        disruption_index += traffic_mod.get("disruption_index", 0.0)

        duration = round(max(30.0, min(365.0, duration)), 1)
        risk_score = round(max(0.0, min(100.0, risk_score)), 1)
        disruption_index = round(max(0.0, min(100.0, disruption_index)), 1)

        timeline = self._generate_timeline(int(duration))

        return {
            "metrics": {
                "duration": duration,
                "risk_score": risk_score,
                "disruption_index": disruption_index,
            },
            "timeline": timeline,
        }

    def _generate_timeline(self, total_days: int) -> List[Dict[str, float]]:
        """Generate a simple S-curve time-progress projection."""

        if total_days <= 0:
            return [{"day": 0, "progress": 100.0}]

        step = max(1, total_days // 20)
        timeline: List[Dict[str, float]] = []

        for day in range(0, total_days + 1, step):
            normalized_day = day / total_days
            if normalized_day < 0.1:
                progress = normalized_day * 40
            elif normalized_day < 0.8:
                progress = 4 + (normalized_day - 0.1) * 135
            else:
                progress = 95 + (normalized_day - 0.8) * 25

            progress = min(100.0, max(0.0, progress + random.uniform(-2, 2)))
            timeline.append({"day": day, "progress": round(progress, 1)})

        timeline[-1]["progress"] = 100.0
        return timeline

    def generate_explanation(
        self,
        baseline_metrics: Dict[str, float],
        policy_metrics: Dict[str, float],
        policy: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Produce qualitative insight for frontend cards."""

        duration_delta = policy_metrics["duration"] - baseline_metrics["duration"]
        risk_delta = policy_metrics["risk_score"] - baseline_metrics["risk_score"]
        disruption_delta = policy_metrics["disruption_index"] - baseline_metrics["disruption_index"]

        if risk_delta <= 5 and duration_delta <= 0:
            verdict = "Recommended"
        elif risk_delta > 20 or disruption_delta > 25:
            verdict = "High Risk"
        else:
            verdict = "Acceptable with Conditions"

        summary = (
            f"Simulated policy: {'24x7 shifts' if policy['night_shifts'] else 'day-only'}, "
            f"{policy['safety_level']} safety, {policy['urgency']} urgency, "
            f"{policy['labor']} labor, {policy['traffic']} traffic plan. "
            f"Schedule delta {duration_delta:+.0f} days; risk {risk_delta:+.0f} pts."
        )

        trade_offs: List[str] = []
        if duration_delta < 0:
            trade_offs.append(f"Faster by {abs(duration_delta):.0f} days")
        if duration_delta > 0:
            trade_offs.append(f"Slower by {duration_delta:.0f} days")
        if risk_delta > 5:
            trade_offs.append(f"Risk up {risk_delta:.0f} pts")
        elif risk_delta < -5:
            trade_offs.append(f"Risk down {abs(risk_delta):.0f} pts")
        if disruption_delta > 8:
            trade_offs.append(f"Disruption up {disruption_delta:.0f} pts")
        elif disruption_delta < -8:
            trade_offs.append(f"Disruption down {abs(disruption_delta):.0f} pts")

        trade_offs_text = "; ".join(trade_offs) if trade_offs else "Minimal deviation from baseline"

        warnings: List[str] = []
        if risk_delta > 15:
            warnings.append("Safety risk exceeds ethical threshold")
        if disruption_delta > 20:
            warnings.append("Consider mitigation for community disruption")
        if policy["night_shifts"] and policy["safety_level"] == "low":
            warnings.append("Night work with low safety controls is discouraged")
        if policy["labor"] == "increased" and policy["safety_level"] == "low":
            warnings.append("Surged labor plus low safety will magnify injury risk")
        if policy["traffic"] == "basic" and disruption_delta > 15:
            warnings.append("Upgrade traffic plan to advanced to offset disruption")

        return {
            "verdict": verdict,
            "summary": summary,
            "trade_offs": trade_offs_text,
            "warnings": warnings,
        }