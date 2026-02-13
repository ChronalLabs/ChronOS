"""
Risk & Sensitivity Detection (Task 8)
Flag unsafe trade-offs automatically using threshold logic
"""

from typing import Dict, List
from enum import Enum


class RiskLevel(Enum):
    """Risk classification"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    ACCEPTABLE = "acceptable"


class RiskDetector:
    """Detect and flag risky policy trade-offs"""
    
    # Configurable thresholds
    THRESHOLDS = {
        'risk_increase': {
            'critical': 30,    # >30% risk increase is critical
            'high': 20,        # >20% is high
            'medium': 10,      # >10% is medium
            'low': 5           # >5% is low
        },
        'time_vs_risk': {
            'min_time_benefit_per_risk': 2.0  # Need 2 days saved per 1% risk increase
        },
        'cost_increase': {
            'critical': 50,    # >50% cost increase
            'high': 30,
            'medium': 15,
            'low': 5
        },
        'incidents_increase': {
            'critical': 1.0,   # Any incident increase in residential
            'high': 0.5,
            'medium': 0.3,
            'low': 0.1
        }
    }
    
    # Domain-specific sensitivity
    ZONE_SENSITIVITY = {
        'residential': {
            'risk_multiplier': 1.5,      # Risks are 1.5x more serious
            'incident_tolerance': 0,      # Zero incident tolerance
            'noise_sensitivity': 'high'
        },
        'commercial': {
            'risk_multiplier': 1.0,
            'incident_tolerance': 0.2,
            'noise_sensitivity': 'medium'
        },
        'industrial': {
            'risk_multiplier': 0.8,
            'incident_tolerance': 0.5,
            'noise_sensitivity': 'low'
        }
    }
    
    def __init__(self):
        """Initialize detector"""
        self.flags = []
        self.sensitivity_adjustments = {}
    
    def detect_unsafe_tradeoffs(
        self,
        time_saved: float,
        risk_increase: float,
        cost_increase: float,
        incidents_increase: float,
        zone: str = "commercial",
        policy_name: str = "Unknown"
    ) -> Dict:
        """
        Detect unsafe trade-offs in policy simulation
        
        Args:
            time_saved (float): Days saved (positive = faster)
            risk_increase (float): Risk percentage increase
            cost_increase (float): Cost percentage increase
            incidents_increase (float): Incident count increase
            zone (str): Zone type for sensitivity
            policy_name (str): Policy name
            
        Returns:
            dict: Risk assessment with flags
        """
        self.flags = []
        
        # Get zone sensitivity
        zone_config = self.ZONE_SENSITIVITY.get(zone.lower(), self.ZONE_SENSITIVITY['commercial'])
        risk_multiplier = zone_config['risk_multiplier']
        incident_tolerance = zone_config['incident_tolerance']
        
        # Adjust risk by zone sensitivity
        adjusted_risk = risk_increase * risk_multiplier
        
        # Check risk thresholds
        risk_level = self._classify_risk(adjusted_risk, 'risk_increase')
        if risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH]:
            self.flags.append({
                'type': 'risk_threshold',
                'severity': risk_level.value,
                'message': f"Risk increase of {adjusted_risk:.1f}% exceeds {risk_level.value} threshold",
                'value': adjusted_risk
            })
        
        # Check time vs risk trade-off
        required_time_benefit = risk_increase * self.THRESHOLDS['time_vs_risk']['min_time_benefit_per_risk']
        if time_saved < required_time_benefit and risk_increase > 5:
            self.flags.append({
                'type': 'poor_tradeoff',
                'severity': 'high',
                'message': f"Time saved ({time_saved:.0f} days) doesn't justify risk increase ({risk_increase:.1f}%)",
                'required': required_time_benefit,
                'actual': time_saved
            })
        
        # Check cost thresholds
        cost_level = self._classify_risk(cost_increase, 'cost_increase')
        if cost_level in [RiskLevel.CRITICAL, RiskLevel.HIGH]:
            self.flags.append({
                'type': 'cost_threshold',
                'severity': cost_level.value,
                'message': f"Cost increase of {cost_increase:.1f}% is {cost_level.value}",
                'value': cost_increase
            })
        
        # Check incident tolerance
        if incidents_increase > incident_tolerance:
            self.flags.append({
                'type': 'incident_threshold',
                'severity': 'critical' if zone.lower() == 'residential' else 'high',
                'message': f"Incident increase ({incidents_increase:.2f}) exceeds zone tolerance ({incident_tolerance})",
                'value': incidents_increase,
                'tolerance': incident_tolerance
            })
        
        # Calculate overall risk level
        overall_risk = self._calculate_overall_risk(adjusted_risk, cost_increase, incidents_increase, zone)
        
        # Generate recommendation
        recommendation = self._generate_recommendation(overall_risk, self.flags)
        
        return {
            'policy': policy_name,
            'zone': zone,
            'risk_level': overall_risk.value,
            'adjusted_risk_increase': adjusted_risk,
            'flags': self.flags,
            'flag_count': len(self.flags),
            'is_acceptable': overall_risk in [RiskLevel.LOW, RiskLevel.ACCEPTABLE],
            'recommendation': recommendation,
            'metrics': {
                'time_saved': time_saved,
                'risk_increase': risk_increase,
                'cost_increase': cost_increase,
                'incidents_increase': incidents_increase
            }
        }
    
    def _classify_risk(self, value: float, threshold_type: str) -> RiskLevel:
        """Classify risk level based on thresholds"""
        thresholds = self.THRESHOLDS.get(threshold_type, {})
        
        if value >= thresholds.get('critical', float('inf')):
            return RiskLevel.CRITICAL
        elif value >= thresholds.get('high', float('inf')):
            return RiskLevel.HIGH
        elif value >= thresholds.get('medium', float('inf')):
            return RiskLevel.MEDIUM
        elif value >= thresholds.get('low', float('inf')):
            return RiskLevel.LOW
        else:
            return RiskLevel.ACCEPTABLE
    
    def _calculate_overall_risk(
        self,
        risk_increase: float,
        cost_increase: float,
        incidents_increase: float,
        zone: str
    ) -> RiskLevel:
        """Calculate overall risk level"""
        # Weight factors
        risk_weight = 0.4
        cost_weight = 0.2
        incident_weight = 0.4
        
        # Normalize values
        risk_score = min(100, risk_increase * 2)
        cost_score = min(100, cost_increase)
        incident_score = min(100, incidents_increase * 100)
        
        # Weighted average
        overall = (risk_score * risk_weight + 
                   cost_score * cost_weight + 
                   incident_score * incident_weight)
        
        # Zone adjustment
        if zone.lower() == 'residential':
            overall *= 1.3
        
        # Classify
        if overall >= 60:
            return RiskLevel.CRITICAL
        elif overall >= 40:
            return RiskLevel.HIGH
        elif overall >= 25:
            return RiskLevel.MEDIUM
        elif overall >= 10:
            return RiskLevel.LOW
        else:
            return RiskLevel.ACCEPTABLE
    
    def _generate_recommendation(self, risk_level: RiskLevel, flags: List) -> str:
        """Generate recommendation based on risk assessment"""
        if risk_level == RiskLevel.CRITICAL:
            return "❌ REJECT - Critical risks identified. Policy requires major revision."
        elif risk_level == RiskLevel.HIGH:
            return "⚠️ REVISE - High risks need mitigation before approval."
        elif risk_level == RiskLevel.MEDIUM:
            return "⚖️ REVIEW - Moderate risks should be addressed."
        elif risk_level == RiskLevel.LOW:
            return "✓ ACCEPTABLE - Low risks within tolerance."
        else:
            return "✅ APPROVED - No significant risks identified."
    
    def sensitivity_analysis(
        self,
        baseline_metrics: Dict[str, float],
        parameter_ranges: Dict[str, tuple]
    ) -> Dict:
        """
        Perform sensitivity analysis on parameters
        
        Args:
            baseline_metrics: {'time_saved': 20, 'risk_increase': 10, ...}
            parameter_ranges: {'night_work_hours': (0, 8), ...}
            
        Returns:
            dict: Sensitivity analysis results
        """
        sensitivity_results = {}
        
        for param, (min_val, max_val) in parameter_ranges.items():
            # Test at min, mid, and max
            test_points = [min_val, (min_val + max_val) / 2, max_val]
            outcomes = []
            
            for value in test_points:
                # Simulate impact (simplified linear model)
                impact = self._estimate_parameter_impact(param, value, baseline_metrics)
                outcomes.append({'value': value, 'impact': impact})
            
            # Calculate variance
            impacts = [o['impact'] for o in outcomes]
            variance = max(impacts) - min(impacts)
            
            sensitivity_results[param] = {
                'test_points': outcomes,
                'variance': variance,
                'sensitivity': 'high' if variance > 20 else 'medium' if variance > 10 else 'low'
            }
        
        # Rank by sensitivity
        ranked = sorted(
            sensitivity_results.items(),
            key=lambda x: x[1]['variance'],
            reverse=True
        )
        
        return {
            'parameter_sensitivity': sensitivity_results,
            'most_sensitive': [
                {'parameter': k, 'variance': v['variance'], 'sensitivity': v['sensitivity']}
                for k, v in ranked[:3]
            ],
            'recommendation': f"Focus on controlling: {ranked[0][0]}" if ranked else "No sensitive parameters"
        }
    
    def _estimate_parameter_impact(
        self,
        param: str,
        value: float,
        baseline: Dict
    ) -> float:
        """Estimate parameter impact on overall risk"""
        # Simplified impact model
        impact_factors = {
            'night_work_hours': 3.0,      # High impact per hour
            'overtime_percentage': 1.5,    # Moderate impact
            'worker_overtime': 2.0,        # High impact
            'inspection_frequency': -2.0   # Negative = more inspections reduce risk
        }
        
        factor = impact_factors.get(param, 1.0)
        return value * factor
    
    def generate_risk_report(self) -> str:
        """Generate comprehensive risk report"""
        report = "═" * 60 + "\n"
        report += "RISK ASSESSMENT REPORT\n"
        report += "═" * 60 + "\n\n"
        
        if not self.flags:
            report += "✅ No risk flags identified.\n"
        else:
            report += f"⚠️ {len(self.flags)} risk flag(s) identified:\n\n"
            for i, flag in enumerate(self.flags, 1):
                report += f"{i}. [{flag['severity'].upper()}] {flag['type']}\n"
                report += f"   {flag['message']}\n\n"
        
        return report


# Quick test
if __name__ == "__main__":
    detector = RiskDetector()
    
    # Test assessment
    assessment = detector.detect_unsafe_tradeoffs(
        time_saved=10,           # Only 10 days saved
        risk_increase=25,        # But risk increases 25%
        cost_increase=5,
        incidents_increase=0.8,
        zone='residential',
        policy_name="Emergency Night Construction"
    )
    
    print(f"📊 Risk Level: {assessment['risk_level'].upper()}")
    print(f"🚩 Flags: {assessment['flag_count']}")
    for flag in assessment['flags']:
        print(f"  ⚠️ {flag['message']}")
    print(f"\n{assessment['recommendation']}")
