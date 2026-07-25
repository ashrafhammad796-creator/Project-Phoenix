 #student attendance SystemError
attendance = set()

for i in range(5):
    name = input("Enter student name: ")
    attendance.add(name)

print("====attendance====")
for student in attendance:
    print(student)