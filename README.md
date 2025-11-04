# Illuminati project - Backend Service

## Overview

This repository contains the backend part of the Illuminati Project.
The backend is implemented with Django REST Framework and runs in a Docker container together with a MariaDB database.
Its main responsibilities include:
-Managing users, posts, and voting flows.
-Handling authentication via JWT (access & refresh tokens).
-Forwarding and receiving data from external services.

## Requirements

-Django==5.1
-djangorestframework==3.15.2
-djangorestframework-simplejwt==5.4.0
-mysqlclient==2.2.4
-Pillow==11.0.0
-django-cors-headers==4.4.0
-pytest-django==4.9.0
-coverage==7.6.2
-pytest-cov==5.0.0
-requests==2.32.3

## Installation and Setup

1. **Clone the Repository:**

```bash
git clone https://github.com/Code-Illuminators/Illuminators_backend.git
cd backend_service
```

2. **Create a .env file:**
   Create a .env file in the project root with the following variables:

```bash
MARIADB_HOST={{ mariadb_host }}
MARIADB_DATABASE={{ mariadb_database }}
MARIADB_PORT_NUMBER={{ mariadb_port }}
MARIADB_ROOT_PASSWORD={{ mariadb_root_password }}
DB_EXTERNAL_PORT={{ mariadb_external_port }}
BACKEND_PORT={{ backend_port }}
BACKEND_EXTERNAL_PORT={{ backend_external_port }}
CORS_ALLOWED_ORIGIN={{ cors_allowed_origin }}
DJANGO_SECRET_KEY={{ django_secret_key }}
MARIADB_USER={{ mariadb_user }}
INTERNAL_SERVICE_TOKEN={{ internal_service_token }}
VOTING_SERVICE_URL={{voting_service_url}}
```

3. **Build image using Dockerfile and run using Docker Compose:**

```bash
docker build -t illuminati-backend .
docker-compose up
```

This will launch:
-MariaDB database (mariadb:11)
-Django backend (python:3.13-slim)

## Testing and Coverage

Test coverage is automatically analyzed in SonarQube Cloud through workflow integration.
To run tests locally:

```bash
pytest --cov=. --cov-report=xml
```

This will generate a coverage report:

```bash
coverage.xml
```
