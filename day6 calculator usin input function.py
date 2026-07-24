a =int (input("Enter first number"))
b = int(input("enter second number"))
operator =input("Enter an operator +,-,*,/")
if operator== "+":
    def add (a,b):
     return a+b
    result=add(a,b)
    print(result)     
elif operator=="-":
    def subtract(a,b):
        return a-b
    result=subtract(a,b)
    print(result)
    
elif operator== "*":
   def multplication(a,b):
       
    return a*b
   result=multplication(a,b)
   print(result)
else:
    def division(a,b):
        return a/b
    result=division(a,b)
    print(result)