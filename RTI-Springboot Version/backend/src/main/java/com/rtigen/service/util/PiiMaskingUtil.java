package com.rtigen.service.util;

import java.util.regex.Pattern;

public class PiiMaskingUtil {

    private static final Pattern EMAIL_PATTERN = Pattern.compile("\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z]{2,6}\\b",
            Pattern.CASE_INSENSITIVE);
    private static final Pattern PHONE_PATTERN = Pattern.compile("\\b\\d{10}\\b");

    public static String mask(String input) {
        if (input == null)
            return null;
        String masked = EMAIL_PATTERN.matcher(input).replaceAll("[EMAIL_REDACTED]");
        masked = PHONE_PATTERN.matcher(masked).replaceAll("[PHONE_REDACTED]");
        // Add more patterns (Aadhaar, PAN) as needed
        return masked;
    }
}
