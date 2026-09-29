from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.auth import (
    authenticate_user,
    create_access_token
)

from routes.students import router as student_router


# ==================================================
# FASTAPI APPLICATION
# ==================================================

app = FastAPI(
    title="Project Phoenix AI",
    description="Secure Student Management API with JWT Authentication",
    version="3.0"
)


# ==================================================
# INCLUDE STUDENT ROUTER
# ==================================================

app.include_router(student_router)


# ==================================================
# TOKEN RESPONSE MODEL
# ==================================================

class Token(BaseModel):
    access_token: str
    token_type: str


# ==================================================
# HOME ROUTE
# ==================================================

@app.get("/")
def home():
    return {
        "message": "Welcome to Project Phoenix AI",
        "status": "API is running",
        "security": "JWT authentication enabled"
    }


# ==================================================
# LOGIN ROUTE
# ==================================================

@app.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    authenticated = authenticate_user(
        form_data.username,
        form_data.password
    )

    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    access_token = create_access_token(
        form_data.username
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }