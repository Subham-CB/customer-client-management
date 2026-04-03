# Customer-Client Management System

A Django web application for managing relationships between **clients** and **contacts** with bidirectional linking, auto-generated client codes, and a clean, responsive UI.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [Running with Docker](#running-with-docker)
- [Running Locally](#running-locally)
- [API Routes](#api-routes)
- [Database Models](#database-models)
- [Admin Interface](#admin-interface)

---

## Features

- **Client Management** — Create, view, edit, and delete clients. Each client gets an auto-generated unique 6-character code (e.g. `ABC001`).
- **Contact Management** — Create, view, edit, and delete contacts with unique email addresses.
- **Bidirectional Linking** — Link/unlink contacts to clients and vice-versa via AJAX (no page reload).
- **Auto-generated Client Codes** — Intelligent 3-letter prefix derived from the client name + 3-digit numeric suffix.
- **Responsive UI** — Built with Tailwind CSS; tabbed detail pages, flash notifications, and sortable lists.
- **Django Admin** — Full admin interface available at `/admin/`.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12 |
| Framework | Django 6.0.3 |
| Database | PostgreSQL 16 |
| Frontend | HTML5, Tailwind CSS, Vanilla JavaScript |
| Server | Django dev server (local) / Gunicorn-ready (Docker) |
| Containerisation | Docker & Docker Compose |

---

## Project Structure

```
customer-client-management/
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
├── .env                        # Environment variables (create from example below)
├── ccm_project/                # Django project settings & URL config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── clients/                    # Client app (models, views, forms, urls)
├── contacts/                   # Contact app (models, views, forms, urls)
├── templates/                  # HTML templates (base + per-app)
└── static/css/style.css        # Custom CSS
```

---

## Environment Variables

Create a `.env` file in the project root. Use the table below as a reference.

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_NAME` | PostgreSQL database name | `ccm_db` |
| `DB_USER` | PostgreSQL user | `postgres` |
| `DB_PASSWORD` | PostgreSQL password | *(required)* |
| `DB_HOST` | Database host | `db` (Docker) / `localhost` (local) |
| `DB_PORT` | Database port | `5432` |

### Example `.env` for Docker

```env
DB_NAME=ccm_db
DB_USER=postgres
DB_PASSWORD=strongpassword
DB_HOST=db
DB_PORT=5432
```

### Example `.env` for local development

```env
DB_NAME=ccm_db
DB_USER=postgres
DB_PASSWORD=strongpassword
DB_HOST=localhost
DB_PORT=5432
```

> **Note:** For production, also set `SECRET_KEY` to a long random string, set `DEBUG=False`, and configure `ALLOWED_HOSTS` in `ccm_project/settings.py`.

---

## Running with Docker

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/Subham-CB/customer-client-management.git
   cd customer-client-management
   ```

2. **Create your `.env` file**

   ```bash
   cp .env .env.backup   # optional: back up any existing .env
   ```

   Create (or edit) `.env` in the project root:

   ```env
   DB_NAME=ccm_db
   DB_USER=postgres
   DB_PASSWORD=strongpassword
   DB_HOST=db
   DB_PORT=5432
   ```

   > Keep `DB_HOST=db` — this is the Docker Compose service name for the database container.

3. **Build and start the containers**

   ```bash
   docker compose up --build
   ```

   This will:
   - Pull the PostgreSQL 16 image and start the database
   - Build the Django application image
   - Wait for the database to be healthy
   - Run `python manage.py migrate` automatically
   - Start the development server on port `8000`

4. **Open the application**

   ```
   http://localhost:8000/clients/
   ```

5. **(Optional) Create a Django superuser for the admin panel**

   In a second terminal:

   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

6. **Stop the containers**

   ```bash
   docker compose down
   ```

   To also remove the database volume (all data):

   ```bash
   docker compose down -v
   ```

### Useful Docker Commands

```bash
# View live logs
docker compose logs -f web

# Open a Django shell inside the container
docker compose exec web python manage.py shell

# Run migrations manually
docker compose exec web python manage.py migrate

# Collect static files
docker compose exec web python manage.py collectstatic --noinput
```

---

## Running Locally

### Prerequisites

- Python 3.12+
- PostgreSQL 16+ running locally
- `pip` package manager

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/Subham-CB/customer-client-management.git
   cd customer-client-management
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS / Linux
   venv\Scripts\activate           # Windows
   ```

3. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a PostgreSQL database**

   ```bash
   psql -U postgres -c "CREATE DATABASE ccm_db;"
   ```

5. **Create your `.env` file**

   ```env
   DB_NAME=ccm_db
   DB_USER=postgres
   DB_PASSWORD=strongpassword
   DB_HOST=localhost
   DB_PORT=5432
   ```

   > Set `DB_HOST=localhost` when running without Docker.

6. **Apply database migrations**

   ```bash
   python manage.py migrate
   ```

7. **(Optional) Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

8. **Start the development server**

   ```bash
   python manage.py runserver
   ```

9. **Open the application**

   ```
   http://localhost:8000/clients/
   ```

---

## API Routes

### Clients (`/clients/`)

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/clients/` | List all clients |
| GET, POST | `/clients/create/` | Create a new client |
| GET, POST | `/clients/<id>/` | View or edit a client |
| POST | `/clients/<id>/delete/` | Delete a client |
| POST | `/clients/<id>/link-contact/` | Link a contact to a client (AJAX) |
| POST | `/clients/<id>/unlink-contact/<contact_id>/` | Unlink a contact from a client (AJAX) |
| GET | `/clients/<id>/available-contacts/` | List contacts not yet linked to this client (AJAX) |

### Contacts (`/contacts/`)

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/contacts/` | List all contacts |
| GET, POST | `/contacts/create/` | Create a new contact |
| GET, POST | `/contacts/<id>/` | View or edit a contact |
| POST | `/contacts/<id>/delete/` | Delete a contact |
| POST | `/contacts/<id>/link-client/` | Link a client to a contact (AJAX) |
| POST | `/contacts/<id>/unlink-client/<client_id>/` | Unlink a client from a contact (AJAX) |
| GET | `/contacts/<id>/available-clients/` | List clients not yet linked to this contact (AJAX) |

---

## Database Models

### Client

| Field | Type | Notes |
|-------|------|-------|
| `id` | BigAutoField | Primary key |
| `name` | CharField(255) | Client name |
| `client_code` | CharField(6) | Auto-generated, unique (e.g. `ABC001`) |
| `created_at` | DateTimeField | Set on creation |
| `updated_at` | DateTimeField | Updated on every save |

**Client code generation rules:**

- 3-word name → first letter of each word → e.g. `Apple Banana Co` → `ABC`
- 2-word name → first letter + first 2 letters of second word → e.g. `John Smith` → `JSM`
- 1-word name → first 3 letters → e.g. `Apple` → `APP`
- Suffix: 3-digit auto-increment per prefix → `ABC001`, `ABC002`, …

### Contact

| Field | Type | Notes |
|-------|------|-------|
| `id` | BigAutoField | Primary key |
| `name` | CharField(255) | First name |
| `surname` | CharField(255) | Last name |
| `email` | EmailField | Unique |
| `clients` | ManyToManyField | Linked clients |
| `created_at` | DateTimeField | Set on creation |
| `updated_at` | DateTimeField | Updated on every save |

### Relationship

Clients and Contacts share a **many-to-many** relationship — one client can have many contacts and one contact can belong to many clients.

---


