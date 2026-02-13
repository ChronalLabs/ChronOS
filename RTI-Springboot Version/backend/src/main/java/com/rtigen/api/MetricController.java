package com.rtigen.api;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/metrics")
public class MetricController {

    @GetMapping("/custom")
    public Map<String, Object> getCustomMetrics() {
        Map<String, Object> metrics = new HashMap<>();
        metrics.put("rti_generated_count", 42); // Placeholder - connect to service count
        metrics.put("active_users", 5);
        metrics.put("ai_latency_avg_ms", 120);
        return metrics;
    }
}
