# Production-Ready Small Business Commerce Platform

Full-stack eCommerce + business management system using Django/DRF, React + TypeScript, PostgreSQL, Redis/Celery, Docker, and GitHub Actions.

## Architecture

- **Backend**: Django monolith with modular apps (`accounts`, `catalog`, `orders`, `payments`, `inventory`, `analytics_app`, `website`)
- **Frontend**: React TypeScript SPA with SEO-oriented structure and public pages
- **Data**: PostgreSQL
- **Async and cache**: Redis + Celery workers
- **Storage**: local media for dev and S3-compatible storage for production
- **CI**: GitHub Actions for backend tests and frontend build

## Implemented Features

- JWT authentication and role-aware user model (`admin`, `customer`)
- Public pages: Home, About, Contact, Testimonials section
- Product and category CRUD with filtering, search, ordering, pagination
- Cart, checkout, and order creation with atomic stock decrement and oversell prevention
- Payment records with idempotency, webhook endpoint with signature verification
- Order and shipment management with status tracking
- Inventory transaction logging and low-stock alert background task
- Admin dashboard placeholder frontend page for management workflows
- Analytics API for revenue/orders/top-products with date range and CSV export
- Security baselines: strong password validators, CSRF middleware, secure-cookie toggles, HTTPS redirect controls

## Quick Start (Docker)

```bash
cp .env.example .env
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- Django admin: http://localhost:8000/admin

## Backend Local Development

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
pytest
```

## Frontend Local Development

```bash
cd frontend
npm install
npm run dev
```

## Main API Endpoints

- `POST /api/auth/register/`
- `POST /api/auth/token/` and `POST /api/auth/token/refresh/`
- `GET/POST/PUT/DELETE /api/products/`
- `GET/POST/PUT/DELETE /api/categories/`
- `GET/POST /api/cart/`
- `GET /api/orders/`, `POST /api/orders/checkout/`, `POST /api/orders/{id}/update_status/`
- `GET/POST /api/payments/`, `POST /api/payments/webhook/`
- `GET /api/analytics/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
- `GET /api/analytics/?format=csv`

## Deployment Notes

- Enable `USE_S3=1` and configure S3 credentials for media storage.
- Set secure flags in `.env` for TLS deployments.
- Run migrations at deploy (`python manage.py migrate`).
- Deploy with reverse proxy and HTTPS termination.
- Attach centralized logging/monitoring stack (e.g., ELK/Cloud logging + Prometheus).
