import pytest
import requests


class TestApi:
    url = "http://127.0.0.1:5000/api/accounts"
    account_details = {"name": "james", "surname": "hetfield", "pesel": "89092909825"}

    @pytest.fixture(autouse=True, scope="function")
    def set_up(self):
        response = requests.post(self.url, json=self.account_details)
        assert response.status_code == 201
        yield
        accounts = requests.get(self.url).json()
        for acc in accounts:
            delete_response = requests.delete(f"{self.url}/{acc['pesel']}")
            assert delete_response.status_code == 200

    data = [
        (
            0,
            0,
            "12345678901",
            500,
            "incoming",
            404,
            "error",
            "Can't find this account!",
        ),
        (
            0,
            0,
            account_details["pesel"],
            500,
            "lol",
            400,
            "error",
            "Unknown transfer type",
        ),
        (
            0,
            500,
            account_details["pesel"],
            500,
            "incoming",
            200,
            "message",
            "The order is accepted for realization",
        ),
        (
            500,
            0,
            account_details["pesel"],
            500,
            "outgoing",
            200,
            "message",
            "The order is accepted for realization",
        ),
        (
            400,
            400,
            account_details["pesel"],
            500,
            "outgoing",
            422,
            "error",
            "Too big value for transaction",
        ),
        (
            500,
            -1,
            account_details["pesel"],
            500,
            "express",
            200,
            "message",
            "The order is accepted for realization",
        ),
        (
            400,
            400,
            account_details["pesel"],
            500,
            "express",
            422,
            "error",
            "Too big value for transaction",
        ),
    ]

    ids = [
        "wrong pesel",
        "wrong transfer type",
        "correct incoming transfer",
        "correct outgoing transfer",
        "too big value for outgoing transfer",
        "correct express transfer",
        "too big value for express transfer",
    ]

    @pytest.mark.parametrize(
        "balance,expected_balance,pesel,amount,type,expected_code,expected_type_msg,expected_msg",
        data,
        ids=ids,
    )
    def test_transfers(
        self,
        balance,
        expected_balance,
        pesel,
        amount,
        type,
        expected_code,
        expected_type_msg,
        expected_msg,
    ):
        if type == "outgoing" or type == "express":
            requests.post(
                f"{self.url}/{pesel}/transfer",
                json={"amount": balance, "type": "incoming"},
            )  # czy robic tu assert tez?
        payload = {"amount": amount, "type": type}
        response = requests.post(f"{self.url}/{pesel}/transfer", json=payload)
        request_data = requests.get(
            f"{self.url}/89092909825"
        )  # czy robic tu assert tez?
        curr_balance = request_data.json()["balance"]
        assert curr_balance == expected_balance
        assert response.status_code == expected_code
        assert response.json()[expected_type_msg] == expected_msg


# czy robic testy jesli mamy amount < 0?
