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
    DOJ = input("Leave record last updated on:  Enter date in dd-mm-yyyy format: ")
           # When was the leave record last updated on:  in dd-mm-yyyy format: ")
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
    #DOJ = input("When was the leave record last updated on:  in dd-mm-yyyy format: ")
    DOJ_date = datetime.datetime.strptime(DOJ, "%d-%m-%Y")
    d.update({employeeNumber:{
        "name": employeeName,
        "employee number" : employeeNumber,
        "Leave updated as on" : DOJ,
        "casual leave": casualLeave,
        "earned leave" : earnedLeave,
        "sick leave" : sickleave,
        "RH": RH,
        "casual leave dict": {},
        "RH list": [],
        "Earned leave list": [],
        "sick leave dict": {},
        "Quarantine leave list":[],
        "Special leave list":{},
        "LOP":[],
        "Leave encashment": {}
        }
    }
    )
    save_data()



def update_casual_leave(employeenumber, casualLeave):
    currentCLbalance = d[employeenumber]['casual leave']
    newCLbalance = float(currentCLbalance) - float(casualLeave)
    
    d[employeenumber]['casual leave'] = newCLbalance
    save_data()
    #print(d[employeenumber])


def delete_casual_leave(employeenumber):
    
   # employeenumber = req_emp_no()
    #employeenumber = input("Enter employee number")

    print(d[employeenumber]['casual leave dict'])
    delete_cl = input("Enter date in dd-mm-yyyy format: ")
    delete_cl_date = datetime.datetime.strptime(delete_cl, "%d-%m-%Y")
    delete_cl_date_string = delete_cl_date.strftime("%d-%m-%Y")

    if delete_cl_date_string in d[employeenumber]['casual leave dict'].keys():
        casualleave = delete_cl_date.strftime("%d-%m-%Y")
    else:
        print("Entered date is not present")
        return
    if d[employeenumber]['casual leave dict'][casualleave] == "half":
        update_casual_leave(employeenumber, -0.5)

    else:
        update_casual_leave(employeenumber, -1)
    d[employeenumber]['casual leave dict'].pop(casualleave)
    save_data()

def add_casual_leave(employeenumber):
    
    print("Current CL count for employee", d[employeenumber]['casual leave'])
    dict_casual_leave_list = d[employeenumber]['casual leave dict'].keys()
    print(dict_casual_leave_list)
    type_CL = input("Enter whether full or half CL: ")

    start_cl = input("Enter start date in dd-mm-yyyy format: ")
    start_cl_date = datetime.datetime.strptime(start_cl, "%d-%m-%Y")
    
    if start_cl_date.strftime("%d-%m-%Y") in dict_casual_leave_list:
        print("Casual leave already entered")
        return
    if type_CL == "half":
        end_cl = ""
    else:
        end_cl = input("Enter end date: ")
    
    if end_cl == "":
        end_cl_date = start_cl_date
    elif end_cl != "":
         end_cl_date = datetime.datetime.strptime(end_cl, "%d-%m-%Y")

    no_of_days = numOfDays(start_cl_date, end_cl_date)+1
    
    if type_CL == "full":
        update_casual_leave(employeenumber, no_of_days)
    elif type_CL == "half":
        update_casual_leave(employeenumber, no_of_days/2)
    
    casual_leave_list = []
    dict_casual_leave = d[employeenumber]['casual leave dict']
    local_dict = {}
    if end_cl_date == start_cl_date:
        start_cl_date_string = start_cl_date.strftime('%d-%m-%Y')
        local_dict.update({start_cl_date_string: type_CL})
    else:
       for dt in daterange(start_cl_date, end_cl_date):
           casual_leave_list.append(dt)
    for dt in casual_leave_list:
        date_string = dt.strftime('%d-%m-%Y')
        local_dict.update({date_string: type_CL})   
    
    d[employeenumber]['casual leave dict'].update(local_dict)
    save_data()

def delete_employee(employeenumber):
    backup_data()
    d.pop(employeenumber)
    save_data()


