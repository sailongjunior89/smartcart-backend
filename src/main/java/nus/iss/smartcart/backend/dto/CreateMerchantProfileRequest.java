package nus.iss.smartcart.backend.dto;

import lombok.Getter;
import lombok.Setter;
import org.springframework.web.multipart.MultipartFile;

@Getter
@Setter
public class CreateMerchantProfileRequest {

    private Long userId;
    private String businessName;
    private String uen;
    private String businessType;
    private String businessAddress;
    private String postalCode;
    private String contactNumber;
    private String productCategory;
    private String businessDescription;
    private Boolean pickupAvailable;
    private MultipartFile logo;
    private MultipartFile registrationDocument;

    public CreateMerchantProfileRequest() {
        // Required by the controller to construct the request DTO
        // before assigning multipart form values.
    }
}