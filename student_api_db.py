from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
import psycopg2
from dotenv import load_dotenv
import os


# ==================================================
# LOAD ENVIRONMENT VARIABLES
# ==================================================

load_dotenv()


# ==================================================
# FASTAPI APP
# ==================================================

app = FastAPI(
    title="Project Phoenix AI",
    description="Secure Student Management API with JWT Authentication",
    version="3.0"
)


# ==================================================
# JWT CONFIGURATION
# ==================================================

SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "development-secret-key"
)

ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256"
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ==================================================
# PASSWORD HASHING
# ==================================================

password_hash = PasswordHash.recommended()


# ==================================================
# OAUTH2
# ==================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/token"
)


# ==================================================
# DEMO USER
# ==================================================

DEMO_USERNAME = "hammad"

DEMO_PASSWORD_HASH = password_hash.hash("1234")


# ==================================================
# DATABASE CONNECTION
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
# VERIFY USER
# ==================================================

def authenticate_user(
    username: str,
    password: str
):

    if username != DEMO_USERNAME:
        return False

    return password_hash.verify(
        password,
        DEMO_PASSWORD_HASH
    )


# ==================================================
# CREATE JWT TOKEN
# ==================================================

def create_access_token(
    username: str
):

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
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
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

        if username != DEMO_USERNAME:
            raise credentials_exception

        return username

    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    except jwt.InvalidTokenError:

        raise credentials_exception


# ==================================================
# STUDENT MODEL
# ==================================================

class Student(BaseModel):

    name: str = Field(
        ...,
        min_length=2
    )

    age: int = Field(
        ...,
        gt=0,
        le=100
    )

    course: str = Field(
        ...,
        min_length=2
    )


# ==================================================
# STUDENT RESPONSE
# ==================================================

class StudentResponse(BaseModel):

    id: int
    name: str
    age: int
    course: str


# ==================================================
# TOKEN RESPONSE
# ==================================================

class Token(BaseModel):

    access_token: str
    token_type: str


# ==================================================
# HOME
# ==================================================

@app.get("/")
def home():

    return {
        "message": "Welcome to Project Phoenix AI",
        "status": "API is running",
        "security": "JWT authentication enabled"
    }


# ==================================================
# LOGIN
# ==================================================

@app.post(
    "/token",
    response_model=Token
)
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


# ==================================================
# GET ALL STUDENTS
# PROTECTED
# ==================================================

@app.get(
    "/students",
    response_model=list[StudentResponse]
)
def get_students(
    current_user: str = Depends(get_current_user),
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
# PROTECTED
# ==================================================

@app.get(
    "/student/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    current_user: str = Depends(get_current_user),
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
# PROTECTED
# ==================================================

@app.post(
    "/student",
    status_code=201,
    response_model=StudentResponse
)
def create_student(
    student: Student,
    current_user: str = Depends(get_current_user),
    connection=Depends(get_connection)
):

    cursor = connection.cursor()

    try:

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
# PROTECTED
# ==================================================

@app.put(
    "/student/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    student: Student,
    current_user: str = Depends(get_current_user),
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
# PROTECTED
# ==================================================

@app.delete(
    "/student/{student_id}"
)
def delete_student(
    student_id: int,
    current_user: str = Depends(get_current_user),
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