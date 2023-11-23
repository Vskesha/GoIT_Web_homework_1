from collections import UserDict
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

import calendar
import re
import json


class Field(ABC):
    """
    A base class for representing fields with validation.
    Args:
        value: The initial value of the field.
    """

    def __init__(self, value: str):
        self.__value = None
        self.value = value

    @abstractmethod
    def validate(self, new_value: str) -> bool:
        """
        Validates a new value for the field.
        """
        return True

    @property
    def value(self) -> str:
        """
        Property representing the field's value.
        """
        return self.__value

    @value.setter
    def value(self, new_value: str):
        """
        Setter for the field's value.
        """
        self.__value = new_value

    def __str__(self) -> str:
        """
        Returns a string representation of the field's value.
        """
        return str(self.value)


class Phone(Field):
    """
    A class representing a phone number field with validation.
    Args:
        value: The initial value of the phone number.
    """

    def __init__(self, value: str = None):
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value: str):
        """
        Setter method for the phone number field.
         """
        if not self.validate(new_value):
            return f'The phone number {new_value} cannot be assigned as it is not valid.'
        Field.value.fset(self, new_value)

    def validate(self, number: str) -> bool:
        """
        Validates a new phone number value.
        """
        if number is None:
            return False
        phone_format = r'^\+\d{1,3}\d{9}$'
        return bool(re.match(phone_format, number))


class Email(Field):
    """
    A class representing an email address field with validation.
    Args:
        value: The initial value of the email address.
    """

    def __init__(self, value: str = None):
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value: str):
        """
        Setter method for the email field.
        """
        if not self.validate(new_value):
            return f'The email {new_value} cannot be assigned as it is not valid.'
        Field.value.fset(self, new_value)

    def validate(self, email: str) -> bool:
        """
        Validates a email value.
        """
        if email is None:
            return False
        email_format = (r'\b(?![A-Za-z0-9._%+-]*a@t[A-Za-z0-9._%+-]*)\b'
                        r'(?![0-9]{2})[A-Za-z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
        return bool(re.match(email_format, email))


class Name(Field):
    """
    A class representing a name field with validation.
    Args:
        value: The initial value of the name.
    """

    def __init__(self, value: str):
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value: str):
        """
        Setter method for the new name value.
        """
        if not self.validate(new_value):
            return f'The name {new_value} cannot be assigned as it is not valid.'
        Field.value.fset(self, new_value)

    def validate(self, name: str) -> bool:
        """
        Validates a new name value.
        """
        if name is None or not re.match(r'^[A-Za-zА-Яа-я\s]+$', name) or len(name) <= 1:
            return False
        return True


class Birthday(Field):
    """
    A class representing a birthday field with validation.
    Args:
        value: The initial value of the birthday.
    """

    def __init__(self, value: str = None):
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value: str) -> str:
        """
        Setter method for the new birthday value.
        """
        if not self.validate(new_value):
            return f'The date of birth {new_value} cannot be assigned as it is not valid.'
        Field.value.fset(self, new_value)

    def validate(self, new_value: str) -> bool:
        """
        Validates a new birthday value.
        """
        try:
            parsed_date = datetime.strptime(new_value, '%d.%m.%Y').date()
            today = datetime.now().date()
            if parsed_date > today:
                return False
            return True
        except ValueError:
            return False
        except TypeError:
            return False


