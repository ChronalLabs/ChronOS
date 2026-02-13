package com.rtigen.engine;

import com.rtigen.model.RtiDraft;
import org.springframework.stereotype.Service;
import java.util.ArrayList;
import java.util.List;

@Service
public class RuleEngine {

    /**
     * validateDraft checks the RTI draft for compliance.
     * 
     * @param draft The draft to validate.
     * @return List of suggestions/issues. Empty if perfect.
     */
    public List<String> validateDraft(RtiDraft draft) {
        List<String> issues = new ArrayList<>();
        List<String> validQuestions = new ArrayList<>();

        // Rule 1: Subject length
        if (draft.getSubject() == null || draft.getSubject().length() < 10) {
            issues.add("Subject is too short. Be timely and specific.");
        }

        // Rule 2: Question Check & Transform
        if (draft.getQuestions() != null) {
            for (String q : draft.getQuestions()) {
                String cleaned = q.trim();

                // Transformation: "Why" -> "Provide reasons/records"
                if (cleaned.toLowerCase().startsWith("why")) {
                    cleaned = cleaned.replaceFirst("(?i)why can't",
                            "Provide certified copies of records indicating reasons why cannot");
                    cleaned = cleaned.replaceFirst("(?i)why",
                            "Provide certified copies of records indicating reasons for");
                    issues.add("Transformed 'Why' question to records request: " + q + " -> " + cleaned);
                }

                // Transformation: "Opinion" -> Warn and try to fix
                if (cleaned.toLowerCase().contains("opinion")) {
                    issues.add("Flagged opinion request. Ensure you are asking for existing records.");
                }

                validQuestions.add(cleaned);
            }
            draft.setQuestions(validQuestions);
        }

        // Rule 3: Word Limit (implied)
        if (draft.getQuestions() != null && draft.getQuestions().size() > 20) {
            issues.add("Too many questions. Limit to focus area to avoid rejection.");
        }

        return issues;
    }

    public int calculateQualityScore(List<String> issues) {
        int baseScore = 100;
        return Math.max(0, baseScore - (issues.size() * 10)); // Deduct 10 per issue
    }
}
