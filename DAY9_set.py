# SET FUNCTION PRACTIC
students ={"hammad","Ali","Rehan","Ali"}
print(students)
#addd new element
students={"hammad","Ali"}
students.add("Rehan")
print(students)
# Remove a leement
students={"hammad","Ali"}
students.remove("Ali")
print(students)
# discarding value agr value na mily to error nahy deta
students={"hammad","Ali"}
students.discard("Bilal")
print(students)
#hans on practic
cities ={"pattoki","islambad"}
cities.add("karachi")
print(cities)
 #student attendance SystemError
attendance = set()

for i in range(5):
    name = input("Enter student name: ")
    attendance.add(name)

print("====attendance====")
for student in attendance:
    print(student)

