name = input("Enter Student Name: ")
obtained_marks = int(input("Enter Obtained Marks: "))

total_marks = 500

percentage = (obtained_marks / total_marks) * 100

print("Percentage:", percentage)

# Grade
if percentage >= 80:
    grade = "A"
elif percentage >= 65:
    grade = "B"
elif percentage >= 55:
    grade = "C"
elif percentage >= 45:
    grade = "D"
elif percentage >= 35:
    grade = "E"
else:
    grade = "F"

print("Grade:", grade)

# Pass / Fail
if percentage >= 40:
    status = "Pass"
else:
    status = "Fail"

print("Status:", status)

# Remarks
if percentage >= 80:
    remarks = "Excellent"
elif percentage >= 65:
    remarks = "Very Good"
elif percentage >= 55:
    remarks = "Good"
elif percentage >= 45:
    remarks = "Average"
elif percentage >= 40:
    remarks = "Needs Improvement"
else:
    remarks = "Work Hard"

print("Remarks:", remarks)

print("\n===== STUDENT REPORT =====")
print("Name:", name)
print("Obtained Marks:", obtained_marks)
print("Total Marks:", total_marks)
print("Percentage:", percentage)
print("Grade:", grade)
print("Status:", status)
print("Remarks:", remarks)