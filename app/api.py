from flask import Flask, request, jsonify
from src.account_registry import AccountRegistry
from src.personal_account import PersonalAccount

app = Flask(__name__)
registry = AccountRegistry()


@app.route("/api/accounts", methods=["POST"])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")
    acc = registry.search_account(data["pesel"])
    if acc is not None:
        return jsonify({"message": "Account with this pesel already exists"}), 409
    account = PersonalAccount(data["name"], data["surname"], data["pesel"])
    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201


@app.route("/api/accounts", methods=["GET"])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.get_all_accounts()
    accounts_data = [
        {
            "name": acc.first_name,
            "surname": acc.last_name,
            "pesel": acc.pesel,
            "balance": acc.balance,
        }
        for acc in accounts
    ]
    return jsonify(accounts_data), 200


@app.route("/api/accounts/count", methods=["GET"])
def get_account_count():
    print("Get account count request received")
    count = registry.number_of_accounts()
    # implementacja powinna znaleźć się tutaj
    return jsonify({"count": count}), 200


@app.route("/api/accounts/<pesel>", methods=["GET"])
def get_account_by_pesel(pesel):
    acc = registry.search_account(pesel)
    if acc is None:
        return jsonify({"error": "Can't find this account!"}), 404
    return (
        jsonify(
            {
                "name": acc.first_name,
                "surname": acc.last_name,
                "pesel": acc.pesel,
                "balance": acc.balance,
            }
        ),
        200,
    )


@app.route("/api/accounts/<pesel>", methods=["PATCH"])
def update_account(pesel):
    data = request.get_json()
    acc = registry.search_account(pesel)
    if acc is None:
        return jsonify({"error": "Can't find this account!"}), 404
    index = registry.accounts.index(acc)
    if "name" in data or "surname" in data:
        if "name" in data:
            registry.accounts[index].first_name = data["name"]
        if "surname" in data:
            registry.accounts[index].last_name = data["surname"]
        return jsonify({"message": "Account updated"}), 200
    else:
        return jsonify({"error": "Wrong params!"}), 404


@app.route("/api/accounts/<pesel>", methods=["DELETE"])
def delete_account(pesel):
    acc = registry.search_account(pesel)
    if acc is None:
        return jsonify({"error": "Can't find this account!"}), 404
    registry.accounts.remove(acc)
    # implementacja powinna znaleźć się tutaj
    return jsonify({"message": "Account deleted"}), 200


@app.route("/api/accounts/<pesel>/transfer", methods=["POST"])
def transfer(pesel):
    data = request.get_json()
    acc = registry.search_account(pesel)
    value = data["amount"]
    if acc is None:
        return jsonify({"error": "Can't find this account!"}), 404

    if data["type"] == "incoming":
        acc.incoming_transfer(value)
    elif data["type"] == "outgoing":
        if acc.balance < value:
            return jsonify({"error": "Too big value for transaction"}), 422
        acc.outgoing_transfer(value)
    elif data["type"] == "express":
        if acc.balance < value:
            return jsonify({"error": "Too big value for transaction"}), 422
        acc.outgoing_express_transfer(value)
    else:
        return jsonify({"error": "Unknown transfer type"}), 400

    return jsonify({"message": "The order is accepted for realization"}), 200
