age = int(input("Enter your age: "))

if age >= 18:

    salary = int(input("Enter your salary: "))

    if salary >= 50000:
        print("Loan Approved")

    else:
        print("Low Salary")

else:
    print("Not Eligible")