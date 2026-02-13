package com.rtigen.api;

import com.rtigen.model.Template;
import com.rtigen.service.TemplateService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/v1/templates")
public class TemplateController {

    private final TemplateService templateService;

    public TemplateController(TemplateService templateService) {
        this.templateService = templateService;
    }

    @GetMapping
    public ResponseEntity<List<Template>> getAllTemplates(@RequestParam(required = false) String department) {
        if (department != null) {
            return ResponseEntity.ok(templateService.getTemplatesByDepartment(department));
        }
        return ResponseEntity.ok(templateService.getAllTemplates());
    }

    @PostMapping
    public ResponseEntity<Template> createTemplate(@RequestBody Template template) {
        return ResponseEntity.ok(templateService.createTemplate(template));
    }
}
