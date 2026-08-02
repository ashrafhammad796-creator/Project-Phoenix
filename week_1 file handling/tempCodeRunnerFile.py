name = input("Enter Name: ")
age = input("Enter Age: ")
course = input("Enter Course: ")

with open("students.txt", "a") as file:
    file.write("======================\n")
    file.write("    Student Record\n")
    file.write("======================\n")
    file.write("Name : " + name + "\n")
    file.write("Age : " + age + "\n")
    file.write("Course : " + course + "\n")
    file.write("======================\n")
    file.write("\n")

with open("students.txt", "r") as file:
    print(file.read())
       