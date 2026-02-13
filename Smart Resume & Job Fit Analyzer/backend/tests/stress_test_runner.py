import sys
import os
import time
import json
from collections import defaultdict
from tqdm import tqdm

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

try:
    import pydantic
    print(f"DEBUG: Pydantic version: {pydantic.VERSION}")
    print(f"DEBUG: Pydantic path: {pydantic.__file__}")
    from parsers.section_detector import detect_sections
    from tests.data_generator import generate_resume_data
except ImportError:
    print("DEBUG: Pydantic not installed or Import Error")
except Exception as e:
    print(f"DEBUG: Import Error: {e}")
    import traceback
    traceback.print_exc()


def run_stress_test(num_resumes=100):
    print(f"Starting stress test with {num_resumes} resumes...")
    
    results = {
        "passed": 0,
        "failed": 0,
        "partial": 0,
        "details": []
    }
    
    domain_stats = defaultdict(lambda: {"total": 0, "passed": 0})
    layout_stats = defaultdict(lambda: {"total": 0, "passed": 0})
    
    import random
    
    for i in tqdm(range(num_resumes)):
        # Generate resume with random layout
        layout = random.choice(["standard", "compact", "messy"])
        data = generate_resume_data(layout=layout)
        raw_text = data["raw_text"]
        metadata = data["metadata"]
        
        # Mock blocks (simplified for now as just lines with vertical spacing)
        # In a real scenario, we'd have OCR blocks. Here we simulate them from lines.
        lines = raw_text.split('\n')
        blocks = []
        full_text_reconstructed = ""
        current_top = 0
        for line in lines:
            if not line.strip():
                current_top += 20
                continue
            
            blocks.append({
                "text": line,
                "is_bold": line.isupper() and len(line) < 50, # Simple heuristic
                "left": 0,
                "top": current_top,
                "width": 500,
                "height": 12
            })
            current_top += 15
            full_text_reconstructed += line + "\n"
            
        # Parse
        try:
            sections = detect_sections(full_text_reconstructed, blocks)
            
            # Validation
            missing_critical = []
            if not sections.get("education"): missing_critical.append("education")
            if not sections.get("experience"): missing_critical.append("experience")
            if not sections.get("skills"): missing_critical.append("skills")
            
            # Check for specific expected data
            found_email = sections.get("contact_info", {}).get("email")
            email_match = found_email == metadata["email_expected"] if "email_expected" in metadata else True
            
            status = "passed"
            if missing_critical:
                status = "failed" if len(missing_critical) >= 2 else "partial"
                
            # Update stats
            results[status] += 1
            domain_stats[metadata["domain"]]["total"] += 1
            layout_stats[metadata["layout"]]["total"] += 1
            
            if status == "passed":
                domain_stats[metadata["domain"]]["passed"] += 1
                layout_stats[metadata["layout"]]["passed"] += 1
                
            results["details"].append({
                "id": i,
                "domain": metadata["domain"],
                "layout": metadata["layout"],
                "status": status,
                "missing": missing_critical,
                "email_match": email_match
            })
            
        except Exception as e:
            results["failed"] += 1
            results["details"].append({
                "id": i,
                "error": str(e),
                "status": "error"
            })
            print(f"ERROR processing resume {i}: {e}")
            import traceback
            traceback.print_exc(file=sys.stdout) # Print to stdout!
            
    # Print Report
    print("\n" + "="*50)
    print("STRESS TEST RESULTS")
    print("="*50)
    print(f"Total: {num_resumes}")
    print(f"Passed (All Critical Sections): {results['passed']}")
    print(f"Partial (Missing 1 Critical Section): {results['partial']}")
    print(f"Failed (Missing >= 2 Critical Sections): {results['failed']}")
    
    print("\nBy Domain:")
    for domain, stats in domain_stats.items():
        rate = (stats["passed"] / stats["total"]) * 100
        print(f"  {domain}: {rate:.1f}% ({stats['passed']}/{stats['total']})")
        
    print("\nBy Layout:")
    for layout, stats in layout_stats.items():
        rate = (stats["passed"] / stats["total"]) * 100
        print(f"  {layout}: {rate:.1f}% ({stats['passed']}/{stats['total']})")

    # Save detailed results
    with open("stress_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
        
if __name__ == "__main__":
    run_stress_test()
