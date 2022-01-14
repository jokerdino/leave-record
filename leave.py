import json

#print("Hello")

#employee = input("Enter name of employee: ")

#employeeList = []

#employeeList.append(employee)



d = dict(dict())
 
a_file = open("data.json","r")
d = a_file.read()

print(d)



#d = {
 #   "Barneedhar" : {
  #      "name": "Barneedhar",
   #     "employee number": 44515,
    #    "casual leave": 12
    #}
#}

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
#d.update({employee:""})


#for i in employeeList:
 #   d[i] = None

print(d)

#print(employeeList)


a_file = open("data.json", "w")
json.dump(d,a_file)

a_file.close()

a_file = open("data.json", "r")
output = a_file.read()

print(output)

a_file.close()
