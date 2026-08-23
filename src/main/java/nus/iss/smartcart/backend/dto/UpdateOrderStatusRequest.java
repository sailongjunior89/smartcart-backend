package nus.iss.smartcart.backend.dto;

import lombok.Getter;
import lombok.Setter;
import nus.iss.smartcart.backend.model.OrderStatus;

@Getter
@Setter
public class UpdateOrderStatusRequest {

    private OrderStatus status;
}