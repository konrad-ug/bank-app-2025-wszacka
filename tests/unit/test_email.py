from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
from pytest_mock import MockFixture
from datetime import datetime
import pytest


class TestEmail:
    todays_date = datetime.today().strftime("%Y-%m-%d")
    email_adress = "test@email.com"

    def test_PersonalAccount_email(self, mocker: MockFixture):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.history = [150.0, -50.0]
        mock_send = mocker.patch("src.account.SMTPClient.send", return_value=True)

        result = account.send_history_via_email(self.email_adress)

        assert result is True
        mock_send.assert_called_once_with(
            "Account Transfer History " + self.todays_date,
            "Personal Account History: " + account.history.__str__(),
            self.email_adress,
        )

    def test_PersonalAccount_email_false(self, mocker: MockFixture):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.history = [150.0, -50.0]
        mock_send = mocker.patch("src.account.SMTPClient.send", return_value=False)
        result = account.send_history_via_email(self.email_adress)

        assert result is False

    @pytest.fixture(autouse=True)
    def setup_mock(self, mocker: MockFixture):
        mocker.patch.object(CompanyAccount, "is_company_active", return_value=True)

    def test_CompanyAccount_email(self, mocker: MockFixture):
        account = CompanyAccount("Nazwa", "8461627563")
        account.history = [150.0, -50.0]
        mock_send = mocker.patch("src.account.SMTPClient.send", return_value=True)

        result = account.send_history_via_email(self.email_adress)

        assert result is True
        mock_send.assert_called_once_with(
            "Account Transfer History " + self.todays_date,
            "Company Account History: " + account.history.__str__(),
            self.email_adress,
        )

    def test_CompanyAccount_email_false(self, mocker: MockFixture):
        account = CompanyAccount("Nazwa", "8461627563")
        account.history = [150.0, -50.0]
        mock_send = mocker.patch("src.account.SMTPClient.send", return_value=False)

        result = account.send_history_via_email(self.email_adress)

        assert result is False
