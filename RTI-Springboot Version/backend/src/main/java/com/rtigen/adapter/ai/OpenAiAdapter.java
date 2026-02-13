package com.rtigen.adapter.ai;

import org.springframework.stereotype.Service;
import org.springframework.context.annotation.Primary;
import java.util.Map;
import lombok.extern.slf4j.Slf4j;
import com.rtigen.dto.*;
import java.util.List;
import java.util.Collections;

/**
 * Production implementation would use RestTemplate/WebClient to call OpenAI
 * API.
 * Currently falls back to local logic if no API key is present (Simulated).
 */
@Service("cloudAiAdapter")
@Primary
public class OpenAiAdapter implements AiAdapter {

    private static final org.slf4j.Logger log = org.slf4j.LoggerFactory.getLogger(OpenAiAdapter.class);

    @org.springframework.beans.factory.annotation.Value("${openai.api.key:}")
    private String apiKey;

    @org.springframework.beans.factory.annotation.Value("${AI_ADAPTER:local}")
    private String activeAdapter;

    private final LocalLlmAdapter fallback;
    private final org.springframework.web.client.RestTemplate restTemplate;
    private final com.fasterxml.jackson.databind.ObjectMapper objectMapper;

    public OpenAiAdapter(LocalLlmAdapter fallback) {
        this.fallback = fallback;
        org.springframework.http.client.SimpleClientHttpRequestFactory factory = new org.springframework.http.client.SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(5000); // 5 seconds
        factory.setReadTimeout(60000); // 60 seconds
        this.restTemplate = new org.springframework.web.client.RestTemplate(factory);
        this.objectMapper = new com.fasterxml.jackson.databind.ObjectMapper();
    }

    @Override
    public Map<String, Object> analyzeIntent(String plainText) {
        if (!"openai".equalsIgnoreCase(activeAdapter)) {
            log.info("AI_ADAPTER is not 'openai', falling back to local.");
            return fallback.analyzeIntent(plainText);
        }

        try {
            log.info("Calling OpenAI API for intent...");
            String url = "https://api.openai.com/v1/chat/completions";

            Map<String, Object> parsedBody = callOpenAi(url,
                    "You are an expert Indian RTI Act Drafting Assistant. Analyze the user's input and extract the following JSON fields: 'subject' (concise title), 'department' (government dept), 'classification' (EDUCATION, MUNICIPAL, POLICE, or GENERAL). Return ONLY valid JSON.",
                    plainText);

            return parsedBody;
        } catch (Exception e) {
            log.error("OpenAI call failed", e);
            return fallback.analyzeIntent(plainText);
        }
    }

    @Override
    public String generateQuestions(Map<String, Object> context) {
        if (!"openai".equalsIgnoreCase(activeAdapter)) {
            return fallback.generateQuestions(context);
        }

        try {
            log.info("Calling OpenAI API for questions...");
            String promptContext = "Subject: " + context.get("subject") + ", Dept: " + context.get("department");

            Map<String, Object> result = callOpenAi("https://api.openai.com/v1/chat/completions",
                    "You are an RTI Expert. Generate 3-4 specific, legally potent questions for an RTI application based on the context. Return them as a numbered list (1., 2., 3.) separated by newlines. Do not include intro/outro text.",
                    promptContext);

            // Quick hack: callOpenAi returns the content String. analyzeIntent parses it.
            return (String) result.get("content_raw");
        } catch (Exception e) {
            log.error("OpenAI questions failed", e);
            return fallback.generateQuestions(context);
        }
    }

