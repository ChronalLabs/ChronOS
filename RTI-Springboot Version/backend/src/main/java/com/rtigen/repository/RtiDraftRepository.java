package com.rtigen.repository;

import com.rtigen.model.RtiDraft;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

@Repository
public class RtiDraftRepository {

    private final Map<String, RtiDraft> store = new ConcurrentHashMap<>();

    public RtiDraft save(RtiDraft draft) {
        if (draft.getId() == null) {
            draft.setId(UUID.randomUUID().toString());
        }
        store.put(draft.getId(), draft);
        return draft;
    }

    public Optional<RtiDraft> findById(String id) {
        return Optional.ofNullable(store.get(id));
    }

    public List<RtiDraft> findByUserId(String userId) {
        return store.values().stream()
                .filter(d -> userId.equals(d.getUserId()))
                .collect(Collectors.toList());
    }

    public List<RtiDraft> findAll() {
        return new ArrayList<>(store.values());
    }

    public void deleteById(String id) {
        store.remove(id);
    }
}
