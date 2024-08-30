from model_utils import Choices


class UserConstants:
    USER_ROLES = Choices(
        ("DEFAULT", "Default"),
        ("MODERATOR", "MODERATOR"),
    )
    USER_ROLES_MAX_LENGTH = 9
