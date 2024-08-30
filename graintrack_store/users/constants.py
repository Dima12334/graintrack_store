from model_utils import Choices


class UserConstants:
    USERNAME_MAX_LENGTH = 150
    PASSWORD_MAX_LENGTH = 128

    ROLE_MAX_LENGTH = 9
    ROLE_CHOICE = Choices(
        ("DEFAULT", "Default"),
        ("MODERATOR", "MODERATOR"),
    )
