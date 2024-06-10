import json

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
