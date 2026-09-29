from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.database import get_connection
from app.auth import get_current_user


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


class Student(BaseModel):
    name: str = Field(..., min_length=2)
    age: int = Field(..., gt=0, le=100)
    course: str = Field(..., min_length=2)


class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    course: str


@router.get("/", response_model=list[StudentResponse])
def get_students(
    current_user: str = Depends(get_current_user),
    connection=Depends(get_connection)
):
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT id, name, age, course
            FROM students
            ORDER BY id
        """)

        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "course": row[3]
            }
            for row in rows
        ]

    finally:
        cursor.close()


@router.post("/", status_code=201, response_model=StudentResponse)
def create_student(
    student: Student,
    current_user: str = Depends(get_current_user),
    connection=Depends(get_connection)
):
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO students (name, age, course)
            VALUES (%s, %s, %s)
            RETURNING id, name, age, course
        """, (
            student.name,
            student.age,
            student.course
        ))

        row = cursor.fetchone()
        connection.commit()

        return {
            "id": row[0],
            "name": row[1],
            "age": row[2],
            "course": row[3]
        }

    except Exception as e:
        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database Error: {str(e)}"
        )

    finally:
        cursor.close()


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student: Student,
    current_user: str = Depends(get_current_user),
    connection=Depends(get_connection)
):
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE students
            SET name = %s,
                age = %s,
                course = %s
            WHERE id = %s
            RETURNING id, name, age, course
        """, (
            student.name,
            student.age,
            student.course,
            student_id
        ))

        row = cursor.fetchone()

        if row is None:
            connection.rollback()

            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        connection.commit()

        return {
            "id": row[0],
            "name": row[1],
            "age": row[2],
            "course": row[3]
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


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    current_user: str = Depends(get_current_user),
    connection=Depends(get_connection)
):
    cursor = connection.cursor()

    try:
        cursor.execute("""
            DELETE FROM students
            WHERE id = %s
            RETURNING id, name, age, course
        """, (student_id,))

        row = cursor.fetchone()

        if row is None:
            connection.rollback()

            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        connection.commit()

        return {
            "message": "Student deleted successfully",
            "student": {
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "course": row[3]
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