students=[] 
for i in range(3):
    name=input("Enter student name:")
    students.append(name)

print("====STUDENT RECORD====")
for student in students:
    print(student)
print("Total Students:", len(students))
    
