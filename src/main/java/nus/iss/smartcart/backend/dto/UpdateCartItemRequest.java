package nus.iss.smartcart.backend.dto;

import lombok.Getter;
import lombok.Setter;

// Author: Htet Nandar (Grace)
@Getter
@Setter
public class UpdateCartItemRequest {

    public UpdateCartItemRequest() {}
    private Integer quantity;
    public UpdateCartItemRequest(Integer quantity) {
        this.quantity = quantity;
    }
}
