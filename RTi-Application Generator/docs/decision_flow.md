# Decision Flow Documentation

## Intent Classification Flow

```
Input: User's issue description
                │
                ▼
┌───────────────────────────────────┐
│     STEP 1: Keyword Matching      │
│   (Rule Engine - intent_rules.py) │
└───────────────────────────────────┘
                │
        ┌───────┴───────┐
        │               │
    MATCHED         NOT MATCHED
        │               │
        ▼               ▼
   Return Result   ┌─────────────────────┐
   (confidence:1.0)│ STEP 2: Legal Triggers│
                   │ (legal_triggers.py)  │
                   └─────────────────────┘
                            │
                    ┌───────┴───────┐
                    │               │
                MATCHED         NOT MATCHED
                    │               │
                    ▼               ▼
               Return Result   ┌─────────────────────┐
               (confidence:0.9)│ STEP 3: NLP Intent  │
                               │ (spacy_engine.py)   │
                               └─────────────────────┘
                                        │
                                        ▼
                               ┌─────────────────────┐
                               │ STEP 4: Semantic    │
                               │ (distilbert)        │
                               └─────────────────────┘
                                        │
                                        ▼
                               Return with Confidence Score
```

## Document Type Determination

| Signal | Document Type | Confidence |
|--------|---------------|------------|
| "information", "records", "RTI" | RTI Application | High |
| "complaint", "grievance", "problem" | Public Complaint | High |
| "appeal", "review", "reconsider" | Appeal | High |
| Mixed signals | Ask User | Low |

## Authority Resolution Flow

```
Issue Category + State
        │
        ▼
┌───────────────────────────────────┐
│  STEP 1: Department Mapping       │
│  (issue_rules.py)                 │
└───────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────┐
│  STEP 2: State-specific Authority │
│  (authority_resolver.py)          │
└───────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────┐
│  STEP 3: Semantic Match (if no    │
│  exact match) - distilbert        │
└───────────────────────────────────┘
        │
        ▼
Return Authority List with Confidence
```