class Record:
    """
    A class representing a contact record in an address book.

    Args:
        name: The name of the contact.
        phone: The phone number of the contact. Default is None.
        birthday: The birthday of the contact in 'dd.mm.yyyy' format. Default is None.
        email: The email address of the contact. Default is None.
    """

    def __init__(self, name: str, phone: str = None, birthday: str = None, email: str = None):
        self.birthday = Birthday(birthday) if birthday is not None else None
        self.email = Email(email) if email is not None else None
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone is not None else []

    def add_email(self, email_value: str) -> bool:
        """
        Adds an email address to the contact's record.
        """
        if email_value:
            self.email = Email(email_value)
            return True
        return False

    def change_email(self, email: str, new_email_value: str) -> bool:
        """
        Changes the email address of the contact.
        """
        if self.email is not None and self.email.value == email:
            if self.email.validate(new_email_value):
                self.email = Email(new_email_value)
                return True
        return False

    def remove_email(self, del_email: str) -> bool:
        """
        Removes the email address from the contact's record.
        """
        if self.email and self.email.value == del_email:
            self.email = None
            return True
        return False

    def add_phone_number(self, number: str) -> bool:
        """
        Adds a phone number to the contact's record.
        """
        phone = Phone(number)
        if phone.validate(number) and number not in self.phones:
            self.phones.append(phone)
            return True
        else:
            return False

    def change_phone_number(self, number: str, new_number: str) -> bool:
        """
         Changes a phone number in the contact's record.
        """
        for index, phone in enumerate(self.phones):
            if phone.value == number:
                self.phones[index] = Phone(new_number)
                return True
        return False

    def remove_phone_number(self, number: str) -> bool:
        """
        Removes a phone number from the contact's record.
        """
        if any(phone.value == number for phone in self.phones):
            new_phones = [phone for phone in self.phones if phone.value != number]
            self.phones = new_phones
            return True
        return False

    def days_to_birthday(self) -> int | None:
        """
         Calculates the number of days remaining until the contact's next birthday.
        """
        if self.birthday and self.birthday.validate(self.birthday.value):
            parsed_date = datetime.strptime(self.birthday.value, '%d.%m.%Y').date()
            date_now = datetime.now().date()
            date_now_year = date_now.year
            next_year = date_now.year + 1
            parsed_date = parsed_date.replace(year=date_now_year)

            if parsed_date <= date_now:
                if calendar.isleap(next_year):
                    time_delta = (parsed_date - date_now + timedelta(days=366)).days
                else:
                    time_delta = (parsed_date - date_now + timedelta(days=365)).days
            else:
                time_delta = (parsed_date - date_now).days
            return time_delta
        else:
            return None

    def __str__(self) -> str:
        """
        Returns a string representation of the contact record.
        """
        phones_str = ', '.join(str(phone) for phone in self.phones)
        if not phones_str:
            phones_str = "None"
        if not self.birthday:
            birthday_str = "None"
        else:
            birthday_str = self.birthday.value
        if not self.email:
            email_str = "None"
        else:
            email_str = self.email.value
        return f"Name: {self.name.value}, Phones: {phones_str}, Email: {email_str}, Birthday: {birthday_str}"


