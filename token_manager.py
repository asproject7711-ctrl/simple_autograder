# token_manager.py
from storage import get_user, ensure_user, update_user, add_log

class TokenManager:
    @staticmethod
    def bootstrap_user(user_id: str, name="User", role="student", token_limit=100000):
        return ensure_user(user_id, name, role, token_limit)

    @staticmethod
    def log_usage(user_id: str, tokens: int, cost: float, model: str, task: str):
        user = get_user(user_id)
        if not user:
            # auto-create with defaults if not present
            user = TokenManager.bootstrap_user(user_id)
        # increment usage
        new_used = int(user["token_used"]) + int(tokens)
        update_user(user_id, token_used=new_used)
        # append log
        return add_log(user_id, task, model, int(tokens), float(cost))

    @staticmethod
    def remaining_tokens(user_id: str):
        user = get_user(user_id)
        if not user:
            return None
        return int(user["token_limit"]) - int(user["token_used"])

    @staticmethod
    def reset_usage(user_id: str):
        user = get_user(user_id)
        if not user:
            return None
        update_user(user_id, token_used=0)
        return True

    @staticmethod
    def set_limit(user_id: str, new_limit: int):
        user = get_user(user_id)
        if not user:
            user = TokenManager.bootstrap_user(user_id, token_limit=new_limit)
        else:
            update_user(user_id, token_limit=int(new_limit))
        return get_user(user_id)
