# Client Contact Manager (CCM)

A Django web application for managing clients and their associated contacts. Supports full CRUD operations for both entities, with a many-to-many relationship between them managed through a tabbed detail interface and AJAX-powered linking/unlinking.

---

## Features

- **Clients** — Create, view, edit, and delete clients. Each client receives an auto-generated unique 6-character code (e.g. `ABC001`) derived from their name.
- **Contacts** — Create, view, edit, and delete contacts with a unique email address.
- **Many-to-Many Linking** — Link/unlink contacts to clients (and vice versa) via a live AJAX interface without page reloads.
- **Tabbed Detail Pages** — Client and contact detail pages use a tabbed UI (General / Contacts or Clients).
- **PostgreSQL** — Uses PostgreSQL as the database backend.
- **Dockerised** — Full Docker Compose setup with a PostgreSQL service and Django web service.

---

## Project Structure

```
client_contact_app/
├── ccm_project/          # Django project settings, URLs, WSGI/ASGI
├── clients/              # Clients app (models, views, forms, URLs)
├── contacts/             # Contacts app (models, views, forms, URLs)
├── templates/            # HTML templates (base, clients/, contacts/)
├── static/               # Static assets (CSS)
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env                  # Environment variables (not committed to git)
```

---

## URL Reference

| URL | Description |
|-----|-------------|
| `/clients/` | List all clients |
| `/clients/create/` | Create a new client |
| `/clients/<pk>/` | View / edit a client |
| `/clients/<pk>/delete/` | Delete a client |
| `/clients/<pk>/link-contact/` | AJAX — link a contact to a client |
| `/clients/<pk>/unlink-contact/<contact_id>/` | AJAX — unlink a contact |
| `/clients/<pk>/available-contacts/` | AJAX — list linkable contacts |
| `/contacts/` | List all contacts |
| `/contacts/create/` | Create a new contact |
| `/contacts/<pk>/` | View / edit a contact |
| `/contacts/<pk>/delete/` | Delete a contact |
| `/contacts/<pk>/link-client/` | AJAX — link a client to a contact |
| `/contacts/<pk>/unlink-client/<client_id>/` | AJAX — unlink a client |
| `/contacts/<pk>/available-clients/` | AJAX — list linkable clients |
| `/admin/` | Django admin panel |

---

## Environment Variables (`.env`)

Create a `.env` file in the project root. This file is used by both Docker Compose and the Django app.

```env
# PostgreSQL database settings
DB_NAME=ccm_db
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=db          # Use 'db' for Docker, 'localhost' for local dev
DB_PORT=5432
```



---

## Running with Docker

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed and running
- [Docker Compose](https://docs.docker.com/compose/install/) (included with Docker Desktop)

### Steps

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd client_contact_app
```

**2. Create the `.env` file**
```bash
cp .env.example .env   # or create it manually (see above)
```
Make sure `DB_HOST=db` (the Docker Compose service name for PostgreSQL).

**3. Build and start the containers**
```bash
docker compose up --build
```

This will:
- Pull the `postgres:16-alpine` image and start the database
- Build the Django image from the `Dockerfile`
- Wait for the database to be healthy
- Run `python manage.py migrate` automatically
- Start the Django dev server on port `8000`

**4. Open the app**

Visit [http://localhost:8000/clients/](http://localhost:8000/clients/)

**5. (Optional) Create a Django superuser**
```bash
docker compose exec web python manage.py createsuperuser
```

### Useful Docker commands

```bash
# Start in background (detached)
docker compose up -d

# View logs
docker compose logs -f web

# Stop containers
docker compose down

# Stop and remove volumes (wipes the database)
docker compose down -v

# Run any manage.py command inside the container
docker compose exec web python manage.py <command>
```

---

## Running Locally (without Docker)

### Prerequisites
- Python 3.12+
- PostgreSQL installed and running locally
- `pip` and `venv`

### Steps

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd client_contact_app
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create a PostgreSQL database**
```bash
psql -U postgres
```
```sql
CREATE DATABASE ccm_db;
\q
```

**5. Create the `.env` file**
```env
DB_NAME=ccm_db
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
```
> Note: `DB_HOST` must be `localhost` for local development (not `db`).

**6. Apply migrations**
```bash
python manage.py migrate
```

**7. (Optional) Create a superuser**
```bash
python manage.py createsuperuser
```

**8. Run the development server**
```bash
python manage.py runserver
```

Visit [http://localhost:8000/clients/](http://localhost:8000/clients/)

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django 6.0.3 |
| Database | PostgreSQL 16 |
| DB Driver | psycopg2-binary |
| Frontend | Tailwind CSS (CDN), Vanilla JS |
| Containerisation | Docker, Docker Compose |
| Python | 3.12 |
