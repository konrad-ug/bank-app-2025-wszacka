from src.company_account import CompanyAccount
import pytest


class TestAccount:
    @pytest.fixture()
    def account(self):
        account = CompanyAccount("Nazwa", "1234567890")
        return account

    data = [
        ([1775, 100, 200, -100], 100, 50, True, 150),
        ([1775, 100, 1775, 200, -100], 100, 50, True, 150),
        ([100, -100, 100, 1000], 100, 50, False, 100),
        ([100, -100, 100, 1000], 100, 60, False, 100),
        ([1775, 100, 200, -100], 100, 60, False, 100),
    ]
    ids = [
        "correct loan with one ZUS",
        "correct loan with two ZUS",
        "no payment for ZUS in history",
        "too big loan",
        "too big loan and no ZUS in history",
    ]

    @pytest.mark.parametrize(
        "history,balance,amount,expected_result,expected_balance", data, ids=ids
    )
    def test_loan(
        self, account, history, balance, amount, expected_result, expected_balance
    ):
        account.history = history
        account.balance = balance
        result = account.take_loan(amount)
        assert result == expected_result
        assert account.balance == expected_balance
