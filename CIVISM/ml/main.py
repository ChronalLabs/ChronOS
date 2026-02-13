#!/usr/bin/env python3
"""
CIVISIM ML/AI Pipeline - Complete Integration
One-command execution of all ML tasks
"""

import sys
from pathlib import Path

# Add models directory to path
sys.path.insert(0, str(Path(__file__).parent))

from models.document_parser import DocumentParser
from models.intent_extractor import PolicyIntentExtractor
from models.policy_ner import PolicyNER
from models.ambiguity_detector import AmbiguityDetector
from models.policy_classifier import PolicyClassifier
from models.policy_mapper import PolicyParameterMapper
from models.impact_explainer import ImpactExplainer
from models.risk_detector import RiskDetector
import json


def run_civisim_pipeline(policy_text: str = None, policy_file: str = None, policy_name: str = "Unknown"):
    """
    Execute complete CIVISIM ML pipeline
    
    Args:
        policy_text (str): Direct policy text input
        policy_file (str): Path to PDF or DOCX policy file
        policy_name (str): Human-readable policy name
    """
    
    print("=" * 70)
    print("CIVISIM ML/AI PIPELINE - FULL EXECUTION")
    print("=" * 70)
    
    # ✅ TASK 1: Extract text (or use provided text)
    print("\n[1/8] Extracting/Loading policy text...")
    if policy_file:
        parser = DocumentParser()
        extraction = parser.extract_generic(policy_file)
        if not extraction:
            print("❌ Failed to extract policy")
            return None
        print(f"✓ Extracted {len(extraction['full_text'])} characters")
        policy_text = extraction['full_text']
    elif policy_text:
        print(f"✓ Using provided text ({len(policy_text)} characters)")
    else:
        print("❌ No policy text or file provided")
        return None
    
    # ✅ TASK 2: Intent & keyword extraction
    print("\n[2/8] Extracting policy intent...")
    intent_extractor = PolicyIntentExtractor()
    intent_results = intent_extractor.extract_intent(policy_text)
    print(f"✓ Found {len(intent_results['key_sentences'])} key sentences")
    
    # ✅ TASK 3: NER - Named entities
    print("\n[3/8] Extracting policy entities...")
    ner = PolicyNER()
    ner_results = ner.summarize_extraction(policy_text)
    print(f"✓ Extracted {len(ner_results)} entity types")
    if ner_results:
        print(f"  Types: {', '.join(list(ner_results.keys())[:5])}")
    
    # ✅ TASK 4: Ambiguity detection
    print("\n[4/8] Analyzing ambiguity...")
    ambiguity_detector = AmbiguityDetector()
    ambiguity_data = ambiguity_detector.ambiguity_score(policy_text)
    print(f"✓ Ambiguity Score: {ambiguity_data['overall_score']:.1f}/100")
    print(f"  Trust Level: {ambiguity_data['trust_level']}")
    print(f"  Critical: {ambiguity_data['by_severity']['critical']} | High: {ambiguity_data['by_severity']['high']}")
    
    # ✅ TASK 5: Policy classification
    print("\n[5/8] Classifying policy...")
    classifier = PolicyClassifier()
    classification = classifier.classify_policy_focus(policy_text)
    print(f"✓ Classification: {classification['primary_classification'][:50]}...")
    print(f"  Confidence: {classification['confidence']:.2%}")
    
    # ✅ TASK 6: Parameter mapping
    print("\n[6/8] Mapping to simulation parameters...")
    mapper = PolicyParameterMapper()
    sim_params = mapper.integrate_extraction(ner_results, classification, ambiguity_data['overall_score'])
    print(f"✓ Generated {len(sim_params['simulation_parameters'])} parameters")
    
    # ✅ TASK 7: Impact explanation (simulated results for demo)
    print("\n[7/8] Generating impact explanations...")
    explainer = ImpactExplainer()
    
    # Simulated results (in production, these come from CIVISIM simulation)
    time_impact = explainer.explain_time_delta(180, 150, policy_name)
    risk_impact = explainer.explain_risk_delta(5.0, 12.5, ['policy_changes', 'schedule_pressure'], policy_name)
    safety_impact = explainer.explain_safety_impact(3.0, 2.0, ['enhanced_protocols'], policy_name)
    cost_impact = explainer.explain_cost_impact(500000, 550000, {'labor': 30000, 'equipment': 20000}, policy_name)
    overall = explainer.explain_overall_impact(30, 7.5, 1, 50000, policy_name)
    print(f"✓ Generated {len(explainer.explanations)} impact explanations")
    
    # ✅ TASK 8: Risk detection
    print("\n[8/8] Detecting risky trade-offs...")
    risk_detector = RiskDetector()
    
    # Determine zone from NER results
    zone = 'commercial'  # default
    if 'ZONE' in ner_results:
        zone_text = ner_results['ZONE'][0].lower() if ner_results['ZONE'] else 'commercial'
        if 'residential' in zone_text:
            zone = 'residential'
        elif 'industrial' in zone_text:
            zone = 'industrial'
    
    risk_assessment = risk_detector.detect_unsafe_tradeoffs(
        time_saved=30,
        risk_increase=7.5,
        cost_increase=10,
        incidents_increase=0.2,
        zone=zone,
        policy_name=policy_name
    )
    print(f"✓ Risk Level: {risk_assessment['risk_level'].upper()}")
    if risk_assessment['flags']:
        print(f"  Flags: {len(risk_assessment['flags'])}")
    
    # ✅ Generate final report
    print("\n" + "=" * 70)
    print("PIPELINE COMPLETE - FINAL REPORT")
    print("=" * 70)
    
    report = {
        'policy_name': policy_name,
        'text_length': len(policy_text),
        'key_sentences': [s['sentence'][:100] for s in intent_results['key_sentences'][:3]],
        'entities_extracted': {k: v[:3] for k, v in ner_results.items()},
        'ambiguity': {
            'score': ambiguity_data['overall_score'],
            'trust_level': ambiguity_data['trust_level'],
            'critical_phrases': ambiguity_data['by_severity']['critical']
        },
        'classification': {
            'focus': classification['primary_classification'][:60],
            'confidence': classification['confidence'],
            'recommendation': classification['recommendation']
        },
        'risk_assessment': {
            'level': risk_assessment['risk_level'],
            'flags': len(risk_assessment['flags']),
            'recommendation': risk_assessment['recommendation']
        },
        'simulation_parameters': sim_params['simulation_parameters'],
        'overall_impact': {
            'trade_off_score': overall['trade_off_score'],
            'recommendation': overall['recommendation']
        }
    }
    
    print("\n📊 SUMMARY:")
    print(f"  Policy: {policy_name}")
    print(f"  Classification: {classification['primary_classification'][:50]}")
    print(f"  Ambiguity: {ambiguity_data['overall_score']:.1f}/100 ({ambiguity_data['trust_level']})")
    print(f"  Risk Level: {risk_assessment['risk_level'].upper()}")
    print(f"  Trade-off Score: {overall['trade_off_score']:.1f}/100")
    print(f"\n{overall['recommendation']}")
    
    # ✅ Save report
    report_dir = Path("data/results")
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{policy_name.replace(' ', '_')}_report.json"
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    print(f"\n✓ Report saved to: {report_path}")
    
    return report


