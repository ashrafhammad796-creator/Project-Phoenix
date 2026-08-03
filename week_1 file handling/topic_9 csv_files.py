#csv file practic
import csv
with open("student.csv","w",newline="")as file:
    writer=csv.writer(file)
    writer.writerow(["`Name","Age","Course"])
    writer.writerow(["Hammad","22","AI"])
    writer.writerow(["Ali","20","AI"])
    writer.writerow(["Ahmwd","21","Mechine Lerning"])
    #read data from csv
import csv
with open("student.csv","r")as file:
        reader=csv.reader(file)
        for row in reader:
            print(row)
            # input student 
import csv

name = input("Enter your name: ")
age = input("Enter your age: ")
course = input("Enter your course: ")

with open("student.csv", "a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([name, age, course])

print("Data added successfully.")
 # challenge code
import csv
name=input("Enter your name:")
salary=input("Enter your salary:")
Department=input("Enter Depertment:")
with open("employees.csv","w",newline="")as file:
    writer=csv.writer(file)
    writer.writerow(["Name","Salary","Department"])
    writer.writerow([name,salary,Department])
    print("data enter sucessfully")
    # print record
import csv
with open("employees.csv","r")as file:
    reader=csv.reader(file)
    for row in reader:
        print(row)
    
 