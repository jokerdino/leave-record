import json

#from pprint import pprint
from json.decoder import JSONDecodeError
from datetime import timedelta
import datetime
import pandas as pd
from fractions import Fraction

from contextlib import redirect_stdout

try:
    f = open('data.json')
    try:
        d = json.load(f)
    except JSONDecodeError:
        d = {}
        pass
except FileNotFoundError:
    d = {}
    pass

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

def numOfDays(date1, date2):
    return (date2-date1).days

def validate_employee_number():
    while True:
        print("Employees already present in database: ",  d.keys())
        employeeNumber_input = input("Enter new employee number: ")
        if employeeNumber_input not in d.keys():
            print("Accepted")
            return employeeNumber_input
        else:
            print("Employee number already exists. Enter unique employee number.")

def update_employee(emp_no, update_type, update):

    d[emp_no][update_type] = update

    print("%s has been updated to %s." % (update_type, update))
    save_data()

def create_employee():

    employee_number = validate_employee_number()
    employee_name = input("Enter name of the employee: ")
    DOJ = input("Leave record last updated on:  Enter date in dd-mm-yyyy format: ")

    casual_leave = input("Enter current casual leave: ")
    casual_leave = min(int(casual_leave), 12)

    earned_leave = input("Enter current earned leave: ")
    earned_leave = min(int(earned_leave),270)

    sick_leave = input("Enter current sick leave: ")
    sick_leave = min(int(sick_leave),240)

    RH = input("Enter current RH count: ")
    RH = min(int(RH),2)

    d.update({employee_number:{
        "name": employee_name,
        "employee number" : employee_number,
        "Leave updated as on" : DOJ,
        "casual leave": casual_leave,
        "earned leave" : earned_leave,
        "sick leave" : sick_leave,
        "RH": RH,
        "casual leave dict": {},
        "RH list": [],
        "Earned leave list": [],
        "sick leave dict": {},
        "Special leave list":{},
        "LOP":{},
        "Leave encashment": {}
        }
    }
    )
    save_data()
    print("Employee %s with employee number %s has been created." % (employee_name, employee_number))
    display_emp(employee_number)

def update_leave(emp_no, leave_type, no_of_days):

    current_balance = d[emp_no][leave_type]
    newbalance = float(current_balance) - float(no_of_days)

    d[emp_no][leave_type] = newbalance
    save_data()
    print("%s has been updated. New balance: %s" % (leave_type, newbalance))

def del_casual_leave(emp_no):

    print(d[emp_no]['casual leave dict'])
    delete_cl = input("Enter date in dd-mm-yyyy format: ")
    delete_cl_date = datetime.datetime.strptime(delete_cl, "%d-%m-%Y")
    delete_cl_date_string = delete_cl_date.strftime("%d-%m-%Y")

    if delete_cl_date_string in d[emp_no]['casual leave dict'].keys():
        casualleave = delete_cl_date.strftime("%d-%m-%Y")
    else:
        print("Entered date is not present.")
        return
    if d[emp_no]['casual leave dict'][casualleave] == "half":
        update_leave(emp_no, "casual leave", -0.5)

    else:
        update_leave(emp_no, "casual leave", -1)
    d[emp_no]['casual leave dict'].pop(casualleave)
    save_data()
    print("%s has been deleted from casual leave list." % delete_cl)

def check_leave_count(emp_no, leave_type, no_of_days):
    current_leave_balance = d[emp_no][leave_type]

    if (int(current_leave_balance) - no_of_days) < 0:
        print("Insufficient leave balance.")
        return False

def add_casual_leave(emp_no):

    print("Current CL count for employee", d[emp_no]['casual leave'])
    dict_casual_leave_list = d[emp_no]['casual leave dict'].keys()
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

    if check_leave_count(emp_no,"casual leave",no_of_days) is False:
        return

    if type_CL == "full":
        update_leave(emp_no, "casual leave", no_of_days)
    elif type_CL == "half":
        update_leave(emp_no, "casual leave", no_of_days/2)

    casual_leave_list = []

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

    d[emp_no]['casual leave dict'].update(local_dict)
    save_data()
    print("Casual leave has been added.")

def delete_employee(emp_no):
    backup_data()
    d.pop(emp_no)
    print("Employee number %s has been deleted." %emp_no)
    save_data()

