class Validator:
    MOBILE_NO_STRING_VALIDATOR: str = r"(^([+]{1}[8]{2}|0088)?(01){1}[3-9]{1}\d{8})$"
    EMAIL_STRING_VALIDATOR: str = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    NID_STRING_VALIDATOR: str = r"^[0-9]{9,17}+$"
    USERNAME_STRING_VALIDATOR = r"^[a-zA-Z0-9_]{3,20}$"
    NAME_STRING_VALIDATOR: str = r"^[a-zA-Z0-9_ ]+$"
