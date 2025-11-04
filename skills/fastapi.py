"""FastAPI scaffolding skill."""

from typing import Dict, Any, List


def get_fastapi_skill() -> Dict[str, Any]:
    """Get FastAPI scaffolding skill definition."""
    return {
        "name": "fastapi",
        "description": "Scaffold a FastAPI application with JWT auth, PostgreSQL, and tests",
        "files": [
            {
                "path": "main.py",
                "content": """from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from typing import Optional
import os

app = FastAPI(title="FastAPI App", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

# User model
class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    username: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return {"username": username}

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/auth/register", response_model=UserResponse)
async def register(user: User):
    # In production, hash password and store in database
    return UserResponse(username=user.username)

@app.post("/auth/login", response_model=Token)
async def login(user: User):
    # In production, verify against database
    if user.username == "admin" and user.password == "admin":
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password"
    )

@app.get("/auth/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return UserResponse(username=current_user["username"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
            },
            {
                "path": "requirements.txt",
                "content": """fastapi==0.104.1
uvicorn[standard]==0.24.0
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
pydantic==2.5.0
pydantic-settings==2.1.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
"""
            },
            {
                "path": "docker-compose.yml",
                "content": """version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: fastapi_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
"""
            },
            {
                "path": "test_main.py",
                "content": """import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_register():
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_login():
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_protected_endpoint():
    # First login to get token
    login_response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin"}
    )
    token = login_response.json()["access_token"]
    
    # Use token to access protected endpoint
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "admin"
"""
            },
            {
                "path": ".gitignore",
                "content": """__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv
*.egg-info/
dist/
build/
.env
.venv
"""
            },
            {
                "path": "README.md",
                "content": """# FastAPI Application

A FastAPI application with JWT authentication and PostgreSQL.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start PostgreSQL:
```bash
docker-compose up -d
```

3. Run the application:
```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload
```

4. Run tests:
```bash
pytest
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user (requires authentication)

## Authentication

Use the JWT token in the Authorization header:
```
Authorization: Bearer <token>
```
"""
            }
        ]
    }