class AddressBook(UserDict):
    """
    A class representing an address book that stores and
    manages contact records.
    """

    def add_record(self, record: Record) -> bool:
        """
        Adds a contact record to the address book
        if it passes validation.
        """
        if self.validate_record(record):
            key = record.name.value
            self.data[key] = record
            return True
        else:
            return False

    def find_records(self, **search_criteria: dict) -> list:
        """
        Finds and returns a list of contact records that
        match the given search criteria.
        """
        result = []
        found = False
        for record in self.data.values():
            if ('name' in search_criteria and len(search_criteria['name']) >= 2
                    and search_criteria['name'] in record.name.value):
                result.append(record)
                found = True
            if 'phones' in search_criteria and len(search_criteria['phones']) >= 5:
                for phone in record.phones:
                    if search_criteria['phones'] in phone.value:
                        result.append(record)
                        found = True
                        break
        if not found:
            print("There is no contact that matches the specified search criteria.")
        return result

    def get_all_records(self) -> list:
        """
        Retrieves all contact records in the address book
        and returns them as a list.
        """
        if self.data:
            contacts = list(self.data.values())
        else:
            contacts = []

        return contacts

    def get_birthdays_per_week(self, num: int) -> list:
        """
        Finds and returns a list of names whose birthdays
        begin after a given number of days.
        """
        to_day = datetime.now().date()
        new_date = to_day + timedelta(days=num)

        happy_birthday = []
        for record in self.data.values():
            if record.birthday:
                birthdate = datetime.strptime(record.birthday.value, '%d.%m.%Y').date()
                if birthdate.day == new_date.day and birthdate.month == new_date.month:
                    happy_birthday.append(record.name.value)

        print(f'List of birthday celebrants to greet in {num} day(s): {happy_birthday}')
        return happy_birthday

    def get_record_by_name(self, name: str) -> Record | None:
        """
        Retrieves a contact record by searching for a name.
        """
        for record in self.data.values():
            if record.name.value == name:
                return record
        return None

    def remove_record(self, name: str) -> bool:
        """
        Removes a contact record by name.
        """
        if name in self.data:
            del self.data[name]
            return True
        else:
            return False

    @staticmethod
    def validate_record(record: Record) -> bool:
        """
        Validates a contact record, including name,
        phone numbers, birthday, and email.
        """
        valid_phones = all(isinstance(phone, Phone) and phone.validate(phone.value) for phone in record.phones)
        valid_name = isinstance(record.name, Name)

        if record.birthday:
            valid_birthday = isinstance(record.birthday, Birthday) and record.birthday.validate(record.birthday.value)
        else:
            valid_birthday = True

        if record.email:
            valid_email = isinstance(record.email, Email) and record.email.validate(record.email.value)
        else:
            valid_email = True

        if not valid_phones:
            print("Phone numbers are not valid.")
        if not valid_name:
            print("Name is not valid.")
        if not valid_birthday:
            print("Date of birth is not valid.")
        if not valid_email:
            print("Email is not valid.")
        return valid_phones and valid_name and valid_birthday and valid_email

    def iterator(self, n: int):
        """
        Splits the address book into iterators with 'n'
        records per iteration.
        """
        return (list(self.data.values())[i:i + n] for i in range(0, len(self.data), n))

    def __iter__(self):
        """
        Initializes the iterator for the address book.
        """
        self.index = 0
        return self

    def __next__(self) -> 'Record':
        """
        Iterates through the address book, returning one record at a time.
        """
        if self.index < len(self.data):
            record = list(self.data.values())[self.index]
            self.index += 1
            return record
        else:
            raise StopIteration

    def __str__(self) -> str:
        """
        Returns a string representation of the address book.
        """
        book_str = "\n".join(f"{name}: {record}" for name, record in self.data.items())
        return book_str


class AddressBookFileHandler:
    """
    A class for handling the serialization and deserialization of an AddressBook to/from a file.
    Args:
        file_name (str): The name of the file to read from or write to.
    """

    def __init__(self, file_name: str):
        self.file_name = file_name

    def save_to_file(self, address_book: AddressBook) -> None:
        """
        Serializes and saves an AddressBook to a file.
        """
        with open(self.file_name, 'w') as file:
            json.dump(address_book.data, file, default=self._serialize_record, indent=4)

    @staticmethod
    def _deserialize_record(contact_data: dict) -> Record | None:
        """
        Deserializes a contact record from a dictionary.
        """
        if isinstance(contact_data, str):
            return None
        name = contact_data.get('name')
        phones = contact_data.get('phones', [])
        birthday = contact_data.get('birthday')
        email = contact_data.get('email')
        record = Record(name, None, birthday, email)
        for phone in phones:
            record.add_phone_number(phone)
        return record

    def load_from_file(self) -> AddressBook:
        """
        Loads and deserializes an AddressBook from a file.
        """
        addressbook = AddressBook()
        try:
            with open(self.file_name, 'r') as file:
                records_data = json.load(file)
                for contact_data in records_data.values():
                    addressbook.add_record(self._deserialize_record(contact_data))
        except FileNotFoundError:
            pass
        except Exception:
            pass
        return addressbook

    @staticmethod
    def _serialize_record(record: Record) -> dict:
        """
       Serializes a contact record to a dictionary.
        """
        return {
            'name': record.name.value,
            'phones': [phone.value for phone in record.phones],
            'birthday': record.birthday.value if record.birthday else None,
            'email': record.email.value if record.email else None
        }
