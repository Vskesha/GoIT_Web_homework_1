from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import simpledialog

from colorama import Fore
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit import prompt

from commands import COMMANDS, COMMAND_DESCRIPTIONS


class UserViewer(ABC):
    @abstractmethod
    def display_contacts(self, contacts):
        pass

    @abstractmethod
    def display_commands(self):
        pass

    @abstractmethod
    def get_user_input(self):
        pass

    @abstractmethod
    def get_data_input(self, prompt):
        pass

    @abstractmethod
    def display_message(self, message):
        pass

    @abstractmethod
    def display_error(self, message):
        pass


class ConsoleUserViewer(UserViewer):
    def display_contacts(self, contacts):
        formatted_contacts = self.format_contacts(contacts)
        print(formatted_contacts)

    def format_contacts(self, contacts):
        all_contacts = []
        header = '{:<20} {:<30} {:<20} {:<20}'.format('Name', 'Phone', 'Birthday', 'Email')
        separator = '-' * len(header)
        all_contacts.append(header)
        all_contacts.append(separator)
        if contacts:
            for record in contacts:
                phones = ', '.join([f'{phone.value}' for phone in record.phones])
                birthday_str = record.birthday.value if record.birthday else '-'
                email_str = record.email.value if record.email else '-'
                record_str = '{:<20} {:<30} {:<20} {:<20}'.format(
                    record.name.value,
                    phones,
                    birthday_str,
                    email_str
                )
                all_contacts.append(record_str)
        else:
            all_contacts.append("The address book is empty.")

        return '\n'.join(all_contacts)

    def display_commands(self):
        print(Fore.GREEN, "Available commands:")
        separator = '|----------------------|--------------------------------------------|'
        print(separator, f'\n|  Commands            |  Description {" ":30}|\n', separator, sep='')
        for description, commands in COMMAND_DESCRIPTIONS.items():
            print(f"| {Fore.WHITE} {', '.join(commands):<20}{Fore.GREEN}| {description:<43}|")
        print(separator, '\n')

    def get_user_input(self):
        completer = NestedCompleter.from_nested_dict({command[0]: None for command in COMMANDS.values()})
        user_input = prompt('>>>', completer=completer, lexer=None).strip().lower()
        return user_input

    def get_data_input(self, prompt):
        return input(prompt)

    def display_message(self, message):
        print(message)

    def display_error(self, message):
        print(message)


class GuiUserViewer(UserViewer):
    def __init__(self):
        super().__init__()
        self.window = tk.Tk()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.title("Address Book")
        self.window.geometry(f"{screen_width // 2}x{screen_height // 2}+0+0")
        self.command_text = tk.Text(self.window, wrap=tk.WORD, width=65, height=22)
        self.command_text.pack()

        self.contacts_window = tk.Toplevel(self.window)
        self.contacts_window.title("Contacts Window")
        self.contacts_window.geometry(f"{screen_width // 2}x{screen_height // 2}+{screen_width - screen_width // 2}+0")
        self.contacts_text = tk.Text(self.contacts_window, wrap=tk.WORD, width=80, height=30)
        self.contacts_text.pack()
        self.contacts_window.withdraw()

        self.message_window = tk.Toplevel(self.window)
        self.message_window.geometry(
            f"{screen_width // 3}x{screen_height // 10}+{(screen_width - screen_width // 3) // 2}"
            f"+{(screen_height + screen_height // 10) // 2}")
        custom_font = ("Helvetica", 13)
        self.message_label = tk.Label(self.message_window, text="", width=50, height=5, font=custom_font,
                                      wraplength=380)
        self.message_label.pack()
        self.message_window.withdraw()

    def display_contacts(self, contacts):
        self.contacts_window.deiconify()
        self.contacts_text.delete(1.0, tk.END)
        if contacts:
            formatted_contacts = []
            header = '{:<20} {:<30} {:<15} {:<15}'.format('Name', 'Phone', 'Birthday', 'Email')
            separator = '-' * len(header)
            formatted_contacts.append(header)
            formatted_contacts.append(separator)

            for record in contacts:
                phones = ', '.join([f'{phone.value}' for phone in record.phones])
                birthday_str = record.birthday.value if record.birthday else '-'
                email_str = record.email.value if record.email else '-'
                record_str = '{:<20} {:<30} {:<15} {:<15}'.format(
                    record.name.value,
                    phones,
                    birthday_str,
                    email_str
                )
                formatted_contacts.append(record_str)

            self.contacts_text.insert(1.0, '\n'.join(formatted_contacts))
            self.window.after(10000, self.contacts_window.withdraw)
        else:
            self.contacts_text.insert(tk.END, "The address book is empty.")
            self.window.after(10000, self.contacts_window.withdraw)

    def display_commands(self):
        self.command_text.delete(1.0, tk.END)
        separator = '|------------------|--------------------------------------------|\n'
        self.command_text.insert(tk.END, separator)
        self.command_text.insert(tk.END, f'\n|  Commands        |  Description {" ":30}|\n')
        self.command_text.insert(tk.END, separator)
        for description, commands in COMMAND_DESCRIPTIONS.items():
            self.command_text.insert(tk.END, f"| {', '.join(commands):<17}| {description:<43}|\n")
        self.command_text.insert(tk.END, separator)

    def get_user_input(self):
        self.window.deiconify()
        self.command_text.pack()
        user_input = tk.simpledialog.askstring("User Input", "Enter a command:")
        return user_input

    def get_data_input(self, prompt):
        self.command_text.forget()
        self.window.withdraw()
        data_input = simpledialog.askstring("Data Input", prompt)
        return data_input

    def display_message(self, message):
        self.message_window.deiconify()
        self.message_label.config(text=message)
        self.window.after(7000, self.message_window.withdraw)
        return message

    def display_error(self, message):
        self.message_window.deiconify()
        self.message_label.config(text=message)
        self.window.after(7000, self.message_window.withdraw)
        return message
