from src.account_registry import AccountRegistry
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
import pytest


class TestRegistry:
    @pytest.fixture()
    def registry(self):
        registry = AccountRegistry()
        return registry

    @pytest.fixture()
    def account(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        return account

    def test_create_registry(self, registry, account):
        assert registry.accounts == []

    def test_add_personal(self, registry, account):
        registry.add_account(account)
        assert registry.accounts == [account]

    def test_search_acc(self, registry, account):
        registry.accounts = [account]
        assert registry.search_account(account.pesel) == account

    def test_search_acc_none(self, registry, account):
        registry.accounts = [account]
        assert registry.search_account("12245678901") is None

    def test_get_all_accounts(self, registry, account):
        registry.accounts = [account]
        assert registry.get_all_accounts() == [account]

    def test_number_of_accounts(self, registry, account):
        registry.accounts = [account]
        assert registry.number_of_accounts() == 1
