# TODO:

# 1. fix earned leave calculation -- done
# 2. prettify the output
# 3. design a useable GUI
# 4. make the reports exportable to text file
# 5. improve the leave record exported text file -- preferably to PDF file if possible
# 6. optimise the code - avoid DRY (dont repeat yourself)
# 7. write a leave letter status module
# 8. write help strings for each function for clarify and easier maintenance
# 9. Validate for LOP and strikes -- done
# 10. validate for special leave type -- done
# 11. Move old year data to a different file to prevent clog up -- all data belonging to previous year can be moved to a different file etc
# 12. move backup data stuff to a different folder to prevent clog up of the whole directory

import json

import leave_program

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
        if employeeNumber_input.isnumeric():
            if employeeNumber_input not in d.keys():
                print("Accepted")
                return employeeNumber_input
            else:
                print("Employee number already exists. Enter unique employee number.")
        else:
            print("Please enter numbers only.")

def validate_date(date):

    try:
        date = datetime.datetime.strptime(date,"%d-%m-%Y")
        date = date.strftime("%d-%m-%Y")
    except ValueError:
        date = input('Incorrect format. Kindly enter the date in dd-mm-yyyy format: ')
        date = validate_date(date)
    return date

def validate_letters(letter):

    if letter.isascii() is False:
        letter = input("Kindly enter letters only: ")
        letter = validate_letters(letter)

    return letter

def update_employee(emp_no, update_type, update):

    d[emp_no][update_type] = update

    print("%s has been updated to %s." % (update_type, update))
    save_data()

def mixed_to_float(x):
    """Function credit to https://stackoverflow.com/a/46303199"""
    return float(sum(Fraction(term) for term in x.split()))

def create_employee():

    employee_number = validate_employee_number()

    employee_name = input("Enter name of the employee: ")
    employee_name = validate_letters(employee_name)

    DOJ = input("Leave record last updated on:  Enter date in dd-mm-yyyy format: ")
    DOJ = validate_date(DOJ)

    casual_leave = input("Enter current casual leave: ")
    casual_leave = max(0,min(int(casual_leave), 12))

    earned_leave = input("Enter current earned leave: ")
    print(mixed_to_float(earned_leave))
    earned_leave = mixed_to_float(earned_leave)
    earned_leave = max(0,(min(float(earned_leave),270)))

    sick_leave = input("Enter current sick leave: ")
    sick_leave = max(0,min(int(sick_leave),240))

    RH = input("Enter current RH count: ")
    RH = max(0,min(int(RH),2))

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
    if leave_type != "earned leave":

        print("%s has been updated. New balance: %s" % (leave_type, newbalance))
    elif leave_type == "earned leave":
        mixed_frac = dec_to_proper_frac(emp_no)
        print("%s has been updated. New balance: %s" % (leave_type, mixed_frac))

def del_casual_leave(emp_no):

    print(d[emp_no]['casual leave dict'])
    delete_cl = input("Enter date in dd-mm-yyyy format: ")
    delete_cl = validate_date(delete_cl)

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

    if (float(current_leave_balance) - float(no_of_days)) < 0:
        print("Insufficient leave balance.")
        return False

def add_casual_leave(emp_no):

    print("Current CL count for employee", d[emp_no]['casual leave'])
    dict_casual_leave_list = d[emp_no]['casual leave dict'].keys()
    print(dict_casual_leave_list)
    type_CL = input("Enter whether full or half CL: ")
    if type_CL != "half":
        type_CL = "full"

    #TODO: To validate full or half CL input
#    while True:
#        if type_CL != "full" or "half":
#            type_CL = input("Enter full or half: ")
#            if type_CL == "full" or "half":
#                break
#                #return type_CL
#        #else return

    start_cl = input("Enter start date in dd-mm-yyyy format: ")
    start_cl = validate_date(start_cl)

    start_cl_date = datetime.datetime.strptime(start_cl, "%d-%m-%Y")

    if start_cl_date.strftime("%d-%m-%Y") in dict_casual_leave_list:

        print("Casual leave already entered")
        return
    if type_CL == "half":
        end_cl = ""
    else:
        end_cl = input("Enter end date if there are more than one days, otherwise press enter: ")

    if end_cl == "":
        end_cl_date = start_cl_date
    elif end_cl != "":
        end_cl_ = validate_date(end_cl)
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
    delete_leave = validate_date(delete_leave)

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

    #mixed_frac = dec_to_proper_frac(emp_no)

    #print(mixed_frac)
    #print(d[emp_no]['earned leave'])
    print("Already entered earned leave for the employee is as follows: ",d[emp_no]['Earned leave list'])


    earned_leave_list_string = d[emp_no]['Earned leave list']
    earned_leave_list = []

    start_el = input("Enter start date in dd-mm-yyyy format: ")
    start_el = validate_date(start_el)

    start_el_date = datetime.datetime.strptime(start_el, "%d-%m-%Y")

    if start_el_date.strftime("%d-%m-%Y") in earned_leave_list_string:
        print("Earned leave already entered.")
        return
    end_el = input("Enter end date in dd-mm-yyyy format: ")
    end_el = validate_date(end_el)

    end_el_date = datetime.datetime.strptime(end_el, "%d-%m-%Y")

    no_of_days = numOfDays(start_el_date, end_el_date)+1

    # calculating the current leave balance before checking for sufficient leave balance
    calculate_el_emp(emp_no, start_el_date, end_el_date,True)

    doj = d[emp_no]['Leave updated as on']
    doj_datetime = datetime.datetime.strptime(doj, "%d-%m-%Y")

    if check_leave_count(emp_no,"earned leave",no_of_days) is False:
        cal_one_day_before = doj_datetime + timedelta(days=-1)
        cal_one_day_before_string = cal_one_day_before.strftime("%d-%m-%Y")
        d[emp_no]['Leave updated as on'] = cal_one_day_before_string
        return

    cal_el_date_string = end_el_date.strftime("%d-%m-%Y")

    d[emp_no]['Leave updated as on'] = cal_el_date_string

    update_leave(emp_no, "earned leave", no_of_days)

    #print(no_of_days)
    for dt in daterange(start_el_date, end_el_date):
        earned_leave_list.append(dt)
    for dt in earned_leave_list:
        date_string = dt.strftime('%d-%m-%Y')
        earned_leave_list_string.append(date_string)
    d[emp_no]['Earned leave list'] = earned_leave_list_string
    save_data()
    #print("Earned leave has been added.")

def add_sick_leave(emp_no):

    print("Current SL count for employee", d[emp_no]['sick leave'])
    dict_sick_leave_list = d[emp_no]['sick leave dict'].keys()
    print(dict_sick_leave_list)
    type_SL = input("Enter whether full or half pay SL: ")

    if type_SL != "half":
        type_SL = "full"
    #TODO: Validate full or half pay input in casual leave

    start_sl = input("Enter start date in dd-mm-yyyy format: ")
    start_sl = validate_date(start_sl)

    start_sl_date = datetime.datetime.strptime(start_sl, "%d-%m-%Y")

    if start_sl_date.strftime("%d-%m-%Y") in dict_sick_leave_list:
        print("Sick leave already entered")
        return
    end_sl = input("Enter end date or press enter for one day leave: ")

    if end_sl == "":
        end_sl_date = start_sl_date
    elif end_sl != "":
        end_sl = validate_date(end_sl)
        end_sl_date = datetime.datetime.strptime(end_sl, "%d-%m-%Y")

    no_of_days = numOfDays(start_sl_date, end_sl_date)+1
    if type_SL == "full":
        no_of_days = no_of_days * 2
    if check_leave_count(emp_no,"sick leave",no_of_days) is False:
        return
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
    delete_sl = validate_date(delete_sl)

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

    mixed_frac = dec_to_proper_frac(emp_no)
    print("Current earned leave count for %s is %s" % (emp_no, mixed_frac))
    block_year = input("Block year for which leave is being encashed (Enter in YYYY-YYYY format - eg. 2022-2023): ")
    local_dict = {}

    if block_year not in d[emp_no]['Leave encashment'].keys():
        day_of_encash = input("When was the leave encashed? Enter in dd-mm-yyyy format: ")
        day_of_encash = validate_date(day_of_encash)

        day_of_encash_date = datetime.datetime.strptime(day_of_encash,"%d-%m-%Y")
        day_of_encash_string = day_of_encash_date.strftime('%d-%m-%Y')

        no_of_days = input("How many days earned leave is encashed? ")

        while int(no_of_days) > 15:
        #if int(no_of_days) > 15:
            no_of_days = input("Maximum allowed days is 15. Please recheck and enter again: ")

        #no_of_days = min(int(no_of_days),15)

        day_of_encash_plus_one = day_of_encash_date + timedelta(days=1)
        calculate_el_emp(emp_no, day_of_encash_plus_one, day_of_encash_plus_one,True)

        doj = d[emp_no]['Leave updated as on']
        doj_datetime = datetime.datetime.strptime(doj, "%d-%m-%Y")

        day_of_encash_string = day_of_encash_date.strftime("%d-%m-%Y")

        if doj_datetime < day_of_encash_date:

            d[emp_no]['Leave updated as on'] = day_of_encash_string
        if check_leave_count(emp_no,"earned leave",int(no_of_days)) is False:
            return

        local_dict.update({block_year: no_of_days})
        update_leave(emp_no, "earned leave",no_of_days)
        d[emp_no]['Leave encashment'].update(local_dict)
        print("Block year %s has been entered." % (block_year))

        local_dict_special = {day_of_encash_string: "Leave encashment"}
        d[emp_no]['Special leave list'].update(local_dict_special)
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
    start_rh = validate_date(start_rh)

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
    input_type_SL = input("Enter 1 for LOP and 2 for Strike: ")

    if input_type_SL == "1":
        type_SL = "LOP"
    elif input_type_SL == "2":
        type_SL = "Strike"
    else:
        print("Received %s as input instead of 1 or 2. Assuming the entry to be LOP." %(input_type_SL))
        type_SL = "LOP"

    start_sl = input("Enter start date in dd-mm-yyyy format: ")
    start_sl = validate_date(start_sl)

    start_sl_date = datetime.datetime.strptime(start_sl, "%d-%m-%Y")

    if start_sl_date.strftime("%d-%m-%Y") in dict_sick_leave_list:
        print("This date has already been entered.")
        return
    end_sl = input("Enter end date if there are more than one days, otherwise press enter: ")

    if end_sl == "":
        end_sl_date = start_sl_date
    elif end_sl != "":
        end_sl = validate_date(end_sl)
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
    delete_sl = validate_date(delete_sl)

    delete_sl_date = datetime.datetime.strptime(delete_sl, "%d-%m-%Y")
    delete_sl_date_string = delete_sl_date.strftime("%d-%m-%Y")

    if delete_sl_date_string in d[emp_no][leave_type].keys():
        sickleave = delete_sl_date.strftime("%d-%m-%Y")
    else:
        print("Entered date is not present")
        return
    d[emp_no][leave_type].pop(sickleave)
    save_data()

    print("%s has been deleted." % delete_sl)

def add_special_leave(emp_no):

    print("Current SL count for employee", d[emp_no]['Special leave list'])
    dict_sick_leave_list = d[emp_no]['Special leave list'].keys()
    print(dict_sick_leave_list)
    input_type_SL = input("""Enter 1 for Maternity leave.
    Enter 2 for Paternity leave.
    Enter 3 for Quarantine leave.
    Enter 4 for Examination leave.
    Enter 5 for Others: """)

    if input_type_SL == "1":
        type_SL = "Maternity leave"
    elif input_type_SL == "2":
        type_SL = "Paternity leave"
    elif input_type_SL == "3":
        type_SL = "Quarantine leave"
    elif input_type_SL == "4":
        type_SL = "Examination leave"
    elif input_type_SL == "5":
        type_SL = "Others"
    else:
        print("Received %s as input instead of 1-5. Assuming the entry to be Others." %(input_type_SL))
        type_SL = "Others"

    start_sl = input("Enter start date in dd-mm-yyyy format: ")
    start_sl = validate_date(start_sl)

    start_sl_date = datetime.datetime.strptime(start_sl, "%d-%m-%Y")

    if start_sl_date.strftime("%d-%m-%Y") in dict_sick_leave_list:
        print("Special leave already entered")
        return
    end_sl = input("Enter end date if there are more than one days, otherwise press enter: ")

    if end_sl == "":
        end_sl_date = start_sl_date
    elif end_sl != "":
        end_sl = validate_date(end_sl)
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

    # export data of all employees to text file
    # reset RH list
    # reset casual leave dictionary

    employeelist = d.keys()

    for i in employeelist:

        export_to_text(i)

        d[i]['casual leave'] = 12
        d[i]['casual leave dict'] = {}
        d[i]['RH'] = 2
        d[i]['RH list'] = []
        if (int(d[i]['sick leave']) + 30) > 240:
            d[i]['sick leave'] = 240
        else:
            update_leave(i, "sick leave",-30)
    save_data()

