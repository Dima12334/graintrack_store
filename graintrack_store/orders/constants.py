from model_utils import Choices


class OrderConstants:
    ORDER_CODE_MAX_LENGTH = 20
    COMMENT_MAX_LENGTH = 500
    STATUS_MAX_LENGTH = 8

    STATUS_CHOICE = Choices(
        ("RESERVED", "Reserved"),
        ("SOLD", "Sold"),
    )
