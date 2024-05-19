from typing import List, Tuple
from field import Name, Phone, Birthday, PhoneException


class Record:

    def __init__(self, name: str):
        self.__name: Name = Name(name)
        self.__phones: List[Phone] = []
        self.__birthday: Birthday = None

    def get_name(self) -> Name:
        return self.__name

    def find_phone(self, phone_num: str) -> Phone:
        for phone in self.__phones:
            if phone.get_value() == phone_num:
                return phone

    def get_phones(self) -> Tuple[Phone]:
        return tuple(self.__phones)

    def add_phone(self, phone_num: str) -> None:
        self.__phones.append(Phone(phone_num))

    def remove_phone(self, phone_num: str) -> None:
        self.__phones.remove(Phone(phone_num))

    def edit_phone(self, orig_phone_num: str, upd_phone_num: str) -> None:
        if not Phone._is_valid_phone(upd_phone_num):
            raise PhoneException

        phone: Phone = self.find_phone(orig_phone_num)

        if not phone:
            return

        phone.set_value(upd_phone_num)

    def add_birthday(self, birth_date: str) -> None:
        self.__birthday = Birthday(birth_date)

    def get_birthday(self) -> Birthday:
        return self.__birthday

    def __str__(self):
        descr = f"""Contact name: {self.__name.get_value()},
        phones: {'; '.join(p.get_value() for p in self.__phones)}"""
        
        if self.__birthday:
            descr += f",s birthday: {self.__birthday}"

        return descr


# TESTING

def _should_get_name():
    record = Record()

def _should_get_phones():
    record = Record()
    phone_num1 = "1111111111"
    phone_num2 = "2222222222"
    record.add_phone(phone_num1)
    record.add_phone(phone_num2)
    phones = record.get_phones()
    assert len(phones) == 2
    assert Phone(phone_num1) in phones
    assert Phone(phone_num2) in phones


def _should_find_phone():
    record = Record()
    phone_num1 = "1111111111"
    phone_num2 = "2222222222"
    record.add_phone(phone_num1)
    record.add_phone(phone_num2)
    assert record.find_phone(phone_num2).get_value() == phone_num2


def _should_add_phone():
    record = Record()
    phone_num = "1111111111"
    record.add_phone(phone_num)
    assert record.find_phone(phone_num).get_value() == phone_num


def _should_remove_phone():
    record = Record()
    phone_num = "1111111111"
    record.add_phone(phone_num)
    assert len(record.get_phones()) == 1

    record.remove_phone(phone_num)
    assert len(record.get_phones()) == 0


def _should_edit_phone():
    record = Record()
    phone_num1 = "1111111111"
    phone_num2 = "2222222222"
    record.add_phone(phone_num1)
    record.add_phone(phone_num2)
    phone_num3 = "3333333333"
    record.edit_phone(phone_num2, phone_num3)
    assert record.get_phones()[1].get_value() == phone_num3


def _should_add_birthday():
    record = Record()
    str_date = "01.01.2024"
    record.add_birthday(str_date)
    bday = record.get_birthday().get_value()
    assert bday.strftime(Birthday.DATE_FORMAT) == str_date


if __name__ == "main":
    _should_get_phones()
    _should_find_phone()
    _should_add_phone()
    _should_remove_phone()
    _should_edit_phone()
    _should_add_birthday
