from colorama import init as init_colorama, Fore, Style
from pathlib import Path

from classess_ab import AddressBook, Name, Record, Phone, Birthday, Email, AddressBookFileHandler
from commands import COMMANDS, LOGO, PATH_TO_SAVE
from handling_errors import input_error
from user_interfaces import UserViewer, GuiUserViewer, ConsoleUserViewer


class BotAdressBook:
    def __init__(self, viewer: UserViewer, address_book: AddressBook):
        self.viewer = viewer
        self.address_book = address_book
        self.arg = ''

    def command_parser(self, user_input: str) -> callable:
        """
        Parse user input to determine the corresponding command and data.
        This function parses the user's input to identify the command they want to
        execute and the associated data, if any.
        """
        if not user_input:
            raise IndexError("Nothing was entered ...")
        func = None
        lower_input_end_spaced = user_input.lower() + ' '
        for command, aliases in COMMANDS.items():
            for alias in aliases:
                if lower_input_end_spaced.startswith(alias + ' '):
                    func = getattr(self, f'handle_{command}')
                    # func = globals()[f'self.handle_{command}']
                    self.arg = user_input[len(alias) + 1:].strip()
                    break
            if func:
                break
        if not func:
            raise ValueError(f"There is no such command {user_input.split()[0]}")
        return func

    def handle_add_record(self):
        """
        Command handler for 'add' command. Adds a new contact to the address book.
        """
        name = self.viewer.get_data_input("Enter name:")
        if not Name(name).validate(name):
            self.viewer.display_error("Invalid name. Please use only letters and more than one.")
            return 'Was entered invalid name'
        if name.lower().strip() in [record.name.value.lower().strip() for record in self.address_book.data.values()]:
            self.viewer.display_error("A contact with that name already exists!!!")
            return 'Already exists'

        new_record = Record(name)

        phone = self.viewer.get_data_input("Enter the phone number (+380________):")
        if not phone:
            self.viewer.display_message('The phone was not entered')
        elif Phone(phone).validate(phone):
            new_record.phones = [Phone(phone)]
        else:
            self.viewer.display_error("Invalid phone")

        email = self.viewer.get_data_input("Enter an email in an acceptable format:")
        if not email:
            self.viewer.display_message('The email was not entered')
        elif Email(email).validate(email):
            new_record.email = Email(email)
        else:
            self.viewer.display_error("Invalid email")

        birthday = self.viewer.get_data_input("Enter birthday in the format(dd.mm.yyyy):")
        if not birthday:
            self.viewer.display_message('The birthday was not entered')
        elif Birthday(birthday).validate(birthday):
            new_record.birthday = Birthday(birthday)
        else:
            self.viewer.display_error("Invalid birthday")

        if self.address_book.add_record(new_record):
            self.viewer.display_contacts(self.address_book.get_all_records())
            self.viewer.display_message(f"The contact {new_record.name} has been successfully added to address book.")
            return 'The process is finished'
        else:
            self.viewer.display_message("The data is not valid")
            return None

    def get_contact_by_name(self):
        """
        Checks the presence and validity of a contact by name.
        Returns the contact found or False if the contact is not found or is invalid.
        """
        name = self.viewer.get_data_input("Enter name:")
        if not Name(name).validate(name):
            self.viewer.display_error("Invalid name. Please use only letters and more than one.")
            return False
        contact = self.address_book.get_record_by_name(name)
        if contact is None:
            self.viewer.display_message(f"The contact with the name {name} was not found in the address book.")
            return None
        return contact

    def handle_add_phone_number(self) -> str:
        """
        Command handler for 'add_phone' command. Adds phone
        to a contact in the address book.
        """
        contact = self.get_contact_by_name()
        if not contact:
            return 'The is no contact'
        new_phone = self.viewer.get_data_input("Enter phone in an acceptable format:")
        if not Phone(new_phone).validate(new_phone):
            self.viewer.display_error("The phone is not valid.")
            return 'Was entered invalid phone'
        if new_phone in [record.value for record in contact.phones]:
            self.viewer.display_error(f"The phone {new_phone} has already existed.")
            return 'Was entered phone which existed'
        contact.add_phone_number(new_phone)
        self.viewer.display_contacts(self.address_book.get_all_records())
        self.viewer.display_message("Phone number successfully added.")
        return "Finished when added phone."

    def handle_add_email(self) -> str:
        """
        Command handler for 'add_email' command. Adds an email
        address to a contact in the address book.
        """
        contact = self.get_contact_by_name()
        if not contact:
            return 'The is no contact'
        if contact.email:
            self.viewer.display_message(f"The contact already has email.")
            return 'An email was entered, but the contact already has one.'
        email = self.viewer.get_data_input("Enter email in an acceptable format:")
        if not Email(email).validate(email):
            self.viewer.display_error("The email is not valid.")
            return 'Was entered invalid email'
        contact.add_email(email)
        self.viewer.display_contacts(self.address_book.get_all_records())
        self.viewer.display_message(f"Email {email} added successfully")
        return f"Finished when added email"

    def handle_change_phone_number(self) -> str:
        """
        Command handler for 'change_phone' command. Changes the phone number of a contact.
        """
        contact = self.get_contact_by_name()
        if not contact:
            return 'The is no contact'
        if not contact.phones:
            self.viewer.display_message(f"The contact {contact.name.value} does not have phone.")
            return 'Was entered phone, but contact have not phone number'

        old_phone = self.viewer.get_data_input("Enter old phone in an acceptable format:")
        if not Phone(old_phone).validate(old_phone):
            self.viewer.display_error("The old_phone is not valid.")
            return 'Was entered old invalid phone'
        if old_phone not in [record.value for record in contact.phones]:
            self.viewer.display_error(f"The phone {old_phone} does not exist in {contact.name.value}.")
            return 'Was entered phone, but contact have not it'

        new_phone = self.viewer.get_data_input("Enter new_phone in an acceptable format:")
        if not Phone(new_phone).validate(new_phone):
            self.viewer.display_error("The new_phone was not entered or it is not valid.")
            return 'Was entered new invalid phone'
        elif new_phone in [record.value for record in contact.phones]:
            self.viewer.display_error(f"The new_phone {new_phone} is already exist.")
            return 'Was entered phone, but the new phone matches the old one'
        else:
            contact.change_phone_number(old_phone, new_phone)
            self.viewer.display_contacts(self.address_book.get_all_records())
            self.viewer.display_message(f'The phone has been successfully changed from {old_phone} to {new_phone}.')
        return "Finished when changed phone"

    def handle_change_email(self) -> str:
        """
        Command handler for 'change_email' command. Changes the email address of a contact.
        """
        contact = self.get_contact_by_name()
        if not contact:
            return 'The is no contact'
        if not contact.email:
            self.viewer.display_message(f"The contact {contact.name.value} does not have email.")
            return 'Was entered email, but contact have not phone email'

        old_email = self.viewer.get_data_input("Enter old email in an acceptable format:")
        if not Email(old_email).validate(old_email):
            self.viewer.display_error("The old_email is not valid.")
            return 'Was entered old invalid email'
        elif old_email != contact.email.value:
            self.viewer.display_error(f"The email {old_email} does not exist.")
            return 'Was entered old email, but it does not exist'

        new_email = self.viewer.get_data_input("Enter new email in an acceptable format:")
        if not Email(new_email).validate(new_email):
            self.viewer.display_error("The new email is not valid.")
            return 'Was entered new invalid email'
        contact.change_email(old_email, new_email)
        self.viewer.display_contacts(self.address_book.get_all_records())
        self.viewer.display_message(f"The email has been successfully changed from {old_email} to {new_email}.")
        return "Finished when changed email"

    def handle_remove_phone_number(self) -> str:
        """
        Command handler for 'remove_phone' command. Removes a phone
        number from a contact in the address book.
        """
        contact = self.get_contact_by_name()
        if not contact:
            return 'The is no contact'
        if not contact.phones:
            self.viewer.display_message(f"The contact {contact.name.value} does not have phone.")
            return 'Was entered phone, but contact have not phone number'

        phone_to_remove = self.viewer.get_data_input("Enter phone in an acceptable format:")
        if not Phone(phone_to_remove).validate(phone_to_remove):
            self.viewer.display_error("The phone is not valid.")
            return 'Was entered invalid phone'
        if phone_to_remove not in [record.value for record in contact.phones]:
            self.viewer.display_error(f"The phone {phone_to_remove} does not exist.")
            return 'Was entered phone, but it does not exist'
        contact.remove_phone_number(phone_to_remove)
        self.viewer.display_contacts(self.address_book.get_all_records())
        self.viewer.display_message(f"The phone number {phone_to_remove} has been successfully deleted.")
        return "Finished when removed phone"

    def handle_remove_email(self) -> str:
        """
        Command handler for 'remove_email' command. Removes an email
        address from a contact in the address book.
        """
        contact = self.get_contact_by_name()
        if not contact:
            return 'The is no contact'
        if not contact.email:
            self.viewer.display_message(f"The contact {contact.name.value} does not have email.")
            return 'Was entered email, but contact have not email'

        email_to_remove = self.viewer.get_data_input("Enter email in an acceptable format:")
        if not Email(email_to_remove).validate(email_to_remove):
            self.viewer.display_error("The email is not valid.")
            return 'Was entered invalid email'
        elif email_to_remove != contact.email.value:
            self.viewer.display_error(f"The email {email_to_remove} does not exist "
                                              f"in contact {contact.name.value}.")
            return 'Was entered email, but it does not exist'
        contact.remove_email(email_to_remove)
        self.viewer.display_contacts(self.address_book.get_all_records())
        self.viewer.display_message(f"The email {email_to_remove} has been successfully deleted.")
        return "Finished when removed email"

    def handle_remove_record(self) -> str:
        """
        Command handler for 'remove' command. Removes a contact from
        the address book.
        """
        contact = self.get_contact_by_name()
        if not contact:
            return 'The is no contact'
        name = contact.name.value
        if self.address_book.remove_record(name):
            self.viewer.display_contacts(self.address_book.get_all_records())
            self.viewer.display_message(f"Contact {name} has been successfully removed from the address book.")
            return "Finished when removed contact"

    def handle_find_records(self) -> str:
        """
        Command handler for 'find' command. Searches for contacts
        in the address book based on user-specified criteria.
        """
        search_criteria = {}
        self.viewer.display_message("What criteria would you like to search by?\n"
                                    "1. Search by name\n"
                                    "2. Search by phone number.")
        search_option = self.viewer.get_data_input("Select an option (1 or 2): ")
        if search_option == "1":
            search_name = self.viewer.get_data_input(
                "Enter a name to search for (minimum 2 characters): ").strip().lower()
            if len(search_name) >= 2:
                search_criteria['name'] = search_name
            else:
                self.viewer.display_error("You entered too few characters for the name. Name search canceled.")
                return 'Failed when entered characters for the name!!!'
        elif search_option == "2":
            search_phones = self.viewer.get_data_input(
                "Please enter a part of the phone number for the search (minimum 5 characters): ").strip()
            if len(search_phones) >= 5:
                search_criteria['phones'] = search_phones
            else:
                self.viewer.display_error(
                    "You entered too few characters for a phone number. Phone number search canceled.")
                return 'Failed when entered characters for a phone number!!!'
        else:
            self.viewer.display_error("Invalid option selected.")
            return 'Failed option selected!!!'
        results = self.address_book.find_records(**search_criteria)
        if results:
            find = ', '.join([record.name.value for record in results])
            self.viewer.display_message(f"Search results: {find}")
            return 'Finish!!!'
        else:
            self.viewer.display_error("The contact meeting the specified criteria was not found.")
            return 'Failed!!!'

    def handle_get_all_records(self) -> str:
        """
        Command handler for 'all' command. Retrieves and
        returns None.
        """
        self.viewer.display_contacts(self.address_book.get_all_records())
        return 'Found!!!'

    def handle_days_to_birthday(self) -> str:
        """
         Command handler for 'when_birthday' command. Calculates the
         days until the birthday of a contact
        """
        contact = self.get_contact_by_name()
        if not contact:
            return 'The is no contact'
        if contact.birthday:
            days = contact.days_to_birthday()
            self.viewer.display_message(f"Name {contact.name.value} has {days} days left until their birthday.")
            return 'Found'
        else:
            return self.viewer.display_message(f"The contact {contact.name.value} does not have a birthdate specified.")

    def handle_get_birthdays_per_week(self) -> str:
        """
        Command handler for 'get_list' command. Retrieves birthdays
        for the specified number of days ahead.
        """
        num_str = self.viewer.get_data_input("Enter the number of days: ")
        if num_str.isdigit():
            num_days = int(num_str)
            birthdays_list = self.address_book.get_birthdays_per_week(num_days)
            if birthdays_list:
                self.viewer.display_message("\n".join(birthdays_list))
                return 'Found'
            else:
                self.viewer.display_message("No birthdays today.")
                return 'Not founded'
        else:
            self.viewer.display_error('Not a number')
            return 'Failed'

    def handle_load_from_file(self) -> str:
        """
        Command handler for 'load_from_file' command. Loads the address
        book data from a file.
        """
        arg = self.arg.strip()
        if arg and (not Path(arg).exists() or not Path(arg).is_file()):
            return self.viewer.display_message(f"The file path does not exist")
        arg = arg if arg else str(PATH_TO_SAVE)
        file_handler = AddressBookFileHandler(arg)
        loaded_address_book = file_handler.load_from_file()
        self.address_book.data.update(loaded_address_book.data)
        return self.viewer.display_message(f"The address book is loaded from a file {arg}")

    def handle_save_to_file(self) -> str:
        """
        Command handler for 'save' command. Saves the address
        book data to a file.
        """
        PATH_TO_SAVE.parent.mkdir(parents=True, exist_ok=True)
        file_handler = AddressBookFileHandler(str(PATH_TO_SAVE))
        file_handler.save_to_file(self.address_book)
        return self.viewer.display_message(f"The address book has been saved at the following path {str(PATH_TO_SAVE)}")

    def handle_exit(self) -> bool:
        """
        Command handler for 'exit' command. Exits the address book application.
        """
        self.handle_save_to_file()
        return False

    def handle_help(self) -> str:
        """Outputs the command menu"""
        self.viewer.display_commands()
        return 'Help'

    @input_error
    def main_cycle(self) -> bool:
        """
        Return True if it needs to stop the program. False otherwise.
        """
        user_input = self.viewer.get_user_input()
        func = self.command_parser(user_input)
        result = func()
        return result


def choose_viewer() -> UserViewer:
    """
    Prints initial information to the user and returns
    the chosen viewer mode.
    """
    init_colorama()
    print(Fore.BLUE + Style.BRIGHT + LOGO)
    print(Fore.CYAN + "Welcome to your ADDRESS BOOK!")
    print()

    print("Choose how to show commands in the console or on the screen:")
    print("1 - Console")
    print("2 - Screen")
    mode = input("Enter your choice (1/2): ").strip()
    if mode == '1':
        viewer = ConsoleUserViewer()
    elif mode == '2':
        viewer = GuiUserViewer()
    else:
        print("Invalid choice. Defaulting to Console mode.")
        viewer = ConsoleUserViewer()
    viewer.display_commands()
    return viewer


def main():
    """
    Main entry point for the address book program.
    This function initializes the address book, prepares
    the environment, and enters the main program loop.
    """
    viewer = choose_viewer()
    address_book = AddressBook()
    bot = BotAdressBook(viewer, address_book)
    bot.handle_load_from_file()

    while True:
        if not bot.main_cycle():
            break


if __name__ == '__main__':
    main()
