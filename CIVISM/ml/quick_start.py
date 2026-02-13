"""
Quick Start Script for CIVISIM ML Tasks
Run Task 1 and Task 2 on sample policy
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from models.document_parser import DocumentParser
from models.intent_extractor import PolicyIntentExtractor
import json


def main():
    """Run Tasks 1 and 2"""
    print("=" * 70)
    print("CIVISIM ML/AI - Quick Start Demo")
    print("Running Task 1 (Document Parsing) and Task 2 (Intent Extraction)")
    print("=" * 70)
    
    # ========================
    # TASK 1: Document Parsing
    # ========================
    print("\n" + "=" * 70)
    print("TASK 1: Policy Document Text Extraction")
    print("=" * 70)
    
    parser = DocumentParser()
    
    # Check for sample policy
    sample_file = Path("data/policy_samples/sample_construction_policy.txt")
    
    if sample_file.exists():
        print(f"\n✓ Found sample policy: {sample_file.name}")
        
        # Read the text file
        with open(sample_file, 'r', encoding='utf-8') as f:
            policy_text = f.read()
        
        print(f"✓ Loaded policy text ({len(policy_text)} characters)")
        
        # Create extraction result
        extraction_result = {
            'file_name': sample_file.name,
            'file_path': str(sample_file),
            'format': 'txt',
            'full_text': policy_text,
            'total_length': len(policy_text),
            'metadata': {}
        }
        
        # Save extraction
        output_name = sample_file.stem + "_extracted"
        parser.save_extraction(extraction_result, output_name)
        
    else:
        print(f"\n⚠️  Sample policy not found at: {sample_file}")
        print("   Creating sample policy...")
        sample_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Create sample content
        sample_content = """
        CONSTRUCTION POLICY GUIDELINES
        
        Night construction is permitted only in commercial zones with proper authorization.
        Residential zones have strict restrictions on night work to minimize noise disruption.
        Safety inspections are mandatory weekly for all construction sites.
        All workers must have proper safety equipment including hard hats and safety vests.
        Emergency procedures must be established and clearly posted at all sites.
        """
        
        with open(sample_file, 'w', encoding='utf-8') as f:
            f.write(sample_content.strip())
        
        policy_text = sample_content
        print(f"✓ Created sample policy")
    
    # ========================
    # TASK 2: Intent Extraction
    # ========================
    print("\n" + "=" * 70)
    print("TASK 2: Policy Intent & Keyword Extraction")
    print("=" * 70)
    
    print("\n🧠 Initializing DistilBERT model (this may take a moment)...")
    extractor = PolicyIntentExtractor()
    
    print("\n🔍 Analyzing policy intent...")
    intent_result = extractor.extract_intent(policy_text)
    
    print(f"\n✓ Analyzed {intent_result['total_sentences']} sentences")
    print("\n📌 Top Key Sentences:")
    for i, sent in enumerate(intent_result['key_sentences'][:3], 1):
        print(f"\n{i}. {sent['sentence'][:100]}...")
        print(f"   Importance Score: {sent['importance']:.3f}")
    
    # Keyword extraction
    print("\n\n🔑 Extracting Keyword Relevance...")
    
    # Load keywords from config
    config_file = Path("config/parameters.json")
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
            keywords = config.get('policy_keywords', [])
    else:
        keywords = [
            "night construction",
            "safety inspection",
            "residential zone",
            "commercial zone",
            "noise limits"
        ]
    
    keyword_scores = extractor.extract_keywords_semantic(policy_text, keywords)
    
    print(f"\n✓ Scored {len(keyword_scores)} keywords")
    print("\n📊 Top Relevant Keywords:")
    for item in keyword_scores[:5]:
        bar = "█" * int(item['relevance'] * 20)
        print(f"  {item['keyword']:25} {bar} {item['relevance']:.3f}")
    
    # Save results
    results_dir = Path("data/results")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    results = {
        'task1_extraction': extraction_result,
        'task2_intent': intent_result,
        'task2_keywords': keyword_scores
    }
    
    results_file = results_dir / "quick_start_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n\n💾 Results saved to: {results_file}")
    
    # Final summary
    print("\n" + "=" * 70)
    print("✅ Quick Start Complete!")
    print("=" * 70)
    print("\nCompleted Tasks:")
    print("  ✓ Task 1: Document text extraction")
    print("  ✓ Task 2: Policy intent and keyword extraction")
    print("\nNext Steps:")
    print("  • Add your own PDF/DOCX files to data/policy_samples/")
    print("  • Run: python models/document_parser.py")
    print("  • Run: python models/intent_extractor.py")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
