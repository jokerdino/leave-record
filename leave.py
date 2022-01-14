import json

 
f = open('data.json')
d = json.load(f)

print(len(d))
print(d)

def create_employee():
    employeeName = input("Enter name of the employee: ")
    employeeNumber = input("Enter employee number: ")
    casualLeave = input("Enter current casual leave: ")
    earnedLeave = input("Enter current earned leave: ")
    sickleave = input("Enter current sick leave: ")
    d.update({employeeName:{
        "name": employeeName,
        "employee number" : employeeNumber,
        "casual leave": casualLeave,
        "earned leave" : earnedLeave,
        "sick leave" : sickleave
        }
        }

)
create_employee()

a_file = open("data.json", "w")
json.dump(d,a_file)

a_file.close()

print(d)
#a_file = open("data.json", "r")
#output = a_file.read()

#print(output)

#a_file.close()