def calculate_el_emp(emp_no, el_start_date, el_end_date,notfromthere):

    # we are going to update earned leave balance of an employee just before we are going to add new earned leave
    # this is to make sure the employee doesn't go over their 270 or something like that
    # sick leave will not contribute to earned leave accruing
    # same for earned leave also
    # we will set the last update of earned leave to the final leave of earned leave hopefully

    cal_el_date_string = el_start_date.strftime("%d-%m-%Y")

    doj = d[emp_no]['Leave updated as on']
    doj_datetime = datetime.datetime.strptime(doj, "%d-%m-%Y")

    # an employee will accrue earned leave when he/she is "on duty"
    # all leaves other than casual leave, quarantine leave, examination leave and trade union leave
    #  to be excluded when calculating earned leave

    # major leaves to be discounted for calculation of earned leaves are the following:
    # 1. sick leave
    # 2. earned leave
    # 3. strike
    # 4. LOP
    # 5. maternity leave
    # 6. paternity leave

    # counting number of sick leaves

    new_sick_leave_list = []
    for j in d[emp_no]['sick leave dict']:
        date_j = datetime.datetime.strptime(j, "%d-%m-%Y")
        if doj_datetime < date_j and date_j < el_start_date:
            new_sick_leave_list.append(j)
    new_sl_count = len(new_sick_leave_list)

    # counting number of Earned leaves
    new_el_list = []
    for j in d[emp_no]['Earned leave list']:
        date_j = datetime.datetime.strptime(j,"%d-%m-%Y")
        if doj_datetime < date_j and date_j < el_start_date:
            new_el_list.append(j)
    new_el_count_2 = len(new_el_list)

    # counting number of lop
    # LOP dict has both LOP entries and strike entries
    new_lop_list = []
    for j in d[emp_no]['LOP']:
        date_j = datetime.datetime.strptime(j, "%d-%m-%Y")
        if doj_datetime < date_j and date_j < el_start_date:
            new_lop_list.append(j)
    new_lop_count = len(new_lop_list)


    # counting number of paternity leave and maternity leave
    new_special_leave_list = []


    for j in d[emp_no]['Special leave list'].keys():
        if d[emp_no]["Special leave list"][j] == 'Maternity leave':

            date_j = datetime.datetime.strptime(j, "%d-%m-%Y")
            if doj_datetime < date_j and date_j < el_start_date:
                new_special_leave_list.append(j)
        elif d[emp_no]['Special leave list'][j] == "Paternity leave":
            date_j = datetime.datetime.strptime(j, "%d-%m-%Y")
            if doj_datetime < date_j and date_j < el_start_date:
                new_special_leave_list.append(j)

    new_special_leave_count = len(new_special_leave_list)

    if notfromthere:
        no_of_days = numOfDays(doj_datetime,el_start_date)-1

    else:
        no_of_days = numOfDays(doj_datetime,el_start_date)

    current_leave_count = d[emp_no]['earned leave']

    earnedleavedays = no_of_days - int(new_sl_count) - new_el_count_2 - int(new_lop_count) - int(new_special_leave_count)

    accruedleaves = (earnedleavedays) / 11

    new_el_count = float(accruedleaves) + float(current_leave_count)
    new_el_count = min(new_el_count,270)


    if doj_datetime < el_start_date:
        d[emp_no]['earned leave'] = new_el_count
        d[emp_no]['Leave updated as on'] = cal_el_date_string
        frac_earned_leave = dec_to_proper_frac(emp_no)
        print("Earned leave has been updated for employee number %s up to %s. Updated earned leave balance: %s."
                %(emp_no, cal_el_date_string, frac_earned_leave))
    else:
        print("Earned leave has already been updated until %s" % doj_datetime)

