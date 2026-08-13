from datetime import datetime, timedelta, timezone
import os
import secrets

import jwt
import psycopg2
import requests

from dotenv import load_dotenv

from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    status,
)
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)

from pydantic import BaseModel, Field


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Project Phoenix AI",
    description="Professional Student Management API with PostgreSQL, JWT and Role-Based Access",
    version="4.0",
)


# ============================================================
# ENVIRONMENT CONFIGURATION
# ============================================================

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


# ============================================================
# OAUTH2
# ============================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/token"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
    )

    try:
        yield connection

    finally:
        connection.close()


# ============================================================
# MODELS
# ============================================================

class Student(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    age: int = Field(
        ...,
        ge=16,
        le=100,
    )

    course: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )


class StudentResponse(BaseModel):

    id: int
    name: str
    age: int
    course: str


class Token(BaseModel):

    access_token: str
    token_type: str


class CurrentUser(BaseModel):

    username: str
    role: str


class TeacherCreate(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    email: str | None = None


class TeacherResponse(BaseModel):

    id: int
    name: str
    email: str | None = None


class CourseCreate(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    teacher_id: int | None = None


class CourseResponse(BaseModel):

    id: int
    name: str
    teacher_id: int | None = None


class RoleUpdate(BaseModel):

    role: str = Field(
        ...,
        min_length=4,
        max_length=20,
    )


# ============================================================
# CREATE JWT ACCESS TOKEN
# ============================================================

def create_access_token(
    username: str,
    role: str,
):

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "role": role,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


# ============================================================
# GET CURRENT USER
# ============================================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )

    try:

        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )

        username = payload.get("sub")
        role = payload.get("role")

        if username is None or role is None:
            raise credentials_exception

        return CurrentUser(
            username=username,
            role=role,
        )

    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    except jwt.InvalidTokenError:

        raise credentials_exception


# ============================================================
# ROLE AUTHORIZATION
# ============================================================

def require_admin(
    current_user: CurrentUser = Depends(
        get_current_user
    ),
):

    if current_user.role != "admin":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return current_user


def require_teacher_or_admin(
    current_user: CurrentUser = Depends(
        get_current_user
    ),
):

    if current_user.role not in ["admin", "teacher"]:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Teacher or Admin access required",
        )

    return current_user


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Welcome to Project Phoenix AI",
        "status": "API is running",
        "version": "4.0",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "Project Phoenix AI",
        "database": "PostgreSQL",
    }


# ============================================================
# LOGIN
# ============================================================

