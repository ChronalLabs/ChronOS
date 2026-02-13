package com.rtigen.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.util.List;

public class DraftResponse {
    private String draftHtml;
    private String plainText;
    private List<String> questions;
    private List<String> warnings;

    public DraftResponse() {
    }

    public DraftResponse(String draftHtml, String plainText, List<String> questions, List<String> warnings) {
        this.draftHtml = draftHtml;
        this.plainText = plainText;
        this.questions = questions;
        this.warnings = warnings;
    }

    public String getDraftHtml() {
        return draftHtml;
    }

    public void setDraftHtml(String draftHtml) {
        this.draftHtml = draftHtml;
    }

    public String getPlainText() {
        return plainText;
    }

    public void setPlainText(String plainText) {
        this.plainText = plainText;
    }

    public List<String> getQuestions() {
        return questions;
    }

    public void setQuestions(List<String> questions) {
        this.questions = questions;
    }

    public List<String> getWarnings() {
        return warnings;
    }

    public void setWarnings(List<String> warnings) {
        this.warnings = warnings;
    }

    private String complianceLog;

    public String getComplianceLog() {
        return complianceLog;
    }

    public void setComplianceLog(String complianceLog) {
        this.complianceLog = complianceLog;
    }
}
