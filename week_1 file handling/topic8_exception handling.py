# practic code 1
try:
    num = int(input("Enter Number: "))
    print(50 / num)

except ZeroDivisionError:
    print("Zero is not allowed.")
    # practic code 2
try:
    age = int(input("Enter Age: "))
    print(age)

except ValueError:
    print("Enter numbers only.")
    #practic file not founde exception handling 3
try:
    with open("student.txt", "r") as file:
        print(file.read())

except FileNotFoundError:
    print("File not found.")
    # practic code using else & finaly function
try:
    num = int(input("Enter Number: "))

except ValueError:
    print("Invalid Number")

else:
    print("Success")

finally:
    print("Program Finished")
    # challenge
try:
    num1=int(input("Enter number1:"))
    num2=int(input("Enter number2:"))
    print(num1/num2)
except ZeroDivisionError:
        print("Cannot divide by zero.")
        
except ValueError:
    print("Invalid Number")
else:
        print("Thank you for using Project Phoenix.")

        