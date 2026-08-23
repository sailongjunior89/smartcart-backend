package nus.iss.smartcart.backend.dto;

import lombok.Getter;
import lombok.Setter;

import java.math.BigDecimal;

@Getter
@Setter
public class RecommendedProductResponseDTO {

    private Long id;
    private String name;
    private String category;
    private BigDecimal price;
    private String imageUrl;
    private String reason;
    private Double score;

    public RecommendedProductResponseDTO() {}

    public RecommendedProductResponseDTO(Long id, String name, String category, 
                                        BigDecimal price, String imageUrl, 
                                        String reason, Double score) {
        this.id = id;
        this.name = name;
        this.category = category;
        this.price = price;
        this.imageUrl = imageUrl;
        this.reason = reason;
        this.score = score;
    }
}