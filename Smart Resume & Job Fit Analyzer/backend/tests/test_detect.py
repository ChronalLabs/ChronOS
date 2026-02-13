import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

try:
    from parsers.section_detector import detect_sections
    print("Imported detect_sections successfully")
    
    # Mock blocks
    text = "Anurag Mishra\nSoftware Engineer"
    blocks = [{"text": "Anurag Mishra", "top": 0, "left": 0}, {"text": "Software Engineer", "top": 20, "left": 0}]
    
    sections = detect_sections(text, blocks)
    print("Detected sections successfully")
    print(sections)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
