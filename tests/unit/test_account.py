from src.account import Account


class TestAccount:
    def test_PersonalAccount_creation(self):
        account = Account()
        assert account.balance == 0
        assert account.express_transfer_fee ==0