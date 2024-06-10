import os
import sys
from bank import Bank
from employee import Employee
from customer import Customer

def clear_screen():
    """Clear the screen based on the operating system."""
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')

def print_menu(bank):
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    print(f"Day {bank.current_day} ({days_of_week[bank.day_of_week]}){' ' * 20}Vault Balance: ${bank.vault_balance}")
    print("Bank Management Simulator")

    print("\nEmployee Management:")
    print("1. Hire Employee")
    print("2. Fire Employee")
    print("3. View Employee")

    print("\nCustomer Management:")
    print("4. Add Customer")
    print("5. View/Edit Customer Info")

    print("\nBanking Tasks for the Day:")
    print("6. Advance Day")
    print("7. View Employee Schedule")
    print("8. View Employees Working Today")
    print("9. Generate Weekly Report")
    print("10. View Bank Balance")

    print("\nMiscellaneous:")
    print("11. Save Data")
    print("12. Load Data")
    print("13. Banking Bonuses")  # New option for Banking Bonuses
    print("0. Exit")

def view_employee(bank):
    print("\nView Employee:")
    
    # Print list of employees
    print("List of Employees:")
    for idx, employee in enumerate(bank.employees, start=1):
        print(f"{idx}. {employee.name}")
    
    choice = input("Enter the number of the employee to view: ")
    try:
        choice = int(choice)
        if 1 <= choice <= len(bank.employees):
            employee = bank.employees[choice - 1]
            print("Selected Employee:", employee.name)
            
            # Display all employee data
            print("\nEmployee Details:")
            print(f"Name: {employee.name}")
            print(f"Age: {employee.age}")
            print(f"Position: {employee.position}")
            print(f"Hourly Rate: {employee.hourly_rate}")
            print(f"Days Employed: {employee.days_employed}")
            print(f"Employee Rating: {employee.employee_rating}")
            print(f"Hours Worked/Week: {employee.hours_worked_week}")
        else:
            print("Invalid employee number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def banking_bonuses(bank):
    print("\nBanking Bonuses:")
    print("1. $25,000 Deposit to Bank's Vault")
    print("2. Bonus 2 (Locked)")
    print("3. Bonus 3 (Locked)")
    print("4. Bonus 4 (Locked)")
    print("5. Bonus 5 (Locked)")
    
    choice = input("Choose a banking bonus: ")
    try:
        choice = int(choice)
        if 1 <= choice <= 5:
            if choice == 1:
                bank.deposit_to_vault(25000)
                print("Congratulations! $25,000 deposited to the bank's vault.")
            else:
                print("This bonus is currently locked. It will be unlocked later.")
        else:
            print("Invalid bonus number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def main():
    bank = Bank()
    while True:
        clear_screen()
        print_menu(bank)
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter employee name: ")
            age = int(input("Enter employee age: "))
            position = input("Enter employee position: ")
            hourly_rate = float(input("Enter employee hourly rate: "))
            bank.hire_employee(Employee(name, age, position, hourly_rate))
        elif choice == "2":
            name = input("Enter employee name to fire: ")
            bank.fire_employee(name)
        elif choice == "3":
            view_employee(bank)
        elif choice == "4":
            name = input("Enter customer name: ")
            age = int(input("Enter customer age: "))
            balance = float(input("Enter customer balance: "))
            monthly_income = float(input("Enter customer monthly income: "))
            bank.add_customer(Customer(name, age, balance, monthly_income))
        elif choice == "5":
            view_edit_customer_info(bank)
        elif choice == "6":
            bank.advance_day()
            print("Day advanced.")
        elif choice == "7":
            print("Employee Schedule:", bank.get_employee_schedule())
        elif choice == "8":
            print("Employees working today:", bank.get_employees_working_on_day(bank.day_of_week))
        elif choice == "9":
            print("Weekly Report:", bank.generate_weekly_report())
        elif choice == "10":
            print("Bank Balance:", bank.balance)
        elif choice == "11":
            file_path = input("Enter file path to save data: ")
            bank.save_data(file_path)
            print("Data saved.")
        elif choice == "12":
            file_path = input("Enter file path to load data: ")
            bank.load_data(file_path)
            print("Data loaded.")
        elif choice == "13":
            banking_bonuses(bank)
        elif choice == "0":
            sys.exit()  # Exit the program
        else:
            print("Invalid choice. Please try again.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()

