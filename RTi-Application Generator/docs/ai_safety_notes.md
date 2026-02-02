# AI Safety Notes

## Why AI is Bounded in This Project

### The Problem with Unconstrained AI

1. **Legal Documents Require Accuracy** - Incorrect legal citations or wrong authorities can invalidate applications
2. **Hallucination Risk** - Generative AI can produce plausible but incorrect information
3. **User Trust** - Citizens need to trust their applications are correct
4. **Accountability** - Someone must be responsible for document content

### Our Approach: AI as Assistant, Not Author

```
┌─────────────────────────────────────────────────────────┐
│                    SAFE ZONE                            │
│                                                         │
│  ✅ Entity Extraction (names, dates, places)            │
│  ✅ Classification (RTI vs Complaint)                   │
│  ✅ Similarity Matching (authority lookup)              │
│  ✅ Language Detection                                  │
│  ✅ Spell Correction (with user confirmation)           │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   DANGER ZONE (FORBIDDEN)               │
│                                                         │
│  ❌ Generating legal text from scratch                  │
│  ❌ Auto-filling authority addresses without lookup     │
│  ❌ Deciding document type without user confirmation    │
│  ❌ Submitting on behalf of users                       │
│  ❌ Storing/learning from user data                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Confidence Thresholds

| Confidence | Action |
|------------|--------|
| > 90% | Auto-apply (with undo option) |
| 70-90% | Suggest with highlight |
| 50-70% | Show alternatives, ask user |
| < 50% | Manual input required |

### Audit Requirements

Every AI decision must log:
1. Input text (anonymized)
2. Model used
3. Confidence score
4. Final decision
5. User override (if any)

### Human-in-the-Loop Checkpoints

1. **Document Type** - User must confirm RTI vs Complaint
2. **Authority Selection** - User must verify target office
3. **Final Draft** - User must review before download
4. **Submission** - User manually submits (no auto-submit)
