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
        earnedLeave = 270
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
#        "casual leave list": [],
        "casual leave dict": {},
        "RH list": [],
        "Earned leave list": [],
        "sick leave dict": {},
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


def delete_casual_leave():
    
    employeenumber = req_emp_no()
    #employeenumber = input("Enter employee number")

    print(d[employeenumber]['casual leave dict'])
    delete_cl = input("Enter date in yyyy-mm-dd format: ")
    delete_cl_date = datetime.datetime.strptime(delete_cl, "%Y-%m-%d")
    delete_cl_date_string = delete_cl_date.strftime("%d/%m/%y")

    if delete_cl_date_string in d[employeenumber]['casual leave dict'].keys():
        casualleave = delete_cl_date.strftime("%d/%m/%y")
    else:
        print("Entered date is not present")
        return
    if d[employeenumber]['casual leave dict'][casualleave] == "half":
        update_casual_leave(employeenumber, -0.5)

    else:
        update_casual_leave(employeenumber, -1)
    d[employeenumber]['casual leave dict'].pop(casualleave)
     

def add_casual_leave(employeenumber):
    
    print("Current CL count for employee", d[employeenumber]['casual leave'])
    #casual_leave_count = d[employeenumber]['casual leave'] * 2
    dict_casual_leave_list = d[employeenumber]['casual leave dict'].keys()
    print(dict_casual_leave_list)
    type_CL = input("Enter whether full or half CL: ")

    start_cl = input("Enter start date in yyyy-mm-dd format: ")
    start_cl_date = datetime.datetime.strptime(start_cl, "%Y-%m-%d")
    
    if start_cl_date.strftime("%d/%m/%y") in dict_casual_leave_list:
        print("Casual leave already entered")
        return
    if type_CL == "half":
        end_cl = ""
    else:
        end_cl = input("Enter end date: ")
    
    if end_cl == "":
        #end_cl_date = datetime.datetime.strptime(end_cl, "%Y-%m-%d")
    #else:
        end_cl_date = start_cl_date
    elif end_cl != "":
         end_cl_date = datetime.datetime.strptime(end_cl, "%Y-%m-%d")

    no_of_days = numOfDays(start_cl_date, end_cl_date)+1
    
    if type_CL == "full":
        update_casual_leave(employeenumber, no_of_days)
    elif type_CL == "half":
        update_casual_leave(employeenumber, no_of_days/2)
    
    casual_leave_list = []
 #   casual_leave_list_string = d[employeenumber]['casual leave list']
    dict_casual_leave = d[employeenumber]['casual leave dict']
    local_dict = {}
    if end_cl_date == start_cl_date:
        start_cl_date_string = start_cl_date.strftime('%d/%m/%y')
  #      casual_leave_list_string.append(start_cl_date_string + " ("+type_CL+")")
        #dict_casual_leave['casual leave dict'].update({start_cl_date_string: type_CL})
        local_dict.update({start_cl_date_string: type_CL})
    else:
       for dt in daterange(start_cl_date, end_cl_date):
           casual_leave_list.append(dt)
           #dict_casual _leave['casual leave dict'].update({start_cl_date_string: type_CL}) 
    for dt in casual_leave_list:
        date_string = dt.strftime('%d/%m/%y')
   #     casual_leave_list_string.append(date_string + " ("+type_CL+")")
#        dict_casual_leave['casual leave dict'].update({date_string: type_CL})
        local_dict.update({date_string: type_CL})   
    #print(casual_leave_list_string)
    
    #d[employeenumber]['casual leave list'] = casual_leave_list_string
    d[employeenumber]['casual leave dict'].update(local_dict)

def delete_employee():
    #print("Employees already present", d.keys())
    #employeenumber = input("Enter employee number to delete: ")
    employeenumber = req_emp_no()
    d.pop(employeenumber)

def update_earned_leave(employeenumber, earnedleavecount):
    
    currentELbalance = d[employeenumber]['earned leave']
    newELbalance = float(currentELbalance) - float(earnedleavecount)
 
    d[employeenumber]['earned leave'] = newELbalance






def delete_earned_leave():

     employeenumber = req_emp_no()
     #employeenumber = input("Enter employee number")
 
     print(d[employeenumber]['Earned leave list'])
     delete_el = input("Enter date in yyyy-mm-dd format: ")
     delete_el_date = datetime.datetime.strptime(delete_el, "%Y-%m-%d")
     delete_el_date_string = delete_el_date.strftime("%d/%m/%y")
 
     if delete_el_date_string in d[employeenumber]['Earned leave list']:
         update_earned_leave(employeenumber, -1)
         earnedleave = delete_el_date.strftime("%d/%m/%y")
     else:
         print("Entered date is not present")
         return
     #if d[employeenumber]['casual leave dict'][casualleave] = "half":
      #   update_casual_leave(employeenumber, -0.5)
 
    # else:
         #update_earned_leave(employeenumber, -1)
     d[employeenumber]['Earned leave list'].remove(earnedleave)





def add_earned_leave(employeenumber):
    print(d[employeenumber]['earned leave'])
    print(d[employeenumber]['Earned leave list'])

    earned_leave_list_string = d[employeenumber]['Earned leave list']
    earned_leave_list = []

    start_el = input("Enter start date in yyyy-mm-dd format: ")
    start_el_date = datetime.datetime.strptime(start_el, "%Y-%m-%d") 

    end_el = input("Enter end date in yyyy-mm-dd format: ")
    end_el_date = datetime.datetime.strptime(end_el, "%Y-%m-%d")
    
  
    no_of_days = numOfDays(start_el_date, end_el_date)+1
  
    update_earned_leave(employeenumber, no_of_days)
   
    print(no_of_days)
    for dt in daterange(start_el_date, end_el_date):
        earned_leave_list.append(dt)
        #dict_casual _leave['casual leave dict'].update({start_cl_date_strin
    for dt in earned_leave_list:
        date_string = dt.strftime('%d/%m/%y')
        earned_leave_list_string.append(date_string)           
      #dict_casual_leave['casual leave dict'].update({date_string: type_CL})
    d[employeenumber]['Earned leave list'] = earned_leave_list_string 

