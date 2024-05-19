from typing import Dict, List
from collections import UserDict
from field import Birthday
from record import Record
from typing import List
from datetime import datetime

_DATE_FORMAT = "%d.%m.%Y"
_NAME_KEY = "name"
_DATE_KEY = "greeting_date"


class AddressBook(UserDict):

    def find(self, name: str) -> Record:
        data: Dict[str, Record] = self.data
        for key in data.keys():
            if key == name:
                return data[key]

        return None

    def find_all(self, name: str) -> Record:
        data: Dict[str, Record] = self.data
        for key in data.keys():
            if key == name:
                return data[key]

        return None

    def add_record(self, record: Record) -> None:
        self.data[record.get_name().get_value()] = record

    def delete(self, name: str) -> None:
        del self.data[name]

    def get_upcoming_birthdays(self) -> List[Dict[str, str]]:
        upcoming_birthdays = []

        cur_date = datetime.today().date()

        records: List[Record] = self.data.values()
        for record in records:
            birth_date = record.get_birthday().get_value()
            greeting_date = AddressBook._to_greeting_date(birth_date, cur_date)

            remaining_days = (greeting_date - cur_date).days

            # current day plus 6 days
            if remaining_days > 6:
                continue

            weekday_idx = greeting_date.weekday()

            greeting_day = greeting_date.day

            # if birhtday is on Sunday, move to Monday
            if weekday_idx == 6:
                greeting_date = greeting_date.replace(day=greeting_day+1)

            # if birhtday is on Saturday, move to Monday
            if weekday_idx == 5:
                greeting_date = greeting_date.replace(day=greeting_day+2)

            upcoming_birthday = {
                _NAME_KEY: record.get_name().get_value(),
                _DATE_KEY: AddressBook._to_str(greeting_date)}

            upcoming_birthdays.append(upcoming_birthday)

        return upcoming_birthdays

    @staticmethod
    def _to_greeting_date(birth_date, current_date):
        current_year = current_date.year

        greeting_date = birth_date.replace(year=current_year)

        if greeting_date < current_date:
            return greeting_date.replace(year=current_year + 1)

        return greeting_date

    @staticmethod
    def _to_str(datetime_date) -> str:
        return datetime_date.strftime(_DATE_FORMAT)


# TESTING


def _should_find_record():
    book = AddressBook()
    name = "One"
    record1 = Record(name)
    book.add_record(record1)
    book.add_record(Record("Two"))
    assert book.find(name) == record1


def _should_add_record():
    book = AddressBook()
    record1 = Record("One")
    record2 = Record("Two")
    book.add_record(record1)
    book.add_record(record2)
    assert len(book.data) == 2

    records = book.data.values()
    assert record1 in records
    assert record2 in records


def _should_delete_record():
    book = AddressBook()
    record1 = Record("One")
    name2 = "Two"
    record2 = Record(name2)
    book.add_record(record1)
    book.add_record(record2)
    assert len(book.data) == 2

    book.delete(name2)
    assert len(book.data) == 1
    assert record1 in book.data.values()


def _should_add_today():
    name = "Art"
    record = Record(name)
    date_today = datetime.today()
    str_today = date_today.strftime(Birthday.DATE_FORMAT)
    record.add_birthday(str_today)
    book = AddressBook()
    book.add_record(record)

    name_to_bday = book.get_upcoming_birthdays()[0]
    assert name_to_bday[_NAME_KEY] == name
    # greeting day is dynamic thus checked if exists
    assert name_to_bday[_DATE_KEY] != None


if __name__ == "__main__":
    _should_find_record()
    _should_add_record()
    _should_delete_record()
    _should_add_today()
