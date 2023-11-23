from pathlib import Path


# User commands and descriptions
LOGO = """
                .o8        .o8                                       
               "888       "888                                       
 .oooo.    .oooo888   .oooo888  oooo d8b  .ooooo.   .oooo.o  .oooo.o 
`P  )88b  d88' `888  d88' `888  `888""8P d88' `88b d88(  "8 d88(  "8 
 .oP"888  888   888  888   888   888     888ooo888 `"Y88b.  `"Y88b.  
d8(  888  888   888  888   888   888     888    .o o.  )88b o.  )88b 
`Y888""8o `Y8bod88P" `Y8bod88P" d888b    `Y8bod8P' 8""888P' 8""888P' 

             .o8                           oooo        
            "888                           `888        
             888oooo.   .ooooo.   .ooooo.   888  oooo  
             d88' `88b d88' `88b d88' `88b  888 .8P'   
             888   888 888   888 888   888  888888.    
             888   888 888   888 888   888  888 `88b.  
             `Y8bod8P' `Y8bod8P' `Y8bod8P' o888o o888o 
"""

PATH_TO_SAVE = Path.home() / "orgApp" / "address_book.json"  # for working on different filesystems
PATH_TO_SAVE.parent.mkdir(parents=True, exist_ok=True)


COMMANDS = {
    'add_email': ['add_email'],
    'add_phone_number': ['add_phone'],
    'add_record': ['add'],
    'change_email': ['change_email'],
    'change_phone_number': ['change_phone'],
    'days_to_birthday': ['when_birthday'],
    'exit': ['exit'],
    'find_records': ['find'],
    'get_all_records': ['all'],
    'get_birthdays_per_week': ['get_list'],
    'load_from_file': ['load'],
    'remove_email': ['remove_email'],
    'remove_phone_number': ['remove_phone'],
    'remove_record': ['remove'],
    'save_to_file': ['save'],
    'help': ['help']
}

COMMAND_DESCRIPTIONS = {
    'add an email': ['add_email'],
    'add a phone number': ['add_phone'],
    'add contact to AdressBook ': ['add'],
    'change an email ': ['change_email'],
    'change phone number': ['change_phone'],
    'return days until birthday': ['when_birthday'],
    'exit from AdressBook ': ['exit'],
    'find contact in AdressBook': ['find'],
    'display all contacts': ['all'],
    'return list of birthdays': ['get_list'],
    'load information about contacts from file': ['load'],
    'remove an email': ['remove_email'],
    'remove phone number': ['remove_phone'],
    'remove contact from AdressBook': ['remove'],
    'save information about contacts to file': ['save'],
    'display help': ['help']
}

