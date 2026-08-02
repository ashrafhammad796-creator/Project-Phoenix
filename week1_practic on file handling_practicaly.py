# practic on file handling 
# opening new file
file = open("notes.txt","w")
file.write("welcome to project phoenix/n")
file.close()
print("File creat successfully")
# addding new data in file
file = open("notes.txt", "w")

file.write("python\n")
file.write("file handling\n")
file.write("project phonenix\n")

file.close()
print("Data Added Successfully")
# reading data from file

file=open("notes.txt","r")
data=file.read()
print(data)
file.close()
# appending data in file
file=open("notes.txt","a")
file.write("\nReading python every day")
file.close()
#student.txt file creating
file=open("student.txt","w")
file.write("Name : Hammad")
file.write("\n Age : 22")
file.write("\nCourse : python")
file.close()
print("File created successfully")
# read data from student.txt
file=open("student.txt","r")
data=file.read()
print(data)
file.close()
#append data in student .txt
file=open("student.txt","a")
file.write("\ncity : lahore")
file.close()
print("data added successfully")
# creat college.txt file
file=open("college.txt","w")
file.write("\nuniversity name = uvas")
file.write("\n Department = flsbm")
file.write("\nsemester = 4")
file.close()
print("data aded successfully")
# read data from college.txt
file=open("college.txt","r")
data=file.read()
print(data)
file.close()