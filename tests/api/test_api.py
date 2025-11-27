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
            delete_response = requests.delete(f"{self.url}/{acc['pesel']}")
            assert delete_response.status_code == 200


    def test_create_account(self):
        payload = {
            "name": "james",
            "surname": "hetfield",
            "pesel": "89092909825"
        }
        response = requests.post(self.url, json=payload)
        assert response.status_code == 201
        assert response.json()["message"] == "Account created"

    def test_get_account_count(self):
        response = requests.get(f"{self.url}/count")
        assert response.status_code == 200
        assert response.json()["count"] == 1