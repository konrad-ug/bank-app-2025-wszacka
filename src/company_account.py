from src.account import Account

class CompanyAccount(Account):
    def __init__(self, name, nip):
        super().__init__()
        self.name = name
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"
        self.express_transfer_fee = 5

    def is_nip_valid(self,nip):
        if isinstance(nip, str) and len(nip) == 10:
            return True