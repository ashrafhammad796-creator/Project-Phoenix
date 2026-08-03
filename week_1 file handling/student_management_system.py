import csv

def menu():
    print("\n============================")
    print(" Student Record Management")
    print("============================")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Delete Student")
    print("5. Exit")
    print("============================")


while True:

    menu()

    choice = input("Enter your choice: ")

    
    # Add Student
    
    if choice == "1":

        name = input("Enter Name: ")

        try:
            age = int(input("Enter Student Age: "))

        except ValueError:
            print("Please enter numbers only.")
            continue

        course = input("Enter Course: ")

        with open("students.csv", "a", newline="") as file:

            writer = csv.writer(file)

            if file.tell() == 0:
                writer.writerow(["Name", "Age", "Course"])

            writer.writerow([name, age, course])

            print("Student Added Successfully.")

    
    # View Students
    
    elif choice == "2":

        try:
            with open("students.csv", "r") as file:

                reader = csv.reader(file)

                print("\n------ Student Records ------")

                for row in reader:
                    print(row)

        except FileNotFoundError:
            print("No student records found.")

    
    # Search Student
    
    elif choice == "3":

        search = input("Enter Student Name: ")

        found = False

        try:
            with open("students.csv", "r") as file:

                reader = csv.reader(file)

                for row in reader:

                    if len(row) > 0 and row[0].lower() == search.lower():

                        print("\nStudent Found")
                        print("Name :", row[0])
                        print("Age :", row[1])
                        print("Course :", row[2])

                        found = True
                        break

                if not found:
                    print("Student Not Found.")

        except FileNotFoundError:
            print("No student records found.")

    
    # Delete Student
    
    elif choice == "4":

        delete_name = input("Enter Student Name to Delete: ")

        records = []

        deleted = False

        try:

            with open("students.csv", "r") as file:

                reader = csv.reader(file)

                for row in reader:

                    if len(row) > 0 and row[0].lower() == delete_name.lower():

                        deleted = True

                    else:
                        records.append(row)

            with open("students.csv", "w", newline="") as file:

                writer = csv.writer(file)

                writer.writerows(records)

            if deleted:
                print("Student Deleted Successfully.")

            else:
                print("Student Not Found.")

        except FileNotFoundError:
            print("No student records found.")

    # Exit
    
    elif choice == "5":

        print("Thank you for using Project Phoenix.")
        break

    
    # Invalid Choice
    
    else:

        print("Invalid Choice. Please Try Again.")