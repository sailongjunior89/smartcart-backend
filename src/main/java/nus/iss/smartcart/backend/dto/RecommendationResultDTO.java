package nus.iss.smartcart.backend.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
public class RecommendationResultDTO {

    @JsonProperty("agent_summary")
    private String agentSummary;

    @JsonProperty("products")
    private List<RecommendedProductResponseDTO> products;

    public RecommendationResultDTO() {}

    public RecommendationResultDTO(String agentSummary, List<RecommendedProductResponseDTO> products) {
        this.agentSummary = agentSummary;
        this.products = products;
    }
}