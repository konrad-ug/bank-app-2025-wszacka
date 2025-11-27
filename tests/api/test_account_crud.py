import pytest
import requests

class TestApi:
    url = "http://127.0.0.1:5000/api/accounts"
    account_details = {
            "name": "james",
            "surname": "hetfield",
            "pesel": "89092909825"
        }
    @pytest.fixture(autouse=True, scope="function")
    def set_up(self):
        response = requests.post(self.url, json=self.account_details)
        assert response.status_code == 201
        yield
        accounts = requests.get(self.url).json()
        for acc in accounts:
            delete_response = requests.delete(f"{self.url}/{acc["pesel"]}")
            assert delete_response.status_code == 200