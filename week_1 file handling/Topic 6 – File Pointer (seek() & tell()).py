# tell()ya cursor ki possitiion batata hy
file = open("student.txt","r")

print(file.tell())

file.close()
#2nd practic
file = open("student.txt","r")

print(file.read(4))

print(file.tell())

file.close()
# pratic 3rd
file = open("student.txt","r")

file.seek(3)

print(file.read())

file.close()
# practic 4th
file = open("student.txt","r")

print(file.read(2))

print(file.tell())

file.seek(0)

print(file.read())

file.close()
# challenge practic

file=open("python.txt","w")
file.write("Python Programming Language")

file=open("python.txt","r")
print(file.tell())
print(file.read(6))
print(file.tell())
file.seek(0)
print(file.read())
file.close()