def run_demo():
    """Run demo with sample policy text"""
    sample_policy = """
    CONSTRUCTION POLICY FOR RESIDENTIAL ZONES
    
    Night construction in residential zones is prohibited between 8 PM and 6 AM.
    Commercial construction sites must have weekly safety inspections.
    All demolition work requires structural integrity assessment.
    Road construction may continue during off-peak hours where feasible.
    
    Safety inspections should be conducted as required by site conditions.
    Contractors must make reasonable attempts to minimize noise where applicable.
    Emergency repairs may be permitted with proper authorization.
    
    Worker protection equipment is mandatory at all times.
    Heavy machinery operation is restricted during peak hours in residential areas.
    Construction permits must be displayed visibly at all work sites.
    """
    
    return run_civisim_pipeline(
        policy_text=sample_policy,
        policy_name="Sample Construction Policy"
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Running demo with sample policy...")
        print("Usage: python main.py <policy_file> [policy_name]")
        print("       python main.py --demo")
        print()
        run_demo()
    elif sys.argv[1] == "--demo":
        run_demo()
    else:
        policy_file = sys.argv[1]
        policy_name = sys.argv[2] if len(sys.argv) > 2 else Path(policy_file).stem
        run_civisim_pipeline(policy_file=policy_file, policy_name=policy_name)
