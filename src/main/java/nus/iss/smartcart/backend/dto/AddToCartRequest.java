package nus.iss.smartcart.backend.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class AddToCartRequest {

    public AddToCartRequest() {}

    private Long productVariantId;
    private Integer quantity;

    public AddToCartRequest(Long productVariantId, Integer quantity) {
        this.productVariantId = productVariantId;
        this.quantity = quantity;
    }
}
