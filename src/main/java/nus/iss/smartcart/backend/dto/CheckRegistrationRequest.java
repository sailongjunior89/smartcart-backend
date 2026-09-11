package nus.iss.smartcart.backend.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class CheckRegistrationRequest {

    private String username;
    private String email;

    public CheckRegistrationRequest() {
    }

    public CheckRegistrationRequest(
            String username,
            String email
    ) {
        this.username = username;
        this.email = email;
    }
}