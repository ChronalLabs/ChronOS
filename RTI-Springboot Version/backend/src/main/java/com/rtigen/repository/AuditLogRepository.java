package com.rtigen.repository;

import com.rtigen.model.AuditLog;
import org.springframework.stereotype.Repository;

import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

@Repository
public class AuditLogRepository {

    private final Map<String, AuditLog> store = new ConcurrentHashMap<>();

    public AuditLog save(AuditLog log) {
        if (log.getId() == null) {
            log.setId(UUID.randomUUID().toString());
        }
        store.put(log.getId(), log);
        return log;
    }
}
