package com.rtigen.adapter.ai;

import java.util.Map;
import com.rtigen.dto.*;

public interface AiAdapter {
    Map<String, Object> analyzeIntent(String plainText);

    String generateQuestions(Map<String, Object> context);

    SuggestionResponse generateSuggestions(SuggestionRequest request);

    DraftResponse generateStructuredDraft(DraftRequest request);
}
