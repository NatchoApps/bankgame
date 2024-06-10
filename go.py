import json
import random
from datetime import datetime, timedelta

class Employee:
    def __init__(self, name, age, position, hourly_rate):
        self.name = name
        self.age = age
        self.position = position
        self.hourly_rate = hourly_rate
        self.days_employed = 0
        self.employee_rating = 5.0
        self.hours_worked_week = 0
    
    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "position": self.position,
            "hourly_rate": self.hourly_rate,
            "days_employed": self.days_employed,
            "employee_rating": self.employee_rating,
            "hours_worked_week": self.hours_worked_week
        }
    
    @staticmethod
    def from_dict(data):
        employee = Employee(data['name'], data['age'], data['position'], data['hourly_rate'])
        employee.days_employed = data['days_employed']
        employee.employee_rating = data['employee_rating']
        employee.hours_worked_week = data['hours_worked_week']
        return employee

class Customer:
    def __init__(self, name, age, balance, monthly_income):
        self.name = name
        self.age = age
        self.balance = balance
        self.monthly_income = monthly_income
        self.transactions = []
        self.loans = []
        self.credit_cards = []

    def add_transaction(self, amount):
        self.transactions.append(amount)
        if len(self.transactions) > 5:
            self.transactions.pop(0)
    
    def add_loan(self, amount, interest_rate, term):
        self.loans.append({"amount": amount, "interest_rate": interest_rate, "term": term})

    def add_credit_card(self, limit, interest_rate):
        self.credit_cards.append({"limit": limit, "interest_rate": interest_rate})

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "balance": self.balance,
            "monthly_income": self.monthly_income,
            "transactions": self.transactions,
            "loans": self.loans,
            "credit_cards": self.credit_cards
        }
    
    @staticmethod
    def from_dict(data):
        customer = Customer(data['name'], data['age'], data['balance'], data['monthly_income'])
        customer.transactions = data['transactions']
        customer.loans = data['loans']
        customer.credit_cards = data['credit_cards']
        return customer

class Bank:
    def __init__(self):
        self.employees = []
        self.customers = []
        self.current_day = 1
        self.day_of_week = 0  # Monday
        self.schedule = {day: [] for day in range(6)}  # Monday to Saturday
        self.balance = 0.0
    
    def advance_day(self):
        daily_expenses = self.calculate_daily_expenses()
        daily_income = self.calculate_daily_income()
        self.balance += daily_income - daily_expenses
        
        self.current_day += 1
        self.day_of_week = (self.day_of_week + 1) % 7
        if self.day_of_week == 6:  # Skip Sunday
            self.day_of_week = 0
            self.current_day += 1
        for employee in self.employees:
            employee.days_employed += 1
    
    def calculate_daily_expenses(self):
        daily_expenses = sum(e.hourly_rate * 8 for e in self.employees if e.name in self.schedule[self.day_of_week])
        return daily_expenses
    
    def calculate_daily_income(self):
        daily_income = sum(c.monthly_income / 30 for c in self.customers)
        return daily_income
    
    def hire_employee(self, employee):
        self.employees.append(employee)
        self.assign_schedule()
    
    def fire_employee(self, employee_name):
        self.employees = [e for e in self.employees if e.name != employee_name]
        self.assign_schedule()
    
    def assign_schedule(self):
        self.schedule = {day: [] for day in range(6)}  # Clear the schedule
        for employee in self.employees:
            days_to_work = random.sample(range(6), 5)  # Work 5 out of 6 days
            for day in days_to_work:
                self.schedule[day].append(employee.name)
    
    def get_employee_schedule(self):
        return self.schedule
    
    def get_employees_working_on_day(self, day):
        return self.schedule.get(day, [])

    def generate_weekly_report(self):
        return self.schedule

    def add_customer(self, customer):
        self.customers.append(customer)

    def customer_deposit(self, customer_name, amount):
        for customer in self.customers:
            if customer.name == customer_name:
                customer.balance += amount
                customer.add_transaction(amount)
                break
    
    def customer_withdraw(self, customer_name, amount):
        for customer in self.customers:
            if customer.name == customer_name and customer.balance >= amount:
                customer.balance -= amount
                customer.add_transaction(-amount)
                break

    def save_data(self, file_path):
        data = {
            "employees": [e.to_dict() for e in self.employees],
            "customers": [c.to_dict() for c in self.customers],
            "current_day": self.current_day,
            "day_of_week": self.day_of_week,
            "balance": self.balance
        }
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def load_data(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
            self.employees = [Employee.from_dict(e) for e in data['employees']]
            self.customers = [Customer.from_dict(c) for c in data['customers']]
            self.current_day = data['current_day']
            self.day_of_week = data['day_of_week']
            self.balance = data['balance']
            

def print_menu():
    print("\nBank Management Simulator")
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    print(f"\nDay {bank.current_day} ({days_of_week[bank.day_of_week]})")
    print("1. Hire Employee")
    print("2. Fire Employee")
    print("3. Add Customer")
    print("4. Deposit to Customer Account")
    print("5. Withdraw from Customer Account")
    print("6. Advance Day")
    print("7. View Employee Schedule")
    print("8. View Employees Working Today")
    print("9. Generate Weekly Report")
    print("10. View Bank Balance")
    print("11. Save Data")
    print("12. Load Data")
    print("0. Exit")

def main():
    bank = Bank()
    while True:
        print_menu()
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
            name = input("Enter customer name: ")
            age = int(input("Enter customer age: "))
            balance = float(input("Enter customer balance: "))
            monthly_income = float(input("Enter customer monthly income: "))
            bank.add_customer(Customer(name, age, balance, monthly_income))
        elif choice == "4":
            name = input("Enter customer name: ")
            amount = float(input("Enter deposit amount: "))
            bank.customer_deposit(name, amount)
        elif choice == "5":
            name = input("Enter customer name: ")
            amount = float(input("Enter withdrawal amount: "))
            bank.customer_withdraw(name, amount)
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
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")
            
            

# Example usage:
bank = Bank()

# Hire some employees
bank.hire_employee(Employee("John Doe", 30, "Teller", 15.0))
bank.hire_employee(Employee("Jane Smith", 25, "Manager", 25.0))

# Add some customers
bank.add_customer(Customer("Alice Brown", 28, 5000.0, 3000.0))
bank.add_customer(Customer("Bob White", 35, 10000.0, 4000.0))

# Save data to JSON
bank.save_data("bank_data.json")

# Load data from JSON
bank.load_data("bank_data.json")

# Advance the day
bank.advance_day()

# Example operations
print("Employee Schedule:", bank.get_employee_schedule())
print("Employees working on Monday:", bank.get_employees_working_on_day(0))
print("Weekly Report:", bank.generate_weekly_report())

print("Bank Balance:", bank.balance)
bank.advance_day()
print("Bank Balance after 1 day:", bank.balance)

print("Customer Balance:", bank.customers[0].balance)
bank.customer_deposit("Alice Brown", 500)
print("Customer Balance after deposit:", bank.customers[0].balance)
bank.customer_withdraw("Alice Brown", 200)
print("Customer Balance after withdrawal:", bank.customers[0].balance)

# Add loan and credit card to a customer
bank.customers[0].add_loan(10000, 5.0, 24)  # $10,000 loan at 5% interest for 24 months
bank.customers[0].add_credit_card(5000, 15.0)  # $5,000 credit limit at 15% interest
print("Customer Loans:", bank.customers[0].loans)
print("Customer Credit Cards:", bank.customers[0].credit_cards)

if __name__ == "__main__":
    main()