import re
from datetime import datetime


class Field:

    def __init__(self, value: str):
        self._value = value

    def get_value(self) -> str:
        return self._value

    def __eq__(self, other):
        return self._value == other._value

    def __hash__(self):
        return hash(self._value)

    def __str__(self):
        return str(self._value)
    
    def __repr__(self) -> str:
        return str(self._value)


class Name(Field):

    def __eq__(self, other) -> bool:
        if not isinstance(other, Name):
            return False

        return super().__eq__(other)

    def __hash__(self) -> int:
        return super().__hash__()


class Phone(Field):

    def __init__(self, value: str):
        if not Phone._is_valid_phone(value):
            raise PhoneException

        self._value = value

    @staticmethod
    def _is_valid_phone(input: str) -> bool:
        """
        Defines if input corresponds to 10 digit formats, e.g.:
            (XXX)-XXX-XXXX
             XXX-XXX-XXXX
            (XXX)XXXXXXX
             XXXXXXXXXX
        """
        pattern = r"\b\(?\d{3}\)?-?\d{3}-?\d{4}\b"
        return bool(re.match(pattern, input))

    def set_value(self, value: str) -> None:
        self._value = value

    def __eq__(self, other) -> bool:
        if not isinstance(other, Phone):
            return False

        return super().__eq__(other)

    def __hash__(self) -> int:
        return super().__hash__()


class PhoneException(Exception):

    def __init__(self):
        super().__init__("Invalid phone number. It must be a 10-digit number.")


class Birthday(Field):

    DATE_FORMAT = "%d.%m.%Y"
    INVALID_FORMAT_MSG = "Invalid date format. Use DD.MM.YYYY"

    def __init__(self, birth_date: str):
        try:
            self._value = Birthday.__parse_date(birth_date).date()
        except ValueError:
            raise ValueError(Birthday.INVALID_FORMAT_MSG)

    @staticmethod
    def __parse_date(str_date: str) -> datetime:
        return datetime.strptime(str_date, Birthday.DATE_FORMAT)

# TESTING


def _should_hash_name_obj():
    name1 = Name("Art")
    name2 = Name("Art")
    assert hash(name1) == hash(name2)

    name3 = Name("Ann")
    assert hash(name1) != hash(name3)


def _should_hash_phone_obj():
    phone1 = Phone("1111111111")
    phone2 = Phone("1111111111")
    assert hash(phone1) == hash(phone2)

    phone3 = Phone("2222222222")
    assert hash(phone1) != hash(phone3)


def _should_compare_name_obj():
    name1 = Name("Art")
    name2 = Name("Art")
    assert name1 == name2

    name3 = Name("Ann")
    assert name1 != name3


def _should_compare_phone_obj():
    phone1 = Phone("1111111111")
    phone2 = Phone("1111111111")
    assert phone1 == phone2

    phone3 = Phone("2222222222")
    assert phone1 != phone3
    

def _should_parse_date():
    str_date = "01.01.2024"
    date = Birthday(str_date).get_value()
    assert date.strftime(Birthday.DATE_FORMAT) == str_date


def _should_raise_exception():
    invalid_date = "01-01-2024"
    try:
        Birthday(invalid_date)
    except ValueError as exp:
        assert str(exp) == Birthday.INVALID_FORMAT_MSG


if __name__ == "__main__":
    _should_hash_name_obj()
    _should_hash_phone_obj()
    _should_compare_name_obj()
    _should_compare_phone_obj()
    _should_parse_date()
    _should_raise_exception()
