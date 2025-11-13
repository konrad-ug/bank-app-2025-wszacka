from src.personal_account import PersonalAccount
import pytest

class TestAccount:

    @pytest.fixture()
    def account(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        return account

    def test_submit_for_loan_three_incoming_valid(self,account):
        account.history=[100,200,500]
        result = account.submit_for_loan(300.00)
        assert result
        assert account.balance == 300.00

    def test_submit_for_loan_five_history(self,account):
        account.incoming_transfer(20.0)
        account.outgoing_express_transfer(5.00)
        account.incoming_transfer(50.0)
        account.outgoing_transfer(20.0)
        assert account.submit_for_loan(40.00) == True

    def test_submit_for_loan_five_history_too_much(self,account):
        account.incoming_transfer(20.0)
        account.outgoing_express_transfer(5.00)
        account.incoming_transfer(50.0)
        account.outgoing_transfer(20.0)
        assert account.submit_for_loan(50.00) == False

    def test_submit_for_loan_less_five_history(self,account):
        account.incoming_transfer(20.0)
        account.outgoing_express_transfer(5.00)
        account.incoming_transfer(50.0)
        assert account.submit_for_loan(40.00) == False

    def test_submit_for_loan_incoming_invalid(self,account):
        account.incoming_transfer(20.0)
        account.outgoing_transfer(5.0)
        account.incoming_transfer(10.0)
        assert account.submit_for_loan(20.00) == False

    def test_submit_for_loan_less_three_incoming(self,account):
        account.incoming_transfer(20.0)
        account.incoming_transfer(40.0)
        assert account.submit_for_loan(20.00) == False