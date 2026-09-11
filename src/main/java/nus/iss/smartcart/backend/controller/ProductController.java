package nus.iss.smartcart.backend.controller;

import jakarta.validation.Valid;
import nus.iss.smartcart.backend.dto.*;
import nus.iss.smartcart.backend.model.Gender;
import nus.iss.smartcart.backend.service.ImageSearchService;
import nus.iss.smartcart.backend.service.ImageUploadService;
import nus.iss.smartcart.backend.service.ProductService;

import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;

import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

@RestController
@RequestMapping("/api/products")
@CrossOrigin(origins = "http://localhost:4200")
public class ProductController {

    private final ProductService productService;
    private final ImageSearchService imageSearchService;
    private final ImageUploadService imageUploadService;


    public ProductController(
            ProductService productService,
            ImageSearchService imageSearchService,
            ImageUploadService imageUploadService
    ) {
        this.productService = productService;
        this.imageSearchService = imageSearchService;
        this.imageUploadService = imageUploadService;
    }


    // ============================================================
    // GET ALL PRODUCTS
    // GET /api/products
    // ============================================================

    @GetMapping
    public ResponseEntity<List<ProductSearchResult>> getProducts() {

        List<ProductSearchResult> products =
                productService.search(
                        null,   // keyword
                        null,   // category
                        null,   // gender
                        false,  // newestFirst
                        100     // limit
                );

        return ResponseEntity.ok(products);
    }


    // ============================================================
    // SEARCH PRODUCTS BY KEYWORD
    // GET /api/products/search?keyword=shirt
    // ============================================================

    @GetMapping("/search")
    public ResponseEntity<List<ProductSearchResult>> searchProductsByKeyword(
            @RequestParam String keyword
    ) {

        return ResponseEntity.ok(
                productService.searchByKeyword(keyword)
        );
    }


    // ============================================================
    // BROWSE / FILTER PRODUCTS
    // GET /api/products/browse
    // ============================================================

    @GetMapping("/browse")
    public ResponseEntity<List<ProductSearchResult>> browse(

            @RequestParam(required = false)
            String keyword,

            @RequestParam(required = false)
            String category,

            @RequestParam(required = false)
            Gender gender,

            @RequestParam(defaultValue = "false")
            boolean newestFirst,

            @RequestParam(defaultValue = "20")
            int limit
    ) {

        return ResponseEntity.ok(
                productService.search(
                        keyword,
                        category,
                        gender,
                        newestFirst,
                        limit
                )
        );
    }


    // ============================================================
    // GET PRODUCT DETAIL
    // GET /api/products/{id}
    // ============================================================

    @GetMapping("/{id}")
    public ResponseEntity<ProductDetailResponse> getProductDetail(
            @PathVariable Long id
    ) {

        return ResponseEntity.ok(
                productService.getProductDetail(id)
        );
    }


    // ============================================================
    // CREATE PRODUCT
    // POST /api/products
    // ============================================================

    @PostMapping
    public ResponseEntity<ProductDetailResponse> createProduct(

            @Valid
            @RequestBody
            ProductRequest request
    ) {

        ProductDetailResponse response =
                productService.createProduct(request);

        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(response);
    }


    // ============================================================
    // UPDATE PRODUCT
    // PUT /api/products/{id}
    // ============================================================

    @PutMapping("/{id}")
    public ResponseEntity<ProductDetailResponse> updateProduct(

            @PathVariable Long id,

            @Valid
            @RequestBody
            ProductRequest request
    ) {

        ProductDetailResponse response =
                productService.updateProduct(id, request);

        return ResponseEntity.ok(response);
    }


    // ============================================================
    // DEACTIVATE PRODUCT
    // DELETE /api/products/{id}
    // ============================================================

    @DeleteMapping("/{id}")
    public ResponseEntity<ProductDetailResponse> deactivateProduct(
            @PathVariable Long id
    ) {

        ProductDetailResponse response =
                productService.deactivateProduct(id);

        return ResponseEntity.ok(response);
    }


    // ============================================================
    // GET CURRENT MERCHANT PRODUCTS
    // GET /api/products/own
    // ============================================================

    @GetMapping("/own")
    public ResponseEntity<List<ProductSearchResult>> getMerchantProducts() {

        List<ProductSearchResult> response =
                productService.getMerchantProducts();

        return ResponseEntity.ok(response);
    }


    // ============================================================
    // UPLOAD PRODUCT IMAGE
    // POST /api/products/image-upload
    // ============================================================

    @PostMapping("/image-upload")
    public ResponseEntity<ImageUploadResponse> uploadImage(

            @RequestParam("file")
            MultipartFile file
    ) {

        String imageUrl =
                imageUploadService.uploadImage(file);

        ImageUploadResponse response =
                ImageUploadResponse.builder()
                        .imageUrl(imageUrl)
                        .build();

        return ResponseEntity.ok(response);
    }


    // ============================================================
    // ACTIVATE PRODUCT
    // PATCH /api/products/{id}/activate
    // ============================================================

    @PatchMapping("/{id}/activate")
    public ResponseEntity<ProductDetailResponse> activateProduct(
            @PathVariable Long id
    ) {

        ProductDetailResponse response =
                productService.activateProduct(id);

        return ResponseEntity.ok(response);
    }


    // ============================================================
    // SEARCH PRODUCT BY IMAGE
    // POST /api/products/search/image
    // ============================================================

    @PostMapping(
            value = "/search/image",
            consumes = MediaType.MULTIPART_FORM_DATA_VALUE
    )
    public ResponseEntity<ImageSearchResponse> searchByImage(

            @RequestParam("image")
            MultipartFile image
    ) {

        return ResponseEntity.ok(
                imageSearchService.searchByImage(image)
        );
    }
}