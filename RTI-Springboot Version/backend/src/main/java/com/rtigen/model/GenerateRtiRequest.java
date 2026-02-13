package com.rtigen.model;

public class GenerateRtiRequest {
    private String inputText; // user's plain language
    private String language; // "en"|"hi"
    private boolean privacyMode;
    private boolean consentToSendPii; // required if privacyMode==false and PII present
    private Applicant applicant;

    public String getInputText() {
        return inputText;
    }

    public void setInputText(String inputText) {
        this.inputText = inputText;
    }

    public String getLanguage() {
        return language;
    }

    public void setLanguage(String language) {
        this.language = language;
    }

    public boolean isPrivacyMode() {
        return privacyMode;
    }

    public void setPrivacyMode(boolean privacyMode) {
        this.privacyMode = privacyMode;
    }

    public boolean isConsentToSendPii() {
        return consentToSendPii;
    }

    public void setConsentToSendPii(boolean consentToSendPii) {
        this.consentToSendPii = consentToSendPii;
    }

    public Applicant getApplicant() {
        return applicant;
    }

    public void setApplicant(Applicant applicant) {
        this.applicant = applicant;
    }

    public static class Applicant {
        private String name;
        private String address;
        private String email;

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public String getAddress() {
            return address;
        }

        public void setAddress(String address) {
            this.address = address;
        }

        public String getEmail() {
            return email;
        }

        public void setEmail(String email) {
            this.email = email;
        }
    }
}
