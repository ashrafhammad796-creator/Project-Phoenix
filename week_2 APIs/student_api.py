from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Project Phoenix AI",
    description="Week 2 Final Project - Student API",
    version="1.0"
)

# -------------------------
# Student Model
# -------------------------
class Student(BaseModel):
    name: str
    age: int
    course: str


# Fake Database
students = []


# -------------------------
# Home Endpoint
# -------------------------
@app.get("/")
def home():
    return {
        "message": "Welcome to Project Phoenix AI"
    }


# -------------------------
# About Endpoint
# -------------------------
@app.get("/about")
def about():
    return {
        "Developer": "Hammad",
        "Project": "Project Phoenix AI",
        "Version": "1.0"
    }


# -------------------------
# Create Student
# -------------------------
@app.post("/student")
def create_student(student: Student):
    students.append(student)
    return {
        "message": "Student Added Successfully",
        "student": student
    }


# -------------------------
# Get All Students
# -------------------------
@app.get("/students")
def get_students():
    return students


# -------------------------
# Get Student by Name
# -------------------------
@app.get("/student/{name}")
def get_student(name: str):

    for student in students:
        if student.name.lower() == name.lower():
            return student

    return {
        "message": "Student Not Found"
    }


# -------------------------
# Search Student
# -------------------------
@app.get("/search")
def search_student(course: str):

    result = []

    for student in students:
        if student.course.lower() == course.lower():
            result.append(student)

    return result


# -------------------------
# Update Student
# -------------------------
@app.put("/student/{name}")
def update_student(name: str, updated_student: Student):

    for index, student in enumerate(students):

        if student.name.lower() == name.lower():

            students[index] = updated_student

            return {
                "message": "Student Updated Successfully",
                "student": updated_student
            }

    return {
        "message": "Student Not Found"
    }


# -------------------------
# Delete Student
# -------------------------
@app.delete("/student/{name}")
def delete_student(name: str):

    for index, student in enumerate(students):

        if student.name.lower() == name.lower():

            deleted = students.pop(index)

            return {
                "message": "Student Deleted Successfully",
                "student": deleted
            }

    return {
        "message": "Student Not Found"}