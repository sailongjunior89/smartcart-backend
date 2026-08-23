package nus.iss.smartcart.backend.dto;

// Author: Junior

import lombok.Getter;
import lombok.Setter;

import java.math.BigDecimal;

@Getter
@Setter
public class CreateUserProfileRequest {

    private Long userId;

    private String firstName;

    private String lastName;

    private String address;

    private String postalCode;

    private String phoneNumber;

    private BigDecimal budget;

    private String interests;

    private String preferredCategories;

    private String avatarUrl;

    public CreateUserProfileRequest() {
        // Required by the controller to construct the request DTO
        // before assigning multipart form values.
    }
}