import requests
import pytest


class TestPerf:
    url = "http://127.0.0.1:5000/api/accounts"
    account_details = {"name": "james", "surname": "hetfield", "pesel": "89092909825"}
    iteration_count = 100
    timeout = 0.5

    @pytest.fixture(autouse=True, scope="function")
    def clear(self):
        response = requests.get(self.url, timeout=self.timeout)
        accounts = response.json()
        for account in accounts:
            pesel = account["pesel"]
            requests.delete(f"{self.url}/{pesel}", timeout=self.timeout)

    def test_create_del_perf(self):
        for _ in range(self.iteration_count):
            create_response = requests.post(
                self.url, json=self.account_details, timeout=0.5
            )
            assert create_response.status_code == 201
            del_response = requests.delete(
                f"{self.url}/{self.account_details['pesel']}"
            )
            assert del_response.status_code == 200

    def test_create_del_perf_group(self):
        pesels = [f"12345678{i:03d}" for i in range(1000)]
        for pesel in pesels:
            body = {**self.account_details, "pesel": pesel}
            create_res = requests.post(self.url, json=body, timeout=self.timeout)
            assert create_res.status_code == 201
        for pesel in pesels:
            del_res = requests.delete(f"{self.url}/{pesel}", timeout=self.timeout)
            assert del_res.status_code == 200

    def test_transfer_perf(self):
        create_response = requests.post(
            self.url, json=self.account_details, timeout=self.timeout
        )
        assert create_response.status_code == 201
        for _ in range(self.iteration_count):
            transfer_response = requests.post(
                f"{self.url}/{self.account_details['pesel']}/transfer",
                json={"type": "incoming", "amount": 100},
                timeout=5,
            )
        account = requests.get(
            f"{self.url}/{self.account_details['pesel']}", timeout=self.timeout
        )
        assert account.json()["balance"] == 100 * self.iteration_count
        del_response = requests.delete(f"{self.url}/{self.account_details['pesel']}")
        assert del_response.status_code == 200
