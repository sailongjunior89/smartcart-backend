# SmartCart Backend

Backend platform for **SmartCart**, an AI-assisted e-commerce application.

The project is implemented primarily with **Spring Boot 4.1.0 / Java 17** and provides REST APIs for authentication, customer profiles, products, categories, shopping carts, checkout/orders, merchant operations, administration, recommendations, AI chat, image search, and internal AI-agent tools.

The repository also contains a **FastAPI-based Python AI microservice** used for agentic chat, product recommendations, image search, trend/lookbook generation, and merchant spotlight generation.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Local Setup](#local-setup)
- [Environment Configuration](#environment-configuration)
- [Running the Application](#running-the-application)
- [Docker Compose](#docker-compose)
- [Authentication](#authentication)
- [REST API](#rest-api)
  - [Authentication](#authentication-api)
  - [Categories](#categories-api)
  - [Products](#products-api)
  - [Cart](#cart-api)
  - [Orders](#orders-api)
  - [Customer Profile](#customer-profile-api)
  - [Merchant Profile](#merchant-profile-api)
  - [Home Content](#home-content-api)
  - [AI Chat](#ai-chat-api)
  - [Recommendations](#recommendations-api)
  - [Product Vector Export](#product-vector-export-api)
  - [Public Statistics](#public-statistics-api)
  - [Admin](#admin-api)
  - [Internal AI Tools](#internal-ai-tools-api)
- [AI Microservice](#ai-microservice)
- [Database](#database)
- [Testing](#testing)
- [Code Quality and Coverage](#code-quality-and-coverage)
- [CI/CD and Security](#cicd-and-security)
- [AWS Infrastructure](#aws-infrastructure)
- [Troubleshooting](#troubleshooting)
- [Security Notes](#security-notes)
- [License](#license)

---

## Overview

SmartCart is an e-commerce platform with three major application layers:

1. **Spring Boot backend**
   - Business logic
   - Authentication and authorization
   - Product, cart and order management
   - Customer and merchant management
   - Database access
   - AI-service orchestration

2. **Python AI service**
   - Agentic shopping assistant
   - LLM-powered recommendations
   - Product vector search
   - CNN-based image search
   - Fashion trend/lookbook generation
   - Merchant spotlight generation
   - MCP/tool integration

3. **Frontend**
   - The backend's Docker Compose configuration expects a separate `smartcart-web` frontend directory.

---

## Key Features

### Customer

- Register and log in
- JWT authentication
- Change/reset password
- Browse products
- Search products by keyword
- Filter products by category and gender
- Sort by newest arrivals
- View product details
- Upload/search products using an image
- Manage shopping cart
- Checkout
- View order details
- Manage customer profile
- Upload customer avatar
- Use AI shopping chat
- Receive personalized product recommendations

### Merchant

- Merchant registration
- Merchant profile creation
- Product creation/update/deactivation
- View own products
- Upload product images
- View merchant order items
- Merchant account lifecycle managed by administrators

### Administrator

- View dashboard statistics
- View/manage administrators
- Create administrator accounts
- View merchant accounts
- View merchant details
- Suspend/reinstate merchant accounts
- View product listings
- Moderate product status

### AI

- Agentic AI shopping chat
- Product-search tools
- Order-history tools
- Cart tools
- Vector-based product retrieval
- Personalized recommendations
- CNN image similarity/search
- Fashion trend generation
- Merchant spotlight generation
- MCP-based tool integration

---

## Architecture

```text
                           ┌─────────────────────┐
                           │  Web / Mobile App   │
                           └──────────┬──────────┘
                                      │
                                  REST / HTTP
                                      │
                                      ▼
                    ┌─────────────────────────────────┐
                    │       Spring Boot Backend       │
                    │                                 │
                    │  Controllers                    │
                    │       │                         │
                    │  Services                       │
                    │       │                         │
                    │  Repositories                   │
                    │       │                         │
                    │  Security / JWT                 │
                    └──────────────┬──────────────────┘
                                   │
                  ┌────────────────┼─────────────────┐
                  │                │                 │
                  ▼                ▼                 ▼
             ┌─────────┐    ┌─────────────┐   ┌────────────┐
             │  MySQL  │    │ Python AI   │   │ Cloudinary │
             │         │    │  FastAPI    │   │  Images    │
             └─────────┘    └──────┬──────┘   └────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼              ▼
                OpenAI/        ChromaDB        CNN Model
                OpenRouter      Vector DB       Image Search
                                   │
                                   ▼
                              MCP / Tools
```

### Main backend flow

```text
HTTP Request
     │
     ▼
Controller
     │
     ▼
Service
     │
     ├──────────────► AI Service
     │
     ▼
Repository
     │
     ▼
MySQL
```

---

## Technology Stack

| Component | Technology |
|---|---|
| Backend language | Java 17 |
| Backend framework | Spring Boot 4.1.0 |
| REST API | Spring WebMVC |
| Security | Spring Security |
| Authentication | JWT |
| Password hashing | BCrypt |
| ORM | Spring Data JPA / Hibernate |
| Database | MySQL 8 |
| Validation | Jakarta Validation |
| JSON | Jackson |
| HTTP clients | Spring WebFlux / Apache HttpClient 5 |
| Image hosting | Cloudinary |
| Testing | JUnit / Spring Boot Test / Mockito |
| Coverage | JaCoCo |
| Static analysis | SonarCloud configuration |
| Containerization | Docker |
| Orchestration | Docker Compose |
| AI API | OpenAI / OpenRouter depending on AI component configuration |
| AI framework | LangChain / LangGraph |
| AI API framework | FastAPI |
| Vector database | ChromaDB |
| Computer vision | TensorFlow / CNN |
| AI tools | MCP |
| Infrastructure | AWS / Terraform / EKS / ECR |
| CI/CD | GitHub Actions |

---

## Repository Structure

```text
smartcart-backend/
│
├── src/
│   ├── main/
│   │   ├── java/nus/iss/smartcart/backend/
│   │   │
│   │   │   ├── admin/
│   │   │   │   ├── controller/
│   │   │   │   ├── dto/
│   │   │   │   └── service/
│   │   │   │
│   │   │   ├── chat/
│   │   │   │   ├── controller/
│   │   │   │   ├── dto/
│   │   │   │   ├── model/
│   │   │   │   ├── repository/
│   │   │   │   └── service/
│   │   │   │
│   │   │   ├── config/
│   │   │   ├── controller/
│   │   │   ├── dto/
│   │   │   ├── exception/
│   │   │   ├── model/
│   │   │   ├── repository/
│   │   │   ├── security/
│   │   │   └── service/
│   │   │
│   │   └── resources/
│   │       ├── application.properties
│   │       └── data.sql
│   │
│   └── test/
│
├── smartcart-ai-service/
│   ├── main.py
│   ├── routers/
│   ├── services/
│   ├── tools/
│   ├── models/
│   ├── prompts/
│   ├── training/
│   ├── cnn/
│   └── tests/
│
├── terraform/
│   ├── ecr.tf
│   ├── eks.tf
│   ├── oidc.tf
│   ├── vpc.tf
│   └── ...
│
├── .github/
│   └── workflows/
│
├── Dockerfile
├── docker-compose.yml
├── pom.xml
├── .env.example
└── README.md
```

---

# Prerequisites

Install:

- Java 17
- Maven 3.9+
- MySQL 8
- Python 3.12+ recommended for the AI service
- pip
- Docker Desktop
- Docker Compose
- Git

Optional for cloud deployment:

- AWS CLI
- Terraform
- kubectl

Verify:

```bash
java -version
mvn -version
mysql --version
python --version
docker --version
docker compose version
```

---

# Local Setup

## 1. Clone the repository

```bash
git clone https://github.com/sailongjunior89/smartcart-backend.git
cd smartcart-backend
```

## 2. Create the database

```sql
CREATE DATABASE smartcart_db;
```

The local Spring configuration currently expects:

```text
Database: smartcart_db
Host: localhost
Port: 3306
```

## 3. Configure database credentials

Do not use the credentials committed in example/local configuration for a real deployment.

Recommended environment variables:

```text
SPRING_DATASOURCE_URL=jdbc:mysql://localhost:3306/smartcart_db
SPRING_DATASOURCE_USERNAME=root
SPRING_DATASOURCE_PASSWORD=<your-password>
JWT_SECRET=<your-random-secret>
```

## 4. Build

```bash
mvn clean install
```

## 5. Run

```bash
mvn spring-boot:run
```

Backend:

```text
http://localhost:8080
```

---

# Environment Configuration

The repository contains `.env.example`.

Copy it:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Example:

```env
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=smartcart_db
MYSQL_USER=smartcart_user
MYSQL_PASSWORD=change-me

JWT_SECRET=generate-a-long-random-secret
```

The Python AI service has its own environment configuration under:

```text
smartcart-ai-service/.env.example
```

Configure AI credentials there rather than committing secrets.

---

# Running the AI Service

```bash
cd smartcart-ai-service

python -m venv .venv
```

Activate on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Activate on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

Health check:

```http
GET http://localhost:8001/api/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "smartcart-ai-service"
}
```

---

# Running with Docker Compose

The repository contains a complete Compose configuration for:

- MySQL
- SmartCart AI service
- Spring Boot backend
- Frontend

Start:

```bash
docker compose up --build
```

Run in background:

```bash
docker compose up --build -d
```

Stop:

```bash
docker compose down
```

Stop and remove volumes:

```bash
docker compose down -v
```

Services:

| Service | Port |
|---|---:|
| MySQL | `3306` |
| Spring Boot backend | `8080` |
| AI service | `8001` |
| Frontend | `4200` |

---

# Authentication

SmartCart uses stateless JWT authentication.

## Login flow

```text
Client
  │
  │ POST /api/auth/login
  ▼
Spring Boot
  │
  │ Validate credentials
  ▼
BCrypt password verification
  │
  ▼
JWT generated
  │
  ▼
Client
  │
  │ Authorization: Bearer <token>
  ▼
Protected API
```

Header:

```http
Authorization: Bearer <JWT_TOKEN>
```

JWT expiration is configured by:

```properties
jwt.expiration-ms=86400000
```

which is 24 hours in the current configuration.

Password hashing uses:

```text
BCryptPasswordEncoder
```

---

# REST API

Base URL:

```text
http://localhost:8080
```

> The authentication column below describes the current `SecurityConfig` rules in this repository. Some customer-facing endpoints are currently declared `permitAll` even though their service implementation obtains the current customer from the security context. If those endpoints are intended to require login, update `SecurityConfig` accordingly.

---

## Authentication API

Base path:

```text
/api/auth
```

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/register` | Public | Register customer |
| POST | `/api/auth/merchant/register` | Public | Register merchant |
| POST | `/api/auth/login` | Public | Authenticate user and return JWT |
| POST | `/api/auth/change-password` | JWT | Change current user's password |
| POST | `/api/auth/reset-password` | Public | Reset password |
| POST | `/api/auth/check-email` | Public | Check whether email exists |
| POST | `/api/auth/logout` | Public | Return logout confirmation |

### Register

```http
POST /api/auth/register
Content-Type: application/json
```

Request model:

```json
{
  "username": "alex",
  "email": "alex@example.com",
  "password": "password123"
}
```

### Merchant registration

```http
POST /api/auth/merchant/register
Content-Type: application/json
```

Uses the same `RegisterRequest` DTO.

### Login

```http
POST /api/auth/login
Content-Type: application/json
```

```json
{
  "email": "alex@example.com",
  "password": "password123"
}
```

The response uses `LoginResponse` and contains the authentication result/JWT information.

### Change password

```http
POST /api/auth/change-password
Authorization: Bearer <JWT>
Content-Type: application/json
```

Request uses `ChangePasswordRequest`.

### Reset password

```http
POST /api/auth/reset-password
Content-Type: application/json
```

Request uses `ResetPasswordRequest`.

### Check email

```http
POST /api/auth/check-email
Content-Type: application/json
```

```json
{
  "email": "alex@example.com"
}
```

### Logout

```http
POST /api/auth/logout
```

Current implementation returns:

```json
{
  "message": "Logout successful"
}
```

The current logout controller does not maintain a server-side token blacklist.

---

# Categories API

Base path:

```text
/api/categories
```

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/categories` | Public | List product categories |

Example:

```bash
curl http://localhost:8080/api/categories
```

---

# Products API

Base path:

```text
/api/products
```

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/products/search?keyword={keyword}` | Public | Keyword search |
| GET | `/api/products/browse` | Public | Filter/sort product catalogue |
| GET | `/api/products/{id}` | Public | Product details |
| POST | `/api/products` | Public* | Create product |
| PUT | `/api/products/{id}` | Public* | Update product |
| DELETE | `/api/products/{id}` | Public* | Deactivate product |
| GET | `/api/products/own` | Public* | Merchant's products |
| POST | `/api/products/image-upload` | Public | Upload product image |
| PATCH | `/api/products/{id}/activate` | Public* | Activate product |
| POST | `/api/products/search/image` | Public | Search by image |

\* The current security matcher permits `/api/products/**`; service-level ownership/role checks should therefore be treated as the authoritative protection for merchant operations.

### Keyword search

```http
GET /api/products/search?keyword=shirt
```

### Browse

```http
GET /api/products/browse
```

Optional query parameters:

| Parameter | Type | Default | Description |
|---|---|---:|---|
| `keyword` | string | none | Product keyword |
| `category` | string | none | Category filter |
| `gender` | enum | none | Gender filter |
| `newestFirst` | boolean | `false` | Sort newest products first |
| `limit` | integer | `20` | Maximum number of products |

Example:

```http
GET /api/products/browse?category=Tops&gender=MEN&newestFirst=true&limit=10
```

### Product detail

```http
GET /api/products/1
```

### Create product

```http
POST /api/products
Authorization: Bearer <JWT>
Content-Type: application/json
```

Uses:

```text
ProductRequest
```

### Update product

```http
PUT /api/products/1
Authorization: Bearer <JWT>
Content-Type: application/json
```

### Deactivate product

```http
DELETE /api/products/1
Authorization: Bearer <JWT>
```

### Activate product

```http
PATCH /api/products/1/activate
Authorization: Bearer <JWT>
```

### Own products

```http
GET /api/products/own
Authorization: Bearer <JWT>
```

### Upload image

```http
POST /api/products/image-upload
Content-Type: multipart/form-data
```

Form field:

```text
file=<image>
```

Maximum upload size in the current Spring configuration:

```text
10 MB
```

### Image search

```http
POST /api/products/search/image
Content-Type: multipart/form-data
```

Form field:

```text
image=<image>
```

The request is forwarded to the Python CNN/image-search service.

---

# Cart API

Base path:

```text
/api/cart
```

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/cart/items` | Current-user service logic | Add item |
| GET | `/api/cart` | Current-user service logic | Get cart |
| PATCH | `/api/cart/items/{cartItemId}` | Current-user service logic | Update quantity/remove |

### Add item

```http
POST /api/cart/items
Content-Type: application/json
Authorization: Bearer <JWT>
```

Uses:

```text
AddToCartRequest
```

Core fields:

```json
{
  "productVariantId": 1,
  "quantity": 2
}
```

### Get cart

```http
GET /api/cart
Authorization: Bearer <JWT>
```

### Update quantity

```http
PATCH /api/cart/items/1
Authorization: Bearer <JWT>
Content-Type: application/json
```

```json
{
  "quantity": 3
}
```

Quantity `<= 0` removes the cart row according to the controller documentation.

---

# Orders API

Base path:

```text
/api/orders
```

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/orders/checkout` | Current-user service logic | Checkout |
| GET | `/api/orders/{id}` | Current-user service logic | Customer order details |
| GET | `/api/orders/merchant` | Current-user service logic | Merchant order items |

### Checkout

```http
POST /api/orders/checkout
Authorization: Bearer <JWT>
Content-Type: application/json
```

Uses:

```text
CheckoutRequest
```

Returns:

```text
List<CheckoutResponse>
```

### Order details

```http
GET /api/orders/1
Authorization: Bearer <JWT>
```

### Merchant order items

```http
GET /api/orders/merchant
Authorization: Bearer <JWT>
```

---

# Customer Profile API

Base path:

```text
/api/user-profile
```

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/user-profile` | Current-user service logic | Get profile |
| POST | `/api/user-profile` | Public matcher | Create profile |
| POST | `/api/user-profile/with-avatar` | Public | Create profile with avatar |

### Get profile

```http
GET /api/user-profile
Authorization: Bearer <JWT>
```

### Create profile

```http
POST /api/user-profile
Content-Type: application/json
```

Uses:

```text
CreateUserProfileRequest
```

### Create profile with avatar

```http
POST /api/user-profile/with-avatar
Content-Type: multipart/form-data
```

Parameters:

```text
userId
firstName
lastName
address
postalCode
phoneNumber
avatar (optional)
```

---

# Merchant Profile API

Base path:

```text
/api/merchant
```

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/merchant/profile` | Auth/service logic | Create merchant profile |

Request is `multipart/form-data`.

Required fields:

```text
userId
businessName
uen
businessType
businessAddress
postalCode
contactNumber
productCategory
businessDescription
pickupAvailable
registrationDocument
```

Optional:

```text
logo
```

Example:

```bash
curl -X POST http://localhost:8080/api/merchant/profile \
  -F "userId=1" \
  -F "businessName=SmartCart Official" \
  -F "uen=202600000A" \
  -F "businessType=Retail" \
  -F "businessAddress=Singapore" \
  -F "postalCode=018956" \
  -F "contactNumber=65001234" \
  -F "productCategory=Fashion" \
  -F "businessDescription=Online fashion retailer" \
  -F "pickupAvailable=true" \
  -F "registrationDocument=@registration.pdf" \
  -F "logo=@logo.jpg"
```

---

# Home Content API

Base path:

```text
/api/home
```

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/home/trends/lookbook` | Current security matcher | Fashion lookbook |
| GET | `/api/home/merchants/spotlight` | Current security matcher | Merchant spotlight |

These endpoints obtain AI-generated home-page content through the Python AI service.

---

# AI Chat API

Base path:

```text
/api/chat
```

Spring Boot exposes the session-oriented chat API:

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/chat/start` | Current security matcher | Start chat session |
| POST | `/api/chat/{sessionId}` | Current security matcher | Send chat message |

### Start session

```http
POST /api/chat/start
```

The response is a `ChatResponse`/session representation.

### Send message

```http
POST /api/chat/{sessionId}
Content-Type: application/json
```

Request:

```json
{
  "message": "Show me casual shoes under $80"
}
```

The Spring service communicates with the Python AI service.

The AI agent can use SmartCart tools such as:

- Product search
- Cart lookup
- Order history
- Product catalogue retrieval

---

# Recommendations API

Base path:

```text
/api/v1/recommendations
```

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/recommendations` | JWT expected by controller | Personalized recommendations |

The controller obtains the authenticated principal, looks up the corresponding user, and calls:

```text
RecommendationOrchestratorService
```

Example:

```http
GET /api/v1/recommendations
Authorization: Bearer <JWT>
```

The result uses:

```text
RecommendationResultDTO
```

---

# Product Vector Export API

Base path:

```text
/api/v1/products
```

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/products/vector-export` | Current security matcher | Export products for vector storage |

Example:

```http
GET /api/v1/products/vector-export
```

This endpoint provides product data used by the AI/vector-search layer.

---

# Public Statistics API

Base path:

```text
/api/public
```

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/public/stats` | Public | Aggregate application statistics |

Example:

```http
GET /api/public/stats
```

Returns:

```text
PublicStatsDto
```

---

# Admin API

All `/api/admin/**` endpoints are protected by:

```text
hasRole("ADMIN")
```

## Admin accounts

Base path:

```text
/api/admin/admins
```

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/admin/admins` | ADMIN | List administrators |
| POST | `/api/admin/admins` | ADMIN | Create administrator |

### List admins

```http
GET /api/admin/admins
Authorization: Bearer <ADMIN_JWT>
```

### Create admin

```http
POST /api/admin/admins
Authorization: Bearer <ADMIN_JWT>
Content-Type: application/json
```

Uses:

```text
CreateAdminRequest
```

---

## Admin dashboard

Base path:

```text
/api/admin/dashboard
```

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/admin/dashboard/stats` | ADMIN | Dashboard statistics |

Example:

```http
GET /api/admin/dashboard/stats
Authorization: Bearer <ADMIN_JWT>
```

Returns:

```text
AdminDashboardStatsDto
```

---

## Admin merchants

Base path:

```text
/api/admin/merchants
```

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/admin/merchants` | ADMIN | List merchants |
| GET | `/api/admin/merchants/{id}` | ADMIN | Merchant details |
| PATCH | `/api/admin/merchants/{id}/status` | ADMIN | Update merchant status |

### Update merchant status

```http
PATCH /api/admin/merchants/1/status
Authorization: Bearer <ADMIN_JWT>
Content-Type: application/json
```

Uses:

```text
UpdateMerchantStatusRequest
```

Merchant lifecycle statuses are represented by:

```text
MerchantVerificationStatus
```

---

## Admin products

Base path:

```text
/api/admin/products
```

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/admin/products` | ADMIN | List all products |
| PATCH | `/api/admin/products/{id}/status` | ADMIN | Moderate product status |

### Update product status

```http
PATCH /api/admin/products/1/status
Authorization: Bearer <ADMIN_JWT>
Content-Type: application/json
```

Uses:

```text
UpdateProductStatusRequest
```

---

# Internal AI Tools API

Base path:

```text
/internal/tools
```

| Method | Endpoint | Auth in current config | Description |
|---|---|---|---|
| GET | `/internal/tools/order-history?userId={id}` | Public matcher | Retrieve order history for AI tools |
| GET | `/internal/tools/products/search` | Public matcher | Search products for AI |
| GET | `/internal/tools/cart?userId={id}` | Public matcher | Retrieve cart for AI tools |

These endpoints are used by the AI agent/tool layer.

## Important security consideration

The current `SecurityConfig` explicitly permits:

```text
/internal/tools/**
```

and accepts a `userId` query parameter for some tool operations.

For production, these endpoints should be protected behind an internal authentication mechanism, service-to-service credentials, network policy, or equivalent control.

---

# AI Microservice

Location:

```text
smartcart-ai-service/
```

Framework:

```text
FastAPI
```

Default port:

```text
8001
```

## AI service endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Health check |
| POST | `/api/chat` | Agentic AI chat |
| POST | `/api/v1/recommendations` | AI recommendations |
| POST | `/api/image-search` | CNN image search |
| POST | `/api/v1/trends/lookbook` | Generate fashion lookbook |
| POST | `/api/v1/promotions/spotlight` | Generate merchant spotlight |

---

## AI chat

```http
POST /api/chat
Content-Type: application/json
```

Request:

```json
{
  "session_id": "session-123",
  "message": "Find me white sneakers under $80",
  "history": [],
  "user_id": 2
}
```

Response structure:

```json
{
  "reply": "Here are some options...",
  "session_id": "session-123",
  "products": [],
  "orders": []
}
```

The agent can use SmartCart data tools to ground responses in application data.

---

## AI recommendations

```http
POST /api/v1/recommendations
Content-Type: application/json
```

The request is represented by:

```text
RecommendationRequest
```

The response is:

```text
RecommendationResponse
```

The recommendation service combines customer/profile information with product data.

---

## AI image search

```http
POST /api/image-search
Content-Type: multipart/form-data
```

Field:

```text
image=<image>
```

The CNN service loads the trained model from:

```text
smartcart-ai-service/cnn/
```

The repository contains:

- `best_model.keras`
- `feature_vectors.npy`
- `product_index.pkl`
- `category_encoder.pkl`
- `gender_encoder.pkl`

---

## AI trend/lookbook generation

```http
POST /api/v1/trends/lookbook
Content-Type: application/json
```

Example:

```json
{
  "theme": "summer minimalist fashion",
  "target_audience_budget": "$100 - $200"
}
```

The implementation uses:

- LLM
- Tavily search
- SmartCart product/vector search
- An in-memory cache

The current cache duration is approximately 3 hours.

---

## AI merchant spotlight

```http
POST /api/v1/promotions/spotlight
Content-Type: application/json
```

Example:

```json
{
  "merchant_id": 1,
  "merchant_name": "SmartCart Official",
  "brand_story_summary": "Featured fashion seller",
  "products": [
    {
      "id": 1,
      "name": "Classic Crew Tee",
      "category": "Tops",
      "price": 19.90,
      "description": "A soft everyday cotton tee."
    }
  ]
}
```

The response contains generated:

- Headline
- Subheadline
- Brand story
- Product highlights

---

# AI Architecture

```text
                 ┌─────────────────────┐
                 │   Spring Boot API   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Python AI Service   │
                 │      FastAPI        │
                 └──────────┬──────────┘
                            │
            ┌───────────────┼────────────────┐
            │               │                │
            ▼               ▼                ▼
       Agent Service   Recommendation     CNN Service
            │               │                │
            ▼               ▼                ▼
       LangGraph/       ChromaDB          TensorFlow
       LangChain        Vector Store       Model
            │
            ▼
       SmartCart Tools
            │
            ├── Product Search
            ├── Cart
            └── Order History
```

---

# Database

The primary database is:

```text
MySQL 8
```

Database:

```text
smartcart_db
```

Hibernate is configured with:

```properties
spring.jpa.hibernate.ddl-auto=update
```

The application also executes:

```text
src/main/resources/data.sql
```

on startup.

## Main domain models

The backend contains entities/models for:

- User
- UserProfile
- MerchantProfile
- Category
- Product
- ProductVariant
- Cart
- CartItem
- Order
- OrderItem
- Payment
- ChatSession
- ChatMessage

## Important enums

- `UserRole`
- `UserStatus`
- `ProductStatus`
- `OrderStatus`
- `PaymentMethod`
- `MerchantVerificationStatus`
- `Gender`

---

# Seed Data

`src/main/resources/data.sql` contains demo data.

The seeded accounts include:

| Account | Role |
|---|---|
| `smartcart_official` | MERCHANT |
| `grace` | CUSTOMER |
| `alex` | CUSTOMER |
| `admin` | ADMIN |

The seed script documents a common demo password for these accounts.

**Do not use seeded/demo credentials in production.**

---

# Testing

## Spring Boot tests

Run:

```bash
mvn test
```

The repository contains tests for:

- Controllers
- Services
- Security
- JWT
- DTOs
- Models
- Exception handling
- AI integration services
- Repository-related functionality

Examples:

```text
AuthControllerTest
CartControllerTest
ProductControllerTest
OrderControllerTest
RecommendationControllerTest
JwtServiceTest
JwtAuthenticationFilterTest
AuthServiceTest
ProductServiceTest
OrderServiceTest
```

## AI service tests

From:

```text
smartcart-ai-service/
```

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run:

```bash
pytest
```

The AI test suite includes:

- Agent service
- Chat router
- CNN service
- SmartCart tools
- Workflow

---

# Code Quality and Coverage

The Maven build includes:

```text
JaCoCo
```

The configured coverage target is:

```text
85% line coverage
```

Generate the report:

```bash
mvn verify
```

Report:

```text
target/site/jacoco/index.html
```

SonarCloud configuration is also present in `pom.xml`.

Coverage exclusions include DTO/model boilerplate, while JaCoCo excludes:

```text
*Application.class
dto/**
model/**
config/**
```

---

# CI/CD and Security

GitHub Actions configuration is located at:

```text
.github/workflows/backend.yml
```

The project includes CI/CD activities for the backend and container image.

The repository also includes security scanning configuration, including Trivy-related dependency/image hardening.

The Maven build explicitly pins some dependency versions to address security findings.

Typical CI flow:

```text
Git Push
   │
   ▼
GitHub Actions
   │
   ├── Build
   ├── Test
   ├── JaCoCo
   ├── Security Scan
   ├── Docker Build
   ├── Push to AWS ECR
   └── Deploy to AWS EKS
```

---

# AWS Infrastructure

Infrastructure-as-code is located in:

```text
terraform/
```

The Terraform configuration provisions:

- AWS VPC
- EKS cluster
- ECR repositories
- IAM OIDC integration
- GitHub Actions deployment role

Main files:

```text
terraform/
├── ecr.tf
├── eks.tf
├── oidc.tf
├── outputs.tf
├── variables.tf
├── versions.tf
├── vpc.tf
└── terraform.tfvars.example
```

## Initial Terraform setup

```bash
cd terraform

cp terraform.tfvars.example terraform.tfvars

terraform init

terraform plan

terraform apply
```

After provisioning, the GitHub Actions IAM role ARN is used by the CI/CD workflow.

## Destroy infrastructure

```bash
terraform destroy
```

### Important

The Terraform documentation notes that the project is designed for a short-lived academic/demo deployment.

The current Kubernetes MySQL configuration uses ephemeral storage, so database data can be lost if the MySQL pod is recreated.

Do not reuse the current infrastructure configuration unchanged for production workloads.

---

# Docker Architecture

```text
                    Docker Compose
                         │
       ┌─────────────────┼──────────────────┐
       │                 │                  │
       ▼                 ▼                  ▼
  ┌─────────┐      ┌──────────────┐   ┌───────────┐
  │ MySQL   │◄────►│ Spring Boot  │◄─►│ AI Service│
  │ :3306   │      │ :8080        │   │ :8001     │
  └─────────┘      └──────────────┘   └───────────┘
                           ▲
                           │
                           ▼
                    ┌─────────────┐
                    │  Frontend   │
                    │    :4200    │
                    └─────────────┘
```

---

# Troubleshooting

## Backend cannot connect to MySQL

Check:

```text
MySQL is running
Port 3306 is available
Database smartcart_db exists
Username/password are correct
```

Test:

```bash
mysql -u root -p
```

Then:

```sql
SHOW DATABASES;
```

---

## AI service unavailable

Check:

```text
http://localhost:8001/api/health
```

Expected:

```json
{
  "status": "ok",
  "service": "smartcart-ai-service"
}
```

Also check the backend setting:

```properties
ai.python-service.base-url=http://localhost:8001
```

When running under Docker Compose, the backend uses:

```text
http://smartcart-ai-service:8001
```

---

## JWT authentication failure

Check that the request includes:

```http
Authorization: Bearer <JWT>
```

Also verify:

```text
JWT_SECRET
JWT expiration
User account status
User role
```

---

## Multipart upload failure

The Spring Boot configuration currently allows:

```text
Maximum file size: 10 MB
Maximum request size: 10 MB
```

Check:

```properties
spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=10MB
```

---

# Security Notes

Before production deployment, review the following items carefully.

## 1. Never commit secrets

The repository contains environment/configuration files. Any real credentials should be removed and rotated.

Use:

```text
.env
environment variables
GitHub Secrets
AWS Secrets Manager
Kubernetes Secrets
```

instead.

## 2. Generate a new JWT secret

Do not reuse the sample JWT secret.

Generate a cryptographically random secret and provide it through:

```text
JWT_SECRET
```

## 3. Protect internal tools

The current configuration permits:

```text
/internal/tools/**
```

These APIs should not normally be exposed publicly.

## 4. Review customer endpoint authorization

The current `SecurityConfig` permits:

```text
/api/cart/**
/api/chat/**
/api/orders/**
/api/user-profile/**
/api/v1/products/**
/api/home/**
```

even though several controllers use `CurrentUserProvider`.

If these endpoints are intended to be authenticated customer APIs, change the authorization rules to require authentication.

## 5. Review logout semantics

The current `/api/auth/logout` endpoint returns a successful response but does not revoke the JWT server-side.

The client should remove the token locally, but a token remains cryptographically valid until expiry unless server-side revocation is implemented.

## 6. Protect AI credentials

The AI service may use:

```text
OPENAI_API_KEY
OPENROUTER_API_KEY
TAVILY_API_KEY
```

These must never be committed to Git.

---

# API Quick Reference

```text
AUTH
POST   /api/auth/register
POST   /api/auth/merchant/register
POST   /api/auth/login
POST   /api/auth/change-password
POST   /api/auth/reset-password
POST   /api/auth/check-email
POST   /api/auth/logout

CATEGORIES
GET    /api/categories

PRODUCTS
GET    /api/products/search
GET    /api/products/browse
GET    /api/products/{id}
POST   /api/products
PUT    /api/products/{id}
DELETE /api/products/{id}
GET    /api/products/own
POST   /api/products/image-upload
PATCH  /api/products/{id}/activate
POST   /api/products/search/image

CART
POST   /api/cart/items
GET    /api/cart
PATCH  /api/cart/items/{cartItemId}

ORDERS
POST   /api/orders/checkout
GET    /api/orders/{id}
GET    /api/orders/merchant

CUSTOMER
GET    /api/user-profile
POST   /api/user-profile
POST   /api/user-profile/with-avatar

MERCHANT
POST   /api/merchant/profile

HOME
GET    /api/home/trends/lookbook
GET    /api/home/merchants/spotlight

CHAT
POST   /api/chat/start
POST   /api/chat/{sessionId}

RECOMMENDATION
GET    /api/v1/recommendations

VECTOR
GET    /api/v1/products/vector-export

PUBLIC
GET    /api/public/stats

ADMIN
GET    /api/admin/admins
POST   /api/admin/admins
GET    /api/admin/dashboard/stats
GET    /api/admin/merchants
GET    /api/admin/merchants/{id}
PATCH  /api/admin/merchants/{id}/status
GET    /api/admin/products
PATCH  /api/admin/products/{id}/status

INTERNAL AI TOOLS
GET    /internal/tools/order-history
GET    /internal/tools/products/search
GET    /internal/tools/cart
```

---

# Project Status

The repository currently contains:

- Spring Boot backend
- JWT authentication
- Customer/merchant/admin roles
- Product catalogue
- Product variants
- Shopping cart
- Checkout/order management
- Merchant management
- Admin dashboard
- Admin moderation
- AI chat
- AI recommendations
- Vector product export
- CNN image search
- Image uploads
- FastAPI AI microservice
- Docker Compose
- Terraform AWS infrastructure
- GitHub Actions CI/CD
- Automated tests
- JaCoCo coverage
- Security scanning configuration

---

# Author

**Sailong Junior**

GitHub:

https://github.com/sailongjunior89

Repository:

https://github.com/sailongjunior89/smartcart-backend

---

# License

This project is currently maintained as an academic/project implementation.

Add an explicit open-source license such as MIT if the project is intended for public redistribution.

---

## Disclaimer

This README was generated from the source code and configuration present in the repository snapshot. Endpoint behavior and security requirements should be re-verified whenever controllers, services, `SecurityConfig`, Docker configuration, or the AI service are changed.
