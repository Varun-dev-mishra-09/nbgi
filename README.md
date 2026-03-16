# NGBI (Next Generation Bus Intelligence)

Production-ready monorepo for a real-time bus tracking and seat booking platform.

## Monorepo layout

```text
ngbi/
├── frontend/
│   ├── apps/
│   │   ├── user/
│   │   ├── conductor/
│   │   └── admin/
│   └── packages/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── notifications/
│   │   ├── payments/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── tasks/
│   │   └── websocket/
│   └── alembic/
└── infrastructure/
    ├── docker/
    ├── nginx/
    └── scripts/
```

## Core capabilities

- Next.js 14 frontend (user, conductor, admin apps)
- FastAPI backend with SQLAlchemy ORM + Alembic
- PostgreSQL + Redis cache and locking
- Redis seat locking TTL = 5 minutes
- WebSocket bus tracking broadcasts
- Razorpay + Paytm order and webhook flows
- Google OAuth + mobile OTP + JWT
- RBAC for user/conductor/admin
- Celery background tasks for OTP, notifications, ticket generation, reconciliation

## Quick start

### 1) Environment

Copy env templates:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### 2) Run with Docker Compose

```bash
docker compose -f infrastructure/docker/docker-compose.yml up --build
```

Services:

- Frontend User: http://localhost:3000
- Frontend Conductor: http://localhost:3001
- Frontend Admin: http://localhost:3002
- Backend API: http://localhost:8000
- Backend Docs: http://localhost:8000/docs

### 3) DB migration

```bash
cd backend
alembic upgrade head
```

## Deployment targets

- Frontend apps: Vercel projects (`user`, `conductor`, `admin`)
- Backend API + workers: Railway/Render
- PostgreSQL: Supabase/Neon
- Redis: Upstash/Redis Cloud

## API surface

### Auth

- `POST /api/v1/auth/google-login`
- `POST /api/v1/auth/otp-send`
- `POST /api/v1/auth/otp-verify`

### User

- `GET /api/v1/user/routes`
- `GET /api/v1/user/trips`
- `POST /api/v1/user/book-seat`
- `GET /api/v1/user/ticket/{booking_id}`

### Conductor

- `GET /api/v1/conductor/trip/{trip_id}`
- `POST /api/v1/conductor/book-seat`
- `POST /api/v1/conductor/verify-ticket`

### Admin

- `POST /api/v1/admin/add-bus`
- `POST /api/v1/admin/create-route`
- `POST /api/v1/admin/create-trip`
- `GET /api/v1/admin/analytics`

### Payments

- `POST /api/v1/payments/create-order`
- `POST /api/v1/payments/verify`
- `POST /api/v1/payments/webhook`

### Tracking

- `POST /api/v1/tracking/gps-update`
- `GET /api/v1/tracking/bus-location/{trip_id}`
- `WS /api/v1/ws/tracking/{trip_id}`

## Seat locking strategy

Redis key: `seat_lock:{trip_id}:{seat_number}`

- `available` => no redis key and no booking row
- `locked` => redis key exists, TTL 300s
- `booked` => booking status `CONFIRMED`

## Example requests

```bash
curl -X POST http://localhost:8000/api/v1/auth/otp-send \
  -H "Content-Type: application/json" \
  -d '{"phone":"+919900001111"}'

curl -X POST http://localhost:8000/api/v1/payments/create-order \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{"trip_id":"<trip_uuid>","seat_number":5,"provider":"razorpay"}'
```

## Security

- JWT access token auth
- Role-based route guards
- Password hashing with bcrypt
- Pydantic input validation
- FastAPI rate limiter middleware scaffold
- Signed payment webhook verification stubs

## Notes

- Replace provider stubs with live credentials.
- Configure Google Maps API key in frontend env for live map tiles.

## Running in GitHub Codespaces

If ports are not being auto-forwarded, run backend from the repository root using one of these commands:

```bash
bash scripts/dev.sh
# or
cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Codespaces verification commands

```bash
pwd
python --version
cd backend
python -c "import app.main; print('import-ok')"
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Expected:
- Terminal prints `Uvicorn running on http://0.0.0.0:8000`
- Codespaces **PORTS** shows `8000` as forwarded.

If you start from repo root without changing directories, use:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --app-dir backend
```
