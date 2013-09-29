#!/usr/bin/env python

from SmsConnect import SmsConnect
from Phonebook import Phonebook
from AddressException import AddressException
import sys


def print_help():
    print('Available commands:')
    print('\tn,   new       - Compose an SMS')
    print('\ta,   add       - Add a new contact')
    print('\td,   del       - Delete a contact')
    print('\tc,   contacts  - Show contacts')
    print('\th,   help      - Show this help information')
    print('\tq,   quit      - Quit this program')

def printRemainingSms(smsconnect):
    try:
        print('You have ' + str(smsconnect.getCreditLimit()) + ' sms remaining.')
    except ConnectionError:
        print('Could not get the available credits.')

def decide(yesno):
    if yesno == 'y' or yesno == 'Y' or yesno == 'yes' or yesno == 'Yes' or yesno == '':
        return True
    return False
    

def main():
    sms = SmsConnect()
    book = Phonebook()

    # Parse config file and read login data:
    sms.readLoginData()

    # Retrieve the contacts from the contacts file:
    book.readContacts()

    print('You are logged in as ' + sms.getUsername() + '.')
    printRemainingSms(sms)

    print("Use 'h' or 'help' to show the available commands.")

    while 1:
        inp = input('> ').strip().lower().partition(' ')
        choice = inp[0]
        params = inp[2]

        if choice in ['h', 'help']:
            print_help()

        elif choice in ['q', 'quit']:
            break

        elif choice in ['c', 'contacts']:
            book.printPhonebook()

        elif choice in ['a', 'add']:
            print('Add a new contact to the phone book.')
            print('Note: A Swiss phone number should begin with 0041.')
            try:
                inp = input('Forename > ').strip()
                forename = inp
                inp = input('Name > ').strip()
                name = inp
                inp = input('Phone number > ').strip()
                number = inp
                number = number.replace(' ', '')
            except(EOFError, KeyboardInterrupt):
                print()
                continue 
            
            try:
                book.addContact(forename, name, number)
                print("Contact '" + forename + ' ' + name + "' added to your phone book.")
            except(AddressException):
                print("'" + forename + ' ' + name + "' already exists in your phone book. No contact added.")
                continue

        elif choice in ['d', 'del']:
            print('Delete a contact from the phonebook.')
            print('Enter the forename and name of the contact that should be deleted.')
            try:
                inp = input('Forename > ').strip()
                forename = inp
                inp = input('Name > ').strip()
                name = inp
            except(EOFError, KeyboardInterrupt):
                print()
                continue
            try:
                book.delContact(forename, name)
                print("Contact '" + forename + ' ' + name + "' removed from the phone book.")
            except(AddressException) as e:
                print( forename + ' ' + name + ' not found in the phone book.')
                #print(e)
                continue


        else:
            print("Unknown command! Try 'h' or 'help' to see the available commands")

    print('\nGoodbye!')



try:
    main()
except(EOFError, KeyboardInterrupt):
    print('\nGoodbye!')
    sys.exit(0)

