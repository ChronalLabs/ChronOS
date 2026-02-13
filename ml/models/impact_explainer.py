"""
Impact Explanation (Task 7)
Explain simulation results without hallucination using templates
"""

from typing import Dict, List
from datetime import datetime


class ImpactExplainer:
    """Generate explanations of simulation impacts"""
    
    # Template library for common scenarios
    TEMPLATES = {
        "time_impact_faster": "Policy reduced project duration by {delta_time:.0f} days ({percentage:.1f}% faster)",
        "time_impact_slower": "Policy extended project duration by {delta_time:.0f} days ({percentage:.1f}% slower)",
        "risk_increase": "Risk increased by {delta_risk:.1f}% due to {reason}",
        "risk_decrease": "Risk decreased by {delta_risk:.1f}% through {reason}",
        "safety_improved": "Safety incidents reduced by {reduction_percent:.1f}% through {mechanism}",
        "safety_degraded": "Safety incidents increased by {increase_percent:.1f}% due to {mechanism}",
        "cost_increase": "Project cost increased by ${abs_cost:,.0f} ({percentage:.1f}%)",
        "cost_decrease": "Project cost decreased by ${abs_cost:,.0f} ({percentage:.1f}% savings)",
    }
    
    def __init__(self):
        """Initialize explainer"""
        self.explanations = []
    
    def explain_time_delta(
        self,
        baseline_days: float,
        simulated_days: float,
        policy_name: str
    ) -> Dict:
        """
        Explain time impact
        
        Args:
            baseline_days (float): Original estimated duration
            simulated_days (float): Simulated duration
            policy_name (str): Policy applied
            
        Returns:
            dict: Explanation with metrics
        """
        delta = baseline_days - simulated_days
        percentage = abs(delta / baseline_days) * 100 if baseline_days > 0 else 0
        
        if delta > 0:
            narrative = self.TEMPLATES["time_impact_faster"].format(
                delta_time=abs(delta),
                percentage=percentage
            )
        else:
            narrative = self.TEMPLATES["time_impact_slower"].format(
                delta_time=abs(delta),
                percentage=percentage
            )
        
        explanation = {
            'type': 'time_impact',
            'policy': policy_name,
            'baseline': baseline_days,
            'simulated': simulated_days,
            'delta': delta,
            'percentage': percentage,
            'direction': 'faster' if delta > 0 else 'slower',
            'narrative': narrative,
            'confidence': self._estimate_confidence('time', delta, baseline_days)
        }
        
        self.explanations.append(explanation)
        return explanation
    
    def explain_risk_delta(
        self,
        baseline_risk: float,
        simulated_risk: float,
        risk_factors: List[str],
        policy_name: str
    ) -> Dict:
        """
        Explain risk impact
        
        Args:
            baseline_risk (float): Baseline risk percentage
            simulated_risk (float): Simulated risk percentage
            risk_factors (List[str]): Factors driving risk change
            policy_name (str): Policy applied
            
        Returns:
            dict: Risk explanation
        """
        delta = simulated_risk - baseline_risk
        
        # Determine primary reason
        reason = self._determine_risk_reason(risk_factors, delta)
        
        if delta > 0:
            narrative = self.TEMPLATES["risk_increase"].format(
                delta_risk=abs(delta),
                reason=reason
            )
        else:
            narrative = self.TEMPLATES["risk_decrease"].format(
                delta_risk=abs(delta),
                reason=reason
            )
        
        explanation = {
            'type': 'risk_impact',
            'policy': policy_name,
            'baseline_risk': baseline_risk,
            'simulated_risk': simulated_risk,
            'delta': delta,
            'direction': 'increased' if delta > 0 else 'decreased',
            'risk_factors': risk_factors,
            'primary_driver': reason,
            'narrative': narrative,
            'is_acceptable': abs(delta) < 15,  # Flag if >15% change
            'confidence': self._estimate_confidence('risk', delta, baseline_risk)
        }
        
        self.explanations.append(explanation)
        return explanation
    
    def explain_safety_impact(
        self,
        baseline_incidents: float,
        simulated_incidents: float,
        safety_mechanisms: List[str],
        policy_name: str
    ) -> Dict:
        """
        Explain safety improvements/degradations
        
        Args:
            baseline_incidents (float): Baseline incident count
            simulated_incidents (float): Simulated incidents
            safety_mechanisms (List[str]): Mechanisms affecting safety
            policy_name (str): Policy applied
            
        Returns:
            dict: Safety explanation
        """
        delta = baseline_incidents - simulated_incidents
        change_percent = abs(delta / baseline_incidents * 100) if baseline_incidents > 0 else 0
        
        mechanism = ", ".join(safety_mechanisms[:2]) if safety_mechanisms else "policy constraints"
        
        if delta >= 0:
            narrative = self.TEMPLATES["safety_improved"].format(
                reduction_percent=change_percent,
                mechanism=mechanism
            )
        else:
            narrative = self.TEMPLATES["safety_degraded"].format(
                increase_percent=change_percent,
                mechanism=mechanism
            )
        
        explanation = {
            'type': 'safety_impact',
            'policy': policy_name,
            'baseline_incidents': baseline_incidents,
            'simulated_incidents': simulated_incidents,
            'reduction': delta,
            'change_percent': change_percent,
            'mechanisms': safety_mechanisms,
            'narrative': narrative,
            'is_positive': delta >= 0,
            'confidence': self._estimate_confidence('safety', delta, baseline_incidents)
        }
        
        self.explanations.append(explanation)
        return explanation
    
    def explain_cost_impact(
        self,
        baseline_cost: float,
        simulated_cost: float,
        cost_drivers: Dict[str, float],
        policy_name: str
    ) -> Dict:
        """
        Explain cost impact
        
        Args:
            baseline_cost (float): Original estimated cost
            simulated_cost (float): Simulated cost
            cost_drivers (Dict[str, float]): {'labor': 5000, 'equipment': 2000, ...}
            policy_name (str): Policy applied
            
        Returns:
            dict: Cost explanation
        """
        delta = simulated_cost - baseline_cost
        percentage = abs(delta / baseline_cost * 100) if baseline_cost > 0 else 0
        
        # Top cost drivers
        top_drivers = sorted(cost_drivers.items(), key=lambda x: abs(x[1]), reverse=True)[:2]
        
        if delta > 0:
            narrative = self.TEMPLATES["cost_increase"].format(
                abs_cost=abs(delta),
                percentage=percentage
            )
        else:
            narrative = self.TEMPLATES["cost_decrease"].format(
                abs_cost=abs(delta),
                percentage=percentage
            )
        
        explanation = {
            'type': 'cost_impact',
            'policy': policy_name,
            'baseline_cost': baseline_cost,
            'simulated_cost': simulated_cost,
            'delta': delta,
            'percentage': percentage,
            'direction': 'increased' if delta > 0 else 'decreased',
            'cost_drivers': cost_drivers,
            'top_drivers': [f"{k}: ${v:,.0f}" for k, v in top_drivers],
            'narrative': narrative,
            'roi': self._calculate_roi(delta, simulated_cost),
            'confidence': self._estimate_confidence('cost', delta, baseline_cost)
        }
        
        self.explanations.append(explanation)
        return explanation
    
    def explain_overall_impact(
        self,
        time_delta: float,
        risk_delta: float,
        safety_delta: float,
        cost_delta: float,
        policy_name: str
    ) -> Dict:
        """
        Generate overall impact summary
        
        Args:
            time_delta (float): Time change in days (positive = faster)
            risk_delta (float): Risk change in percentage points
            safety_delta (float): Incidents reduced (positive = fewer)
            cost_delta (float): Cost change in dollars
            policy_name (str): Policy name
            
        Returns:
            dict: Overall impact assessment
        """
        # Calculate trade-off score
        time_benefit = max(0, time_delta / 100) if time_delta > 0 else 0
        risk_penalty = max(0, risk_delta)
        safety_benefit = max(0, safety_delta)
        cost_penalty = max(0, cost_delta / 100000)
        
        trade_off_score = (time_benefit + safety_benefit - risk_penalty - cost_penalty) * 100
        
        # Determine recommendation
        if trade_off_score > 30:
            recommendation = "✅ RECOMMENDED - Strong positive trade-offs"
        elif trade_off_score > 10:
            recommendation = "⚠️ CONSIDER - Moderate trade-offs need review"
        elif trade_off_score > -10:
            recommendation = "⚖️ NEUTRAL - Trade-offs balance out"
        else:
            recommendation = "❌ NOT RECOMMENDED - Significant risks"
        
        summary = f"""
📊 POLICY IMPACT SUMMARY: {policy_name}

⏱️ TIME: {'+' if time_delta > 0 else ''}{time_delta:.0f} days
  Impact: {'Faster delivery' if time_delta > 0 else 'Extended timeline'}

⚠️ RISK: {'+' if risk_delta > 0 else ''}{risk_delta:.1f}%
  Impact: {'Risk INCREASED' if risk_delta > 0 else 'Risk DECREASED'}

🛡️ SAFETY: {'+' if safety_delta > 0 else ''}{safety_delta:.0f} incidents
  Impact: {'Fewer incidents' if safety_delta > 0 else 'More incidents'}

💰 COST: ${cost_delta:+,.0f}
  Impact: {'Budget increase' if cost_delta > 0 else 'Budget savings'}

🎯 OVERALL TRADE-OFF SCORE: {trade_off_score:.1f}/100
{recommendation}
"""
        
        return {
            'policy': policy_name,
            'time_delta': time_delta,
            'risk_delta': risk_delta,
            'safety_delta': safety_delta,
            'cost_delta': cost_delta,
            'trade_off_score': trade_off_score,
            'recommendation': recommendation,
            'summary_text': summary,
            'timestamp': datetime.now().isoformat()
        }
    
    def _determine_risk_reason(self, risk_factors: List[str], delta: float) -> str:
        """Determine primary reason for risk change"""
        if not risk_factors:
            return "policy constraints"
        
        # Map factors to explanations
        reason_map = {
            'night_work': 'allowing night construction',
            'overtime': 'extended work hours',
            'concurrent_activities': 'concurrent construction activities',
            'reduced_inspections': 'reduced inspection frequency',
            'worker_fatigue': 'worker fatigue from extended hours',
            'safety_protocols': 'enhanced safety protocols',
            'regular_inspections': 'regular safety inspections'
        }
        
        for factor in risk_factors:
            if factor in reason_map:
                return reason_map[factor]
        
        return risk_factors[0] if risk_factors else "unknown factors"
    
    def _estimate_confidence(self, impact_type: str, delta: float, baseline: float) -> float:
        """Estimate confidence in explanation (0-1)"""
        if baseline == 0:
            return 0.5
        
        # Higher confidence for larger deltas
        confidence = min(1.0, abs(delta) / (baseline * 0.5))
        
        # Type-specific adjustments
        if impact_type == 'time':
            confidence *= 0.9  # Time estimates often uncertain
        elif impact_type == 'safety':
            confidence *= 0.85  # Safety harder to predict
        
        return confidence
    
    def _calculate_roi(self, cost_delta: float, total_cost: float) -> Dict:
        """Calculate simple ROI metrics"""
        if cost_delta < 0:
            savings = abs(cost_delta)
            roi = (savings / total_cost) * 100 if total_cost > 0 else 0
            return {'type': 'savings', 'amount': savings, 'percentage': roi}
        else:
            roi = (cost_delta / total_cost) * 100 if total_cost > 0 else 0
            return {'type': 'additional_cost', 'amount': cost_delta, 'percentage': roi}
    
    def generate_report(self) -> str:
        """Generate comprehensive explanation report"""
        report = "═" * 60 + "\n"
        report += "POLICY SIMULATION IMPACT ANALYSIS\n"
        report += "═" * 60 + "\n\n"
        
        for explanation in self.explanations:
            report += f"\n{'─' * 60}\n"
            report += f"Type: {explanation['type'].upper()}\n"
            report += f"Policy: {explanation['policy']}\n"
            report += f"Narrative: {explanation['narrative']}\n"
            report += f"Confidence: {explanation.get('confidence', 0):.1%}\n"
        
        return report


# Quick test
if __name__ == "__main__":
    explainer = ImpactExplainer()
    
    # Test time impact
    time_exp = explainer.explain_time_delta(180, 150, "Night Construction Allowed")
    print(f"⏱️ {time_exp['narrative']}")
    
    # Test risk impact
    risk_exp = explainer.explain_risk_delta(5.0, 12.5, ['night_work', 'worker_fatigue'], "Night Construction Allowed")
    print(f"⚠️ {risk_exp['narrative']}")
    
    # Overall summary
    overall = explainer.explain_overall_impact(30, 7.5, 2, 50000, "Night Construction Allowed")
    print(overall['summary_text'])