def update_earned_leave(employeenumber, earnedleavecount):
    
    currentELbalance = d[employeenumber]['earned leave']
    newELbalance = float(currentELbalance) - float(earnedleavecount)
 
    d[employeenumber]['earned leave'] = newELbalance
    save_data()

def delete_earned_leave(employeenumber):

 
    print(d[employeenumber]['Earned leave list'])
    delete_el = input("Enter date in dd-mm-yyyy format: ")
    delete_el_date = datetime.datetime.strptime(delete_el, "%d-%m-%Y")
    delete_el_date_string = delete_el_date.strftime("%d-%m-%Y")
 
    if delete_el_date_string in d[employeenumber]['Earned leave list']:
        update_earned_leave(employeenumber, -1)
        earnedleave = delete_el_date.strftime("%d-%m-%Y")
    else:
        print("Entered date is not present")
        return
 
    d[employeenumber]['Earned leave list'].remove(earnedleave)
    save_data()

def add_earned_leave(employeenumber):
    print(d[employeenumber]['earned leave'])
    print(d[employeenumber]['Earned leave list'])

    earned_leave_list_string = d[employeenumber]['Earned leave list']
    earned_leave_list = []

    start_el = input("Enter start date in dd-mm-yyyy format: ")
    start_el_date = datetime.datetime.strptime(start_el, "%d-%m-%Y") 

    if start_el_date.strftime("%d-%m-%Y") in earned_leave_list_string:
        print("Earned leave already entered")
        return
    end_el = input("Enter end date in dd-mm-yyyy format: ")
    end_el_date = datetime.datetime.strptime(end_el, "%d-%m-%Y")
    
  
    no_of_days = numOfDays(start_el_date, end_el_date)+1
  
    update_earned_leave(employeenumber, no_of_days)
   
    print(no_of_days)
    for dt in daterange(start_el_date, end_el_date):
        earned_leave_list.append(dt)
    for dt in earned_leave_list:
        date_string = dt.strftime('%d-%m-%Y')
        earned_leave_list_string.append(date_string)           
    d[employeenumber]['Earned leave list'] = earned_leave_list_string 
    save_data()

def add_sick_leave(employeenumber):
    
    print("Current SL count for employee", d[employeenumber]['sick leave'])
    dict_sick_leave_list = d[employeenumber]['sick leave dict'].keys()
    print(dict_sick_leave_list)
    type_SL = input("Enter whether full or half pay SL: ")

    start_sl = input("Enter start date in dd-mm-yyyy format: ")
    start_sl_date = datetime.datetime.strptime(start_sl, "%d-%m-%Y")
    
    if start_sl_date.strftime("%d-%m-%Y") in dict_sick_leave_list:
        print("Sick leave already entered")
        return
    #if type_SL == "half":
    #    end_sl = ""
    #else:
    end_sl = input("Enter end date: ")
    
    if end_sl == "":
        end_sl_date = start_sl_date
    elif end_sl != "":
         end_sl_date = datetime.datetime.strptime(end_sl, "%d-%m-%Y")

    no_of_days = numOfDays(start_sl_date, end_sl_date)+1
    
    if type_SL == "full":
        update_sick_leave(employeenumber, no_of_days*2)
    elif type_SL == "half":
        update_sick_leave(employeenumber, no_of_days)
    
    sick_leave_list = []
    dict_sick_leave = d[employeenumber]['sick leave dict']
    local_dict = {}
    if end_sl_date == start_sl_date:
        start_sl_date_string = start_sl_date.strftime('%d-%m-%Y')
        local_dict.update({start_sl_date_string: type_SL})
    else:
       for dt in daterange(start_sl_date, end_sl_date):
           sick_leave_list.append(dt)
    for dt in sick_leave_list:
        date_string = dt.strftime('%d-%m-%Y')
        local_dict.update({date_string: type_SL})   
    
    d[employeenumber]['sick leave dict'].update(local_dict)
    save_data()