    private Map<String, Object> callOpenAi(String url, String systemPrompt, String userMsg) {
        org.springframework.http.HttpHeaders headers = new org.springframework.http.HttpHeaders();
        headers.setContentType(org.springframework.http.MediaType.APPLICATION_JSON);
        headers.setBearerAuth(apiKey);

        Map<String, Object> body = new java.util.HashMap<>();
        body.put("model", "gpt-4"); // or gpt-3.5-turbo
        // body.put("temperature", 0.7); // Optional: Adjust if needed

        body.put("messages", java.util.List.of(
                Map.of("role", "system", "content", systemPrompt),
                Map.of("role", "user", "content", userMsg)));

        org.springframework.http.HttpEntity<Map<String, Object>> request = new org.springframework.http.HttpEntity<>(
                body, headers);

        try {
            @SuppressWarnings("unchecked")
            Map<String, Object> response = restTemplate.postForObject(url, request, Map.class);
            if (response == null || !response.containsKey("choices"))
                return new java.util.HashMap<>();

            java.util.List<Map<String, Object>> choices = (java.util.List<Map<String, Object>>) response.get("choices");
            if (choices.isEmpty())
                return new java.util.HashMap<>();

            Map<String, Object> message = (Map<String, Object>) choices.get(0).get("message");
            String content = (String) message.get("content");

            // Clean up Markdown backticks if present
            if (content.startsWith("```json")) {
                content = content.replace("```json", "").replace("```", "").trim();
            } else if (content.startsWith("```")) {
                content = content.replace("```", "").trim();
            }

            // Check if we need to parse JSON
            if (content.trim().startsWith("{")) {
                try {
                    return objectMapper.readValue(content,
                            new com.fasterxml.jackson.core.type.TypeReference<Map<String, Object>>() {
                            });
                } catch (Exception e) {
                    log.warn("Failed to parse JSON from OpenAI: " + content);
                    // Fallback: return raw content in map
                }
            }

            // Return raw content wrapped
            Map<String, Object> wrap = new java.util.HashMap<>();
            wrap.put("content_raw", content);
            return wrap;

        } catch (Exception e) {
            throw new RuntimeException("API Call Failed", e);
        }
    }

    @Override
    public com.rtigen.dto.SuggestionResponse generateSuggestions(com.rtigen.dto.SuggestionRequest request) {
        if (!"openai".equalsIgnoreCase(activeAdapter)) {
            // Fallback for local dev without key
            return new com.rtigen.dto.SuggestionResponse(
                    java.util.List.of(new com.rtigen.dto.SuggestionResponse.Suggestion("local-1", "reword",
                            "Please specify the date of application.", 0.9, false)),
                    new com.rtigen.dto.SuggestionResponse.Meta("local", java.time.LocalDateTime.now().toString()));
        }

        try {
            String systemPrompt = "You are an assistant that provides short, actionable suggestions and clarifying questions to help a human compose an RTI application. Output strictly as JSON with keys: suggestions (array). Each suggestion must include id, type (\"reword\"|\"clarify\"|\"add_question\"), text, and confidence (0-1). Do not return any raw markdown or extraneous text. Keep suggestions short (max 40 words).";
            String userMsg = objectMapper.writeValueAsString(request);

            Map<String, Object> result = callOpenAi("https://api.openai.com/v1/chat/completions", systemPrompt,
                    userMsg);

            // Convert Map back to DTO
            return objectMapper.convertValue(result, com.rtigen.dto.SuggestionResponse.class);
        } catch (Exception e) {
            log.error("Suggestion logic failed", e);
            return new com.rtigen.dto.SuggestionResponse();
        }
    }

