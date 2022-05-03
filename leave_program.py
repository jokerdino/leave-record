import leave

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
            leave.keep_it_going(options)
        else:
            break