def del_list_leave(emp_no, leave_type, leave_list):
    """Function to delete leaves stored in list type: earned leave and Restricted holiday"""
    print(d[emp_no][leave_type])
    print(d[emp_no][leave_list])
    delete_leave = input("Enter date in dd-mm-yyyy format: ")
    delete_leave_date = datetime.datetime.strptime(delete_leave, "%d-%m-%Y")
    delete_leave_date_string = delete_leave_date.strftime("%d-%m-%Y")

    if delete_leave_date_string in d[emp_no][leave_list]:
        update_leave(emp_no, leave_type, -1)
        leave_to_be_removed = delete_leave_date.strftime("%d-%m-%Y")
    else:
        print("Entered date is not present.")
        return
    d[emp_no][leave_list].remove(leave_to_be_removed)

    print("%s %s has been deleted." % (leave_type, delete_leave))

def add_earned_leave(emp_no):
    print(d[emp_no]['earned leave'])
    print(d[emp_no]['Earned leave list'])

    earned_leave_list_string = d[emp_no]['Earned leave list']
    earned_leave_list = []

    start_el = input("Enter start date in dd-mm-yyyy format: ")
    start_el_date = datetime.datetime.strptime(start_el, "%d-%m-%Y")

    if start_el_date.strftime("%d-%m-%Y") in earned_leave_list_string:
        print("Earned leave already entered.")
        return
    end_el = input("Enter end date in dd-mm-yyyy format: ")
    end_el_date = datetime.datetime.strptime(end_el, "%d-%m-%Y")


    no_of_days = numOfDays(start_el_date, end_el_date)+1
    if check_leave_count(emp_no,"earned leave",no_of_days) is False:
        return

    update_leave(emp_no, "earned leave", no_of_days)

    print(no_of_days)
    for dt in daterange(start_el_date, end_el_date):
        earned_leave_list.append(dt)
    for dt in earned_leave_list:
        date_string = dt.strftime('%d-%m-%Y')
        earned_leave_list_string.append(date_string)
    d[emp_no]['Earned leave list'] = earned_leave_list_string
    save_data()
    print("Earned leave has been added.")

def add_sick_leave(emp_no):

    print("Current SL count for employee", d[emp_no]['sick leave'])
    dict_sick_leave_list = d[emp_no]['sick leave dict'].keys()
    print(dict_sick_leave_list)
    type_SL = input("Enter whether full or half pay SL: ")

    start_sl = input("Enter start date in dd-mm-yyyy format: ")
    start_sl_date = datetime.datetime.strptime(start_sl, "%d-%m-%Y")

    if start_sl_date.strftime("%d-%m-%Y") in dict_sick_leave_list:
        print("Sick leave already entered")
        return
    end_sl = input("Enter end date: ")

    if end_sl == "":
        end_sl_date = start_sl_date
    elif end_sl != "":
        end_sl_date = datetime.datetime.strptime(end_sl, "%d-%m-%Y")

    no_of_days = numOfDays(start_sl_date, end_sl_date)+1

    if check_leave_count(emp_no,"sick leave",no_of_days) is False:
        return
    if type_SL == "full":
        update_leave(emp_no, "sick leave", no_of_days*2)
    elif type_SL == "half":
        update_leave(emp_no, "sick leave", no_of_days)

    sick_leave_list = []

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

    d[emp_no]['sick leave dict'].update(local_dict)
    save_data()
    print("Sick leave has been added.")

def del_sick_leave(emp_no):

    print(d[emp_no]['sick leave dict'])
    delete_sl = input("Enter date in dd-mm-yyyy format: ")
    delete_sl_date = datetime.datetime.strptime(delete_sl, "%d-%m-%Y")
    delete_sl_date_string = delete_sl_date.strftime("%d-%m-%Y")

    if delete_sl_date_string in d[emp_no]['sick leave dict'].keys():
        sickleave = delete_sl_date.strftime("%d-%m-%Y")
    else:
        print("Entered date is not present.")
        return
    if d[emp_no]['sick leave dict'][sickleave] == "half":
        update_leave(emp_no,"sick leave", -1)

    else:
        update_leave(emp_no, "sick leave", -2)
    d[emp_no]['sick leave dict'].pop(sickleave)
    save_data()
    print("%s has been deleted." % delete_sl)

