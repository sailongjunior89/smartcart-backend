package nus.iss.smartcart.backend.service;

import jakarta.persistence.EntityNotFoundException;

import nus.iss.smartcart.backend.dto.CreateUserProfileRequest;
import nus.iss.smartcart.backend.dto.UpdateUserProfileRequest;
import nus.iss.smartcart.backend.dto.UserProfileForDeliveryDetails;
import nus.iss.smartcart.backend.dto.UserProfileResponse;

import nus.iss.smartcart.backend.model.User;
import nus.iss.smartcart.backend.model.UserProfile;

import nus.iss.smartcart.backend.repository.UserProfileRepository;
import nus.iss.smartcart.backend.repository.UserRepository;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;


// Author: Junior

@Service
public class UserProfileService {

    private final Path uploadDirectory =
            Paths.get("upload");


    private final UserProfileRepository userProfileRepository;

    private final UserRepository userRepository;

    private final PasswordEncoder passwordEncoder;


    public UserProfileService(
            UserProfileRepository userProfileRepository,
            UserRepository userRepository,
            PasswordEncoder passwordEncoder
    ) {

        this.userProfileRepository =
                userProfileRepository;

        this.userRepository =
                userRepository;

        this.passwordEncoder =
                passwordEncoder;
    }


    // =========================================
    // GET PROFILE FOR DELIVERY DETAILS
    // =========================================

    @Transactional(readOnly = true)
    public UserProfileForDeliveryDetails getProfileForDeliveryDetails(
            Long userId
    ) {

        UserProfile profile =
                userProfileRepository
                        .findByUserId(userId)
                        .orElseThrow(() ->
                                new EntityNotFoundException(
                                        "User profile is not found"
                                )
                        );

        return UserProfileForDeliveryDetails
                .builder()
                .firstName(profile.getFirstName())
                .lastName(profile.getLastName())
                .address(profile.getAddress())
                .phoneNumber(profile.getPhoneNumber())
                .build();
    }


    // =========================================
    // CREATE PROFILE
    // =========================================

    @Transactional
    public UserProfile createProfile(
            CreateUserProfileRequest request
    ) {

        // ==========================
        // VALIDATE USER ID
        // ==========================

        if (request.getUserId() == null) {

            throw new IllegalArgumentException(
                    "User ID is required"
            );
        }


        // ==========================
        // VALIDATE FIRST NAME
        // ==========================

        if (request.getFirstName() == null ||
                request.getFirstName().isBlank()) {

            throw new IllegalArgumentException(
                    "First name is required"
            );
        }


        // ==========================
        // VALIDATE LAST NAME
        // ==========================

        if (request.getLastName() == null ||
                request.getLastName().isBlank()) {

            throw new IllegalArgumentException(
                    "Last name is required"
            );
        }


        // ==========================
        // VALIDATE ADDRESS
        // ==========================

        if (request.getAddress() == null ||
                request.getAddress().isBlank()) {

            throw new IllegalArgumentException(
                    "Address is required"
            );
        }


        // ==========================
        // VALIDATE POSTAL CODE
        // ==========================

        if (request.getPostalCode() == null ||
                request.getPostalCode().isBlank()) {

            throw new IllegalArgumentException(
                    "Postal code is required"
            );
        }


        // ==========================
        // VALIDATE PHONE NUMBER
        // ==========================

        if (request.getPhoneNumber() == null ||
                request.getPhoneNumber().isBlank()) {

            throw new IllegalArgumentException(
                    "Phone number is required"
            );
        }


        // ==========================
        // FIND USER
        // ==========================

        User user =
                userRepository
                        .findById(request.getUserId())
                        .orElseThrow(() ->
                                new EntityNotFoundException(
                                        "User not found"
                                )
                        );


        // ==========================
        // CHECK DUPLICATE PROFILE
        // ==========================

        if (userProfileRepository
                .findByUserId(request.getUserId())
                .isPresent()) {

            throw new IllegalArgumentException(
                    "User profile already exists"
            );
        }


        // ==========================
        // CREATE PROFILE
        // ==========================

        UserProfile profile =
                new UserProfile();

        profile.setUser(user);


        profile.setFirstName(
                request.getFirstName().trim()
        );

        profile.setLastName(
                request.getLastName().trim()
        );

        profile.setAddress(
                request.getAddress().trim()
        );

        profile.setPostalCode(
                request.getPostalCode().trim()
        );

        profile.setPhoneNumber(
                request.getPhoneNumber().trim()
        );


        // ==========================
        // SHOPPING PREFERENCES
        // ==========================

        profile.setBudget(
                request.getBudget()
        );

        profile.setInterests(
                request.getInterests()
        );

        profile.setPreferredCategories(
                request.getPreferredCategories()
        );


        // ==========================
        // AVATAR
        // ==========================

        if (request.getAvatarUrl() != null &&
                !request.getAvatarUrl().isBlank()) {

            profile.setAvatarUrl(
                    request.getAvatarUrl().trim()
            );
        }


        return userProfileRepository.save(
                profile
        );
    }


