# Legal Constraints: RTI Act 2005

## Core Rules for RTI Generation
These rules must be enforced by the Rule Engine and AI post-processing.

### 1. No Opinions (Section 2(f))
- **Rule:** Do not ask "Why" or "How".
- **Reason:** Public Information Officers (PIOs) are only required to furnish "information" that already exists in material form. They are not required to create answers or give opinions.
- **Fix:** Convert "Why is road bad?" -> "Provide certified copies of the inspection report for the road."

### 2. Word Limit (State Specific)
- **Rule:** Keep questions concise (usually < 150 words in total context is best practice, though Act says 500 words in some states).
- **Fix:** Split large queries into multiple applications.

### 3. Third Party Information (Section 8(1)(j))
- **Rule:** Do not ask for personal details of others (Medical records, salaries of peers).
- **Reason:** Exempt from disclosure unless public interest is proven.

### 4. Life & Liberty (Section 7(1))
- **Rule:** If life/liberty is at stake, info must be given in 48 hours.
- **Flag:** Detect urgency words ("Death", "Arrest", "Emergency").