def leave_encashment(emp_no):

    print("Current earned leave count for %s is %s" % (emp_no, d[emp_no]['earned leave']))
    block_year = input("Block year for which leave is being encashed (Enter in YYYY-YYYY format - eg. 2022-2023): ")
    local_dict = {}

    if block_year not in d[emp_no]['Leave encashment'].keys():
        no_of_days = input("How many days earned leave is encashed? ")
        if int(no_of_days) > 15:
            no_of_days = 15
        if check_leave_count(emp_no,"earned leave",no_of_days) is False:
            return
        local_dict.update({block_year: no_of_days})
        update_leave(emp_no, "earned leave",no_of_days)
        d[emp_no]['Leave encashment'].update(local_dict)
        print("Block year %s has been entered." % (block_year))
    else:
        print("Block year %s has already been entered." % block_year)
    save_data()

def del_leave_encashment(emp_no):

    print(d[emp_no]['Leave encashment'])
    block_year = input("Enter block year in YYYY-YYYY (eg. 2022-2023) format: ")

    if block_year in d[emp_no]['Leave encashment'].keys():
        no_of_days = d[emp_no]['Leave encashment'][block_year]
        int_no_days = int(no_of_days) * -1
        d[emp_no]['Leave encashment'].pop(block_year)
        update_leave(emp_no, "earned leave", int_no_days)
        print("Block year %s has been deleted." % block_year)
    else:
        print("Entered block year is not present.")

    save_data()

def add_rh_leave(emp_no):
    print(d[emp_no]['RH'])

    rh_list = d[emp_no]["RH list"]

    start_rh = input("Enter start date in dd-mm-yyyy format: ")
    start_date_rh = datetime.datetime.strptime(start_rh, "%d-%m-%Y")

    if start_date_rh.strftime("%d-%m-%Y") in rh_list:
        print("Restricted holiday already entered.")
    else:
        date_string = start_date_rh.strftime('%d-%m-%Y')
        if check_leave_count(emp_no,"RH",1) is False:
            return
        rh_list.append(date_string)
        update_leave(emp_no,"RH", 1)
    save_data()
    print("Restricted holiday has been added.")

def add_LOP_leave(emp_no):

    dict_sick_leave_list = d[emp_no]['LOP'].keys()
    print(dict_sick_leave_list)
    type_SL = input("Enter whether LOP or strike: ")

    start_sl = input("Enter start date in dd-mm-yyyy format: ")
    start_sl_date = datetime.datetime.strptime(start_sl, "%d-%m-%Y")

    if start_sl_date.strftime("%d-%m-%Y") in dict_sick_leave_list:
        print("This date has already been entered.")
        return
    end_sl = input("Enter end date: ")

    if end_sl == "":
        end_sl_date = start_sl_date
    elif end_sl != "":
        end_sl_date = datetime.datetime.strptime(end_sl, "%d-%m-%Y")


    sick_leave_list = []

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

    d[emp_no]['LOP'].update(local_dict)

    print("%s has been added." % type_SL)

def del_leave(emp_no, leave_type):

    print(d[emp_no][leave_type])
    delete_sl = input("Enter date in dd-mm-yyyy format: ")
    delete_sl_date = datetime.datetime.strptime(delete_sl, "%d-%m-%Y")
    delete_sl_date_string = delete_sl_date.strftime("%d-%m-%Y")

    if delete_sl_date_string in d[emp_no][leave_type].keys():
        sickleave = delete_sl_date.strftime("%d-%m-%Y")
    else:
        print("Entered date is not present")
        return
    d[emp_no][leave_type].pop(sickleave)
    save_data()

    print("%s has been deleted." % delete_SL)

def add_special_leave(emp_no):

    print("Current SL count for employee", d[emp_no]['Special leave list'])
    dict_sick_leave_list = d[emp_no]['Special leave list'].keys()
    print(dict_sick_leave_list)
    type_SL = input("Enter the type of special leave (eg. Maternity leave, Paternity leave, Examination leave, Quantantine leave, etc): ")

    start_sl = input("Enter start date in dd-mm-yyyy format: ")
    start_sl_date = datetime.datetime.strptime(start_sl, "%d-%m-%Y")

    if start_sl_date.strftime("%d-%m-%Y") in dict_sick_leave_list:
        print("Special leave already entered")
        return
    end_sl = input("Enter end date: ")

    if end_sl == "":
        end_sl_date = start_sl_date
    elif end_sl != "":
        end_sl_date = datetime.datetime.strptime(end_sl, "%d-%m-%Y")

    sick_leave_list = []

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

    d[emp_no]['Special leave list'].update(local_dict)
    print("Special leave has been added.")

def req_emp_no():

    print("Employees already present", d.keys())

    if len(d) != 0:
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
            update_leave(i, "sick leave",-30)
    save_data()

