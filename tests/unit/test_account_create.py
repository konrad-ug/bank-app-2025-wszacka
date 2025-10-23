from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678901")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "12345678901"

    def test_pesel_too_long(self):
        account = Account("Ania", "Nowak", "12345678901234")
        assert account.pesel == "Invalid"
    def test_pesel_too_short(self):
        account = Account("Ania", "Nowak", "123456")
        assert account.pesel == "Invalid"
    def test_pesel_none(self):
        account = Account("Ania", "Nowak", None)
        assert account.pesel == "Invalid"

    def test_promo_code_valid(self):
        account = Account("John", "Doe", "12345678901","PROM_123")
        assert account.balance == 50.0
    def test_promo_code_too_long(self):
        account = Account("John", "Doe", "12345678901","PROM_XYZZ")
        assert account.balance == 0.0
    def test_promo_code_too_short(self):
        account = Account("John", "Doe", "12345678901","PROM_XY")
        assert account.balance == 0.0
    def test_promo_code_invalid(self):
        account = Account("John", "Doe", "12345678901","PROX_456")
        assert account.balance == 0.0