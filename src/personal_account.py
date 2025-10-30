from src.account import Account

class PersonalAccount(Account):
    def __init__(self, first_name, last_name,pesel, promo_code=None):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.express_transfer_fee = 1
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.balance = 50.0 if self.is_promo_code_valid(promo_code) & self.is_eligible_for_promo() else 0.0  

    def is_pesel_valid(self,pesel):
        if isinstance(pesel, str) and len(pesel) == 11:
            return True
        
    def is_promo_code_valid(self,promo_code):
        if promo_code is None:
            return False
        if promo_code.startswith("PROM_") and len(promo_code)==8:
            return True
        return False
    
    def is_eligible_for_promo(self):
        if self.pesel != "Invalid":
            year_prefix = self.pesel[:2]
            year = int(year_prefix)
            month = int(self.pesel[2:4])

            if month > 20:
                year += 2000
            else:
                year += 1900
            return year > 1960
        return False

    