@app.post(
    "/token",
    response_model=Token,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):

    username_correct = secrets.compare_digest(
        form_data.username,
        ADMIN_USERNAME,
    )

    password_correct = secrets.compare_digest(
        form_data.password,
        ADMIN_PASSWORD,
    )

    if not username_correct or not password_correct:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    access_token = create_access_token(
        username=ADMIN_USERNAME,
        role=ADMIN_ROLE,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# ============================================================
# CURRENT USER
# ============================================================

@app.get(
    "/me",
    response_model=CurrentUser,
)
def get_me(
    current_user: CurrentUser = Depends(
        get_current_user
    ),
):

    return current_user


# ============================================================
# GET ALL STUDENTS
# PUBLIC
# ============================================================

@app.get(
    "/students",
    response_model=list[StudentResponse],
)
def get_students(
    connection=Depends(get_connection),
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

        return [
            {
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "course": row[3],
            }
            for row in rows
        ]

    finally:

        cursor.close()


# ============================================================
# GET STUDENT BY ID
# PUBLIC
# ============================================================

@app.get(
    "/student/{student_id}",
    response_model=StudentResponse,
)
def get_student(
    student_id: int,
    connection=Depends(get_connection),
):

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT id, name, age, course
            FROM students
            WHERE id = %s
            """,
            (student_id,),
        )

        student = cursor.fetchone()

        if student is None:

            raise HTTPException(
                status_code=404,
                detail="Student Not Found",
            )

        return {
            "id": student[0],
            "name": student[1],
            "age": student[2],
            "course": student[3],
        }

    finally:

        cursor.close()


# ============================================================
# CREATE STUDENT
# ADMIN ONLY
# ============================================================

@app.post(
    "/student",
    status_code=status.HTTP_201_CREATED,
    response_model=StudentResponse,
)
def create_student(
    student: Student,
    current_user: CurrentUser = Depends(
        require_admin
    ),
    connection=Depends(get_connection),
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
                student.course,
            ),
        )

        if cursor.fetchone():

            raise HTTPException(
                status_code=409,
                detail="Student already exists",
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
                student.course,
            ),
        )

        new_student = cursor.fetchone()

        connection.commit()

        return {
            "id": new_student[0],
            "name": new_student[1],
            "age": new_student[2],
            "course": new_student[3],
        }

    except HTTPException:

        connection.rollback()
        raise

    except Exception as e:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database Error: {str(e)}",
        )

    finally:

        cursor.close()


# ============================================================
# UPDATE STUDENT
# ADMIN ONLY
# ============================================================

@app.put(
    "/student/{student_id}",
    response_model=StudentResponse,
)
def update_student(
    student_id: int,
    student: Student,
    current_user: CurrentUser = Depends(
        require_admin
    ),
    connection=Depends(get_connection),
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
                student_id,
            ),
        )

        updated_student = cursor.fetchone()

        if updated_student is None:

            connection.rollback()

            raise HTTPException(
                status_code=404,
                detail="Student Not Found",
            )

        connection.commit()

        return {
            "id": updated_student[0],
            "name": updated_student[1],
            "age": updated_student[2],
            "course": updated_student[3],
        }

    except HTTPException:

        raise

    except Exception as e:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database Error: {str(e)}",
        )

    finally:

        cursor.close()


# ============================================================
# DELETE STUDENT
# ADMIN ONLY
# ============================================================

@app.delete(
    "/student/{student_id}"
)
def delete_student(
    student_id: int,
    current_user: CurrentUser = Depends(
        require_admin
    ),
    connection=Depends(get_connection),
):

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM students
            WHERE id = %s
            RETURNING id, name, age, course
            """,
            (student_id,),
        )

        deleted_student = cursor.fetchone()

        if deleted_student is None:

            connection.rollback()

            raise HTTPException(
                status_code=404,
                detail="Student Not Found",
            )

        connection.commit()

        return {
            "message": "Student Deleted Successfully",
            "student": {
                "id": deleted_student[0],
                "name": deleted_student[1],
                "age": deleted_student[2],
                "course": deleted_student[3],
            },
        }

    except HTTPException:

        raise

    except Exception as e:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database Error: {str(e)}",
        )

    finally:

        cursor.close()


# ============================================================
# CREATE TEACHER
# ADMIN ONLY
# ============================================================

@app.post(
    "/teachers",
    response_model=TeacherResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_teacher(
    teacher: TeacherCreate,
    current_user: CurrentUser = Depends(
        require_admin
    ),
    connection=Depends(get_connection),
):

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO teachers (name, email)
            VALUES (%s, %s)
            RETURNING id, name, email
            """,
            (
                teacher.name,
                teacher.email,
            ),
        )

        new_teacher = cursor.fetchone()

        connection.commit()

        return {
            "id": new_teacher[0],
            "name": new_teacher[1],
            "email": new_teacher[2],
        }

    except psycopg2.errors.UniqueViolation:

        connection.rollback()

        raise HTTPException(
            status_code=409,
            detail="Teacher email already exists",
        )

    except Exception as e:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database Error: {str(e)}",
        )

    finally:

        cursor.close()


# ============================================================
# GET TEACHERS
# ADMIN / TEACHER
# ============================================================

@app.get(
    "/teachers",
    response_model=list[TeacherResponse],
)
def get_teachers(
    current_user: CurrentUser = Depends(
        require_teacher_or_admin
    ),
    connection=Depends(get_connection),
):

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT id, name, email
            FROM teachers
            ORDER BY id
            """
        )

        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "name": row[1],
                "email": row[2],
            }
            for row in rows
        ]

    finally:

        cursor.close()


