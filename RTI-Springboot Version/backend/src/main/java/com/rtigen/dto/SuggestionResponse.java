package com.rtigen.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.util.List;

public class SuggestionResponse {
    private List<Suggestion> suggestions;
    private Meta meta;

    public SuggestionResponse() {
    }

    public SuggestionResponse(List<Suggestion> suggestions, Meta meta) {
        this.suggestions = suggestions;
        this.meta = meta;
    }

    public List<Suggestion> getSuggestions() {
        return suggestions;
    }

    public void setSuggestions(List<Suggestion> suggestions) {
        this.suggestions = suggestions;
    }

    public Meta getMeta() {
        return meta;
    }

    public void setMeta(Meta meta) {
        this.meta = meta;
    }

    public static class Suggestion {
        private String id;
        private String type; // "reword", "clarify", "add_question"
        private String text;
        private double confidence;
        private boolean clarifying;

        public Suggestion() {
        }

        public Suggestion(String id, String type, String text, double confidence, boolean clarifying) {
            this.id = id;
            this.type = type;
            this.text = text;
            this.confidence = confidence;
            this.clarifying = clarifying;
        }

        public String getId() {
            return id;
        }

        public void setId(String id) {
            this.id = id;
        }

        public String getType() {
            return type;
        }

        public void setType(String type) {
            this.type = type;
        }

        public String getText() {
            return text;
        }

        public void setText(String text) {
            this.text = text;
        }

        public double getConfidence() {
            return confidence;
        }

        public void setConfidence(double confidence) {
            this.confidence = confidence;
        }

        public boolean isClarifying() {
            return clarifying;
        }

        public void setClarifying(boolean clarifying) {
            this.clarifying = clarifying;
        }
    }

    public static class Meta {
        private String model;
        private String generatedAt;

        public Meta() {
        }

        public Meta(String model, String generatedAt) {
            this.model = model;
            this.generatedAt = generatedAt;
        }

        public String getModel() {
            return model;
        }

        public void setModel(String model) {
            this.model = model;
        }

        public String getGeneratedAt() {
            return generatedAt;
        }

        public void setGeneratedAt(String generatedAt) {
            this.generatedAt = generatedAt;
        }
    }
}
