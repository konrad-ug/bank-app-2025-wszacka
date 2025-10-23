class Account:
    def __init__(self):
        self.balance = 0.0
        self.express_transfer_fee = 0

    def incoming_transfer(self, value: float) -> None:
        if value > 0:
            self.balance += value
    
    def outgoing_transfer(self,value:float) -> None:
        if 0 <= value <= self.balance:
            self.balance -= value
    
    def outgoing_express_transfer(self,value):
        if value > 0 and value <= self.balance:
            self.balance -= value + self.express_transfer_fee
        return self.balance