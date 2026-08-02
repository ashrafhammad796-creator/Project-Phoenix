with open("student.txt","r")as file:
    print(file.read())
    file.close()
    # write data into file
    with open("teachers.txt","w")as file:
     file.write("Ali\nAhmad\nUsman")
     file.close()
    #append data into file
with open("teachers.txt","a")as file:
     file.write("\nHamza")
     file.close()
    #read data
with open("teachers.txt","r")as file:
    for line in file:
     print(line)
    file.close()
    # challenge 
with open("project.txt","w")as file:
    file.write("project phoenix\npyhton\nAI\nMExhine learning\n")
    file.close()
with open("project.txt","r")as file:
    data=file.read()
    print(data)
    file.close()
        # real world project
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
       