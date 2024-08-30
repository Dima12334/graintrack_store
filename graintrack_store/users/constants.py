from model_utils import Choices


class UserConstants:
    USERNAME_MAX_LENGTH = 150
    PASSWORD_MAX_LENGTH = 128

    USER_ROLES_MAX_LENGTH = 9
    USER_ROLES = Choices(
        ("DEFAULT", "Default"),
        ("MODERATOR", "MODERATOR"),
    )
