package com.rtigen.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.util.List;

public class DraftRequest {
    private Applicant applicant;
    private Department department;
    private String issue;
    private List<String> acceptedSuggestions;
    private String mode; // "assisted" or "ai"
    private String language; // "en" or "hi"

    public DraftRequest() {
    }

    public DraftRequest(Applicant applicant, Department department, String issue, List<String> acceptedSuggestions,
            String mode) {
        this.applicant = applicant;
        this.department = department;
        this.issue = issue;
        this.acceptedSuggestions = acceptedSuggestions;
        this.mode = mode;
    }

    public Applicant getApplicant() {
        return applicant;
    }

    public void setApplicant(Applicant applicant) {
        this.applicant = applicant;
    }

    public Department getDepartment() {
        return department;
    }

    public void setDepartment(Department department) {
        this.department = department;
    }

    public String getIssue() {
        return issue;
    }

    public void setIssue(String issue) {
        this.issue = issue;
    }

    public List<String> getAcceptedSuggestions() {
        return acceptedSuggestions;
    }

    public void setAcceptedSuggestions(List<String> acceptedSuggestions) {
        this.acceptedSuggestions = acceptedSuggestions;
    }

    public String getMode() {
        return mode;
    }

    public void setMode(String mode) {
        this.mode = mode;
    }

    public String getLanguage() {
        return language;
    }

    public void setLanguage(String language) {
        this.language = language;
    }

    public static class Applicant {
        private String name;
        private String address;
        private String mobile;

        public Applicant() {
        }

        public Applicant(String name, String address, String mobile) {
            this.name = name;
            this.address = address;
            this.mobile = mobile;
        }

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

        public String getMobile() {
            return mobile;
        }

        public void setMobile(String mobile) {
            this.mobile = mobile;
        }
    }

    public static class Department {
        private String name;
        private String address;

        public Department() {
        }

        public Department(String name, String address) {
            this.name = name;
            this.address = address;
        }

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
    }
}
