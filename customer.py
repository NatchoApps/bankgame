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
