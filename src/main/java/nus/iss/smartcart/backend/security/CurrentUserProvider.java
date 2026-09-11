package nus.iss.smartcart.backend.security;

import nus.iss.smartcart.backend.exception.ForbiddenException;
import nus.iss.smartcart.backend.model.User;
import nus.iss.smartcart.backend.model.UserRole;
import nus.iss.smartcart.backend.repository.UserRepository;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

@Component
public class CurrentUserProvider {

    private final UserRepository userRepository;


    public CurrentUserProvider(
            UserRepository userRepository
    ) {
        this.userRepository = userRepository;
    }


    // ============================================================
    // GET CURRENT USER
    // ============================================================

    public User getCurrentUser() {

        Authentication authentication =
                SecurityContextHolder
                        .getContext()
                        .getAuthentication();


        if (authentication == null
                || !authentication.isAuthenticated()) {

            throw new ForbiddenException(
                    "Not authenticated."
            );
        }


        // ============================================================
        // GET EMAIL FROM AUTHENTICATED USER
        // ============================================================

        String email = authentication.getName();


        System.out.println(
                "========================================"
        );

        System.out.println(
                "CURRENT AUTHENTICATED USER: " + email
        );

        System.out.println(
                "AUTHENTICATION TYPE: "
                        + authentication.getClass().getName()
        );

        System.out.println(
                "========================================"
        );


        return userRepository
                .findByEmail(email)
                .orElseThrow(() ->
                        new ForbiddenException(
                                "Authenticated user no longer exists. Email: "
                                        + email
                        )
                );
    }


    // ============================================================
    // GET CURRENT CUSTOMER
    // ============================================================

    public User getCurrentCustomer() {

        User user = getCurrentUser();


        if (user.getRole() != UserRole.CUSTOMER) {

            throw new ForbiddenException(
                    "This action requires a CUSTOMER account."
            );
        }


        return user;
    }


    // ============================================================
    // GET CURRENT MERCHANT
    // ============================================================

    public User getCurrentMerchant() {

        User user = getCurrentUser();


        if (user.getRole() != UserRole.MERCHANT) {

            throw new ForbiddenException(
                    "This action requires a MERCHANT account."
            );
        }


        return user;
    }


    // ============================================================
    // GET CURRENT ADMIN
    // ============================================================

    public User getCurrentAdmin() {

        User user = getCurrentUser();


        if (user.getRole() != UserRole.ADMIN) {

            throw new ForbiddenException(
                    "This action requires an ADMIN account."
            );
        }


        return user;
    }
}