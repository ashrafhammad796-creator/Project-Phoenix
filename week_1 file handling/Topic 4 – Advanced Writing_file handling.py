# simple write function in files
file = open("student.txt", "w")

file.write("Name : Hammad\n")
file.write("Age : 22\n")
file.write("Course : Python")

file.close()
# write multiple data in file at once
student =["hammad\n","Rehan\n","Ali\n","Ahmad\n"]
file=open("student.txt","w")
file.writelines(student)
file.close()
print("data added successfuly")
# markes files 
marks = [
    "Math = 95\n",
    "Physics = 88\n",
    "English = 90\n"
]

file = open("marks.txt", "w")

file.writelines(marks)

file.close()
# course file ma data add krna
courses = [
    "Python\n",
    "AI\n",
    "Machine Learning\n",
    "Data Science\n"
]

file = open("courses.txt", "w")

file.writelines(courses)

file.close()
# challenge practic
Employee = ["Employee: Hammad\n","Salary : 50000\n",
            "Department : AI\n","Employee : Ali\n","Salary : 40000\n","Depertment : python\n"]
file=open("Employee.txt","w")
file.writelines(Employee)
file.close()
print("data added succesfuly")
# test challenge code output
file = open("Employee.txt","r")

data = file.read()

print(data)

file.close()