import requests
import random


class TestPerf:
    url = "http://127.0.0.1:5000/api/accounts"
    account_details = {"name": "james", "surname": "hetfield", "pesel": "89092909825"}

    def test_create_del_100(self):
        for _ in range(100):
            response = requests.post(self.url, json=self.account_details, timeout=0.5)
            assert response.status_code == 201
            assert response.json()["message"] == "Account created"
            response = requests.delete(f"{self.url}/{self.account_details['pesel']}")
            assert response.status_code == 200
            assert response.json()["message"] == "Account deleted"

    def test_create_transfer_100(self):
        response = requests.post(self.url, json=self.account_details, timeout=0.5)
        assert response.status_code == 201
        assert response.json()["message"] == "Account created"
        for _ in range(100):
            payload = {"amount": 5, "type": "incoming"}
            response = requests.post(
                f"{self.url}/{self.account_details['pesel']}/transfer",
                json=payload,
                timeout=5,
            )
        request_data = requests.get(f"{self.url}/{self.account_details['pesel']}")
        curr_balance = request_data.json()["balance"]
        assert curr_balance == 500
        assert response.status_code == 200
        assert response.json()["message"] == "The order is accepted for realization"
        response = requests.delete(f"{self.url}/{self.account_details['pesel']}")

    # def test_create_1000_then_del(self):
    #     pesel_list = []
    #     for _ in range(10):
    #         pesel = random.randint(10000000000, 99999999999)
    #         acc = {"name": "jola", "surname": "polska", "pesel": pesel}
    #         response = requests.post(self.url, json=acc, timeout=5)
    #         pesel_list.append(pesel)
    #         assert response.status_code == 201
    #         assert response.json()["message"] == "Account created"
    #     for i in range(10):
    #         response = requests.delete(f"{self.url}/{pesel_list[i]}", timeout=5)
    #         assert pesel_list == 10
    #         assert response.status_code == 200
    #         assert response.json()["message"] == "Account deleted"
