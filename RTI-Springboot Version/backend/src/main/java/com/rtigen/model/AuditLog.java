package com.rtigen.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.CreatedDate;
import java.time.LocalDateTime;

public class AuditLog {
    @Id
    private String id;
    private String action; // "EXPORT_PDF", "GENERATE_AI", "LOGIN"
    private String userId;
    private String metadata; // Non-PII details
    private boolean success;

    @CreatedDate
    private LocalDateTime timestamp;

    public AuditLog() {
    }

    public AuditLog(String id, String action, String userId, String metadata, boolean success,
            LocalDateTime timestamp) {
        this.id = id;
        this.action = action;
        this.userId = userId;
        this.metadata = metadata;
        this.success = success;
        this.timestamp = timestamp;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getAction() {
        return action;
    }

    public void setAction(String action) {
        this.action = action;
    }

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String getMetadata() {
        return metadata;
    }

    public void setMetadata(String metadata) {
        this.metadata = metadata;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public LocalDateTime getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }
}
