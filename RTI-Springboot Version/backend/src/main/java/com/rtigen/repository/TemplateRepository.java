package com.rtigen.repository;

import com.rtigen.model.Template;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

@Repository
public class TemplateRepository {

    private final Map<String, Template> store = new ConcurrentHashMap<>();

    public Template save(Template template) {
        if (template.getId() == null) {
            template.setId(UUID.randomUUID().toString());
        }
        store.put(template.getId(), template);
        return template;
    }

    public List<Template> findAll() {
        return new ArrayList<>(store.values());
    }

    public Optional<Template> findById(String id) {
        return Optional.ofNullable(store.get(id));
    }

    public List<Template> findByDepartment(String department) {
        return store.values().stream()
                .filter(t -> department.equalsIgnoreCase(t.getDepartment()))
                .collect(Collectors.toList());
    }

    public List<Template> findByState(String state) {
        return store.values().stream()
                .filter(t -> state.equalsIgnoreCase(t.getState()))
                .collect(Collectors.toList());
    }

    public List<Template> findByDepartmentAndState(String department, String state) {
        return store.values().stream()
                .filter(t -> department.equalsIgnoreCase(t.getDepartment()) && state.equalsIgnoreCase(t.getState()))
                .collect(Collectors.toList());
    }
}
