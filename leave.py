import json
from json.decoder import JSONDecodeError
 
f = open('data.json')
try:
    d = json.load(f)
except JSONDecodeError:
    d = {}
    pass

#print(len(d))
print(d)

def create_employee():
    employeeName = input("Enter name of the employee: ")
    employeeNumber = input("Enter employee number: ")
    casualLeave = input("Enter current casual leave: ")
    earnedLeave = input("Enter current earned leave: ")
    sickleave = input("Enter current sick leave: ")
    d.update({employeeNumber:{
        "name": employeeName,
        "employee number" : employeeNumber,
        "casual leave": casualLeave,
        "earned leave" : earnedLeave,
        "sick leave" : sickleave
        }
        }

)

def update_casual_leave():
    employeeNumber = input("Enter employee number: ")
    casualLeave = input("Enter new casual leave: ")
#    print(d.items())
#    for employeeNumber, casualLeave in d.items():
    d[employeeNumber]['casual leave'] = casualLeave

    print(d[employeeNumber])


options = input("What do you want to do?")

if options == "1":
    create_employee()
if options == "2":
    update_casual_leave()
if options == "3":
    employeenumber = input("Enter number to display current status: ")
    print(d[employeenumber])
    

a_file = open("data.json", "w")
json.dump(d,a_file)

a_file.close()

#print(d)
#a_file = open("data.json", "r")
#output = a_file.read()

#print(output)

#a_file.close()
