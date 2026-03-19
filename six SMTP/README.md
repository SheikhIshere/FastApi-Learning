# FastAPI SMTP Service

A professional FastAPI application with user authentication and SMTP email functionality.

## Features

- User registration and authentication with JWT tokens
- SMTP email sending with logging
- RESTful API with proper documentation
- SQLAlchemy ORM with database models
- Pydantic schemas for data validation
- CORS support
- Environment-based configuration

## Project Structure

```
.
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── api.py          # API router aggregation
│   │       ├── auth.py         # Authentication endpoints
│   │       ├── users.py        # User endpoints
│   │       └── emails.py       # Email endpoints
│   ├── core/
│   │   ├── config.py          # Configuration settings
│   │   ├── security.py        # Security utilities
│   │   └── email.py           # SMTP service
│   ├── crud/
│   │   └── user.py            # Database operations
│   ├── db/
│   │   └── database.py        # Database connection
│   ├── models/
│   │   └── user.py            # SQLAlchemy models
│   ├── schemas/
│   │   └── user.py            # Pydantic schemas
│   └── main.py                # FastAPI application
├── tests/                     # Test files
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy environment variables:
```bash
cp .env.example .env
```

4. Update `.env` with your configuration:
- Set your `SECRET_KEY`
- Configure SMTP settings
- Set database URL

## Running the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/token` - Login and get access token

### Users
- `GET /api/v1/users/me` - Get current user info
- `GET /api/v1/users` - List all users (requires authentication)

### Emails
- `POST /api/v1/emails/send` - Send an email (requires authentication)
- `GET /api/v1/emails/logs` - Get email logs (requires authentication)

## Usage Examples

### Register a user
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "username": "testuser",
       "password": "securepassword"
     }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=testuser&password=securepassword"
```

### Send an email
```bash
curl -X POST "http://localhost:8000/api/v1/emails/send" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "to_email": "recipient@example.com",
       "subject": "Test Email",
       "body": "This is a test email from FastAPI SMTP service."
     }'
```

## Development

The application follows FastAPI best practices:
- Separation of concerns with modular structure
- Type hints throughout
- Pydantic models for validation
- SQLAlchemy for database operations
- JWT authentication
- Proper error handling

## License

MIT License
