import sys
import re
from typing import Tuple, Any, Dict, List, Callable
from book import AddressBook
from record import Record


cmd_to_func: Dict[str, str] = {}
cmd_to_func["hello"] = "_greet"
cmd_to_func["add"] = "_add_contact"
cmd_to_func["change"] = "_change_contact"
cmd_to_func["phone"] = "_show_phone"
cmd_to_func["all"] = "_show_all"
cmd_to_func["add-birthday"] = "_add_birthday"
cmd_to_func["show-birthday"] = "_show_birthday"
cmd_to_func["birthdays"] = "_birthdays"
cmd_to_func["close"] = "_exit"
cmd_to_func["exit"] = "_exit"


book: AddressBook = AddressBook()


def main():
    print("Welcome to the assistant bot!\n")
    while True:
        str_input: str = input("Enter a command: ")
        tuple_input: Tuple[str, list] = _parse_input(str_input)

        cmd: str = tuple_input[0]

        if not cmd in cmd_to_func:
            print("Invalid command\n")
            continue

        args: list = tuple_input[1]

        _call_function(cmd, args)


def _parse_input(input: str) -> Tuple[str, list]:
    list_input: List[str] = input.strip().split()

    func = list_input[0].lower()
    args = list_input[1:]

    return (func, args)


def _call_function(cmd: str, args: tuple) -> None:
    func: str = cmd_to_func[cmd]
    globs: Dict[str, Any] = globals()

    if not _is_function(func, globs):
        print(f"Function '{func}' not found\n")

        return

    globs[func](*args)


def _is_function(name: str, globs: Dict[str, Any]) -> bool:
    return name in globs and callable(globs[name])


def _input_error(func: Callable) -> Callable:
    def inner(*args):
        try:
            func(*args)
        except KeyError:
            print("Contact not foud\n")
        except ValueError:
            print("Phone number should have 10 digits\n")
        except Exception as exc:
            print(exc)
            print("")

    return inner


@_input_error
def _greet() -> None:
    print("How can I help you?\n")


@_input_error
def _add_contact(name: str, phone: str) -> None:
    if not _is_phone(phone):
        raise ValueError

    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    
    print("Contact added\n")


def _is_phone(input: str) -> bool:
    """
    Defines if input corresponds to 10 digit formats, e.g.:
        (XXX)-XXX-XXXX
         XXX-XXX-XXXX
        (XXX)XXXXXXX
         XXXXXXXXXX
    """
    pattern = r"\b\(?\d{3}\)?-?\d{3}-?\d{4}\b"

    return bool(re.match(pattern, input))


@_input_error
def _change_contact(name: str, orig_phone_num: str, upd_phone_num) -> None:
    if not name in book:
        raise KeyError

    if not _is_phone(upd_phone_num):
        raise ValueError

    record : Record = book.find(name)
    record.edit_phone(orig_phone_num, upd_phone_num)
    
    print("Contact updated\n")


@_input_error
def _show_phone(name: str) -> None:
    if not name in book:
        raise KeyError
    
    record : Record = book.find(name)

    print(record.get_phones())
    print()


def _show_all() -> None:
    for record in book.values():
        print(record)

    print()


@_input_error
def _add_birthday(name: str, birth_date: str):
    record : Record = book.find(name)
    record.add_birthday(birth_date)
    
    print("Birthday added\n")


@_input_error
def _show_birthday(name: str):
    record : Record = book.find(name)
    
    print(record.get_birthday())
    print()


@_input_error
def _birthdays():
    for birthday in book.get_upcoming_birthdays():
        print(birthday)
    print("\n")


def _exit() -> None:
    print("Good bye\n")

    sys.exit(0)


# testing


main()
