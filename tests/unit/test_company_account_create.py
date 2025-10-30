from src.company_account import CompanyAccount


class TestCompanyAccount:
    def test_CompanyAccount_creation(self):
        c_account = CompanyAccount("Nazwa", "1234567890")
        assert c_account.name == "Nazwa"
        assert c_account.balance == 0.0
        assert c_account.nip == "1234567890"
    
    def test_nip_too_long(self):
        c_account = CompanyAccount("Nazwa", "1234567890123")
        c_account.nip = "Invalid"
    def test_nip_too_short(self):
        c_account = CompanyAccount("Nazwa", "123456")
        c_account.nip = "Invalid"
    def test_nip_none(self):
        c_account = CompanyAccount("Nazwa", None)
        c_account.nip = "Invalid"
    
    def test_history_transfer_incoming(self):
        c_account = CompanyAccount("Nazwa", "1234567890")
        c_account.incoming_transfer(200.00)
        assert c_account.history == [200.00]
    def test_history_transfer_outcoming(self):
        c_account = CompanyAccount("Nazwa", "1234567890")
        c_account.balance = 300.00
        c_account.outgoing_transfer(300.00)
        assert c_account.history == [-300.00]
    def test_history_transfer_express(self):
        c_account = CompanyAccount("Nazwa", "1234567890")
        c_account.balance = 300.00
        c_account.outgoing_express_transfer(270.00)
        assert c_account.history == [-270.00, -5]
    