def calculate_el():
    today = datetime.datetime.now()
    today_string = today.strftime("%d-%m-%Y")

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
        new_el_count = min(new_el_count,270)

        if d[i]['Leave updated as on'] != today_string:
            d[i]['earned leave'] = new_el_count
        d[i]['Leave updated as on'] = today_string
    save_data()

def report_leave(date):

    emp_list = d.keys()

    print("List of employees who were absent on %s." % date)
    for i in emp_list:
        leave_type = ['Earned leave list','RH list']
        dict_type = ['casual leave dict', 'Special leave list','LOP','sick leave dict']
        for j in leave_type:
            if date in d[i][j]:
                print("Name: %s. Type of leave: %s" % (str(d[i]['name']), j))
        for j in dict_type:
            if date in d[i][j]:
                print("Name: %s. Type of leave: %s Nature of leave: %s" % (str(d[i]['name']), j, d[i][j][date]))

def report_lop(leave_type,lop_choice):
    emp_list = d.keys()

    print("List of employees who are on %s: " % lop_choice)
    for i in emp_list:
        for j in d[i][leave_type].keys():

            if d[i][leave_type][j] == lop_choice:
                print("Name: %s. Date: %s" % (d[i]['name'], j))

def dec_to_proper_frac(emp_no):

    earned_leave = float(d[emp_no]['earned leave'])

    if not (earned_leave).is_integer():

        a = int(earned_leave)
        new = earned_leave - a
        b = Fraction(new % 11).limit_denominator(100)
        fraction = str(a)+" "  + str(b)
        return fraction
    else:
        return earned_leave

def export_to_text(emp_no):


    date = datetime.datetime.now()
    emp_name = d[emp_no]['name']
    file_name = emp_name+emp_no + str(date)+".txt"

    with open(file_name, 'w') as f:
        with redirect_stdout(f):

            display_emp(emp_no)
    print("Leave data of %s has been exported to text file." % emp_no)

def display_emp(emp_no):

    frac_earned_leave = dec_to_proper_frac(emp_no)

    leave_encashment_status = ""
    if len(d[emp_no]['Leave encashment']) == 0:
        leave_encashment_status = "Leave encashment not availed"
    else:
        block = list(d[emp_no]['Leave encashment'].keys())[-1]
        leave_encashment_status = "Leave encashment last availed for the block year " + block

    print("""=========================================================================
Employee name                      : %s
Employee number                    : %s
Current Casual leave balance       : %s
Current EL balance                 : %s
Leave encashment                   : %s.
Current sick leave balance         : %s
Current Restricted holiday balance : %s
List of casual leaves              : %s
List of earned leaves              : %s
List of sick leaves                : %s
List of RH                         : %s
List of LOP                        : %s
List of special leaves             : %s
=========================================================================
    """ % (d[emp_no]['name'], d[emp_no]['employee number'], d[emp_no]['casual leave'], frac_earned_leave, leave_encashment_status, d[emp_no]['sick leave'], d[emp_no]['RH'], d[emp_no]['casual leave dict'], d[emp_no]['Earned leave list'],d[emp_no]['sick leave dict'],d[emp_no]['RH list'], d[emp_no]['LOP'],d[emp_no]['Special leave list'] ))

def save_data():
    a_file = open("data.json", "w")
    json.dump(d,a_file)

    a_file.close()

def backup_data():
    date = datetime.datetime.now()
    backup_file_name = "data" + str(date) +".json"

    #json.dump(d,backup_file_name)
    open(backup_file_name, "w") #ais f:
    #.write(d)

def employeeloop(empno, choice):

    if choice == "1":

        #print(d[empno])
        display_emp(empno)
    elif choice == "2":
        add_casual_leave(empno)
    elif choice == "3":
        add_earned_leave(empno)
    elif choice == "4":
        add_sick_leave(empno)
    elif choice == "8":
        export_to_text(empno)
    elif choice == "5":
        leave_input = input("""
 Press 1 to enter leave encashment.
 Press 2 to enter restricted holiday.
 Press 3 to enter LOP or strike.
 Press 4 to enter Special leave (eg. Examination leave, Maternity leave, paternity leave, quarantine leave, etc.)
 Press 9 to return to previous menu.
Enter your option:
  """)

        if leave_input == "1":
            leave_encashment(empno)
        elif leave_input == "2":
            add_rh_leave(empno)

        elif leave_input == "3":
            add_LOP_leave(empno)
        elif leave_input == "4":
            add_special_leave(empno)
        else:
            return
    elif choice == "6":
        leave_input = input("""
 Press 1 to delete casual leave.
 Press 2 to delete earned leave.
 Press 3 to delete sick leave.
 Press 4 to delete Restricted holiday.
 Press 5 to delete leave encashment.
 Press 6 to delete LOP / Strike.
 Press 7 to delete Special leave.
 Press 9 to return to previous menu.
Enter your option:
""")
        if leave_input == "1":
            del_casual_leave(empno)
        elif leave_input == "2":
            del_list_leave(empno,"earned leave","Earned leave list")
        elif leave_input == "3":
            del_sick_leave(empno)
        elif leave_input == "4":
            del_list_leave(empno,"RH", "RH list")
        elif leave_input == "5":
            del_leave_encashment(empno)
        elif leave_input == "6":
            del_leave(empno,"LOP")
        elif leave_input == "7":
            del_leave(empno,"Special leave list")
        else:
            return
    else:
        return

