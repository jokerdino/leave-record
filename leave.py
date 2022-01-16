import json


from json.decoder import JSONDecodeError
from datetime import timedelta
import datetime
import pandas as pd
from fractions import Fraction

from contextlib import redirect_stdout

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

    employee_number = validate_employee_number()
    employee_name = input("Enter name of the employee: ")
    DOJ = input("Leave record last updated on:  Enter date in dd-mm-yyyy format: ")
           # When was the leave record last updated on:  in dd-mm-yyyy format: ")
    casual_leave = input("Enter current casual leave: ")
    if int(casual_leave) > 12:
        casual_leave = 12
    earned_leave = input("Enter current earned leave: ")
    if int(earned_leave) > 270:
        earned_leave = 270
    sick_leave = input("Enter current sick leave: ")
    if int(sick_leave) > 240:
        sick_leave = 240
    RH = input("Enter current RH count: ")
    if int(RH) > 2:
        RH = 2
    #DOJ_date = datetime.datetime.strptime(DOJ, "%d-%m-%Y")
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
        "Quarantine leave list":[],
        "Special leave list":{},
        "LOP":{},
        "Leave encashment": {}
        }
    }
    )
    save_data()


def update_leave(emp_no, leave_type, no_of_days):

    current_balance = d[emp_no][leave_type]
    newbalance = float(current_balance) - float(no_of_days)

    d[emp_no][leave_type] = newbalance
    save_data()


def delete_casual_leave(employeenumber):

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
        update_leave(employeenumber, "casual leave", -0.5)

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
        update_leave(employeenumber, "casual leave", no_of_days)
    elif type_CL == "half":
        update_leave(employeenumber, "casual leave", no_of_days/2)

    casual_leave_list = []
    #dict_casual_leave = d[employeenumber]['casual leave dict']
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
    print("Employee number %s deleted" %employeenumber)
    save_data()

def delete_earned_leave(employeenumber):

    print(d[employeenumber]['Earned leave list'])
    delete_el = input("Enter date in dd-mm-yyyy format: ")
    delete_el_date = datetime.datetime.strptime(delete_el, "%d-%m-%Y")
    delete_el_date_string = delete_el_date.strftime("%d-%m-%Y")

    if delete_el_date_string in d[employeenumber]['Earned leave list']:
        update_leave(employeenumber, "earned leave", -1)
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

    update_leave(employeenumber, "earned leave", no_of_days)

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
    end_sl = input("Enter end date: ")

    if end_sl == "":
        end_sl_date = start_sl_date
    elif end_sl != "":
        end_sl_date = datetime.datetime.strptime(end_sl, "%d-%m-%Y")

    no_of_days = numOfDays(start_sl_date, end_sl_date)+1

    if type_SL == "full":
        update_leave(employeenumber, "sick leave", no_of_days*2)
    elif type_SL == "half":
        update_leave(employeenumber, "sick leave", no_of_days)

    sick_leave_list = []
    #dict_sick_leave = d[employeenumber]['sick leave dict']
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
        update_leave(employeenumber,"sick leave", -1)

    else:
        update_leave(employeenumber, "sick leave", -2)
    d[employeenumber]['sick leave dict'].pop(sickleave)
    save_data()

def leave_encashment(emp_no):

    print("Current earned leave count for %s is %s" % (emp_no, d[emp_no]['earned leave']))
    block_year = input("Block year for which leave is being encashed (Enter in YYYY-YYYY format - eg. 2022-2023): ")
    local_dict = {}

    if block_year not in d[emp_no]['Leave encashment'].keys():
        no_of_days = input("How many days earned leave is encashed? ")
        if int(no_of_days) > 15:
            no_of_days = 15
        local_dict.update({block_year: no_of_days})
        update_leave(emp_no, "earned leave",no_of_days)
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
        update_leave(emp_no, "earned leave", int_no_days)
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
        rh_list.append(date_string)
        update_leave(emp_no,"RH", 1)
    save_data()

