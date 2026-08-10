from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
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
    description="Student Management API with PostgreSQL",
    version="2.1"
)

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
# STUDENT MODEL
# ==================================================

class Student(BaseModel):

    name: str = Field(..., min_length=2)
    age: int = Field(..., gt=0, le=100)
    course: str = Field(..., min_length=2)

# ==================================================
# STUDENT RESPONSE MODEL
# ==================================================

class StudentResponse(BaseModel):

    id: int
    name: str
    age: int
    course: str

# ==================================================
# HOME
# ==================================================

@app.get("/")
def home():

    return {
        "message": "Welcome to Project Phoenix AI",
        "status": "API is running"
    }

# ==================================================
# GET ALL STUDENTS
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
# ==================================================

@app.post(
    "/student",
    status_code=201,
    response_model=StudentResponse
)
def create_student(
    student: Student,
    connection=Depends(get_connection)
):

    cursor = connection.cursor()

    try:

        query = """
        INSERT INTO students (name, age, course)
        VALUES (%s, %s, %s)
        RETURNING id, name, age, course
        """

        cursor.execute(
            query,
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
# ==================================================

@app.put(
    "/student/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    student: Student,
    connection=Depends(get_connection)
):

    cursor = connection.cursor()

    try:

        query = """
        UPDATE students
        SET name = %s,
            age = %s,
            course = %s
        WHERE id = %s
        RETURNING id, name, age, course
        """

        cursor.execute(
            query,
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
# ==================================================

@app.delete(
    "/student/{student_id}"
)
def delete_student(
    student_id: int,
    connection=Depends(get_connection)
):

    cursor = connection.cursor()

    try:

        query = """
        DELETE FROM students
        WHERE id = %s
        RETURNING id, name, age, course
        """

        cursor.execute(
            query,
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