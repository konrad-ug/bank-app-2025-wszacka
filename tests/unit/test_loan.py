from src.personal_account import PersonalAccount
import pytest


class TestAccount:
    @pytest.fixture()
    def account(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        return account

    data = [
        ([100, 100, 100], 500, True, 500),
        ([-100, 100, -100, 100, 1000], 700, True, 700),
        ([-100, 2000, -100, 100, -1000], 1000, False, 0),
        ([100], 666, False, 0),
        ([-100, 100, 100], 50, False, 0),
        ([100, 200, -100, 100], 100, False, 0),
    ]
    ids = [
        "three postives",
        "five transactions with two negatives",
        "too big loan for 5 transactions",
        "less than 3 transactions for loan",
        "negative in 3 transactions",
        "second last negative in 4 transactions",
    ]

    @pytest.mark.parametrize(
        "history,amount,expected_result,expected_balance", data, ids=ids
    )
    def test_loan(self, account, history, amount, expected_result, expected_balance):
        account.history = history
        result = account.submit_for_loan(amount)
        assert result == expected_result
        assert account.balance == expected_balance