# ============================================================
# CREATE COURSE
# ADMIN ONLY
# ============================================================

@app.post(
    "/courses",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_course(
    course: CourseCreate,
    current_user: CurrentUser = Depends(
        require_admin
    ),
    connection=Depends(get_connection),
):

    cursor = connection.cursor()

    try:

        if course.teacher_id is not None:

            cursor.execute(
                """
                SELECT id
                FROM teachers
                WHERE id = %s
                """,
                (course.teacher_id,),
            )

            if cursor.fetchone() is None:

                raise HTTPException(
                    status_code=404,
                    detail="Teacher Not Found",
                )

        cursor.execute(
            """
            INSERT INTO courses
            (name, teacher_id)
            VALUES (%s, %s)
            RETURNING id, name, teacher_id
            """,
            (
                course.name,
                course.teacher_id,
            ),
        )

        new_course = cursor.fetchone()

        connection.commit()

        return {
            "id": new_course[0],
            "name": new_course[1],
            "teacher_id": new_course[2],
        }

    except HTTPException:

        connection.rollback()
        raise

    except psycopg2.errors.UniqueViolation:

        connection.rollback()

        raise HTTPException(
            status_code=409,
            detail="Course already exists",
        )

    except Exception as e:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database Error: {str(e)}",
        )

    finally:

        cursor.close()


# ============================================================
# GET COURSES
# ADMIN / TEACHER
# ============================================================

@app.get(
    "/courses",
    response_model=list[CourseResponse],
)
def get_courses(
    current_user: CurrentUser = Depends(
        require_teacher_or_admin
    ),
    connection=Depends(get_connection),
):

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT id, name, teacher_id
            FROM courses
            ORDER BY id
            """
        )

        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "name": row[1],
                "teacher_id": row[2],
            }
            for row in rows
        ]

    finally:

        cursor.close()


# ============================================================
# GET EXTERNAL API DATA
# DEMONSTRATION OF API INTEGRATION
# ============================================================

@app.get(
    "/external-api"
)
def external_api():

    api_url = "https://jsonplaceholder.typicode.com/posts/1"

    try:

        response = requests.get(
            api_url,
            timeout=10,
        )

        response.raise_for_status()

        return {
            "source": "JSONPlaceholder",
            "status_code": response.status_code,
            "data": response.json(),
        }

    except requests.RequestException as e:

        raise HTTPException(
            status_code=502,
            detail=f"External API Error: {str(e)}",
        )


# ============================================================
# STUDENT REPORT DATA
# DAY 6 DOCUMENT AUTOMATION FOUNDATION
# ============================================================

@app.get(
    "/student/{student_id}/report-data"
)
def student_report_data(
    student_id: int,
    current_user: CurrentUser = Depends(
        require_teacher_or_admin
    ),
    connection=Depends(get_connection),
):

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT id, name, age, course
            FROM students
            WHERE id = %s
            """,
            (student_id,),
        )

        student = cursor.fetchone()

        if student is None:

            raise HTTPException(
                status_code=404,
                detail="Student Not Found",
            )

        return {
            "student": {
                "id": student[0],
                "name": student[1],
                "age": student[2],
                "course": student[3],
            },
            "report_status": "Ready for document generation",
        }

    finally:

        cursor.close()


# ============================================================
# ADMIN USER ROLE VIEW
# ============================================================

@app.get(
    "/admin/status"
)
def admin_status(
    current_user: CurrentUser = Depends(
        require_admin
    ),
):

    return {
        "message": "Admin access verified",
        "username": current_user.username,
        "role": current_user.role,
    }