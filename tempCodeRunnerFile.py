secret_number=7
attempts=0
while True:
  guess=int(input("enter a guess number:"))
attempts += 1    
if(guess==secret_number):
      print("congratulation")
      print("You guessed the number in attempts.",attempts)  
      break  
else:
    print("wrong guess")

       