student = {}
student["name"]=input("Enter yousss good name: ")
student["Age"] = input("Enter your aaage:")
student["City"]=input("Enter your city name:")
student["Roll Number"]="BCSF24M001"
student["semester"]=4
student["CGPA"] = float(input("Enter your CGPA: "))
print("====student information====")
print("name:",student["name"])
print("age:",student["Age"])
print("City:",student["City"])
print("Roll no:",student["Roll Number"])
print("semester: ",student["semester"])
print("CGPA: ",student["CGPA"])
if student["CGPA"] >= 3.5:
    print("Excellent Performance")
else:
    print("Keep Working Hard")