    @Override
    public com.rtigen.dto.DraftResponse generateStructuredDraft(com.rtigen.dto.DraftRequest request) {
        if (!"openai".equalsIgnoreCase(activeAdapter)) {
            // Simple fallback
            return new com.rtigen.dto.DraftResponse(
                    "<p>Local Mode Draft</p>",
                    "Local Mode Draft",
                    java.util.List.of("Q1?", "Q2?"),
                    java.util.List.of());
        }

        try {
            String baseTemplate = "To,\\nThe Public Information Officer,\\n[Department Name],\\n[Address]\\n\\nDate: [Current Date]\\nSubject: Request for information under Right to Information Act, 2005.\\n\\nSir / Ma'am,\\nPlease provide true, certified copies of the following information:\\n1. [Question 1]\\n2. [Question 2]\\n...\\n\\nName: [Applicant Name]\\nAddress: [Address]\\nMobile: [Mobile]\\n\\nI hereby inform that:\\nI am a citizen of India.\\nI am above the poverty line.\\nA copy of my ID proof is attached.\\n\\n[Signature Space]\\nSignature of the applicant";

            String selectedLanguage = request.getLanguage() != null ? request.getLanguage() : "en";
            boolean isHindi = "hi".equalsIgnoreCase(selectedLanguage);

            String instructions = "Follow these STRICT rules:\n"
                    + "1. **STRICT FORMAT LOCK**: The output HTML MUST MATCH the provided legal structure EXACTLY. Do NOT add new sections, change headings, or reorder paragraphs.\n"
                    + "2. **DATA INJECTION**: Use 'department.address' for [Address], 'applicant.mobile' for [Mobile], and 'applicant.name' for [Applicant Name]. Do NOT invent them.\n"
                    + "3. **DATE**: Insert today's date.\n";

            if (isHindi) {
                instructions += "4. **LANGUAGE**: Translate the ENTIRE content to Hindi (Devanagari script). \n"
                        + "   - **MANDATORY**: You MUST transliterate English proper nouns (Name, Address, City) to Hindi (e.g., 'Yogesh Sanodiya' -> 'योगेश सनोजिया', 'Krishna Nagar' -> 'कृष्णा नगर'). \n"
                        + "   - **OFFICE ADDRESS**: Translate the Department Address completely to Hindi. Do NOT leave it in English.\n"
                        + "   - **SUBJECT**: Translate the subject summary to Hindi. Do NOT include the original English text.\n"
                        + "   - PRESERVE the exact HTML structure.\n";
            } else {
                instructions += "4. **LANGUAGE**: Keep the content in English 'Times New Roman' style.\n";
            }

            String systemPrompt;
            if ("ai".equalsIgnoreCase(request.getMode())) {
                // AI Mode: Smart Expansion + Compliance
                systemPrompt = "You are an expert RTI Act Consultant. " + instructions
                        + "5. **SMART EXPANSION**: Convert the user's issue into 4-5 specific, technical RTI questions (e.g., 'certified copies of muster rolls') "
                        + (isHindi ? "in Hindi" : "in English") + ". \n"
                        + "   - **IMPORTANT**: If the JSON input contains 'acceptedSuggestions', YOU MUST INCLUDE THEM as additional questions.\n"
                        + "6. **COMPLIANCE**: Ensure questions are Section 6(1) compliant (fact-based).\n"
                        + "Output JSON with keys: `draftHtml`, `plainText`, `questions`, `complianceLog` (Status Block).";
            } else {
                // Assisted Mode: Strict Formatter + Compliance
                systemPrompt = "You are a Legal Drafting Assistant. " + instructions
                        + "5. **STRICT FORMATTING**: Use the user's questions exactly as provided, just polish grammar "
                        + (isHindi ? "in Hindi" : "in English") + ". \n"
                        + "   - **CRITICAL**: The input JSON contains 'acceptedSuggestions'. You MUST include these as numbered questions in the draft. Do NOT ignore them.\n"
                        + "   - Do NOT invent new questions outside of the provided issue and suggestions.\n"
                        + "6. **COMPLIANCE CHECK**: Generate a 'complianceLog' block (Green/Yellow/Red) checking Section 6(1) and PIO addressing.\n"
                        + "Output JSON with keys: `draftHtml`, `plainText`, `questions`, `complianceLog` (Status Block).";
            }

            String userMsg = objectMapper.writeValueAsString(request);

            Map<String, Object> result = callOpenAi("https://api.openai.com/v1/chat/completions", systemPrompt,
                    userMsg);

            // Fallback: If AI returns raw text instead of JSON, parse it as best effort
            if (result.containsKey("content_raw")) {
                String raw = (String) result.get("content_raw");
                return new DraftResponse(
                        raw, // Treat raw content as draftHtml
                        raw, // Treat raw content as plainText
                        java.util.Collections.emptyList(),
                        java.util.List.of("Warning: Parsing failed, specific fields missing."));
            }

            return objectMapper.convertValue(result, com.rtigen.dto.DraftResponse.class);
        } catch (Exception e) {
            log.error("Draft generation failed", e);
            throw new RuntimeException("Draft generation failed", e);
        }
    }
}
