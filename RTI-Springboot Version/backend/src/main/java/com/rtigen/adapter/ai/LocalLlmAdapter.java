package com.rtigen.adapter.ai;

import org.springframework.stereotype.Service;
import com.rtigen.dto.*;
import java.util.Collections;
import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

@Service("localAiAdapter")
public class LocalLlmAdapter implements AiAdapter {

    private static final org.slf4j.Logger log = org.slf4j.LoggerFactory.getLogger(LocalLlmAdapter.class);

    @Override
    public Map<String, Object> analyzeIntent(String plainText) {
        log.info("Using Local LLM Adapter for intent analysis");
        // Simulated local AI logic (Rules/Regex/Stub)
        Map<String, Object> result = new HashMap<>();

        if (plainText.toLowerCase().contains("scholarship")) {
            result.put("classification", "EDUCATION");
            result.put("department", "Social Welfare Department");
            result.put("subject", "Request for information regarding scholarship delay");
        } else if (plainText.toLowerCase().contains("road") || plainText.toLowerCase().contains("repair")) {
            result.put("classification", "MUNICIPAL");
            result.put("department", "Public Works Department");
            result.put("subject", "Request for status of road repair works");
        } else {
            result.put("classification", "GENERAL");
            result.put("department", "Public Information Officer");
            result.put("subject", "Application under RTI Act 2005");
        }

        return result;
    }

    @Override
    public String generateQuestions(Map<String, Object> context) {
        log.info("Using Local LLM Adapter for question generation");
        return "1. [Auto-Generated Question 1]\n2. [Auto-Generated Question 2]";
    }

    @Override
    public com.rtigen.dto.SuggestionResponse generateSuggestions(com.rtigen.dto.SuggestionRequest request) {
        return new com.rtigen.dto.SuggestionResponse(
                java.util.List.of(new com.rtigen.dto.SuggestionResponse.Suggestion("local-s1", "reword",
                        "Please specify the date of application.", 0.85, false)),
                new com.rtigen.dto.SuggestionResponse.Meta("local-model", java.time.LocalDateTime.now().toString()));
    }

    @Override
    public com.rtigen.dto.DraftResponse generateStructuredDraft(com.rtigen.dto.DraftRequest request) {
        String applicantName = (request.getApplicant() != null) ? request.getApplicant().getName() : "Unknown";
        String deptName = (request.getDepartment() != null) ? request.getDepartment().getName() : "Unknown Dept";
        return new com.rtigen.dto.DraftResponse(
                "<div class='p-4'><h3>Local Draft</h3><p>Applicant: " + applicantName + "</p><p>Dept: " + deptName
                        + "</p><p>Mode: "
                        + request.getMode() + "</p></div>",
                "Local Draft Plain Text",
                java.util.List.of("1. Local Q1?", "2. Local Q2?"),
                java.util.List.of());
    }
}
