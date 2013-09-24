import csv

class Contact:
    def __init__(self, forename, name, phonenumber):
        self.contact = {'forename':forename,
                'name':name,
                'phonenumber':phonenumber
                }
        self.sortBy = 'forename' 
    
    def getForename(self):
        return self.contact['forename']

    def getName(self):
        return self.contact['name']

    def getPhonenumber(self):
        return self.contact['phonenumber']

    def setForename(self, forename):
        self.contact['forename'] = forename

    def setName(self, name):
        self.contact['name'] = name

    def setPhonenumber(self, number):
        self.contact['phonenumber'] = number

    def sortByName(self):
        self.sortBy = 'name'

    def sortByForename(self):
        self.sortBy = 'forename'

    def compare(self, contact):
        """Compare this contact object to another. Returns 1, 
        if the forename and name correspond. Returns 2,
        if the phone numbers are the same and returns 0 else.

        Keyword arguments:
        contact -- the other contact object to compare with

        """
        if self.getForename() == contact.getForename() and self.getName() == contact.getName():
            return 1
        elif self.getPhonenumber() == contact.getPhonenumber():
            return 2
        else:
            return 0

    def __lt__(self, contact):
        if self.sortBy == 'name':
            #return self.getName() < contact.getName()
            if self.getName() < contact.getName():
                return True
            elif self.getName() == contact.getName():
                return self.getForename() < contact.getForename()
            else:
                return False
        else:
            #return self.getForename() < contact.getForename()
            if self.getForename() < contact.getForename():
                return True
            elif self.getForename() == contact.getForename():
                return self.getName() < contact.getName()
            else:
                return False

    def __eq__(self, contact):
        if self.sortBy == 'name':
            return self.getName() == contact.getName()
        else:
            return self.getForename() == contact.getForename()


class Phonebook:

    def __init__(self):
        self.phonebook = []
        self.sortBy = 'forename' 

    def printPhonebook(self):
        for contact in self.phonebook:
            print('Forename: ' + contact.getForename())
            print('Name: ' + contact.getName())
            print('Phone number: ' + contact.getPhonenumber())
            print()

    def sortByName(self):
        self.sortBy = 'name'
        for contact in self.phonebook:
            contact.sortByName()

    def sortByForename(self):
        self.sortBy = 'forename'
        for contact in self.phonebook:
            contact.sortByForeame()


    def addContact(self, forename, name, phonenumber):
        """Adds a contact to the phone book.

        """
        contact = Contact(forename, name, phonenumber)
        self.phonebook.append(contact)
        # TODO: Save the phone book
