from models.account_model import AccountModel

class AuthenticationController:
    def __init__(self, account_model):
        # controller RECEIVES the model, it does NOT recreate it
        self.account_model = account_model

    def login(self, username, password):
        account = self.account_model.get_account_by_username(username)
        if account and account["Password"] == password:
            return {
                "success": True,
                "role": account["Role"],
                "account_id": account["AccountID"]
            }
        return {
            "success": False,
            "role": None,
            "account_id": None
        }

    def register_account(self, username, password, role, security_question=None, security_answer=None):
        return self.account_model.create_account(
            username, password, role, security_question, security_answer
        )

    def verify_security_answer(self, account_id, answer):
        return self.account_model.verify_security_answer(account_id, answer)

    def reset_password(self, account_id, new_password):
        return self.account_model.update_password(account_id, new_password)
