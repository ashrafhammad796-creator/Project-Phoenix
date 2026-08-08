import psycopg2

# Database connection
connection = psycopg2.connect(
    host="localhost",
    database="phoenix_db",
    user="postgres",
    password="1234",
    port="5432"
)

# Create cursor
cursor = connection.cursor()

# Take student data
name = input("Enter student name: ")
age = int(input("Enter student age: "))
course = input("Enter student course: ")

# Insert student
query = """
INSERT INTO students (name, age, course)
VALUES (%s, %s, %s)
"""

cursor.execute(query, (name, age, course))

# Save changes
connection.commit()

print("Student added successfully!")

# Get all students
cursor.execute("SELECT * FROM students")

students = cursor.fetchall()

print("\nAll Students:")

for student in students:
    print(student)

# Close connection
cursor.close()
connection.close()