def add_sick_leave(employeenumber):
    
    print("Current SL count for employee", d[employeenumber]['sick leave'])
    #casual_leave_count = d[employeenumber]['casual leave'] * 2
    dict_sick_leave_list = d[employeenumber]['sick leave dict'].keys()
    print(dict_sick_leave_list)
    type_SL = input("Enter whether full or half pay SL: ")

    start_sl = input("Enter start date in yyyy-mm-dd format: ")
    start_sl_date = datetime.datetime.strptime(start_sl, "%Y-%m-%d")
    
    if start_sl_date.strftime("%d/%m/%y") in dict_sick_leave_list:
        print("Sick leave already entered")
        return
    if type_SL == "half":
        end_sl = ""
    else:
        end_sl = input("Enter end date: ")
    
    if end_sl == "":
        #end_cl_date = datetime.datetime.strptime(end_cl, "%Y-%m-%d")
    #else:
        end_sl_date = start_sl_date
    elif end_sl != "":
         end_sl_date = datetime.datetime.strptime(end_sl, "%Y-%m-%d")

    no_of_days = numOfDays(start_sl_date, end_sl_date)+1
    
    if type_SL == "full":
        update_sick_leave(employeenumber, no_of_days*2)
    elif type_SL == "half":
        update_sick_leave(employeenumber, no_of_days)
    
    sick_leave_list = []
 #   casual_leave_list_string = d[employeenumber]['casual leave list']
    dict_sick_leave = d[employeenumber]['sick leave dict']
    local_dict = {}
    if end_sl_date == start_sl_date:
        start_sl_date_string = start_sl_date.strftime('%d/%m/%y')
  #      casual_leave_list_string.append(start_cl_date_string + " ("+type_CL+")")
        #dict_casual_leave['casual leave dict'].update({start_cl_date_string: type_CL})
        local_dict.update({start_sl_date_string: type_SL})
    else:
       for dt in daterange(start_sl_date, end_sl_date):
           sick_leave_list.append(dt)
           #dict_casual _leave['casual leave dict'].update({start_cl_date_string: type_CL}) 
    for dt in sick_leave_list:
        date_string = dt.strftime('%d/%m/%y')
   #     casual_leave_list_string.append(date_string + " ("+type_CL+")")
#        dict_casual_leave['casual leave dict'].update({date_string: type_CL})
        local_dict.update({date_string: type_SL})   
    #print(casual_leave_list_string)
    
    #d[employeenumber]['casual leave list'] = casual_leave_list_string
    d[employeenumber]['sick leave dict'].update(local_dict)

def delete_sick_leave(employeenumber):
    
    print(d[employeenumber]['sick leave dict'])
    delete_sl = input("Enter date in yyyy-mm-dd format: ")
    delete_sl_date = datetime.datetime.strptime(delete_sl, "%Y-%m-%d")
    delete_sl_date_string = delete_sl_date.strftime("%d/%m/%y")

    if delete_sl_date_string in d[employeenumber]['sick leave dict'].keys():
        sickleave = delete_sl_date.strftime("%d/%m/%y")
    else:
        print("Entered date is not present")
        return
    if d[employeenumber]['sick leave dict'][sickleave] == "half":
        update_risk_leave(employeenumber, -1)

    else:
        update_sick_leave(employeenumber, -2)
    d[employeenumber]['sick leave dict'].pop(sickleave)

def update_sick_leave(employeenumber, sickleavecount):
    
    currentsickbalance = d[employeenumber]['sick leave']
    newsickbalance = float(currentsickbalance) - float(sickleavecount)
 
    d[employeenumber]['sick leave'] = newsickbalance

def req_emp_no():
    print("Employees already present", d.keys())
    return input("Enter employee number: ")

def keep_it_going(options):

    if options == "3":
        create_employee()
    if options == "2":
        employeenumber = input("Enter number to display current status: ")
        print(d[employeenumber])
    if options == "5":
        employeenumber = input("Enter employee number: ")
        add_casual_leave(employeenumber)
    if options == "1":
        print(d)
    if options == "4":
        delete_employee()
    if options == "6":
        delete_casual_leave()
    if options == "7":
        emp_no = req_emp_no()
        add_earned_leave(emp_no)
    if options == "9":
        emp_no = req_emp_no()
        add_sick_leave(emp_no)
    if options == "8":
        delete_earned_leave()
    if options == "10":
        emp_no = req_emp_no()
        delete_sick_leave(emp_no)
    #if options == "12"
while(True):
    
    options = input("""Choose your options:
 Press 1 to display all employees and their current leave status.
 Press 2 to display current leave status of a particular employee.
 Press 3 to create a new employee master.
 Press 4 to delete an employee.
 Press 5 to add casual leave.
 Press 6 to delete already entered casual leave.
 Press 7 to add earned leave.
 Press 8 to delete already entered earned leave.
 Press 9 to add sick leave.
 Press 10 to delete already entered sick leave.
 Press 11 to exit the program.

Enter your option :""")
    if options != "11":
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
