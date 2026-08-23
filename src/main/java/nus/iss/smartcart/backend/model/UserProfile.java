package nus.iss.smartcart.backend.model;

import java.math.BigDecimal;
import java.util.Arrays;
import java.util.List;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

//Author: Junior

@Getter
@Setter
@Entity
@Table(name = "smartcart_user_profile")
public class UserProfile {

    public UserProfile() {
        // Required by JPA - Hibernate instantiates entities via reflection when loading from the DB.
    }

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false, unique = true)
    private User user;

    @Column(nullable = false)
    private String firstName;

    @Column(nullable = false)
    private String lastName;

    @Column(nullable = false)
    private String address;

    @Column(name = "postal_code", nullable = false)
    private String postalCode;

    @Column(nullable = false)
    private String phoneNumber;

    private String avatarUrl;

    @Column(name = "budget", precision = 10, scale = 2)
    private BigDecimal budget;

    @Column(name = "interests")
    private String interests;

    @Column(name = "preferred_categories")
    private String preferredCategories;

 // --- Helper Methods for FastAPI DTO Conversion For Recommender AI ---
    public List<String> getInterestsList() {
        if (interests == null || interests.isBlank()) return List.of();
        return Arrays.stream(interests.split(","))
                     .map(String::trim)
                     .toList();
    }

    public List<String> getPreferredCategoriesList() {
        if (preferredCategories == null || preferredCategories.isBlank()) return List.of();
        return Arrays.stream(preferredCategories.split(","))
                     .map(String::trim)
                     .toList();
    }
    
}
