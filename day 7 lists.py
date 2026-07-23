students = ["Hammad", "Ali", "Ahmed"]

print(students[0])
# cities list
cities=["pattoki","karachi","islamabad"]
print(cities)
# fruites list

fruits = ["mango","apple","banana","orange"]
print(fruits)
# subjects list
subjects = [
    "Python",
    "AI",
    "DSA",
    "Database",
    "English"
]
print(subjects[0])
print(subjects[2])
print(subjects[4])
# changing list element by index
fruits= ["apple","mango","banana"]
fruits [1]="orange"
print(fruits)
#append numbers in list
student =["hammad","rehan"]
student.append("roman")
print(student)

#subjects list append
subjects =["python","AI"]
subjects.append("DSA")
subjects.append("Database")
subjects.append("English")
print(subjects)
# insertion elements
numbers = [10,20,40]
numbers.insert(2,30)
print(numbers)
# remove elements from list
fruits = ["Apple", "Mango", "Banana", "Orange"]
fruits.remove("Mango")
print(fruits)
# pop concept in lists
numbers = [10, 20, 30, 40, 50]
numbers.pop(4)
print(numbers)
#Student Record Management System
students =[]
         
for i in range(3):
    name=input("Enter student name:")
    students.append(name)

print(students)
print(len(students))
#show subject list line by line using for loop in lists
subjects=["DSA","AI","SE","JAVA"]
for subject in subjects:
    print(subject)