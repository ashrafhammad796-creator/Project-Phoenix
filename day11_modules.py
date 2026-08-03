import math
print(math.sqrt(25))
#use power in modules
import math
print(math.pow(2,5))
#pi in modules code
import math
print(math.pi)
# ceiling in modules
import math

print(math.ceil(4.2))
# floor in python modules
import math

print(math.floor(4.9))
# random in pyhton_modules
import random

print(random.randint(1,10))
# random choice
import random

colors = ["Red","Blue","Green","Black"]

print(random.choice(colors))
# date/time python_modules
import datetime

today = datetime.date.today()

print(today)
# current time_module
import datetime

now = datetime.datetime.now()

print(now)
# from import in python_modules
from math import sqrt

print(sqrt(64))
# multiple functions in from_module
from math import sqrt,pow

print(sqrt(81))
print(pow(2,4))
#alias (as)inpython_modules
import math as m

print(m.sqrt(100))