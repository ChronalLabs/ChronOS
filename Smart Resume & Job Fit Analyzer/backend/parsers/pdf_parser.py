"""
PDF parsing module using pdfplumber.
Extracts text with layout awareness for section detection.
"""
import pdfplumber
from typing import Tuple


def parse_pdf(file_path: str) -> Tuple[str, list[dict]]:
    """
    Parse a PDF file and extract text with positioning.
    
    Args:
        file_path: Path to the PDF file
    
    Returns:
        Tuple of (raw_text, text_blocks)
        - raw_text: Full concatenated text
        - text_blocks: List of text blocks with coordinates
    """
    text_blocks = []
    raw_text_parts = []
    
    with pdfplumber.open(file_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            # Extract text with layout
            text = page.extract_text() or ""
            raw_text_parts.append(text)
            
            # Extract text with positioning for layout analysis
            words = page.extract_words()
            
            # Group words into lines based on vertical position
            lines = _group_words_into_lines(words)
            
            for line_num, line_data in enumerate(lines, start=1):
                text_blocks.append({
                    "text": line_data["text"],
                    "page": page_num,
                    "line": line_num,
                    "top": line_data["top"],
                    "left": line_data.get("left", 0),
                    "font_size": line_data.get("font_size"),
                    "is_bold": line_data.get("is_bold", False),
                })
    
    raw_text = "\n".join(raw_text_parts)
    return raw_text, text_blocks


def _group_words_into_lines(words: list[dict], tolerance: float = 3.0) -> list[dict]:
    """
    Group words into lines based on vertical position.
    
    Args:
        words: List of word dictionaries from pdfplumber
        tolerance: Vertical tolerance for grouping
    
    Returns:
        List of line dictionaries with combined text
    """
    if not words:
        return []
    
    # Sort by vertical position, then horizontal
    sorted_words = sorted(words, key=lambda w: (w.get("top", 0), w.get("x0", 0)))
    
    lines = []
    current_line = {
        "words": [],
        "top": sorted_words[0].get("top", 0),
    }
    
    for word in sorted_words:
        word_top = word.get("top", 0)
        
        # Check if word is on the same line
        if abs(word_top - current_line["top"]) <= tolerance:
            current_line["words"].append(word)
        else:
            # Save current line and start new one
            if current_line["words"]:
                lines.extend(_finalize_line_with_gaps(current_line))
            current_line = {
                "words": [word],
                "top": word_top,
            }
    
    # Don't forget the last line
    if current_line["words"]:
        lines.extend(_finalize_line_with_gaps(current_line))
    
    return lines


def _finalize_line_with_gaps(line_data: dict, gap_threshold: float = 50.0) -> list[dict]:
    """
    Finalize a line by combining words, but splitting if there are large gaps (columns).
    Returns a list of text block dicts.
    """
    words = sorted(line_data["words"], key=lambda w: w.get("x0", 0))
    if not words:
        return []
    
    # Identify segments based on gaps
    segments = []
    current_segment = [words[0]]
    
    for i in range(1, len(words)):
        prev_word = words[i-1]
        curr_word = words[i]
        
        # Calculate gap between end of prev word and start of current word
        gap = curr_word.get("x0", 0) - prev_word.get("x1", 0)
        
        if gap > gap_threshold:
            # End current segment
            segments.append(current_segment)
            current_segment = [curr_word]
        else:
            current_segment.append(curr_word)
    
    segments.append(current_segment)
    
    # Create blocks for each segment
    results = []
    for segment in segments:
        text = " ".join(w.get("text", "") for w in segment)
        
        # Get approximate font size from first word
        font_size = None
        if segment and "height" in segment[0]:
            font_size = segment[0]["height"]
            
        results.append({
            "text": text.strip(),
            "top": line_data["top"],
            "left": segment[0].get("x0", 0),
            "font_size": font_size,
            "is_bold": False,  # pdfplumber doesn't easily expose font weight
        })
            
    return results
