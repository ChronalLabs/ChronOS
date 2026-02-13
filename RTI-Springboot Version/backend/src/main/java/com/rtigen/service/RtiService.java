package com.rtigen.service;

import com.rtigen.model.RtiDraft;
import com.rtigen.repository.RtiDraftRepository;
import com.rtigen.engine.IntentEngine;
import com.rtigen.engine.RuleEngine;
import com.rtigen.adapter.pdf.PdfExportService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.io.IOException;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import com.rtigen.dto.*;

@Service
public class RtiService {

    private final RtiDraftRepository rtiDraftRepository;
    private final IntentEngine intentEngine;
    private final RuleEngine ruleEngine;
    private final PdfExportService pdfExportService;
    private final com.rtigen.adapter.ai.AiAdapter aiAdapter; // Direct access for specialized modes

    public RtiService(RtiDraftRepository rtiDraftRepository, IntentEngine intentEngine, RuleEngine ruleEngine,
            PdfExportService pdfExportService, com.rtigen.adapter.ai.AiAdapter aiAdapter) {
        this.rtiDraftRepository = rtiDraftRepository;
        this.intentEngine = intentEngine;
        this.ruleEngine = ruleEngine;
        this.pdfExportService = pdfExportService;
        this.aiAdapter = aiAdapter;
    }

    public com.rtigen.dto.SuggestionResponse generateSuggestions(com.rtigen.dto.SuggestionRequest request) {
        return aiAdapter.generateSuggestions(request);
    }

    public com.rtigen.dto.DraftResponse generateStructuredDraft(com.rtigen.dto.DraftRequest request) {
        return aiAdapter.generateStructuredDraft(request);
    }

    // Create Draft from Intent
    public RtiDraft createDraftFromIntent(String plainText, String userId) {
        Map<String, Object> analysis = intentEngine.analyze(plainText);
        String generatedQuestions = intentEngine.generateQuestions(analysis);

        // Improved splitting:
        // 1. Unescape literal "\n" strings if present
        // 2. Split by newline
        // 3. Clean up leading numbers
        String cleanQuestions = generatedQuestions.replace("\\n", "\n");
        List<String> questionList = java.util.Arrays.stream(cleanQuestions.split("\n"))
                .map(String::trim)
                .filter(s -> !s.isEmpty())
                // Remove leading "1.", "2)", "- " etc. if the AI included them
                .map(s -> s.replaceAll("^\\d+[\\.\\)]\\s*|^-\\s*", ""))
                .collect(java.util.stream.Collectors.toList());

        RtiDraft draft = new RtiDraft();
        draft.setUserId(userId);
        draft.setSubject((String) analysis.getOrDefault("subject", "Information Request"));
        draft.setDepartment((String) analysis.getOrDefault("department", "Unknown Dept"));
        draft.setQuestions(questionList);
        draft.setStatus("DRAFT");
        draft.setCreatedAt(LocalDateTime.now());

        return rtiDraftRepository.save(draft);
    }

    // Save/Update Draft
    public RtiDraft saveDraft(RtiDraft draft) {
        draft.setUpdatedAt(LocalDateTime.now());
        // Auto-calc quality on save
        List<String> issues = ruleEngine.validateDraft(draft);
        draft.setQualityScore(ruleEngine.calculateQualityScore(issues));

        return rtiDraftRepository.save(draft);
    }

    public Optional<RtiDraft> getDraft(String id) {
        return rtiDraftRepository.findById(id);
    }

    public List<RtiDraft> getUserDrafts(String userId) {
        return rtiDraftRepository.findByUserId(userId);
    }

    // Export PDF
    public byte[] exportPdf(String draftId) throws IOException {
        RtiDraft draft = getDraft(draftId).orElseThrow(() -> new RuntimeException("Draft not found"));
        return pdfExportService.generateRtiPdf(draft);
    }
}
