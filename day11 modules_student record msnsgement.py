class Student:

    def set_data(self, name, age, department):
        self.name = name
        self.age = age
        self.department = department

    def display(self):
        print("\n----- Student Information -----")
        print("Name :", self.name)
        print("Age :", self.age)
        print("Department :", self.department)


student1 = Student()

name = input("Enter Student Name: ")
age = input("Enter Age: ")
department = input("Enter Department: ")

student1.set_data(name, age, department)

student1.display()