"""
Experience depth signal extractor.
Detects duration, scale, leadership, and technical complexity signals.
Returns structured signals for rule engine consumption.
"""
import re
from typing import Optional
from dataclasses import dataclass


@dataclass
class ExperienceSignal:
    """Structured experience depth signal."""
    category: str
    text: str
    value: Optional[float] = None
    confidence: str = "medium"
    source_text: str = ""


def extract_signals(text: str) -> list[ExperienceSignal]:
    """
    Extract experience depth signals from text.
    
    Args:
        text: Resume text (experience section)
    
    Returns:
        List of ExperienceSignal objects
    """
    signals = []
    
    # Duration signals
    signals.extend(_extract_duration_signals(text))
    
    # Scale signals
    signals.extend(_extract_scale_signals(text))
    
    # Leadership signals
    signals.extend(_extract_leadership_signals(text))
    
    # Technical complexity signals
    signals.extend(_extract_complexity_signals(text))
    
    return signals


def _extract_duration_signals(text: str) -> list[ExperienceSignal]:
    """Extract duration-related signals."""
    signals = []
    text_lower = text.lower()
    
    # Years of experience
    years_pattern = r"(\d+)\+?\s*years?\s*(of\s*)?(experience|exp)?"
    for match in re.finditer(years_pattern, text_lower):
        years = int(match.group(1))
        signals.append(ExperienceSignal(
            category="duration",
            text=match.group(),
            value=years,
            confidence="high" if years >= 3 else "medium",
            source_text=_get_surrounding_text(text, match.start(), match.end()),
        ))
    
    # Months (for shorter durations)
    months_pattern = r"(\d+)\s*months?\s*(of\s*)?(experience|exp)?"
    for match in re.finditer(months_pattern, text_lower):
        months = int(match.group(1))
        signals.append(ExperienceSignal(
            category="duration",
            text=match.group(),
            value=months / 12,  # Convert to years
            confidence="medium",
            source_text=_get_surrounding_text(text, match.start(), match.end()),
        ))
    
    return signals


def _extract_scale_signals(text: str) -> list[ExperienceSignal]:
    """Extract scale-related signals."""
    signals = []
    text_lower = text.lower()
    
    patterns = [
        # Team size
        (r"team of (\d+)", "team_size", lambda m: int(m.group(1))),
        (r"(\d+)\s*(engineers?|developers?|members?)", "team_size", lambda m: int(m.group(1))),
        
        # User/traffic scale
        (r"(\d+)\s*(million|m)\s*(users?|customers?|requests?)", "user_scale", 
         lambda m: int(m.group(1)) * 1_000_000),
        (r"(\d+)\s*(thousand|k)\s*(users?|customers?|requests?)", "user_scale",
         lambda m: int(m.group(1)) * 1_000),
        
        # Data scale
        (r"(\d+)\s*(tb|terabytes?)", "data_scale", lambda m: int(m.group(1)) * 1000),
        (r"(\d+)\s*(gb|gigabytes?)", "data_scale", lambda m: int(m.group(1))),
    ]
    
    for pattern, subcategory, value_fn in patterns:
        for match in re.finditer(pattern, text_lower):
            try:
                value = value_fn(match)
                signals.append(ExperienceSignal(
                    category="scale",
                    text=match.group(),
                    value=value,
                    confidence="high",
                    source_text=_get_surrounding_text(text, match.start(), match.end()),
                ))
            except (ValueError, IndexError):
                continue
    
    # Qualitative scale indicators
    qualitative_patterns = [
        (r"large[- ]?scale", 50),
        (r"high[- ]?traffic", 50),
        (r"enterprise", 40),
        (r"production", 30),
        (r"global", 35),
    ]
    
    for pattern, value in qualitative_patterns:
        if re.search(pattern, text_lower):
            signals.append(ExperienceSignal(
                category="scale",
                text=pattern,
                value=value,
                confidence="medium",
            ))
    
    return signals


