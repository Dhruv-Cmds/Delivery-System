# API Documentation

This document describes the HTTP API exposed by the Food Delivery Management System. The API is implemented with FastAPI and uses JSON request and response bodies.

The interactive OpenAPI documentation is available when the backend is running:

```text
Swagger UI: http://127.0.0.1:8000/docs
ReDoc:      http://127.0.0.1:8000/redoc
OpenAPI:    http://127.0.0.1:8000/openapi.json
```

---

# API Overview

All application routes are mounted below the `/api` prefix.

```text
Client
   │
   │ HTTP / JSON
   ▼
FastAPI Application
   │
   ├── /api/auth              Authentication
   ├── /api/user              User administration
   ├── /api/restaurant        Restaurant management
   ├── /api/menus             Menu management and browsing
   ├── /api/order             Order processing
   ├── /api/payment           Payment processing
   ├── /api/traking           Order tracking
   ├── /api/delivery_partner  Delivery partner management
   ├── /api/notification      Notifications
   └── /api/health            Health monitoring
```

The default local development server is normally started with:

```bash
uvicorn app.main:app --reload --port 8000
```

---

# Authentication

Authentication uses JWT access tokens. First authenticate with `/api/auth/login`, then send the returned token with every protected request.

```http
Authorization: Bearer <ACCESS_TOKEN>
```

The API accepts JSON requests using the following content type:

```http
Content-Type: application/json
```

Unauthenticated public endpoints include health checks, restaurant lookup, menu browsing, and delivery partner lookup by partner ID. All other endpoint access is controlled by authentication and role checks.

---

# Roles and Access Rules

| Role | Main permissions |
|------|------------------|
| `CUSTOMER` | Create orders, make payments, view owned orders and notifications |
| `RESTAURANT_OWNER` | Create and manage owned restaurants and menu items |
| `DELIVERY_PARTNER` | Manage the partner profile and assigned location |
| `ADMIN` | Administrative access across users, payments, deliveries, notifications, and tracking |

Resource ownership is checked in the service layer. For example, a restaurant owner cannot modify another owner's restaurant, and a customer cannot read another customer's order or payment information.

---

# Endpoint Summary

## Authentication

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| `POST` | `/api/auth/signup` | Public | Register a user |
| `POST` | `/api/auth/login` | Public | Authenticate and return a JWT |

## Health

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| `GET` | `/api/health` | Public | Check application and database health |

## Users

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| `GET` | `/api/user/` | Admin | List all users |
| `GET` | `/api/user/{user_id}` | Admin | Get a user by ID |
| `GET` | `/api/user/email/{user_email}` | Admin | Get a user by email |
| `GET` | `/api/user/username/{username}` | Admin | Get a user by username |

## Restaurants

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| `POST` | `/api/restaurant/` | Admin, owner, customer | Create a restaurant |
| `GET` | `/api/restaurant/{restaurant_id}` | Public | Get a restaurant |
| `PUT` | `/api/restaurant/{restaurant_id}` | Admin, owner | Replace restaurant details |
| `PATCH` | `/api/restaurant/{restaurant_id}/status` | Admin, owner | Change restaurant status |
| `DELETE` | `/api/restaurant/{restaurant_id}` | Admin, owner | Delete a restaurant |

## Menu

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| `POST` | `/api/menus/` | Admin, owner | Create a menu item |
| `GET` | `/api/menus/{menu_id}` | Public | Get a menu item |
| `GET` | `/api/menus/restaurants/{restaurant_id}/menus` | Public | List a restaurant's menu items |
| `PUT` | `/api/menus/{menu_id}` | Admin, owner | Replace menu item details |
| `PATCH` | `/api/menus/{menu_id}/status` | Admin, owner | Change menu availability |
| `DELETE` | `/api/menus/{menu_id}` | Admin, owner | Delete a menu item |

## Orders

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| `POST` | `/api/order` | Customer | Create an order |
| `GET` | `/api/order/all` | Authenticated | List orders visible to the current user |
| `GET` | `/api/order/{order_id}` | Authenticated | Get an order |
| `PATCH` | `/api/order/{order_id}/status` | Admin, owner | Change order status |
| `DELETE` | `/api/order/{order_id}` | Admin, owner | Delete an order when its state allows it |
| `GET` | `/api/menu_item/{menu_item_id}` | Admin, owner | Get a menu item for order processing |

## Payments

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| `POST` | `/api/order/{order_id}/payment` | Customer | Create or complete an order payment |
| `GET` | `/api/payment/all` | Authenticated | List the current user's payments |
| `GET` | `/api/order/{order_id}/payment` | Authenticated | Get payment for an owned order |
| `GET` | `/api/payment/{payment_id}` | Admin | Get a payment by ID |
| `PATCH` | `/api/payment/{payment_id}/status` | Admin | Change payment status |

