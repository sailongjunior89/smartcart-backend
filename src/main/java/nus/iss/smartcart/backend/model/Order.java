package nus.iss.smartcart.backend.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
@Entity
@Table (name = "orders")
public class Order {

    public Order() {
        // Required by JPA - Hibernate instantiates entities via reflection when loading from the DB.
    }

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL)
    private List<OrderItem> items = new ArrayList<>();

    private BigDecimal totalAmount;

    @Enumerated(EnumType.STRING)
    @Column(name = "status")
    private OrderStatus status;

    private String firstName;

    private String lastName;

    private String shippingAddress;

    private String phoneNumber;

    private LocalDateTime deliveredAt;

    private LocalDateTime orderDate;

    @PrePersist
    protected void onCreate() {
        this.orderDate = LocalDateTime.now(ZoneId.of("Asia/Singapore"));
    }

    @Column(name = "tracking_no", unique = true)
    private String trackingNo;

    @Column(name = "delivery_person_id")
    private Long deliveryPersonId;

    @Column(name = "delivery_proof_key")
    private String deliveryProofKey;
}
