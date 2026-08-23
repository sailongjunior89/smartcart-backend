package nus.iss.smartcart.backend.dto;

// Author: Junior

import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
public class ImageSearchResponse {

    private String prediction;
    private String gender;
    private String color;
    private String category;
    private List<ProductSearchResult> products;

    public ImageSearchResponse() {
        // Required by Jackson
    }
}