def delete_sick_leave(employeenumber):
    
    print(d[employeenumber]['sick leave dict'])
    delete_sl = input("Enter date in dd-mm-yyyy format: ")
    delete_sl_date = datetime.datetime.strptime(delete_sl, "%d-%m-%Y")
    delete_sl_date_string = delete_sl_date.strftime("%d-%m-%Y")

    if delete_sl_date_string in d[employeenumber]['sick leave dict'].keys():
        sickleave = delete_sl_date.strftime("%d-%m-%Y")
    else:
        print("Entered date is not present")
        return
    if d[employeenumber]['sick leave dict'][sickleave] == "half":
        update_risk_leave(employeenumber, -1)

    else:
        update_sick_leave(employeenumber, -2)
    d[employeenumber]['sick leave dict'].pop(sickleave)
    save_data()

def update_sick_leave(employeenumber, sickleavecount):
    
    currentsickbalance = d[employeenumber]['sick leave']
    newsickbalance = float(currentsickbalance) - float(sickleavecount)
 
    d[employeenumber]['sick leave'] = newsickbalance
    save_data()

def leave_encashment(emp_no):

    print("Current earned leave count for %s is %d." % (emp_no, d[emp_no]['earned leave']))
    block_year = input("Block year for which leave is being encashed (Enter in YYYY-YYYY format - eg. 2022-2023): ")
    #no_of_days = input("How many days earned leave is encashed? ")
    local_dict = {}
    #local_dict.update({block_year: no_of_days})
    if block_year not in d[emp_no]['Leave encashment'].keys():
        no_of_days = input("How many days earned leave is encashed? ")
        if int(no_of_days) > 15:
            no_of_days = 15
        local_dict.update({block_year: no_of_days})
        update_earned_leave(emp_no, no_of_days)
        d[emp_no]['Leave encashment'].update(local_dict)
    else:
        print("Block year already entered.")
    save_data()

def del_leave_encashment(emp_no):

    print(d[emp_no]['Leave encashment'])
    block_year = input("Enter block year in YYYY-YYYY (eg. 2022-2023) format: ")

    if block_year in d[emp_no]['Leave encashment'].keys():
        no_of_days = d[emp_no]['Leave encashment'][block_year] 
        int_no_days = int(no_of_days) * -1
        d[emp_no]['Leave encashment'].pop(block_year)
        update_earned_leave(emp_no, int_no_days)
    else:
        print("Entered block year is not present.")

    save_data()

def add_rh_leave(emp_no):
    print(d[emp_no]['RH'])
    
    #string_leave_type_list = leave_type + "list"
    rh_list = d[emp_no]["RH list"]

    start_rh = input("Enter start date in dd-mm-yyyy format: ")
    start_date_rh = datetime.datetime.strptime(start_rh, "%d-%m-%Y")
    
    if start_date_rh.strftime("%d-%m-%Y") in rh_list:
        print("Restricted holiday already entered.")
    else:
        date_string = start_date_rh.strftime('%d-%m-%Y')
        rh_list.append(date_string)
        update_rh_leave(emp_no,1)
    save_data()

def update_rh_leave(emp_no, no_of_days):
    
    current_balance_rh = d[emp_no]['RH']
    new_balance_rh = int(current_balance_rh) - int(no_of_days)

    d[emp_no]['RH'] = new_balance_rh


def del_rh_leave(emp_no):

    print(d[emp_no]['RH list'])
    delete_el = input("Enter date in dd-mm-yyyy format: ")
    delete_el_date = datetime.datetime.strptime(delete_el, "%d-%m-%Y")
    delete_el_date_string = delete_el_date.strftime("%d-%m-%Y")
 
    if delete_el_date_string in d[emp_no]['RH list']:
        update_rh_leave(emp_no, -1)
        earnedleave = delete_el_date.strftime("%d-%m-%Y")
    else:
        print("Entered date is not present")
        return 
    d[emp_no]['RH list'].remove(earnedleave)

def req_emp_no():
    print("Employees already present", d.keys())
    while True:

        user_input = input("Enter employee number: ")
        if user_input not in d.keys():
            print("Employee number not in record. Enter again.")
        else:
            return user_input

def new_year_reset():
    employeelist = d.keys()
    for i in employeelist:

        d[i]['casual leave'] = 12
        d[i]['casual leave dict'] = {}
        d[i]['RH'] = 2
        if (int(d[i]['sick leave']) + 30) > 240:
            d[i]['sick leave'] = 240
        else:
            update_sick_leave(i, -30)
    save_data()

