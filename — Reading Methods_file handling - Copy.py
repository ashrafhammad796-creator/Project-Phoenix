# read completely file  once read()
file = open("student.txt","r")

data = file.read()

print(data)

file.close()
# readline()function read one line 
file=open("notes.txt","r")
data=file.readline()
print(data)
file.close()

#readlines() ya sary lines ki list banata hy
file = open("notes.txt","r")

data = file.readlines()

print(data)

file.close()
# read data using loop
file = open("notes.txt","r")

for line in file:

    print(line)

file.close()
# challenge practic
file = open(r"D:\journey of uvas\student.txt", "r")

line = file.readline()

while line != "":
    print(line, end="")
    line = file.readline()

file.close()