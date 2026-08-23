package nus.iss.smartcart.backend.dto;

import lombok.Getter;
import lombok.Setter;

import java.math.BigDecimal;
import java.util.List;

@Getter
@Setter
public class CartItemsResponse {

    public CartItemsResponse(List<CartItemDetail> cartItemDetails, BigDecimal cartTotal) {
        this.cartItemDetails = cartItemDetails;
        this.cartTotal = cartTotal;
    }
    private List<CartItemDetail> cartItemDetails;
    private BigDecimal cartTotal;
}
