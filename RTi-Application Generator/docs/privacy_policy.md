# Privacy Policy

## Data Handling Principles

### No Database, No Storage

This application is designed with **privacy-first architecture**:

- ❌ No user database
- ❌ No session persistence
- ❌ No analytics tracking
- ❌ No third-party data sharing

### What Happens to Your Data

```
User Input ──▶ Process in Memory ──▶ Generate Document ──▶ Return to User
                     │
                     ▼
              Data Discarded
           (Not stored anywhere)
```

### Data Flow

| Data Type | Collected | Stored | Shared |
|-----------|-----------|--------|--------|
| Name | Yes (for document) | No | No |
| Address | Yes (for document) | No | No |
| Issue Description | Yes (for processing) | No | No |
| Generated Document | No (returned to user) | No | No |
| IP Address | No | No | No |
| Browser Info | No | No | No |

### Session Behavior

- Each request is independent
- No cookies for tracking
- No login required
- Closing browser = all data gone

### Why This Design?

1. **Legal Protection** - We don't want responsibility for storing sensitive legal queries
2. **User Trust** - Citizens may fear surveillance; we eliminate that concern
3. **Simplicity** - No GDPR/data protection compliance needed for stored data
4. **Security** - Can't leak data we don't have

### User Responsibilities

Since we don't store your documents:
- Download and save your generated documents
- Keep copies of your applications
- Track your own submissions

### Contact

For privacy concerns, please open an issue on the project repository.
