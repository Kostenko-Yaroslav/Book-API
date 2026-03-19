# Book API Service

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Django](https://img.shields.io/badge/django-5.0-green.svg)
![DRF](https://img.shields.io/badge/DRF-3.14-red.svg)
![Postgres](https://img.shields.io/badge/postgres-17-blue)
![Docker](https://img.shields.io/badge/docker-compose-orange)

A REST API service for managing a bookshop. The application provides tools to browse a book catalogue, manage authors, register users, and handle automated order processing with stock tracking.

---

## Project Overview

### Technology Stack
* **Core:** Python 3.12, Django, Django Rest Framework
* **Database:** PostgreSQL 17
* **Authentication:** JWT (Simple JWT)
* **Documentation:** OpenAPI 3.0 / Swagger (drf-spectacular)
* **Containerization:** Docker & Docker Compose

### Functionality
* **Books and Authors:** Full CRUD operations for books and authors with filtering and stock control.
* **Orders:** Automated order creation with real-time stock availability checks.
* **Atomic Transactions:** Secure stock reduction during order processing with automated rollback on failure.
* **Security:** Granular access control using JWT tokens and custom Permission Classes.

---

## Quick Start

### With Docker (Recommended)
```bash
# Cloning a repository
git clone https://github.com/Kostenko-Yaroslav/Book-API
cd Book-Store-API

# Create .env file
cp .env.example .env

# Start containers
docker-compose up --build
```
*API: http://localhost:8000 | Swagger UI: http://localhost:8000/docs*

### Locally (Development)
1. **Environment:** `python -m venv .venv` and `source .venv/bin/activate`
2. **Dependencies:** `pip install -r requirements.txt`
3. **Config:** `cp .env.example .env` (specify DATABASE_URL in .env)
4. **Database:** `python manage.py migrate`
5. **Run:** `python manage.py runserver`

---

## API Endpoints

### Auth
| Method | Endpoint | Description | Access |
| --- | --- | --- | --- |
| POST | `/auth/register` | User registration | Public |
| POST | `/auth/login` | Login (Get JWT token) | Public |

### Authors
| Method | Endpoint | Description | Access |
| --- | --- | --- | --- |
| GET | `/authors/` | List all authors | Public |
| GET | `/authors/{id}/` | Get author details | Public |
| POST | `/authors/` | Create author | Admin |

### Books
| Method | Endpoint | Description | Access |
| --- | --- | --- | --- |
| GET | `/books/` | List all books (pagination, filtering) | Public |
| GET | `/books/{id}/` | Get book details | Public |
| POST | `/books/` | Create book | Admin |
| PATCH | `/books/{id}/` | Update book | Admin |
| DELETE | `/books/{id}/` | Delete book | Admin |

### Orders
| Method | Endpoint | Description | Access |
| --- | --- | --- | --- |
| POST | `/orders/` | Create order | Authenticated |

---

## Testing

```bash
# Set dependencies for tests
pip install -r requirements.txt

# Run tests
pytest
```