def reports():

    report_options = input("""
Press 1 to display all the employees who were on leave on a particular day.
Press 2 to display all the employees who are on LOP / strike.
Press 3 to display all the employees who took half pay sick leave.
Enter your choice: """)
    if report_options == "1":
        date = input("Enter the date in dd-mm-yyyy format: ")
        report_leave(date)
    if report_options == "2":
        lop_choice = input("Enter the type (Choose between LOP and strike): ")
        report_lop('LOP',lop_choice)
    if report_options == "3":
        report_lop('sick leave dict','half')

def keep_it_going(options):

    if options == "2":
        create_employee()
    if options == "1":
        for i in d.keys():
            display_emp(i)
    if options == "6":
        for i in d.keys():
            export_to_text(i)
        return
    if options == "4":
        new_year_reset()
    if options == "5":
        calculate_el()
    if options == "8":
        update_emp = req_emp_no()
        update_choice = input("""What do you want to update?
Press 1 to update name.
Press 2 to update employee number.
Press 3 to update casual leave.
Press 4 to update earned leave.
Press 5 to update sick leave.
Press 6 to update RH.
Enter your choice: """)
        if update_choice == "1":
            change = input("Enter new name: ")
            update_employee(update_emp,"name", change)
        elif update_choice == "2":
            change = validate_employee_number()
            update_employee(update_emp,"employee number", change)
            d[change] = d[update_emp]
            d.pop(update_emp)
        elif update_choice == "3":
            change = input("Enter new casual leave count: ")
            update_employee(update_emp,"casual leave", min(12,int(change)))
        elif update_choice == "4":
            change = input("Enter new earned leave count: ")
            update_employee(update_emp,"earned leave", min(270,int(change)))
        elif update_choice == "5":
            change = input("Enter new sick leave count: ")
            update_employee(update_emp,"sick leave", min(240,int(change)))
        elif update_choice == "6":
            change = input("Enter new RH count: ")
            update_employee(update_emp,"RH", min(2,int(change)))
        else:
            return
    if options == "7":
        reports()
    if options == "3":
        if (len(d) != 0):
            emp_no = req_emp_no()
            while True:
                newoptions = input("""
  Press 1 to view current leave status.
  Press 2 to enter casual leave.
  Press 3 to enter earned leave.
  Press 4 to enter sick leave.
  Press 5 to enter misc. leaves (eg. Restricted holidays, LOP, leave encashment and special leaves).
  Press 6 to delete already entered casual, earned, sick leave or RH.
  Press 7 to delete the employee.
  Press 8 to export data to text file.
  Press 9 to return back to main menu.
Enter your choice: """)
                if newoptions == "7":
                    delete_employee(emp_no)
                    return
                elif newoptions != "9":
                    employeeloop(emp_no, newoptions)
                else:
                    break
        else:
            print("No employees present")

def leave_program():

    while True:

        options = input("""Choose your options:
Press 1 to display all employees and their current leave status.
Press 2 to create a new employee master.
Press 3 to view, modify or delete employee's records.
Press 4 to execute new year leave replenishment.
Press 5 to calculate current EL.
Press 6 to export leave data to text file.
Press 7 to generate reports.
Press 8 to modify employee meta data.
Press 9 to exit the program.
Enter your option: """)
        if options != "9":
            keep_it_going(options)
        else:
            break

leave_program()

save_data()
backup_data()

df = pd.DataFrame.from_dict({(i): d[i]
    for i in d.keys()},
    orient='index')

print(df)
df.to_excel("leave-data.xlsx")
