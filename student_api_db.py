from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import psycopg2


# ==================================================
# FASTAPI APP
# ==================================================

app = FastAPI(
    title="Project Phoenix AI",
    description="Student Management API with PostgreSQL",
    version="2.0"
)


# ==================================================
# DATABASE CONNECTION
# ==================================================

def get_connection():

    return psycopg2.connect(
        host="localhost",
        database="phoenix_db",
        user="postgres",
        password="1234",
        port="5432"
    )


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
def get_students():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

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

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Database Error: {str(e)}"
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==================================================
# GET STUDENT BY ID
# ==================================================

@app.get(
    "/student/{student_id}",
    response_model=StudentResponse
)
def get_student(student_id: int):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

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

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Database Error: {str(e)}"
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==================================================
# CREATE STUDENT
# ==================================================

@app.post(
    "/student",
    status_code=201,
    response_model=StudentResponse
)
def create_student(student: Student):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

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

        return new_student

    except Exception as e:

        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database Error: {str(e)}"
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==================================================
# UPDATE STUDENT
# ==================================================

@app.put(
    "/student/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    student: Student
):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

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

        return updated_student

    except HTTPException:

        raise

    except Exception as e:

        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database Error: {str(e)}"
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==================================================
# DELETE STUDENT
# ==================================================

@app.delete(
    "/student/{student_id}"
)
def delete_student(student_id: int):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

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
            "student": deleted_student
        }

    except HTTPException:

        raise

    except Exception as e:

        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database Error: {str(e)}"
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()