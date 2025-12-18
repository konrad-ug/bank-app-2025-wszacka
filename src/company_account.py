from src.account import Account
from datetime import datetime
import os
from dotenv import load_dotenv
import requests

load_dotenv()


class CompanyAccount(Account):
    def __init__(self, name, nip):
        super().__init__()
        self.email_history_text_email = "Company Account History: "
        self.name = name
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"
        self.express_transfer_fee = 5

    def is_nip_valid(self, nip):
        if isinstance(nip, str) and len(nip) == 10:
            return self.is_company_active(nip)

    def take_loan(self, value):
        if self.balance >= value * 2:
            for i in self.history:
                if i == 1775:
                    self.balance += value
                    return True
            return False
        return False

    # dodac to tez do sprawdzania nipu
    def is_company_active(self, nip):
        today_date = datetime.today().strftime("%Y-%m-%d")
        url = os.getenv("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl/")
        print(f"Sending requests to {url}")
        response = requests.get(f"{url}/api/search/nip/{nip}?date={today_date}")
        print(f"Repsonse status code: {response.json()}")
        if response.status_code != 200:
            return False
        data = response.json() or {}
        result = data.get("result") or {}
        subject = result.get("subject") or {}
        status = subject.get("statusValue")
        return status == "Czynny"
