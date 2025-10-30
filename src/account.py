class Account:
    def __init__(self):
        self.balance = 0.0
        self.express_transfer_fee = 0
        self.history = []

    def incoming_transfer(self, value: float) -> None:
        if value > 0:
            self.balance += value
            self.history.append(value)
    
    def outgoing_transfer(self,value:float) -> None:
        if 0 <= value <= self.balance:
            self.balance -= value
            self.history.append(-value)
    
    def outgoing_express_transfer(self,value):
        if value > 0 and value <= self.balance:
            self.balance -= value + self.express_transfer_fee
            self.history.append(-value)
            self.history.append(-self.express_transfer_fee)
        return self.balance