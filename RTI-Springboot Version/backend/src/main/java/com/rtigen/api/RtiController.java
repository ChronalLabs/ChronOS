package com.rtigen.api;

import com.rtigen.model.RtiDraft;
import com.rtigen.service.RtiService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.rtigen.dto.*;

import java.io.IOException;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/rti")
public class RtiController {

    private final RtiService rtiService;

    public RtiController(RtiService rtiService) {
        this.rtiService = rtiService;
    }

    @PostMapping("/generate")
    public ResponseEntity<RtiDraft> generateDraft(@RequestBody com.rtigen.model.GenerateRtiRequest request) {
        String userId = "guest"; // TODO: Extract from Principal

        // Pass request to service (Service needs update to accept DTO or extracted
        // params)
        // For now, mapping manual params to match existing service signature
        // In next step, we will update RtiService signature.
        return ResponseEntity.ok(rtiService.createDraftFromIntent(request.getInputText(), userId));
    }

    @GetMapping("/{id}")
    public ResponseEntity<RtiDraft> getDraft(@PathVariable String id) {
        return rtiService.getDraft(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PutMapping("/{id}")
    public ResponseEntity<RtiDraft> updateDraft(@PathVariable String id, @RequestBody RtiDraft draft) {
        // Ensure ID matches
        draft.setId(id);
        return ResponseEntity.ok(rtiService.saveDraft(draft));
    }

    @PostMapping("/{id}/export/pdf")
    public ResponseEntity<byte[]> exportPdf(@PathVariable String id) throws IOException {
        byte[] pdfBytes = rtiService.exportPdf(id);

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=rti_draft_" + id + ".pdf")
                .contentType(MediaType.APPLICATION_PDF)
                .body(pdfBytes);
    }

    @GetMapping("/user/{userId}")
    public ResponseEntity<List<RtiDraft>> getUserDrafts(@PathVariable String userId) {
        return ResponseEntity.ok(rtiService.getUserDrafts(userId));
    }

    @PostMapping("/generate/assisted/suggestions")
    public ResponseEntity<com.rtigen.dto.SuggestionResponse> getSuggestions(
            @RequestBody com.rtigen.dto.SuggestionRequest request) {
        return ResponseEntity.ok(rtiService.generateSuggestions(request));
    }

    @PostMapping("/generate/assisted/draft")
    public ResponseEntity<com.rtigen.dto.DraftResponse> generateAssistedDraft(
            @RequestBody com.rtigen.dto.DraftRequest request) {
        request.setMode("assisted");
        return ResponseEntity.ok(rtiService.generateStructuredDraft(request));
    }

    @PostMapping("/generate/ai/draft")
    public ResponseEntity<com.rtigen.dto.DraftResponse> generateAiDraft(
            @RequestBody com.rtigen.dto.DraftRequest request) {
        request.setMode("ai");
        return ResponseEntity.ok(rtiService.generateStructuredDraft(request));
    }
}
