package nus.iss.smartcart.backend.dto;

import lombok.Getter;
import lombok.Setter;

import java.math.BigDecimal;

@Getter
@Setter
public class UpdateUserProfileRequest {

    private String password;
    private String firstName;
    private String lastName;
    private String address;
    private String postalCode;
    private String phoneNumber;
    private BigDecimal budget;
    private String interests;
    private String preferredCategories;
    private String avatarUrl;

    public UpdateUserProfileRequest() {
    }
}