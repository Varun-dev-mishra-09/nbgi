# BDS Implementation Plan

## Phase 1 — Platform Foundation (Completed)
- Establish repository conventions and workflow documentation.
- Define clean architecture boundaries for backend services.
- Prepare environment-variable strategy for frontend and backend.

## Phase 2 — Commerce Core + Checkout Payments (Completed)
- Create payment service abstractions in backend service layer.
- Add Razorpay test-mode order creation endpoint.
- Keep Cash on Delivery (COD) flow independent from Razorpay.
- Add frontend Razorpay loader + checkout payment selection component.

## Phase 3 — Catalog, Search, and Filters (In Progress)
- Product/category schemas.
- Search and filter APIs and frontend integration.
- Establish relational database model layer for ecommerce entities.

## Phase 4 — Orders, Tracking, Dashboard (Pending)
- Order lifecycle APIs.
- Customer order timeline + dashboard.

## Phase 5 — Admin/Sadmin Role Surface (Pending)
- `/bds/admin` and `/bds/sadmin` authorization boundaries.
- Admin-only analytics endpoints and views.

## Phase 6 — Advanced Programs and Security Hardening (Pending)
- Coupons, referrals, affiliate, recommendations.
- Security controls: rate limiting, bot detection, CSRF/XSS/SQLi defenses.
