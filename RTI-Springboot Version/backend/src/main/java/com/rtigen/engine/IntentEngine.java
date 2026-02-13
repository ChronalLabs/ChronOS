package com.rtigen.engine;

import com.rtigen.adapter.ai.AiAdapter;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.Map;

@Service
public class IntentEngine {

    private final AiAdapter aiAdapter;

    public IntentEngine(AiAdapter aiAdapter) {
        this.aiAdapter = aiAdapter;
    }

    public Map<String, Object> analyze(String plainText) {
        // 1. Mask PII
        String maskedText = com.rtigen.service.util.PiiMaskingUtil.mask(plainText);

        // 2. Call AI with masked text
        Map<String, Object> result = aiAdapter.analyzeIntent(maskedText);

        // 3. Post-process (no need to unmask for intent analysis usually)
        return result;
    }

    public String generateQuestions(Map<String, Object> context) {
        return aiAdapter.generateQuestions(context);
    }
}
