from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

class TestTransfer:
    def test_incoming_transfer_Personal(self):
        p_account = PersonalAccount("John", "Doe", "12345678901")
        p_account.incoming_transfer(500)
        assert p_account.balance == 500.0
    
    def test_incoming_transfer_negative_Personal(self):
        p_account = PersonalAccount("John", "Doe", "12345678901")
        p_account.incoming_transfer(-20.0)
        assert p_account.balance == 0.0

    def test_outgoing_transfer_Personal(self):
        p_account = PersonalAccount("John", "Doe", "12345678901")
        p_account.balance = 200.0
        p_account.outgoing_transfer(50)
        assert p_account.balance == 150.0
    
    def test_outgoing_tranfer_invalid_Personal(self):
        p_account = PersonalAccount("John", "Doe", "12345678901")
        p_account.balance = 200.0
        p_account.outgoing_transfer(300)
        assert p_account.balance == 200.0
    
    def test_incoming_transfer_Company(self):
        c_account = CompanyAccount("Nazwa", "1234567890")
        c_account.incoming_transfer(500)
        assert c_account.balance == 500.0

    def test_incoming_transfer_negative_Company(self):
        c_account = CompanyAccount("Nazwa", "1234567890")
        c_account.incoming_transfer(-20.0)
        assert c_account.balance == 0.0

    def test_outgoing_transfer_Company(self):
        c_account = CompanyAccount("Nazwa", "1234567890")
        c_account.balance = 200.0
        c_account.outgoing_transfer(50)
        assert c_account.balance == 150.0
    
    def test_outgoing_transfer_invalid_Company(self):
        c_account = CompanyAccount("Nazwa", "1234567890")
        c_account.balance = 200.0
        c_account.outgoing_transfer(300)
        assert c_account.balance == 200.0

        #express transfers

    def test_express_transfer_Personal(self):
        p_account = PersonalAccount("John", "Doe", "12345678901")
        p_account.balance = 200.0
        p_account.outgoing_express_transfer(100)
        assert p_account.balance == 99.0
    
    def test_express_transfer_border_Personal(self):
        p_account = PersonalAccount("John", "Doe", "12345678901")
        p_account.balance = 200.0
        p_account.outgoing_express_transfer(200)
        assert p_account.balance == -1.0

    def test_express_transfer_negative_Personal(self):
        p_account = PersonalAccount("John", "Doe", "12345678901")
        p_account.balance = 200.0
        p_account.outgoing_express_transfer(-100)
        assert p_account.balance == 200.0
    
    def test_express_transfer_ivalid_Personal(self):
        p_account = PersonalAccount("John", "Doe", "12345678901")
        p_account.balance = 200.0
        p_account.outgoing_express_transfer(300)
        assert p_account.balance == 200.0
    
    def test_express_transfer_Company(self):
        c_account = CompanyAccount("Nazwa", "1234567890")
        c_account.balance = 200.0
        c_account.outgoing_express_transfer(100)
        assert c_account.balance == 95.0
    
    def test_express_transfer_border_Company(self):
        c_account = CompanyAccount("Nazwa", "1234567890")
        c_account.balance = 200.0
        c_account.outgoing_express_transfer(200)