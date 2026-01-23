import os
from pymongo import MongoClient
from src.personal_account import PersonalAccount
from src.accounts_repository_interface import AccounstRepository


class MongoAccountRepository(AccounstRepository):
    def __init__(
        self, mongo_url=None, db_name=None, collection_name=None, collection=None
    ):
        if collection is not None:
            self._collection = collection
            return
        mongo_url = mongo_url or "mongodb://localhost:27017"
        db_name = db_name or "bank_app"
        collection_name = collection_name or "accounts"

        client = MongoClient(mongo_url)
        db = client[db_name]
        self._collection = db[collection_name]

    def save_all(self, accounts):
        self._collection.delete_many({})
        for account in accounts:
            self._collection.update_one(
                {"pesel": account.pesel}, {"$set": account.to_dict()}, upsert=True
            )

    def load_all(self):
        accounts = []
        for doc in self._collection.find():
            accounts.append(PersonalAccount.from_dict(doc))
        return accounts