    // =========================================
    // GET CURRENT USER PROFILE
    // =========================================

    @Transactional(readOnly = true)
    public UserProfileResponse getCurrentUserProfile(
            Long userId
    ) {

        User user =
                userRepository
                        .findById(userId)
                        .orElseThrow(() ->
                                new EntityNotFoundException(
                                        "User not found"
                                )
                        );


        UserProfile profile =
                userProfileRepository
                        .findByUserId(userId)
                        .orElseThrow(() ->
                                new EntityNotFoundException(
                                        "User profile not found"
                                )
                        );


        return buildUserProfileResponse(
                user,
                profile
        );
    }


    // =========================================
    // UPDATE CURRENT USER PROFILE
    // =========================================

    @Transactional
    public UserProfileResponse updateCurrentUserProfile(
            Long userId,
            UpdateUserProfileRequest request
    ) {

        // ==========================
        // FIND USER
        // ==========================

        User user =
                userRepository
                        .findById(userId)
                        .orElseThrow(() ->
                                new EntityNotFoundException(
                                        "User not found"
                                )
                        );


        // ==========================
        // FIND PROFILE
        // ==========================

        UserProfile profile =
                userProfileRepository
                        .findByUserId(userId)
                        .orElseThrow(() ->
                                new EntityNotFoundException(
                                        "User profile not found"
                                )
                        );


        // ==========================
        // VALIDATE FIRST NAME
        // ==========================

        if (request.getFirstName() == null ||
                request.getFirstName().isBlank()) {

            throw new IllegalArgumentException(
                    "First name is required"
            );
        }


        // ==========================
        // VALIDATE LAST NAME
        // ==========================

        if (request.getLastName() == null ||
                request.getLastName().isBlank()) {

            throw new IllegalArgumentException(
                    "Last name is required"
            );
        }


        // ==========================
        // VALIDATE ADDRESS
        // ==========================

        if (request.getAddress() == null ||
                request.getAddress().isBlank()) {

            throw new IllegalArgumentException(
                    "Address is required"
            );
        }


        // ==========================
        // VALIDATE POSTAL CODE
        // ==========================

        if (request.getPostalCode() == null ||
                request.getPostalCode().isBlank()) {

            throw new IllegalArgumentException(
                    "Postal code is required"
            );
        }


        // ==========================
        // VALIDATE PHONE NUMBER
        // ==========================

        if (request.getPhoneNumber() == null ||
                request.getPhoneNumber().isBlank()) {

            throw new IllegalArgumentException(
                    "Phone number is required"
            );
        }


        // ==========================
        // UPDATE PERSONAL INFORMATION
        // ==========================

        profile.setFirstName(
                request.getFirstName().trim()
        );

        profile.setLastName(
                request.getLastName().trim()
        );

        profile.setAddress(
                request.getAddress().trim()
        );

        profile.setPostalCode(
                request.getPostalCode().trim()
        );

        profile.setPhoneNumber(
                request.getPhoneNumber().trim()
        );


        // ==========================
        // UPDATE SHOPPING PREFERENCES
        // ==========================

        profile.setBudget(
                request.getBudget()
        );

        profile.setInterests(
                request.getInterests()
        );

        profile.setPreferredCategories(
                request.getPreferredCategories()
        );


        // ==========================
        // UPDATE AVATAR
        // ==========================

        if (request.getAvatarUrl() != null) {

            profile.setAvatarUrl(
                    request.getAvatarUrl()
            );
        }


        // ==========================
        // UPDATE PASSWORD
        // ==========================

        if (request.getPassword() != null &&
                !request.getPassword().isBlank()) {

            String password =
                    request.getPassword();


            // Minimum 6 characters

            if (password.length() < 6) {

                throw new IllegalArgumentException(
                        "Password must be at least 6 characters"
                );
            }


            // At least one uppercase letter

            if (!password.matches(".*[A-Z].*")) {

                throw new IllegalArgumentException(
                        "Password must contain at least one uppercase letter"
                );
            }


            // At least one lowercase letter

            if (!password.matches(".*[a-z].*")) {

                throw new IllegalArgumentException(
                        "Password must contain at least one lowercase letter"
                );
            }


            // At least one number

            if (!password.matches(".*[0-9].*")) {

                throw new IllegalArgumentException(
                        "Password must contain at least one number"
                );
            }


            // Encrypt password

            user.setPassword(
                    passwordEncoder.encode(password)
            );

            userRepository.save(user);
        }


        // ==========================
        // SAVE PROFILE
        // ==========================

        UserProfile savedProfile =
                userProfileRepository.save(profile);


        // ==========================
        // RETURN UPDATED PROFILE
        // ==========================

        return buildUserProfileResponse(
                user,
                savedProfile
        );
    }


