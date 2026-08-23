package nus.iss.smartcart.backend.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class RecommendationRequestDTO {

    @JsonProperty("top_k")
    private Integer topK;

    @JsonProperty("mode")
    private String mode;

    @JsonProperty("customer_profile")
    private CustomerProfileDTO customerProfile;

    public RecommendationRequestDTO() {}

    public RecommendationRequestDTO(Integer topK, String mode, CustomerProfileDTO customerProfile) {
        this.topK = topK;
        this.mode = mode;
        this.customerProfile = customerProfile;
    }
}