package nus.iss.smartcart.backend.dto;

import lombok.Getter;

@Getter
public class CheckRegistrationResponse {

    private boolean usernameExists;
    private boolean emailExists;

    public CheckRegistrationResponse(
            boolean usernameExists,
            boolean emailExists
    ) {
        this.usernameExists = usernameExists;
        this.emailExists = emailExists;
    }

    public boolean isUsernameExists() {
        return usernameExists;
    }

    public boolean isEmailExists() {
        return emailExists;
    }
}