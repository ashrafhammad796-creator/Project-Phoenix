name= input("Enter your name: ")
age= input("Enter your age: ")
cgpa= input("Enter your cgpa: ")
with open("myname.txt", "w") as file:
    file.write(name)
    file.write(age)
    file.write(cgpa)
with open("myname.txt", "a") as file:
    file.write(name + "\n" )
file.write(age + "\n")
file.write(cgpa + "\n" )

with open("myname.txt", "r") as file:
    print(file.read())