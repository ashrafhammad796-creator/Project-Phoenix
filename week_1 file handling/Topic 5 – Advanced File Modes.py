# r+ operator
file = open("student.txt", "r+")

print(file.read())

file.write("\nMachine Learning")

file.close()
# w+ operator
file = open("subjects.txt", "w+")

file.write("Python\nAI\nDBMS")

file.seek(0)

print(file.read())

file.close()
#a+ operator
file = open("subjects.txt", "a+")

file.write("\nData Science")

file.seek(0)

print(file.read())

file.close()
# x+ creating new file
file = open("project.txt", "x")

file.write("Project Phoenix")

file.close()
# challenge program
#creat file
file = open("employee_record.txt", "x")

file.write("Project Phoenix")

file.close()
#implement w+
file=open("employee_record.txt","w+")
file.write("Hammad\npython\n50000")
file.seek(0)
data=file.read()
print(data)
file.close()