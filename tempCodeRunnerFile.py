class Employee:
    
    def set_data(self, name, salary):
        self.name = name
        self.salary = salary

    def display(self):
        print("NAME:", self.name)
        print("SALARY:", self.salary)


emp = Employee()

emp.set_data("HAMMAD", 30000)

emp.display()