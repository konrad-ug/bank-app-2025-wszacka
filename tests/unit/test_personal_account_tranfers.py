from src.personal_account import PersonalAccount
import pytest


class TestPersonalTransfer:

    @pytest.fixture()
    def account(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        return account

    data = [
        (0, 500, 500, "incoming"),
        (0, -20, 0, "incoming"),
        (200, 50, 150, "outgoing"),
        (200, 300, 200, "outgoing"),
        (200, -20, 200, "outgoing"),
        (200, 100, 99, "express"),
        (200, 200, -1, "express"),
        (200, -100, 200, "express"),
        (200, 300, 200, "express"),
    ]

    ids = [
        "correct incoming transfer",
        "negative incoming transfer",
        "correct outgoing transfer",
        "too big outgoing transfer",
        "negative outgoing transfer",
        "correct express transfer",
        "border express transfer",
        "negative express transfer",
        "too big express transfer",
    ]

    @pytest.mark.parametrize(
        "balance,transfer_value,expected_balance,transfer_type", data, ids=ids
    )
    def test_personal_acc_transfers(
        self, account, balance, transfer_value, expected_balance, transfer_type
    ):
        account.balance = balance
        if transfer_type == "incoming":
            account.incoming_transfer(transfer_value)
        elif transfer_type == "outgoing":
            account.outgoing_transfer(transfer_value)
        elif transfer_type == "express":
            account.outgoing_express_transfer(transfer_value)

        assert account.balance == expected_balance
