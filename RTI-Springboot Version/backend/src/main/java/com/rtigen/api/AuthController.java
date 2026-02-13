package com.rtigen.api;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/auth")
public class AuthController {

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody Map<String, String> credentials) {
        // Placeholder: Real impl would use AuthenticationManager
        if ("test@example.com".equals(credentials.get("email"))) {
            return ResponseEntity.ok(Map.of("token", "dummy-jwt-token", "userId", "user-123"));
        }
        return ResponseEntity.status(401).body("Invalid credentials");
    }

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody Map<String, String> user) {
        // Placeholder
        return ResponseEntity.ok(Map.of("message", "User registered successfully"));
    }
}
