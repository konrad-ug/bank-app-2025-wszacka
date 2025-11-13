from src.personal_account import PersonalAccount


class TestPersonalAccount:
    def test_PersonalAccount_creation(self):
        p_account = PersonalAccount("John", "Doe", "12345678901")
        assert p_account.first_name == "John"
        assert p_account.last_name == "Doe"
        assert p_account.balance == 0.0
        assert p_account.pesel == "12345678901"

    def test_pesel_too_long(self):
        p_account = PersonalAccount("Ania", "Nowak", "12345678901234")
        assert p_account.pesel == "Invalid"
    def test_pesel_too_short(self):
        p_account = PersonalAccount("Ania", "Nowak", "123456")
        assert p_account.pesel == "Invalid"
    def test_pesel_none(self):
        p_account = PersonalAccount("Ania", "Nowak", None)
        assert p_account.pesel == "Invalid"

    def test_promo_code_valid(self):
        p_account = PersonalAccount("John", "Doe", "06215678901","PROM_123")
        assert p_account.balance == 50.0
    def test_promo_code_too_long(self):
        p_account = PersonalAccount("John", "Doe", "06215678901","PROM_XYZZ")
        assert p_account.balance == 0.0
    def test_promo_code_too_short(self):
        p_account = PersonalAccount("John", "Doe", "06215678901","PROM_XY")
        assert p_account.balance == 0.0
    def test_promo_code_invalid(self):
        p_account = PersonalAccount("John", "Doe", "06215678901","PROX_456")
        assert p_account.balance == 0.0
    def test_promo_code_too_old(self):
        p_account = PersonalAccount("John", "Doe", "55115678901","PROM_XYZ")
        assert p_account.balance == 0.0

    def test_history_transfer_incoming(self):
        p_account = PersonalAccount("John", "Doe", "12345678901")
        p_account.incoming_transfer(200.00)
        assert p_account.history == [200.00]
    def test_history_transfer_outcoming(self):
        p_account = PersonalAccount("John", "Doe", "12345678901")
        p_account.balance = 300.00
        p_account.outgoing_transfer(300.00)
        assert p_account.history == [-300.00]
    def test_history_transfer_express(self):
        p_account = PersonalAccount("John", "Doe", "12345678901")
        p_account.balance = 300.00
        p_account.outgoing_express_transfer(270.00)
        assert p_account.history == [-270.00, -1]

    def test_submit_for_loan_three_incoming_valid(self):
        p_account = PersonalAccount("John", "Doe", "12345678901")
        p_account.incoming_transfer(20.0)
        p_account.incoming_transfer(40.0)
        p_account.incoming_transfer(10.0)
        assert p_account.submit_for_loan(20.00) == True

    def test_submit_for_loan_five_history(self):
        p_account = PersonalAccount("John", "Doe", "12345678901")
        p_account.incoming_transfer(20.0)
        p_account.outgoing_express_transfer(5.00)
        p_account.incoming_transfer(50.0)
        p_account.outgoing_transfer(20.0)
        assert p_account.submit_for_loan(40.00) == True

    def test_submit_for_loan_five_history_too_much(self):
        p_account = PersonalAccount("John", "Doe", "12345678901")
        p_account.incoming_transfer(20.0)
        p_account.outgoing_express_transfer(5.00)
        p_account.incoming_transfer(50.0)
        p_account.outgoing_transfer(20.0)
        assert p_account.submit_for_loan(50.00) == False

    def test_submit_for_loan_less_five_history(self):
        p_account = PersonalAccount("John", "Doe", "12345678901")
        p_account.incoming_transfer(20.0)
        p_account.outgoing_express_transfer(5.00)
        p_account.incoming_transfer(50.0)
        assert p_account.submit_for_loan(40.00) == False

    def test_submit_for_loan_incoming_invalid(self):
        p_account = PersonalAccount("John", "Doe", "12345678901")
        p_account.incoming_transfer(20.0)
        p_account.outgoing_transfer(5.0)
        p_account.incoming_transfer(10.0)
        assert p_account.submit_for_loan(20.00) == False

    def test_submit_for_loan_less_three_incoming(self):
        p_account = PersonalAccount("John", "Doe", "12345678901")
        p_account.incoming_transfer(20.0)
        p_account.incoming_transfer(40.0)
        assert p_account.submit_for_loan(20.00) == False

    
