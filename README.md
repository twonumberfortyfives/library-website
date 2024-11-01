# DRF Library Project

Welcome to the DRF Library Project! This project is a comprehensive library management system where users can borrow books, manage their borrowed items, and make payments using Stripe. The system is implemented with Django Rest Framework, featuring JWT authorization for secure access, and is containerized using Docker Compose for ease of deployment. Payment handling is managed through Stripe, with asynchronous tasks handled by Celery.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [JWT Authorization](#jwt-authorization)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Overview

The DRF Library Project allows users to:
- Browse and borrow books.
- View the current inventory and borrowing status.
- Manage payments for borrowed books using Stripe.
- Sync book availability and payment status in real-time using Celery.
- Securely access and manage accounts using JWT authorization.

All services are containerized with Docker Compose for seamless setup and deployment.

## Features

- **Book Borrowing System:** Users can browse available books and borrow them.
- **Inventory Management:** Real-time synchronization of book availability.
- **Payment Integration:** Secure payments through Stripe.
- **Asynchronous Task Handling:** Celery is used for handling background tasks.
- **JWT Authorization:** Secure API access using JWT tokens.
- **Containerized Deployment:** Easy setup and deployment using Docker Compose.

## Tech Stack

- **Backend:** Django, Django Rest Framework (DRF)
- **Database:** PostgreSQL
- **Payment Processing:** Stripe
- **Task Queue:** Celery
- **Messaging:** Redis (as a broker for Celery)
- **Authentication:** JWT (JSON Web Token)
- **Containerization:** Docker, Docker Compose

## Prerequisites

Ensure you have the following installed on your machine:

- Docker
- Docker Compose
- Git

## Setup Instructions

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/drf-library.git
    cd drf-library
    ```

2. **Create and configure environment variables:**
    Copy the `.env.example` to `.env` and update the configuration with your details.
    ```bash
    cp .env.example .env
    ```

3. **Start the services:**
    ```bash
    docker-compose up --build
    ```

4. **Apply database migrations:**
    ```bash
    docker-compose exec web python manage.py migrate
    ```

5. **Create a superuser:**
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

6. **Access the application:**
    - The API will be available at: `http://localhost:8000/api/`
    - The admin panel will be available at: `http://localhost:8000/admin/`

## Environment Variables

The project requires the following environment variables:

- **`SECRET_KEY`**: Django secret key.
- **`DEBUG`**: Set to `False` for production.
- **`DATABASE_URL`**: URL for the PostgreSQL database.
- **`STRIPE_SECRET_KEY`**: Your Stripe secret key.
- **`STRIPE_PUBLISHABLE_KEY`**: Your Stripe publishable key.
- **`REDIS_URL`**: URL for the Redis instance (used by Celery).
- **`JWT_SECRET_KEY`**: Secret key for encoding and decoding JWT tokens.

Example `.env` file:

```env
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://user:password@db:5432/library
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
REDIS_URL=redis://redis:6379/0
JWT_SECRET_KEY=your_jwt_secret_key
