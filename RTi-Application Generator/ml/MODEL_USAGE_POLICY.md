# 🚨 MODEL USAGE POLICY

## Non-Negotiable Rules for AI/ML in This Project

### 1. Rule Engine is PRIMARY
- All structural decisions MUST go through the rule engine first
- AI/NLP is ONLY used when rules cannot determine the answer
- Never bypass rules with AI predictions
- **File**: `backend/app/services/rule_engine/`

### 2. AI is BOUNDED
- **spaCy**: Used ONLY for NER (Named Entity Recognition) and phrase matching
  - File: `backend/app/services/nlp/spacy_engine.py`
  - Model: `en_core_web_sm`
  - Memory: ~50MB
  
- **DistilBERT**: Used ONLY for semantic similarity ranking, NOT generation
  - File: `backend/app/services/nlp/distilbert_semantic.py`
  - Model: `distilbert-base-uncased`
  - Memory: ~250MB
  
  
- **No generative AI** (GPT, Claude, etc.) for document content

### 3. Confidence Gating
- Any AI prediction below 70% confidence MUST trigger user confirmation
- Low confidence results should show alternatives
- Users can always override AI suggestions
- **File**: `backend/app/services/nlp/confidence_gate.py`
- **Thresholds**:
  - HIGH: > 90% → Auto-apply
  - MEDIUM: 70-90% → Suggest with highlight
  - LOW: 50-70% → Show alternatives
  - VERY_LOW: < 50% → Manual input required

### 4. No Hallucination Risk
- Document templates are human-written
- AI only fills placeholders with extracted/validated data
- No free-form text generation for legal content

### 5. Audit Trail
- All AI decisions must be logged
- Users can see why a decision was made
- Explainability is mandatory
- Audit functions in `confidence_gate.py`: `log_gating_decision()`, `get_audit_log()`

## Control Flow

```
User Input
    ↓
Rule Engine (PRIMARY)
    ↓
[Confidence < 70%?]
    ↓ Yes
spaCy NLP (Entity Enhancement)
    ↓
[Still Low Confidence?]
    ↓ Yes
DistilBERT (Semantic Similarity)
    ↓
Confidence Gate
    ↓
[Requires Confirmation?]
    ↓ Yes
User Confirmation
    ↓
Template Assembly (No AI)
    ↓
Document Generation
```

## Forbidden Actions
❌ Using AI to generate legal advice  
❌ Auto-submitting documents without user review  
❌ Storing user data beyond session  
❌ Training models on user input without consent  
❌ Bypassing rule engine with AI predictions
❌ Using confidence > 95% (always leave room for uncertainty)

## Allowed Actions
✅ Entity extraction (names, dates, organizations)  
✅ Intent classification (RTI vs Complaint)  
✅ Authority matching via semantic similarity  
✅ Language detection and normalization  
✅ Keyword and phrase matching

## File Structure

```
ml/
├── MODEL_USAGE_POLICY.md     # This file
├── model_manager.py          # Centralized model management
└── requirements.txt          # ML-specific dependencies

backend/app/services/
├── nlp/
│   ├── __init__.py
│   ├── spacy_engine.py       # NER & phrase matching
│   ├── distilbert_semantic.py # Similarity ranking
│   └── confidence_gate.py    # Gating decisions
├── rule_engine/
│   ├── __init__.py
│   ├── intent_rules.py       # Intent classification
│   ├── issue_rules.py        # Issue-department mapping
│   └── legal_triggers.py     # Legal references
└── ...
```

## Testing Guidelines

1. **Unit Tests**: Test each component in isolation
2. **Integration Tests**: Test the full control flow
3. **Confidence Tests**: Verify gating works correctly
4. **Edge Cases**: Test with ambiguous inputs
5. **Performance**: Monitor model loading and inference times

## Model Versions

| Model | Version | Purpose | Memory |
|-------|---------|---------|--------|
| spaCy | en_core_web_sm | NER, POS, Dependencies | ~50MB |
| DistilBERT | distilbert-base-uncased | Semantic Similarity | ~250MB |
| Rule Engine | 1.0.0 | Primary Decisions | N/A |

## Performance Targets

- Rule Engine: < 10ms
- spaCy NER: < 100ms
- DistilBERT Similarity: < 500ms (first call), < 50ms (cached)
- Full Analysis: < 1s total  
