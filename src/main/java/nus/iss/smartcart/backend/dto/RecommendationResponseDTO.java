package nus.iss.smartcart.backend.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
public class RecommendationResponseDTO {

    @JsonProperty("recommendations")
    private List<RecommendationItem> recommendations;
    
    @JsonProperty("agent_summary")
    private String agentSummary;

    public RecommendationResponseDTO() { /* Intentionally left empty */ }

    @Getter
    @Setter
    public static class RecommendationItem {

        @JsonProperty("product_id")
        private String productId;

        @JsonProperty("score")
        private Double score;

        @JsonProperty("reason")
        private String reason;

        public RecommendationItem() { /* Intentionally left empty - required by Jackson for JSON deserialization */ }
    }
}