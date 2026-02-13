package com.rtigen.service;

import com.rtigen.model.Template;
import com.rtigen.repository.TemplateRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class TemplateService {

    private final TemplateRepository templateRepository;

    public TemplateService(TemplateRepository templateRepository) {
        this.templateRepository = templateRepository;
    }

    public List<Template> getAllTemplates() {
        return templateRepository.findAll();
    }

    public List<Template> getTemplatesByDepartment(String dept) {
        return templateRepository.findByDepartment(dept);
    }

    public Template createTemplate(Template template) {
        return templateRepository.save(template);
    }

    public Template getTemplate(String id) {
        return templateRepository.findById(id).orElseThrow(() -> new RuntimeException("Template not found"));
    }
}
