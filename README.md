# User Service API

A FastAPI-based microservice for user management and authentication, part of the OwlBoard ecosystem. This service provides user registration, authentication, and management capabilities with a clean REST API interface.

## 🚀 Features

- **User Registration**: Create new user accounts with email validation
- **User Authentication**: Login system with password hashing using bcrypt
- **User Management**: CRUD operations for user data
- **Database Support**: SQLite for development, MySQL for production
- **Docker Support**: Containerized deployment with Docker Compose
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **CORS Support**: Configured for frontend integration
- **Health Checks**: Built-in health monitoring endpoints
- **Testing Suite**: Comprehensive test coverage with pytest

## 📋 Table of Contents

- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Docker Deployment](#docker-deployment)
- [Development](#development)
- [Contributing](#contributing)

## 🏗️ Architecture

The service follows a clean architecture pattern with the following structure:

```
User_Service/
├── app.py                 # FastAPI application entry point
├── src/
│   ├── config.py         # Configuration management
│   ├── database.py       # Database connection and session management
│   ├── models.py         # SQLAlchemy ORM models
│   ├── schemas.py        # Pydantic models for request/response validation
│   ├── security.py       # Authentication and security utilities
│   ├── crud.py           # Database operations
│   ├── logger_config.py  # Logging configuration
│   └── routes/
│       └── users_routes.py # User-related API endpoints
├── tests/                # Test suite
├── docker-compose.yml    # Docker composition for services
├── Dockerfile           # Container image definition
└── requirements.txt     # Python dependencies
```

### Key Components

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM)
- **Pydantic**: Data validation using Python type annotations
- **bcrypt**: Secure password hashing
- **pytest**: Testing framework
- **Docker**: Containerization platform

## 📋 Prerequisites

- Python 3.11+
- pip (Python package installer)
- Docker and Docker Compose (for containerized deployment)
- MySQL 8+ (for production deployment)

## 🔧 Installation

### Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/OwlBoard/User_Service.git
   cd User_Service
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:8000`

## ⚙️ Configuration

### Environment Variables

The service can be configured using the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./test.db` |

### Database Configuration

- **Development**: Uses SQLite database (`test.db`)
- **Production**: Uses MySQL database via Docker Compose

Example MySQL connection string:
```
DATABASE_URL=mysql+pymysql://user:password@localhost/user_db
```

## 📖 Usage

### Starting the Service

#### Development Mode
```bash
python app.py
```

#### Production Mode (Docker)
```bash
docker-compose up -d
```

### API Documentation

Once the service is running, you can access:

- **Interactive API Documentation (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative API Documentation (ReDoc)**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## 📚 API Endpoints

### Health Check Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint with service information |
| GET | `/health` | Health check endpoint |

### User Management Endpoints

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| POST | `/users/register` | Register a new user | Form data: `email`, `password`, `full_name` (optional) |
| POST | `/users/login` | Authenticate a user | Form data: `email`, `password` |
| GET | `/users/` | Get all users | None |

### Example Requests

#### Register a New User
```bash
curl -X POST "http://localhost:8000/users/register" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "email=user@example.com&password=secretpassword&full_name=John Doe"
```

#### User Login
```bash
curl -X POST "http://localhost:8000/users/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "email=user@example.com&password=secretpassword"
```

#### Get All Users
```bash
curl -X GET "http://localhost:8000/users/"
```

## 🧪 Testing

The project includes a comprehensive test suite using pytest.

### Running Tests

#### Run All Tests
```bash
pytest
```

#### Run Tests with Verbose Output
```bash
pytest -v
```

#### Run Tests with Coverage Report
```bash
pytest --cov=src
```

#### Run Specific Test File
```bash
pytest tests/test_users.py
```

#### Run Specific Test Function
```bash
pytest tests/test_users.py::test_user_registration
```

### Test Structure

The test suite includes:

- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test API endpoints and database interactions
- **Fixture Setup**: Automated test database setup and teardown

### Test Configuration

Tests use a separate SQLite database (`test.db`) to avoid interfering with development data. The test configuration is defined in:

- `pytest.ini`: pytest configuration
- `tests/conftest.py`: Test fixtures and setup
- `pyproject.toml`: Tool configuration for code formatting and linting

### Writing New Tests

When adding new functionality, ensure you:

1. Create corresponding test cases in the `tests/` directory
2. Use appropriate fixtures for database and client setup
3. Test both success and error scenarios
4. Include edge cases and validation testing

Example test structure:
```python
def test_user_registration(client, db_session):
    """Test user registration with valid data."""
    response = client.post(
        "/users/register",
        data={
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User"
        }
    )
    assert response.status_code == 200
    assert "registrado con éxito" in response.json()["message"]
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

The service includes a complete Docker Compose setup with MySQL database:

1. **Start all services**:
   ```bash
   docker-compose up -d
   ```

2. **View logs**:
   ```bash
   docker-compose logs -f user_service
   ```

3. **Stop services**:
   ```bash
   docker-compose down
   ```

4. **Rebuild and restart**:
   ```bash
   docker-compose up --build -d
   ```

### Service Access

- **API**: `http://localhost:5000`
- **MySQL Database**: `localhost:3306`

### Docker Services

- **user_service**: The FastAPI application
- **mysql_db**: MySQL 8 database server

## 💻 Development

### Code Style and Formatting

The project uses several tools to maintain code quality:

- **black**: Code formatter (line length: 88)
- **flake8**: Linting and style checking
- **pytest**: Testing framework

### Running Code Quality Tools

```bash
# Format code with black
black .

# Check code style with flake8
flake8 .

# Run all tests
pytest
```

### Development Workflow

1. Create a new branch for your feature
2. Make your changes
3. Run tests: `pytest`
4. Format code: `black .`
5. Check style: `flake8 .`
6. Commit your changes
7. Create a pull request

### Adding New Features

When adding new functionality:

1. Update the data models in `src/models.py` if needed
2. Add/update Pydantic schemas in `src/schemas.py`
3. Implement business logic in `src/crud.py`
4. Create API endpoints in `src/routes/`
5. Add comprehensive test coverage
6. Update this documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Pull Request Guidelines

- Ensure all tests pass
- Add tests for new functionality
- Update documentation as needed
- Follow the existing code style
- Provide a clear description of changes

## 📄 License

This project is licensed under the terms specified in the LICENSE file.

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Errors**:
   - Ensure MySQL is running (if using Docker Compose)
   - Check DATABASE_URL environment variable
   - Verify database credentials

2. **Port Already in Use**:
   - Change the port in `docker-compose.yml` or `app.py`
   - Check for other services using the same port

3. **Permission Errors**:
   - Ensure proper file permissions
   - Run Docker commands with appropriate privileges

4. **Test Failures**:
   - Check if test database is accessible
   - Ensure all dependencies are installed
   - Run tests with `-v` flag for detailed output

### Getting Help

- Check the [Issues](https://github.com/OwlBoard/User_Service/issues) page
- Review API documentation at `/docs` endpoint
- Examine logs using `docker-compose logs`

---

**Built with ❤️ by the OwlBoard Team**