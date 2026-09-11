package nus.iss.smartcart.backend.dto;

import lombok.Getter;
import lombok.Setter;

import java.math.BigDecimal;

@Getter
@Setter
public class UserProfileResponse {

    private String username;
    private String email;

    private String firstName;
    private String lastName;
    private String address;
    private String postalCode;
    private String phoneNumber;

    private String avatarUrl;

    private BigDecimal budget;
    private String interests;
    private String preferredCategories;

    public UserProfileResponse() {
    }
}