def del_rh_leave(emp_no):

    print(d[emp_no]['RH list'])
    delete_el = input("Enter date in dd-mm-yyyy format: ")
    delete_el_date = datetime.datetime.strptime(delete_el, "%d-%m-%Y")
    delete_el_date_string = delete_el_date.strftime("%d-%m-%Y")

    if delete_el_date_string in d[emp_no]['RH list']:
        update_leave(emp_no, "RH", -1)
        earnedleave = delete_el_date.strftime("%d-%m-%Y")
    else:
        print("Entered date is not present")
        return
    d[emp_no]['RH list'].remove(earnedleave)

def add_LOP_leave(employeenumber):

    dict_sick_leave_list = d[employeenumber]['LOP'].keys()
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
    #dict_sick_leave = d[employeenumber]['LOP']
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

    d[employeenumber]['LOP'].update(local_dict)

def del_leave(employeenumber, leave_type):

    print(d[employeenumber][leave_type])
    delete_sl = input("Enter date in dd-mm-yyyy format: ")
    delete_sl_date = datetime.datetime.strptime(delete_sl, "%d-%m-%Y")
    delete_sl_date_string = delete_sl_date.strftime("%d-%m-%Y")

    if delete_sl_date_string in d[employeenumber][leave_type].keys():
        sickleave = delete_sl_date.strftime("%d-%m-%Y")
    else:
        print("Entered date is not present")
        return
    d[employeenumber][leave_type].pop(sickleave)
    save_data()


def add_special_leave(employeenumber):

    print("Current SL count for employee", d[employeenumber]['Special leave list'])
    dict_sick_leave_list = d[employeenumber]['Special leave list'].keys()
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

    #no_of_days = numOfDays(start_sl_date, end_sl_date)+1

    sick_leave_list = []
    #dict_sick_leave = d[employeenumber]['Special leave list']
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

    d[employeenumber]['Special leave list'].update(local_dict)

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
            update_sick_leave(i, -30)
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
        #if new_el_count > 270:
         #   new_el_count = 270
        if d[i]['Leave updated as on'] != today_string:
            d[i]['earned leave'] = new_el_count
        d[i]['Leave updated as on'] = today_string
    save_data()


from fractions import Fraction    

def dec_to_proper_frac(emp_no):

    earned_leave = float(d[emp_no]['earned leave'])
    
    a = int(earned_leave) #%// 11
    new = earned_leave - a
    b = Fraction(new % 11).limit_denominator(100)
    fraction = str(a)+" "  + str(b)#+"/11"
    return fraction

def export_to_text(emp_no):
   

    date = datetime.datetime.now()
    
    file_name = emp_no + str(date)+".txt"

    with open(file_name, 'w') as f:
        with redirect_stdout(f):

            display_emp(emp_no)


def display_emp(emp_no):
   
    frac_earned_leave = dec_to_proper_frac(emp_no)
    
    leave_encashment_status = ""
    if len(d[emp_no]['Leave encashment']) == 0:
        leave_encashment_status = "Leave encashment not availed."
    else:
        block = list(d[emp_no]['Leave encashment'].keys())[-1]
        leave_encashment_status = "Leave encashment last availed for the block year " + block
#    with open('stuff.txt', 'w') as f:
   #     with redirect_stdout(f):
    print("""=========================================================================
Employee name: %s
Employee number: %s
Current Casual leave balance: %s
Current EL balance: %s
Leave encashment: %s.
Current sick leave balance: %s
Current Restricted holiday balance: %s
List of casual leaves: %s
=========================================================================
    """ % (d[emp_no]['name'], d[emp_no]['employee number'], d[emp_no]['casual leave'], frac_earned_leave, leave_encashment_status, d[emp_no]['sick leave'], d[emp_no]['RH'], d[emp_no]['casual leave dict'] ))


def save_data():
    a_file = open("data.json", "w")
    json.dump(d,a_file)

    a_file.close()

def backup_data():
    date = datetime.datetime.now()
    backup_file_name = "data" + str(date) +".json"

    open(backup_file_name, "w")


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
            delete_casual_leave(empno)
        elif leave_input == "2":
            delete_earned_leave(empno)
        elif leave_input == "3":
            delete_sick_leave(empno)
        elif leave_input == "4":
            del_rh_leave(empno)
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


def keep_it_going(options):

    if options == "2":
        create_employee()
    if options == "1":
        for i in d.keys():
            display_emp(i)
        print(d)

    if options == "4":
        new_year_reset()
    if options == "5":
        calculate_el()
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
