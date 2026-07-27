name = input("Enter your name: ")
age = input("Enter your age: ")
cgpa = input("Enter your cgpa: ")

with open("myname.txt", "w") as file:
    file.write("Name : " + name + "\n")
    file.write("Age: "+ age + "\n")
    file.write("CGPA: " + cgpa)

with open("myname.txt", "r") as file:
    print(file.read())