## Order Tracking

The route prefix is currently spelled `/traking` in the implementation.

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| `POST` | `/api/traking/` | Admin, owner | Create tracking data |
| `GET` | `/api/traking/order/{order_id}` | Authenticated | Get tracking for an owned order |
| `GET` | `/api/traking/all` | Admin, owner | List tracking records |

## Delivery Partners

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| `POST` | `/api/delivery_partner/` | Authenticated | Create a delivery partner profile |
| `GET` | `/api/delivery_partner/{partner_id}` | Public | Get a partner by ID |
| `GET` | `/api/delivery_partner/user/{user_id}` | Admin, owner | Get a partner by user ID |
| `GET` | `/api/delivery_partner/all` | Admin | List all delivery partners |
| `PUT` | `/api/delivery_partner/{partner_id}` | Partner, admin | Update vehicle information |
| `PUT` | `/api/delivery_partner/{partner_id}/location` | Partner, admin | Update latitude and longitude |
| `DELETE` | `/api/delivery_partner/{partner_id}` | Partner, admin | Delete a partner profile |

## Notifications

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| `GET` | `/api/notification/` | Authenticated | List current user's notifications |
| `GET` | `/api/notification/{notification_id}` | Authenticated | Get one notification |
| `PATCH` | `/api/notification/{notification_id}/read` | Authenticated | Mark one notification as read |
| `PATCH` | `/api/notification/read-all` | Authenticated | Mark all user notifications as read |
| `DELETE` | `/api/notification/{notification_id}` | Authenticated | Delete a notification |
| `GET` | `/api/admin/notification/all` | Admin | List all notifications |
| `GET` | `/api/admin/notification/user/{user_id}` | Admin | List notifications for a user |

---

# Request Schemas

## User Registration

`POST /api/auth/signup`

```json
{
  "username": "adam",
  "name": "Adam Das",
  "phone": "9876543201",
  "email": "adamexample@gmail.com",
  "password": "Strongpass123"
}
```

`username`, `name`, and `password` are length-validated. Email must be valid, and passwords must contain between 8 and 100 characters.

## Login

`POST /api/auth/login`

```json
{
  "email": "adamexample@gmail.com",
  "password": "Strongpass123"
}
```

Successful response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## Restaurant

`POST /api/restaurant/` and `PUT /api/restaurant/{restaurant_id}` accept:

```json
{
  "name": "Noodle Nest",
  "phone": "9892760261",
  "address": "101 Food Street, Alkapuri, Vadodara"
}
```

## Menu Item

`POST /api/menus/` and `PUT /api/menus/{menu_id}` accept:

```json
{
  "restaurant_id": 5,
  "item_name": "Cheese Pizza",
  "description": "Cheese pizza with extra toppings",
  "price": 499.00
}
```

## Order

`POST /api/order` accepts one menu item and its quantity:

```json
{
  "menu_item_id": 23,
  "quantity": 2,
  "delivery_address": "101 Food Street, Alkapuri, Vadodara"
}
```

Only available menu items can be ordered. The current maximum quantity is 20, and only active customers can create orders.

## Payment

`POST /api/order/{order_id}/payment` accepts:

```json
{
  "payment_method": "UPI"
}
```

Supported payment methods are `UPI`, `CARD`, `COD`, and `ONLINE`.

## Delivery Partner

`POST /api/delivery_partner/` accepts:

```json
{
  "vehicle_type": "Two wheeler"
}
```

Supported vehicle types are `Two wheeler` and `Four wheeler`.

---

# Response Models

| Model | Main fields |
|-------|-------------|
| `UserResponse` | `id`, `username`, `name`, `phone`, `email`, `role`, `status` |
| `RestaurantResponse` | `id`, `owner_id`, `name`, `phone`, `address`, `status` |
| `MenuResponse` | `id`, `restaurant_id`, `item_name`, `description`, `price`, `status` |
| `OrderResponse` | `id`, `customer_id`, `restaurant_id`, `delivery_partner_id`, `status`, `total_price`, `delivery_address`, `payment_status`, `created_at`, `updated_at`, `order_items` |
| `OrderItemResponse` | `id`, `order_id`, `menu_item_id`, `quantity`, `unit_price`, `total_price` |
| `PaymentResponse` | `id`, `order_id`, `payment_method`, `amount`, `status`, `paid_at`, `transaction_reference` |
| `TrackingResponse` | `id`, `order_id`, `latitude`, `longitude`, `status` |
| `DeliveryPartnerResponse` | `id`, `user_id`, `vehicle_type`, `status`, `rating`, `latitude`, `longitude` |
| `NotificationResponse` | `id`, `user_id`, `message`, `notification_type`, `status`, `created_at` |