def calculate_el():

    print("WORD OF CAUTION. MAKE SURE ALL SICK LEAVES AND EARNED LEAVES ARE ENTERED BEFORE RUNNING FURTHER")
    cal_el_input = input("Upto which date do you want the leaves to be calculated? Enter in dd-mm-yyyy format: ")
    cal_el_input = validate_date(cal_el_input)

    cal_el_date = datetime.datetime.strptime(cal_el_input, "%d-%m-%Y")

    cal_el_date_string = cal_el_date.strftime("%d-%m-%Y")

    employeelist = d.keys()
    for i in employeelist:

        doj = d[i]['Leave updated as on']
        doj_datetime = datetime.datetime.strptime(doj, "%d-%m-%Y")

        # if the updated date is newer than entered date, break the calculation rightaway
        if doj_datetime > cal_el_date:
            print("Leave of %s already updated upto: %s"  % (d[i]['name'], doj))

        new_sick_leave_list = []
        for j in d[i]['sick leave dict']:
            date_j = datetime.datetime.strptime(j, "%d-%m-%Y")
            if doj_datetime < date_j and date_j < cal_el_date:
                new_sick_leave_list.append(j)
        new_sl_count = len(new_sick_leave_list)

        new_el_list = []
        for j in d[i]['Earned leave list']:
            date_j = datetime.datetime.strptime(j,"%d-%m-%Y")
            if doj_datetime < date_j and date_j < cal_el_date:
                new_el_list.append(j)
        new_el_count_2 = len(new_el_list)

        # counting number of lop
        # LOP dict has both LOP entries and strike entries
        new_lop_list = []
        for j in d[i]['LOP']:
            date_j = datetime.datetime.strptime(j, "%d-%m-%Y")
            if doj_datetime < date_j and date_j < cal_el_date:
                new_lop_list.append(j)
        new_lop_count = len(new_lop_list)


        # counting number of paternity leave and maternity leave
        new_special_leave_list = []

        for j in d[i]['Special leave list'].keys():
            if d[i]["Special leave list"][j] == 'Maternity leave':

                date_j = datetime.datetime.strptime(j, "%d-%m-%Y")
                if doj_datetime < date_j and date_j < cal_el_date:
                    new_special_leave_list.append(j)
            elif d[i]['Special leave list'][j] == "Paternity leave":
                date_j = datetime.datetime.strptime(j, "%d-%m-%Y")
                if doj_datetime < date_j and date_j < cal_el_date:
                    new_special_leave_list.append(j)


        new_special_leave_count = len(new_special_leave_list)


        no_of_days = numOfDays(doj_datetime,cal_el_date)

        current_leave_count = d[i]['earned leave']

        earnedleavedays = no_of_days - int(new_sl_count) - new_el_count_2 - int(new_lop_count) - int(new_special_leave_count)

        accruedleaves = earnedleavedays / 11
        new_el_count = float(accruedleaves) + float(current_leave_count)
        new_el_count = min(new_el_count,270)

        if doj_datetime < cal_el_date:
            d[i]['earned leave'] = new_el_count
            d[i]['Leave updated as on'] = cal_el_date_string

            frac_earned_leave = dec_to_proper_frac(i)
            print("Earned leave has been updated for employee number %s up to %s. Updated earned leave balance: %s."
                %(i, cal_el_date_string, frac_earned_leave))
#        else:
 #           print("Earned leave has already been updated until %s" % doj_datetime)


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

