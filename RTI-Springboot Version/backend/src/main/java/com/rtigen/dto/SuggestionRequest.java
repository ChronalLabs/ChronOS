package com.rtigen.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SuggestionRequest {
    private String name;
    private String address;
    private String state;
    private String issue;
}
