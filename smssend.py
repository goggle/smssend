#/usr/bin/env python

import Phonebook
import SmsConnect


def print_help():
    print('Available commands:')
    print('\tn,   new       - Compose an SMS')
    print('\ta,   add       - Add a new contact')
    print('\td,   del       - Delete a contact')
    print('\tc,   contacts  - Show contacts')

def main():
    sms = SmsConnect()
    book = Phonebook()

    # Parse config file and read login data:
    sms.readLoginData()

    # Retrieve the contacts from the contacts file:
    book.readContacts()

    print('You are logged in as %s.', sms.getUsername())
    print('You have %d sms remaining', sms.getCreditLimits())


