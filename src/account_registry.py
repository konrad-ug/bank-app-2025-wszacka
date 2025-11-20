from src.personal_account import PersonalAccount


class AccountRegistry:
    def __init__(self):
        self.accounts = []

    def add_account(self, account: PersonalAccount):
        self.accounts.append(account)

    def search_account(self, pesel):
        for i in self.accounts:
            if i.pesel == pesel:
                return i
        return None

    def get_all_accounts(self):
        return self.accounts

    def number_of_accounts(self):
        return len(self.accounts)
