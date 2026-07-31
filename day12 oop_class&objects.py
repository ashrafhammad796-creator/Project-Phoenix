class Student:

    def set_name(self, name):
        self.name = name

    def display(self):
        print("Name:", self.name)


student1 = Student()

student1.set_name("Hammad")

student1.display()
# student data with multiple attributes
class Student:
    
    def set_data(self, name, age):
        self.name = name
        self.age = age

    def display(self):
        print(self.name)
        print(self.age)


student = Student()

student.set_data("Ali",20)

student.display()

# car data with multiple attributes
class Car:
    
    def set_data(self, brand, color):
        self.brand = brand
        self.color = color

    def display(self):
        print("Brand:", self.brand)
        print("Color:", self.color)


car = Car()

car.set_data("Toyota","White")

car.display()

# laptop data in oop 
class Laptop:
    
    def set_data(self, company, ram):
        self.company = company
        self.ram = ram

    def display(self):
        print("Company:", self.company)
        print("RAM:", self.ram)


lap = Laptop()

lap.set_data("Dell","8GB")

lap.display()

# bank data in oop
class Bank:
    
    def set_data(self, name, balance):
        self.name = name
        self.balance = balance

    def display(self):
        print("Account Holder:", self.name)
        print("Balance:", self.balance)


user = Bank()

user.set_data("Hammad",50000)

user.display()

# employee data in oop
class employee:
    def set_data(self,name,salary):
        self.name=name
        self.salary=salary
        def display(self):
            print("NAME: ",self.name)
            print("SALARY :",self.salary)
            name=employe()
            name.set_data("HAMMAD",30000)
            name.display()