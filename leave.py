import json
from json.decoder import JSONDecodeError
from datetime import timedelta, date
import datetime
import pandas as pd

f = open('data.json')
try:
    d = json.load(f)
except JSONDecodeError:
    d = {}
    pass


def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

def numOfDays(date1, date2):
    return (date2-date1).days

def validate_employee_number():
    while True:
        print("Employees already present: ",  d.keys())
        employeeNumber_input = input("Enter employee number: ")
        if employeeNumber_input not in d.keys():
            print("Accepted")
            return employeeNumber_input
        else:
            print("Employee number already exists.")


def create_employee():

    employeeNumber = validate_employee_number()
    employeeName = input("Enter name of the employee: ")
    casualLeave = input("Enter current casual leave: ")
    if int(casualLeave) > 12:
        casualLeave = 12
    earnedLeave = input("Enter current earned leave: ")
    if int(earnedLeave) > 270:
        earnedleave = 270
    sickleave = input("Enter current sick leave: ")
    if int(sickleave) > 240:
        sickleave = 240
    RH = input("Enter current RH count: ")
    if int(RH) > 2:
        RH = 2
    DOJ = input("Enter date of joining current office in yyyy-mm-dd format: ")
    DOJ_date = datetime.datetime.strptime(DOJ, "%Y-%m-%d")
#    DOJ_date_string = []
    d.update({employeeNumber:{
        "name": employeeName,
        "employee number" : employeeNumber,
        "DOJ current office" : DOJ,
        "casual leave": casualLeave,
        "earned leave" : earnedLeave,
        "sick leave" : sickleave,
        "RH": RH,
        "casual leave list": [],
        "casual leave dict": {},
        "RH list": [],
        "Earned leave list": [],
        "Sick leave list": [],
        "Quarantine leave list":[],
        "Special leave list":[]
        }
        }

)

def update_casual_leave(employeenumber, casualLeave):
    currentCLbalance = d[employeenumber]['casual leave']
    newCLbalance = float(currentCLbalance) - float(casualLeave)
    
    d[employeenumber]['casual leave'] = newCLbalance

    #print(d[employeenumber])


def add_casual_leave(employeenumber):
    
    print("Current CL count for employee", d[employeenumber]['casual leave'])
    #casual_leave_count = d[employeenumber]['casual leave'] * 2

    type_CL = input("Enter whether full or half CL: ")

    start_cl = input("Enter start date in yyyy-mm-dd format: ")
    start_cl_date = datetime.datetime.strptime(start_cl, "%Y-%m-%d")
    end_cl = input("Enter end date: ")
    
    if end_cl != "":
        end_cl_date = datetime.datetime.strptime(end_cl, "%Y-%m-%d")
    else:
        end_cl_date = start_cl_date
    no_of_days = numOfDays(start_cl_date, end_cl_date)+1
    
    if type_CL == "full":
        update_casual_leave(employeenumber, no_of_days)
    elif type_CL == "half":
        update_casual_leave(employeenumber, no_of_days/2)
    
    casual_leave_list = []
    casual_leave_list_string = d[employeenumber]['casual leave list']
    dict_casual_leave = d[employeenumber]['casual leave dict']
    local_dict = {}
    if end_cl_date == start_cl_date:
        start_cl_date_string = start_cl_date.strftime('%d/%m/%y')
        casual_leave_list_string.append(start_cl_date_string + " ("+type_CL+")")
        #dict_casual_leave['casual leave dict'].update({start_cl_date_string: type_CL})
        local_dict.update({start_cl_date_string: type_CL})
    else:
       for dt in daterange(start_cl_date, end_cl_date):
           casual_leave_list.append(dt)
           #dict_casual _leave['casual leave dict'].update({start_cl_date_string: type_CL}) 
    for dt in casual_leave_list:
        date_string = dt.strftime('%d/%m/%y')
        casual_leave_list_string.append(date_string + " ("+type_CL+")")
#        dict_casual_leave['casual leave dict'].update({date_string: type_CL})
        local_dict.update({date_string: type_CL})   
    #print(casual_leave_list_string)
    
    d[employeenumber]['casual leave list'] = casual_leave_list_string
    d[employeenumber]['casual leave dict'].update(local_dict)

def delete_employee():
    print("Employees already present", d.keys())
    employeenumber = input("Enter employee number to delete: ")
    d.pop(employeenumber)

def keep_it_going(options):

    if options == "1":
        create_employee()
    if options == "3":
        employeenumber = input("Enter number to display current status: ")
        print(d[employeenumber])
    if options == "2":
        employeenumber = input("Enter employee number:")
        add_casual_leave(employeenumber)
    if options == "4":
        print(d)
    if options == "6":
        delete_employee()

while(True):
    
    options = input("Choose your options: \nPress 1 for creating new employee master. \nPress 2 for adding casual leave. \nPress 3 for displaying current leave status. \nPress 4 for displaying all employees and their current leave status.\nPress 5 to exit the program.\nPress 6 to delete employee record.\nEnter your option :")
    if options != "5":
        keep_it_going(options)
    else:
        break

a_file = open("data.json", "w")
json.dump(d,a_file)

a_file.close()


df = pd.DataFrame.from_dict({(i): d[i]
    for i in d.keys()},
    orient='index')


print(df)
df.to_excel("leave-data.xlsx")

#print(d)
#a_file = open("data.json", "r")
#output = a_file.read()

#print(output)

#a_file.close()
