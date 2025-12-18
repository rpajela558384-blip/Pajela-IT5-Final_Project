# controllers/authentication.py
# Purpose: Controller class for authentication operations. Handles login, registration, password reset,
# and security question verification. This follows OOP by encapsulating authentication business logic
# and coordinating between the view (UI) and model (database) layers.

from models.account_model import AccountModel

# AuthenticationController class - OOP: Encapsulates authentication business logic
# This is an OOP class because it groups related authentication operations (login, register, reset password)
# into a cohesive unit. It follows the Controller pattern by acting as an intermediary between views
# and models, handling business logic without directly accessing the database or UI.
class AuthenticationController:
    # Constructor: Initialize controller with an account model instance (dependency injection)
    # This demonstrates OOP by using composition - the controller uses the model but doesn't create it
    def __init__(self, account_model):
        self.account_model = account_model

    # Method: Authenticate user by verifying username and password
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

    # Method: Register a new account by delegating to the account model
    def register_account(self, username, password, role, security_question=None, security_answer=None):
        return self.account_model.create_account(
            username, password, role, security_question, security_answer
        )

    # Method: Verify security answer by delegating to the account model
    def verify_security_answer(self, account_id, answer):
        return self.account_model.verify_security_answer(account_id, answer)

    # Method: Reset account password by delegating to the account model
    def reset_password(self, account_id, new_password):
        return self.account_model.update_password(account_id, new_password)
