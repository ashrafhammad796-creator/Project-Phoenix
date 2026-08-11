from datetime import datetime, timedelta, timezone

import os
import secrets

import jwt
import psycopg2

from dotenv import load_dotenv

from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    status
)

from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)

from pydantic import BaseModel, Field


# ==================================================
# LOAD ENVIRONMENT VARIABLES
# ==================================================

load_dotenv()


# ==================================================
# FASTAPI APP
# ==================================================

app = FastAPI(
    title="Project Phoenix AI",
    description="Professional Student Management API with PostgreSQL",
    version="3.0"
)


# ==================================================
# ENVIRONMENT CONFIGURATION
# ==================================================

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
ADMIN_ROLE = os.getenv("ADMIN_ROLE", "admin")


if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is missing from .env")

if not ADMIN_USERNAME or not ADMIN_PASSWORD:
    raise RuntimeError("Admin credentials are missing from .env")


# ==================================================
# OAUTH2 SECURITY
# ==================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/token"
)


# ==================================================
# DATABASE DEPENDENCY
# ==================================================

def get_connection():

    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

    try:

        yield connection

    finally:

        connection.close()


# ==================================================
# STUDENT MODEL
# ==================================================

class Student(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    age: int = Field(
        ...,
        gt=0,
        le=100
    )

    course: str = Field(
        ...,
        min_length=2,
        max_length=100
    )


# ==================================================
# STUDENT RESPONSE MODEL
# ==================================================

class StudentResponse(BaseModel):

    id: int
    name: str
    age: int
    course: str


# ==================================================
# TOKEN RESPONSE MODEL
# ==================================================

class Token(BaseModel):

    access_token: str
    token_type: str


# ==================================================
# CURRENT USER MODEL
# ==================================================

class CurrentUser(BaseModel):

    username: str
    role: str


# ==================================================
# CREATE ACCESS TOKEN
# ==================================================

def create_access_token(
    username: str,
    role: str
):

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "role": role,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )

    return token


# ==================================================
# GET CURRENT USER
# ==================================================

def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:

        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )

        username = payload.get("sub")
        role = payload.get("role")

        if username is None or role is None:
            raise credentials_exception

        return CurrentUser(
            username=username,
            role=role
        )

    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )

    except jwt.InvalidTokenError:

        raise credentials_exception


# ==================================================
# ADMIN AUTHORIZATION
# ==================================================

def require_admin(
    current_user: CurrentUser = Depends(get_current_user)
):

    if current_user.role != "admin":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user


# ==================================================
# HOME
# ==================================================

@app.get("/")
def home():

    return {
        "message": "Welcome to Project Phoenix AI",
        "status": "API is running",
        "version": "3.0"
    }


# ==================================================
# LOGIN / TOKEN
# ==================================================

@app.post(
    "/token",
    response_model=Token
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    username_correct = secrets.compare_digest(
        form_data.username,
        ADMIN_USERNAME
    )

    password_correct = secrets.compare_digest(
        form_data.password,
        ADMIN_PASSWORD
    )

    if not username_correct or not password_correct:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    access_token = create_access_token(
        username=ADMIN_USERNAME,
        role=ADMIN_ROLE
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ==================================================
# CURRENT USER
# ==================================================

@app.get(
    "/me",
    response_model=CurrentUser
)
def get_me(
    current_user: CurrentUser = Depends(
        get_current_user
    )
):

    return current_user


# ==================================================
# GET ALL STUDENTS
# PUBLIC
# ==================================================

@app.get(
    "/students",
    response_model=list[StudentResponse]
)
def get_students(
    connection=Depends(get_connection)
):

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT id, name, age, course
            FROM students
            ORDER BY id
            """
        )

        rows = cursor.fetchall()

        students = []

        for row in rows:

            students.append({
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "course": row[3]
            })

        return students

    finally:

        cursor.close()


# ==================================================
# GET STUDENT BY ID
# PUBLIC
# ==================================================

@app.get(
    "/student/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    connection=Depends(get_connection)
):

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT id, name, age, course
            FROM students
            WHERE id = %s
            """,
            (student_id,)
        )

        student = cursor.fetchone()

        if student is None:

            raise HTTPException(
                status_code=404,
                detail="Student Not Found"
            )

        return {
            "id": student[0],
            "name": student[1],
            "age": student[2],
            "course": student[3]
        }

    finally:

        cursor.close()


# ==================================================
# CREATE STUDENT
# ADMIN ONLY
# ==================================================

@app.post(
    "/student",
    status_code=status.HTTP_201_CREATED,
    response_model=StudentResponse
)
def create_student(
    student: Student,
    current_user: CurrentUser = Depends(
        require_admin
    ),
    connection=Depends(get_connection)
):

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT id
            FROM students
            WHERE LOWER(name) = LOWER(%s)
            AND age = %s
            AND LOWER(course) = LOWER(%s)
            """,
            (
                student.name,
                student.age,
                student.course
            )
        )

        existing_student = cursor.fetchone()

        if existing_student:

            raise HTTPException(
                status_code=409,
                detail="Student already exists"
            )

        cursor.execute(
            """
            INSERT INTO students
            (name, age, course)
            VALUES (%s, %s, %s)
            RETURNING id, name, age, course
            """,
            (
                student.name,
                student.age,
                student.course
            )
        )

        new_student = cursor.fetchone()

        connection.commit()

        return {
            "id": new_student[0],
            "name": new_student[1],
            "age": new_student[2],
            "course": new_student[3]
        }

    except HTTPException:

        connection.rollback()

        raise

    except Exception as e:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database Error: {str(e)}"
        )

    finally:

        cursor.close()


# ==================================================
# UPDATE STUDENT
# ADMIN ONLY
# ==================================================

@app.put(
    "/student/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    student: Student,
    current_user: CurrentUser = Depends(
        require_admin
    ),
    connection=Depends(get_connection)
):

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            UPDATE students
            SET name = %s,
                age = %s,
                course = %s
            WHERE id = %s
            RETURNING id, name, age, course
            """,
            (
                student.name,
                student.age,
                student.course,
                student_id
            )
        )

        updated_student = cursor.fetchone()

        if updated_student is None:

            connection.rollback()

            raise HTTPException(
                status_code=404,
                detail="Student Not Found"
            )

        connection.commit()

        return {
            "id": updated_student[0],
            "name": updated_student[1],
            "age": updated_student[2],
            "course": updated_student[3]
        }

    except HTTPException:

        raise

    except Exception as e:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database Error: {str(e)}"
        )

    finally:

        cursor.close()


# ==================================================
# DELETE STUDENT
# ADMIN ONLY
# ==================================================

@app.delete(
    "/student/{student_id}"
)
def delete_student(
    student_id: int,
    current_user: CurrentUser = Depends(
        require_admin
    ),
    connection=Depends(get_connection)
):

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM students
            WHERE id = %s
            RETURNING id, name, age, course
            """,
            (student_id,)
        )

        deleted_student = cursor.fetchone()

        if deleted_student is None:

            connection.rollback()

            raise HTTPException(
                status_code=404,
                detail="Student Not Found"
            )

        connection.commit()

        return {
            "message": "Student Deleted Successfully",
            "student": {
                "id": deleted_student[0],
                "name": deleted_student[1],
                "age": deleted_student[2],
                "course": deleted_student[3]
            }
        }

    except HTTPException:

        raise

    except Exception as e:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database Error: {str(e)}"
        )

    finally:

        cursor.close()