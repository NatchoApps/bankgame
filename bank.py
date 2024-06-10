import json
import random
from employee import Employee
from customer import Customer

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