    // =========================================
    // BUILD USER PROFILE RESPONSE
    // =========================================

    private UserProfileResponse buildUserProfileResponse(
            User user,
            UserProfile profile
    ) {

        UserProfileResponse response =
                new UserProfileResponse();


        // Account information

        response.setUsername(
                user.getUsername()
        );

        response.setEmail(
                user.getEmail()
        );


        // Personal information

        response.setFirstName(
                profile.getFirstName()
        );

        response.setLastName(
                profile.getLastName()
        );

        response.setAddress(
                profile.getAddress()
        );

        response.setPostalCode(
                profile.getPostalCode()
        );

        response.setPhoneNumber(
                profile.getPhoneNumber()
        );


        // Avatar

        response.setAvatarUrl(
                profile.getAvatarUrl()
        );


        // Shopping preferences

        response.setBudget(
                profile.getBudget()
        );

        response.setInterests(
                profile.getInterests()
        );

        response.setPreferredCategories(
                profile.getPreferredCategories()
        );


        return response;
    }


    // =========================================
    // SAVE AVATAR
    // =========================================

    public String saveAvatar(
            String username,
            MultipartFile avatar
    ) {

        if (avatar == null ||
                avatar.isEmpty()) {

            return null;
        }


        // ==========================
        // VALIDATE IMAGE
        // ==========================

        if (avatar.getContentType() == null ||
                !avatar.getContentType()
                        .startsWith("image/")) {

            throw new IllegalArgumentException(
                    "Avatar must be an image file"
            );
        }


        // ==========================
        // CLEAN USERNAME
        // ==========================

        String safeUsername =
                username.replaceAll(
                        "[^a-zA-Z0-9_-]",
                        "_"
                );


        String filename =
                safeUsername +
                        "-avatar.jpg";


        try {

            // Create upload directory

            Files.createDirectories(
                    uploadDirectory
            );


            Path target =
                    uploadDirectory.resolve(
                            filename
                    );


            // Save file

            Files.write(
                    target,
                    avatar.getBytes()
            );


            return "upload/" + filename;

        } catch (IOException e) {

            throw new RuntimeException(
                    "Unable to save avatar",
                    e
            );
        }
    }
}