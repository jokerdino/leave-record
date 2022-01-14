import json
from json.decoder import JSONDecodeError
from datetime import timedelta, date
import datetime

f = open('data.json')
try:
    d = json.load(f)
except JSONDecodeError:
    d = {}
    pass

#print(len(d))
#print(d)



def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

def numOfDays(date1, date2):
    return (date2-date1).days

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
        "sick leave" : sickleave,
        "casual leave list": []
        }
        }

)

def update_casual_leave(employeenumber, casualLeave):
    currentCLbalance = d[employeenumber]['casual leave']
    newCLbalance = int(currentCLbalance) - casualLeave
    d[employeenumber]['casual leave'] = newCLbalance

    print(d[employeenumber])


def add_casual_leave(employeenumber):
    start_cl = input("Enter start date in yyyy-mm-dd format: ")
    start_cl_date = datetime.datetime.strptime(start_cl, "%Y-%m-%d")
    end_cl = input("Enter end date: ")
    end_cl_date = datetime.datetime.strptime(end_cl, "%Y-%m-%d")
    no_of_days = numOfDays(start_cl_date, end_cl_date)+1
    print(no_of_days)
    update_casual_leave(employeenumber, no_of_days)
    casual_leave_list = []
    casual_leave_list_string = d[employeenumber]['casual leave list']
    if end_cl_date == start_cl_date:
        start_cl_date_string = start_cl_date.strftime('%d/%m/%y')
        casual_leave_list_string.append(start_cl_date_string)
    else:
       for dt in daterange(start_cl_date, end_cl_date):
           casual_leave_list.append(dt)
    for dt in casual_leave_list:
        date_string = dt.strftime('%d/%m/%y')
        casual_leave_list_string.append(date_string)
    print(casual_leave_list_string)
    d[employeenumber]['casual leave list'] = casual_leave_list_string


options = input("Choose your options: Press 1 for creating new employee master. Press 2 for adding casual leave. Press 3 for displaying current leave status. Press 4 for displaying all employees and their current leave status.")


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

a_file = open("data.json", "w")
json.dump(d,a_file)

a_file.close()

#print(d)
#a_file = open("data.json", "r")
#output = a_file.read()

#print(output)

#a_file.close()