def report_leave_encashment():

    emp_list = d.keys()
    print("List of employees who have taken leave encashment: ")

    for i in emp_list:
        for j in d[i]['Leave encashment']:
            print("%s has taken leave encashment in block year %s." % (d[i]['name'],j))

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
    str_date = str(date)
    emp_name = d[emp_no]['name']
    string = ""
    for character in str_date:
        if character.isalnum():
            string = string+character
    file_name = emp_name+emp_no + string+".txt"

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
EL balance last updated on         : %s
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
    """ % (d[emp_no]['name'], d[emp_no]['employee number'], d[emp_no]['casual leave'], frac_earned_leave, d[emp_no]['Leave updated as on'],leave_encashment_status, d[emp_no]['sick leave'], d[emp_no]['RH'], d[emp_no]['casual leave dict'], d[emp_no]['Earned leave list'],d[emp_no]['sick leave dict'],d[emp_no]['RH list'], d[emp_no]['LOP'],d[emp_no]['Special leave list'] ))

def save_data():
    a_file = open("data.json", "w")
    json.dump(d,a_file)

    a_file.close()

def backup_data():
    date = datetime.datetime.now()
    str_date = str(date)
    string = ""
    for character in str_date:
        if character.isalnum():
            string = string+character

    backup_file_name = "data" + string +".json"

    backup_file = open(backup_file_name, "w")
    json.dump(d,backup_file)
    backup_file.close()

def employeeloop(empno, choice):

    if choice == "1":

        display_emp(empno)
    elif choice == "2":
        add_casual_leave(empno)
    elif choice == "3":
        add_earned_leave(empno)
    elif choice == "4":
        add_sick_leave(empno)
    elif choice == "8":
        export_to_text(empno)
    elif choice == "9":
        # calculate earned leave for the employee number here

        start_el = input("Enter date up to which earned leave to be calculated for the employee in dd-mm-yyyy format: ")

        # validate input

        start_el = validate_date(start_el)

        start_el_date = datetime.datetime.strptime(start_el, "%d-%m-%Y")
        calculate_el_emp(empno, start_el_date, start_el_date,False)
    elif choice == "5":
        leave_input = input("""
 Press 1 to enter leave encashment.
 Press 2 to enter restricted holiday.
 Press 3 to enter LOP or strike.
 Press 4 to enter Special leave (eg. Examination leave, Maternity leave, paternity leave, quarantine leave, etc.)
 Press 9 to return to previous menu.
Enter your option: """)

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
Enter your option: """)
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
Press 4 to display all the employees who have taken leave encashment.
Enter your choice: """)
    if report_options == "1":
        date = input("Enter the date in dd-mm-yyyy format: ")
        date = validate_date(date)
        report_leave(date)
    if report_options == "2":
        lop_choice = input("Enter the type (Choose between LOP and strike): ")
        report_lop('LOP',lop_choice)
    if report_options == "3":
        report_lop('sick leave dict','half')
    if report_options == '4':
        report_leave_encashment()
    else:
        return

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
            change = validate_letters(change)

            update_employee(update_emp,"name", change)
        elif update_choice == "2":
            change = validate_employee_number()
            update_employee(update_emp,"employee number", change)
            d[change] = d[update_emp]
            d.pop(update_emp)
        elif update_choice == "3":
            change = input("Enter new casual leave count: ")
            update_employee(update_emp,"casual leave", max(0,min(12,int(change))))
        elif update_choice == "4":
            change = input("Enter new earned leave count: ")
            change = mixed_to_float(change)
            update_employee(update_emp,"earned leave", max(0,min(270,float(change))))
        elif update_choice == "5":
            change = input("Enter new sick leave count: ")
            update_employee(update_emp,"sick leave", max(0,min(240,int(change))))
        elif update_choice == "6":
            change = input("Enter new RH count: ")
            update_employee(update_emp,"RH", max(0,min(2,int(change))))
        else:
            return
    if options == "7":
        reports()
    if options == "3":
        if (len(d) != 0):
            emp_no = req_emp_no()
            while True:
                newoptions = input("""===============================================================================
  Press 1 to view current leave status.
  Press 2 to enter casual leave.
  Press 3 to enter earned leave.
  Press 4 to enter sick leave.
  Press 5 to enter misc. leaves (eg. Restricted holidays, LOP, leave encashment and special leaves).
  Press 6 to delete already entered casual, earned, sick leave or RH.
  Press 7 to delete the employee.
  Press 8 to export data to text file.
  Press 9 to calculate earned leave for the employee.
  Press 10 to return back to main menu.
Enter your choice: """)
                if newoptions == "7":
                    delete_employee(emp_no)
                    return
                elif newoptions != "10":
                    employeeloop(emp_no, newoptions)
                else:
                    break
        else:
            print("No employees present")

def export_to_excel():
    df = pd.DataFrame.from_dict({(i): d[i]
        for i in d.keys()},
        orient='index')

    print(df)
    df.to_excel("leave-data.xlsx")
