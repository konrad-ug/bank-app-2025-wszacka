from src.account import Account


class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        super().__init__()
        self.email_history_text_email = "Personal Account History: "
        self.first_name = first_name
        self.last_name = last_name
        self.express_transfer_fee = 1
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.balance = (
            50.0
            if self.is_promo_code_valid(promo_code) & self.is_eligible_for_promo()
            else 0.0
        )

    def is_pesel_valid(self, pesel):
        if isinstance(pesel, str) and len(pesel) == 11:
            return True

    def is_promo_code_valid(self, promo_code):
        if promo_code is None:
            return False
        if promo_code.startswith("PROM_") and len(promo_code) == 8:
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

    def submit_for_loan(self, value):
        if 3 <= len(self.history) < 5:
            for i in self.history:
                if i <= 0:
                    return False
            self.balance += value
            return True
        elif len(self.history) >= 5:
            sum_last5 = sum([i for i in self.history[-5:]])
            if sum_last5 > value:
                self.balance += value
                return True
            else:
                return False
        return False

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "pesel": self.pesel,
            "balance": self.balance,
            "history": self.history,
        }

    @classmethod
    def from_dict(cls, data):
        account = cls(data.get("first_name"), data.get("last_name"), data.get("pesel"))
        account.balance = data.get("balance", account.balance)
        account.history = data.get("history", [])
        return account