def calculate_el():
    today = datetime.datetime.now()
    today_string = today.strftime("%d-%m-%Y")
#    print(today)
    employeelist = d.keys()
    for i in employeelist:
        
        doj = d[i]['Leave updated as on']
        doj_datetime = datetime.datetime.strptime(doj, "%d-%m-%Y")
        no_of_days = numOfDays(doj_datetime,today)   
        sick_leave_taken = len(d[i]['sick leave dict'])
        
        current_leave_count = d[i]['earned leave']
        earned_leave_count = len(d[i]['Earned leave list'])
        earnedleavedays = no_of_days - int(sick_leave_taken) - earned_leave_count
        accruedleaves = earnedleavedays / 11
        new_el_count = float(accruedleaves) + float(current_leave_count)
        #print()
        if new_el_count > 270:
            new_el_count = 270
        if d[i]['Leave updated as on'] != today_string:
            d[i]['earned leave'] = new_el_count
        d[i]['Leave updated as on'] = today_string
    save_data()

def save_data():
    a_file = open("data.json", "w")
    json.dump(d,a_file)

    a_file.close()

def backup_data():
    date = datetime.datetime.now()
    backup_file_name = "data" + str(date) +".json"

    backup_file = open(backup_file_name, "w")


def employeeloop(empno, choice):
    
    if choice == "1":
        print(d[empno])
    elif choice == "2":
        add_casual_leave(empno)
    elif choice == "3":
        add_earned_leave(empno)
    elif choice == "4":
        add_sick_leave(empno)
    elif choice == "5":
        leave_encashment(empno)
    elif choice == "6":
        add_rh_leave(empno)
    elif choice == "7":
        leave_input = input("""
Enter 1 to delete casual leave.
Enter 2 to delete earned leave.
Enter 3 to delete sick leave.
Enter 4 to delete Restricted holiday.
Enter 5 to delete leave encashment.
        """)
        if leave_input == "1":
            delete_casual_leave(empno)
        elif leave_input == "2":
            delete_earned_leave(empno)
        elif leave_input == "3":
            delete_sick_leave(empno)
        elif leave_input == "4":
            # TODO
            del_rh_leave(empno)
            #print("awaited shortly")
        elif leave_input == "5":
            del_leave_encashment(empno)

    elif choice == "8":
        delete_employee(empno)

def keep_it_going(options):

    if options == "2":
        create_employee()
    if options == "1":
        print(d)
    if options == "4":
        new_year_reset()
    if options == "5":
        calculate_el()
    if options == "3":
        emp_no = req_emp_no()
        while(True):
            newoptions = input("""
  Press 1 to view current leave status.
  Press 2 to enter casual leave.
  Press 3 to enter earned leave.
  Press 4 to enter sick leave.
  Press 5 to enter leave encashment.
  Press 6 to enter Restricted holiday.
  Press 7 to delete already earned casual, earned or sick leave.
  Press 8 to delete the employee.
  Press 9 to return back to main menu.
Enter your choice: """)
            if newoptions != "9":
                employeeloop(emp_no, newoptions)
            else:
                break


while(True):
    
    options = input("""Choose your options:
 Press 1 to display all employees and their current leave status.
 Press 2 to create a new employee master.
 Press 3 to view, modify or delete employee's records.
 Press 4 to execute new year leave replenishment.
 Press 5 to calculate current EL.
 Press 9 to exit the program.
Enter your option: """)
    if options != "9":
        keep_it_going(options)
    else:
        break

def save_data():
    a_file = open("data.json", "w")
    json.dump(d,a_file)

    a_file.close()

def backup_data():
    date = datetime.datetime.now()
    backup_file_name = "data" + str(date) +".json"

    backup_file = open(backup_file_name, "w")

    json.dump(d,backup_file)

save_data()
backup_data()

df = pd.DataFrame.from_dict({(i): d[i]
    for i in d.keys()},
    orient='index')

print(df)
df.to_excel("leave-data.xlsx")
