package nus.iss.smartcart.backend.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
public class CustomerProfileDTO {

    @JsonProperty("customer_id")
    private String customerId;

    @JsonProperty("interests")
    private List<String> interests;

    @JsonProperty("cart")
    private List<String> cart;

    @JsonProperty("recently_viewed")
    private List<String> recentlyViewed;

    @JsonProperty("purchase_history")
    private List<String> purchaseHistory;

    @JsonProperty("preferred_categories")
    private List<String> preferredCategories;

    @JsonProperty("budget")
    private Double budget;

    public CustomerProfileDTO() {}

    public CustomerProfileDTO(String customerId,
                              List<String> interests,
                              List<String> cart,
                              List<String> recentlyViewed,
                              List<String> purchaseHistory,
                              List<String> preferredCategories,
                              Double budget) {
        this.customerId = customerId;
        this.interests = interests;
        this.cart = cart;
        this.recentlyViewed = recentlyViewed;
        this.purchaseHistory = purchaseHistory;
        this.preferredCategories = preferredCategories;
        this.budget = budget;
    }
}