def _extract_leadership_signals(text: str) -> list[ExperienceSignal]:
    """Extract leadership-related signals."""
    signals = []
    text_lower = text.lower()
    
    leadership_patterns = [
        (r"led\s+(a\s+)?team", 100, "high"),
        (r"managed\s+(a\s+)?team", 100, "high"),
        (r"supervised", 80, "high"),
        (r"mentored", 70, "high"),
        (r"trained", 60, "medium"),
        (r"coordinated", 50, "medium"),
        (r"guided", 50, "medium"),
        (r"headed", 90, "high"),
        (r"directed", 80, "high"),
        (r"oversaw", 70, "high"),
    ]
    
    for pattern, value, confidence in leadership_patterns:
        match = re.search(pattern, text_lower)
        if match:
            signals.append(ExperienceSignal(
                category="leadership",
                text=match.group(),
                value=value,
                confidence=confidence,
                source_text=_get_surrounding_text(text, match.start(), match.end()),
            ))
    
    return signals


def _extract_complexity_signals(text: str) -> list[ExperienceSignal]:
    """Extract technical complexity signals."""
    signals = []
    text_lower = text.lower()
    
    complexity_patterns = [
        (r"architected", 100, "high"),
        (r"designed\s+(and\s+)?implemented", 90, "high"),
        (r"built\s+from\s+scratch", 85, "high"),
        (r"full[- ]?stack", 70, "medium"),
        (r"end[- ]?to[- ]?end", 65, "medium"),
        (r"scalable", 60, "medium"),
        (r"optimized", 55, "medium"),
        (r"refactored", 50, "medium"),
        (r"automated", 50, "medium"),
        (r"migrated", 45, "medium"),
        (r"integrated", 40, "medium"),
    ]
    
    for pattern, value, confidence in complexity_patterns:
        match = re.search(pattern, text_lower)
        if match:
            signals.append(ExperienceSignal(
                category="technical_complexity",
                text=match.group(),
                value=value,
                confidence=confidence,
                source_text=_get_surrounding_text(text, match.start(), match.end()),
            ))
    
    # Check for impact metrics
    impact_patterns = [
        (r"improved\s+.*?by\s+(\d+)\s*%", "improvement"),
        (r"reduced\s+.*?by\s+(\d+)\s*%", "improvement"),
        (r"increased\s+.*?by\s+(\d+)\s*%", "improvement"),
        (r"(\d+)x\s+(faster|improvement|increase)", "multiplier"),
    ]
    
    for pattern, category in impact_patterns:
        match = re.search(pattern, text_lower)
        if match:
            signals.append(ExperienceSignal(
                category="impact",
                text=match.group(),
                value=None,
                confidence="high",
                source_text=_get_surrounding_text(text, match.start(), match.end()),
            ))
    
    return signals


def _get_surrounding_text(text: str, start: int, end: int, window: int = 50) -> str:
    """Get surrounding context for a match."""
    context_start = max(0, start - window)
    context_end = min(len(text), end + window)
    return text[context_start:context_end]


def aggregate_signals(signals: list[ExperienceSignal]) -> dict:
    """
    Aggregate signals into summary scores.
    
    Returns a dictionary with category scores for rule engine.
    """
    category_scores = {
        "duration": 0.0,
        "scale": 0.0,
        "leadership": 0.0,
        "technical_complexity": 0.0,
        "impact": 0.0,
    }
    
    category_counts = {k: 0 for k in category_scores}
    
    for signal in signals:
        if signal.category in category_scores and signal.value is not None:
            # Weight by confidence
            confidence_weight = {"high": 1.0, "medium": 0.7, "low": 0.4}.get(signal.confidence, 0.5)
            category_scores[signal.category] += signal.value * confidence_weight
            category_counts[signal.category] += 1
    
    # Normalize scores
    for category in category_scores:
        if category_counts[category] > 0:
            category_scores[category] /= category_counts[category]
    
    return category_scores
