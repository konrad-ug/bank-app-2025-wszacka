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

    def test_create_account(self):
        payload = {"name": "jola", "surname": "nowak", "pesel": "12345678901"}
        response = requests.post(self.url, json=payload)
        assert response.status_code == 201
        assert response.json()["message"] == "Account created"

    def test_create_account_same_pesel(self):
        payload = {"name": "karol", "surname": "mucha", "pesel": "89092909825"}
        response = requests.post(self.url, json=payload)
        assert response.status_code == 409
        assert response.json()["message"] == "Account with this pesel already exists"

    def test_get_account_count(self):
        response = requests.get(f"{self.url}/count")
        assert response.status_code == 200
        assert response.json()["count"] == 1

    def test_get_all_accounts(self):
        response = requests.get(self.url)
        assert response.status_code == 200
        assert response.json() == [
            {
                "name": "james",
                "surname": "hetfield",
                "pesel": "89092909825",
                "balance": 0.0,
            }
        ]

    def test_get_account_by_pesel(self):
        response = requests.get(f"{self.url}/89092909825")
        assert response.status_code == 200
        assert response.json() == {
            "name": "james",
            "surname": "hetfield",
            "pesel": "89092909825",
            "balance": 0.0,
        }

    def test_wrong_get_account_by_pesel(self):
        response = requests.get(f"{self.url}/123456788901")
        assert response.status_code == 404
        assert response.json()["error"] == "Can't find this account!"

    def test_update_account_name_surname(self):
        payload = {"name": "jan", "surname": "nowak"}
        response = requests.patch(f"{self.url}/89092909825", json=payload)
        assert response.status_code == 200
        assert response.json()["message"] == "Account updated"
        response_check = requests.get(f"{self.url}/89092909825")
        assert response_check.status_code == 200
        assert response_check.json() == {
            "name": "jan",
            "surname": "nowak",
            "pesel": "89092909825",
            "balance": 0.0,
        }

    def test_update_account_name(self):
        payload = {"name": "jan"}
        response = requests.patch(f"{self.url}/89092909825", json=payload)
        assert response.status_code == 200
        assert response.json()["message"] == "Account updated"
        response_check = requests.get(f"{self.url}/89092909825")
        assert response_check.status_code == 200
        assert response_check.json() == {
            "name": "jan",
            "surname": "hetfield",
            "pesel": "89092909825",
            "balance": 0.0,
        }

    def test_update_account_surname(self):
        payload = {"surname": "nowak"}
        response = requests.patch(f"{self.url}/89092909825", json=payload)
        assert response.status_code == 200
        assert response.json()["message"] == "Account updated"
        response_check = requests.get(f"{self.url}/89092909825")
        assert response_check.status_code == 200
        assert response_check.json() == {
            "name": "james",
            "surname": "nowak",
            "pesel": "89092909825",
            "balance": 0.0,
        }

    def test_update_account_wrong_pesel(self):
        payload = {"surname": "nowak"}
        response = requests.patch(f"{self.url}/12345678901", json=payload)
        assert response.status_code == 404
        assert response.json()["error"] == "Can't find this account!"
        response_check = requests.get(f"{self.url}/89092909825")
        assert response_check.status_code == 200
        assert response_check.json() == {
            "name": "james",
            "surname": "hetfield",
            "pesel": "89092909825",
            "balance": 0.0,
        }

    def test_update_account_wrong_params(self):
        payload = {"balance": 1.0}
        response = requests.patch(f"{self.url}/89092909825", json=payload)
        assert response.status_code == 404
        assert response.json()["error"] == "Wrong params!"
        response_check = requests.get(f"{self.url}/89092909825")
        assert response_check.status_code == 200
        assert response_check.json() == {
            "name": "james",
            "surname": "hetfield",
            "pesel": "89092909825",
            "balance": 0.0,
        }

    def test_delete_account(self):
        response = requests.delete(f"{self.url}/89092909825")
        assert response.status_code == 200
        assert response.json()["message"] == "Account deleted"
        response_check = requests.get(self.url)
        assert response_check.status_code == 200
        assert response_check.json() == []

    def test_delete_account_wrong_pesel(self):
        response = requests.delete(f"{self.url}/12345678901")
        assert response.status_code == 404
        assert response.json()["error"] == "Can't find this account!"
        response_check = requests.get(self.url)
        assert response_check.status_code == 200
        assert response_check.json() == [
            {
                "name": "james",
                "surname": "hetfield",
                "pesel": "89092909825",
                "balance": 0.0,
            }
        ]