Responses are serialized from SQLAlchemy models through Pydantic response schemas.

---

# Enumerated Values

| Field | Allowed values |
|-------|----------------|
| User role | `CUSTOMER`, `DELIVERY_PARTNER`, `ADMIN`, `RESTAURANT_OWNER` |
| User status | `ACTIVE`, `CLOSE` |
| Restaurant status | `PENDING`, `APPROVED`, `REJECTED`, `SUSPENDED`, `OPEN`, `CLOSED` |
| Menu status | `AVAILABLE`, `UNAVAILABLE` |
| Order status | `PENDING`, `ACCEPTED`, `PREPARING`, `PICKED_UP`, `DELIVERED`, `REPLACE`, `CANCELLED`, `OUT_FOR_DELIVERY` |
| Payment status | `PENDING`, `SUCCESS`, `FAILED`, `REFUNED` |
| Notification status | `UNREAD`, `READ` |
| Notification type | `ORDER_UPDATE`, `PAYMENT`, `DELIVERY`, `SYSTEM` |

Status values are passed as query parameters for status endpoints. For example:

```text
PATCH /api/order/12/status?status=PREPARING
PATCH /api/payment/8/status?status=SUCCESS
PATCH /api/restaurant/5/status?status=OPEN
PATCH /api/menus/23/status?status=AVAILABLE
```

Location updates use query parameters for coordinates:

```text
PUT /api/delivery_partner/3/location?latitude=22.3072&longitude=73.1812
```

---

# Error Handling

Application errors use a consistent JSON structure:

```json
{
  "detail": {
    "error": "ORDER_NOT_FOUND",
    "message": "Order not found"
  }
}
```

Common status codes include:

| Status | Meaning |
|--------|---------|
| `400` | Invalid operation or business-rule violation |
| `401` | Missing, invalid, expired, or incorrect authentication |
| `403` | Authenticated user lacks the required role or ownership |
| `404` | Requested resource does not exist |
| `409` | Duplicate resource or conflicting state |
| `422` | Pydantic request validation failed |
| `429` | Rate limit exceeded |
| `500` | Database or unexpected server error |

Validation errors generated by FastAPI/Pydantic identify the invalid request fields. Domain errors use application error codes such as `USER_NOT_FOUND`, `PERMISSION_DENIED`, `PAYMENT_NOT_FOUND`, and `INVALID_TOKEN`.

---

# Rate Limits

The API uses SlowAPI rate limiting. Important limits include:

| Operation | Limit |
|-----------|-------|
| Signup | 5 requests/minute |
| Login | 10 requests/minute |
| Create order | 5 requests/minute |
| Make payment | 5 requests/minute |
| Read-heavy endpoints | Usually 60–120 requests/minute |
| Location updates | 120 requests/minute |

When a client exceeds a limit, the API returns `429 Too Many Requests`.

---

# Example Workflow

```text
1. Register or log in                         POST /api/auth/signup|login
2. Save the returned JWT
3. Browse restaurants and menus               GET /api/restaurant/{id}
                                               GET /api/menus/restaurants/{id}/menus
4. Create an order                             POST /api/order
5. Make a payment                              POST /api/order/{id}/payment
6. Read order progress                         GET /api/traking/order/{id}
7. Read status notifications                   GET /api/notification/
```

Example authenticated order request:

```bash
curl -X POST http://127.0.0.1:8000/api/order \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "menu_item_id": 23,
    "quantity": 2,
    "delivery_address": "101 Food Street, Alkapuri, Vadodara"
  }'
```

---

# Implementation Notes

- The API is asynchronous and backed by FastAPI and SQLAlchemy Async ORM.
- JWT validation checks the configured secret, algorithm, issuer (`delivery_api`), and user record.
- Request bodies are validated with Pydantic schemas.
- Role and ownership checks are enforced through FastAPI dependencies and service-layer validation.
- Redis caching is used by the service layer where supported.
- The canonical source for generated request and response schemas is the live OpenAPI document at `/openapi.json`.

---

# Related Documentation

- `docs/architecture.md` — system structure, layers, and request lifecycle
- `docs/security.md` — authentication, authorization, validation, and security controls
- `docs/docker.md` — local and containerized API startup
- `docs/deployment.md` — deployment guidance
- `docs/testing.md` — API and integration testing
