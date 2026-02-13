"""
Policy Parameter Mapping (Task 6)
Convert extracted policy intent into simulation parameters (Rule-based)
"""

from typing import Dict
import json
from pathlib import Path


class PolicyParameterMapper:
    """Map policy intent to simulation parameters"""
    
    # Safety level mappings
    SAFETY_LEVEL_MAP = {
        "strict": {
            "safety_priority": 0.85,
            "inspection_frequency_days": 3,
            "incident_risk_multiplier": 0.5,
            "worker_protection_level": 0.95
        },
        "moderate": {
            "safety_priority": 0.65,
            "inspection_frequency_days": 7,
            "incident_risk_multiplier": 0.8,
            "worker_protection_level": 0.70
        },
        "low": {
            "safety_priority": 0.45,
            "inspection_frequency_days": 14,
            "incident_risk_multiplier": 1.2,
            "worker_protection_level": 0.50
        }
    }
    
    # Speed level mappings
    SPEED_LEVEL_MAP = {
        "fast-track": {
            "speed_priority": 0.85,
            "concurrent_activities": True,
            "overtime_allowed": True,
            "night_shifts_allowed": True,
            "rest_days_per_week": 1
        },
        "normal": {
            "speed_priority": 0.65,
            "concurrent_activities": False,
            "overtime_allowed": True,
            "night_shifts_allowed": False,
            "rest_days_per_week": 1
        },
        "conservative": {
            "speed_priority": 0.40,
            "concurrent_activities": False,
            "overtime_allowed": False,
            "night_shifts_allowed": False,
            "rest_days_per_week": 2
        }
    }
    
    # Zone-specific restrictions
    ZONE_RESTRICTIONS = {
        "residential": {
            "noise_limit_db": 55,
            "dust_limit_mg_m3": 0.15,
            "vibration_limit_mm_s": 5,
            "allowed_hours": "7:00-18:00",
            "weekend_allowed": False
        },
        "commercial": {
            "noise_limit_db": 70,
            "dust_limit_mg_m3": 0.5,
            "vibration_limit_mm_s": 10,
            "allowed_hours": "6:00-22:00",
            "weekend_allowed": True
        },
        "industrial": {
            "noise_limit_db": 85,
            "dust_limit_mg_m3": 2.0,
            "vibration_limit_mm_s": 20,
            "allowed_hours": "24/7",
            "weekend_allowed": True
        }
    }
    
    # Construction type constraints
    CONSTRUCTION_TYPE_PARAMS = {
        "residential": {
            "base_duration_days": 180,
            "safety_criticality": "high",
            "approval_time_days": 30,
            "inspection_points": 15
        },
        "commercial": {
            "base_duration_days": 240,
            "safety_criticality": "medium",
            "approval_time_days": 20,
            "inspection_points": 10
        },
        "infrastructure": {
            "base_duration_days": 365,
            "safety_criticality": "critical",
            "approval_time_days": 60,
            "inspection_points": 25
        },
        "demolition": {
            "base_duration_days": 60,
            "safety_criticality": "critical",
            "approval_time_days": 45,
            "inspection_points": 20
        }
    }
    
    def __init__(self):
        """Initialize mapper with all rule tables"""
        self.extracted_parameters = {}
    
    def map_safety_intent(self, safety_keyword: str) -> Dict:
        """
        Map extracted safety keywords to parameters
        
        Args:
            safety_keyword (str): e.g., "strict", "moderate", "low"
            
        Returns:
            dict: Safety parameters
        """
        safety_keyword = safety_keyword.lower()
        
        # Match keyword to safety level
        if any(term in safety_keyword for term in ["strict", "rigorous", "comprehensive"]):
            return self.SAFETY_LEVEL_MAP["strict"]
        elif any(term in safety_keyword for term in ["low", "minimal", "basic"]):
            return self.SAFETY_LEVEL_MAP["low"]
        else:
            return self.SAFETY_LEVEL_MAP["moderate"]
    
    def map_speed_intent(self, speed_keyword: str) -> Dict:
        """
        Map extracted speed keywords to parameters
        
        Args:
            speed_keyword (str): e.g., "urgent", "normal", "phased"
            
        Returns:
            dict: Speed parameters
        """
        speed_keyword = speed_keyword.lower()
        
        if any(term in speed_keyword for term in ["urgent", "fast", "accelerated", "24/7", "night"]):
            return self.SPEED_LEVEL_MAP["fast-track"]
        elif any(term in speed_keyword for term in ["phased", "staged", "careful", "deliberate"]):
            return self.SPEED_LEVEL_MAP["conservative"]
        else:
            return self.SPEED_LEVEL_MAP["normal"]
    
    def map_zone_constraints(self, zone_type: str) -> Dict:
        """
        Map zone type to environmental constraints
        
        Args:
            zone_type (str): e.g., "residential", "commercial", "industrial"
            
        Returns:
            dict: Zone-specific constraints
        """
        zone_type = zone_type.lower()
        
        for zone_key in self.ZONE_RESTRICTIONS:
            if zone_key in zone_type:
                return self.ZONE_RESTRICTIONS[zone_key]
        
        # Default to commercial if not found
        return self.ZONE_RESTRICTIONS["commercial"]
    
    def map_construction_type(self, construction_type: str) -> Dict:
        """
        Map construction type to base parameters
        
        Args:
            construction_type (str): e.g., "residential", "commercial", "infrastructure"
            
        Returns:
            dict: Construction type parameters
        """
        construction_type = construction_type.lower()
        
        for type_key in self.CONSTRUCTION_TYPE_PARAMS:
            if type_key in construction_type:
                return self.CONSTRUCTION_TYPE_PARAMS[type_key]
        
        # Default to commercial if not found
        return self.CONSTRUCTION_TYPE_PARAMS["commercial"]
    
    def integrate_extraction(
        self,
        ner_results: Dict,
        classification_results: Dict,
        ambiguity_score: float
    ) -> Dict:
        """
        Integrate all extraction results into unified parameters
        
        Args:
            ner_results (Dict): From PolicyNER
            classification_results (Dict): From PolicyClassifier
            ambiguity_score (float): From AmbiguityDetector (0-100)
            
        Returns:
            dict: Complete simulation parameters
        """
        # Extract key information
        zones = ner_results.get('ZONE', ['commercial'])[0] if 'ZONE' in ner_results else 'commercial'
        construction_type = ner_results.get('CONSTRUCTION_TYPE', ['commercial'])[0] if 'CONSTRUCTION_TYPE' in ner_results else 'commercial'
        
        # Get safety and speed profiles
        safety_params = self.map_safety_intent("moderate")  # Default
        speed_params = self.map_speed_intent("normal")      # Default
        
        # Override based on classification
        if "safety-focused" in classification_results.get('primary_classification', ''):
            safety_params = self.map_safety_intent("strict")
        elif "speed-focused" in classification_results.get('primary_classification', ''):
            speed_params = self.map_speed_intent("fast-track")
        
        # Get zone constraints
        zone_constraints = self.map_zone_constraints(zones)
        
        # Get construction type parameters
        construction_params = self.map_construction_type(construction_type)
        
        # Apply ambiguity penalty
        ambiguity_penalty = 1 - (ambiguity_score / 100) * 0.2  # Up to 20% penalty
        
        # Integrate all parameters
        integrated = {
            'policy_metadata': {
                'zones': zones,
                'construction_type': construction_type,
                'ambiguity_score': ambiguity_score,
                'ambiguity_penalty': ambiguity_penalty,
                'classification': classification_results.get('primary_classification', 'unknown')
            },
            'safety_profile': safety_params,
            'speed_profile': speed_params,
            'zone_constraints': zone_constraints,
            'construction_params': construction_params,
            'simulation_parameters': {
                **safety_params,
                **speed_params,
                **zone_constraints,
                **construction_params,
                'ambiguity_factor': ambiguity_penalty
            }
        }
        
        self.extracted_parameters = integrated
        return integrated
    
    def export_parameters(self, output_path: str = "config/sim_parameters.json"):
        """Export parameters to JSON"""
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.extracted_parameters, f, indent=2)
        print(f"✓ Parameters exported to {output_path}")
        return output_path


# Quick test
if __name__ == "__main__":
    mapper = PolicyParameterMapper()
    
    # Simulated extraction results
    ner_results = {
        'ZONE': ['residential zone'],
        'CONSTRUCTION_TYPE': ['commercial construction'],
        'TIME_EXPRESSION': ['night hours', 'peak hours']
    }
    
    classification_results = {
        'primary_classification': 'safety-focused policy'
    }
    
    ambiguity_score = 35.5
    
    # Integrate and map
    sim_params = mapper.integrate_extraction(
        ner_results,
        classification_results,
        ambiguity_score
    )
    
    print("🎯 Extracted Simulation Parameters:")
    print(json.dumps(sim_params, indent=2))
