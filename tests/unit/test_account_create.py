from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe",79010288773)
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == 79010288773
