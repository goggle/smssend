import csv
import AddressException

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

    def getContact(self):
        return self.contact

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
        self.contactfile = 'contacts.csv'
        self.readContacts()

    def printPhonebook(self):
        print('Sort by: ' + self.sortBy)
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

    def readContacts(self):
        """Read the contacts form the contact file.

        """
        # FileNotFoundError
        with open(self.contactfile, 'r', newline='') as cfile:
            reader = csv.DictReader(cfile, ['forename', 'name', 'phonenumber'], delimiter=';')
            for row in reader:
                forename = row['forename']
                name = row['name']
                number = row['phonenumber']
                self.addContact(forename, name, number)



    def saveContacts(self):
        """Saves the phone book to the contact file.

        """
        with open(contactfile, 'w', newline='') as cfile:
            writer = csv.DictWriter(cfile, ['forename', 'name', 'phonenumber'], extrasaction='ignore', delimiter=';')
            for c in self.phonebook:
                writer.writerow(c.getContact())


    def addContact(self, forename, name, phonenumber):
        """Adds a contact to the phone book.

        """
        contact = Contact(forename, name, phonenumber)
        for c in self.phonebook:
            compare_value = contact.compare(c)
            if compare_value == 1:
                raise AddressException('Name and forename already exist in the phone book.')
                return
            elif compare_value == 2:
                raise AddressException('Phone number already exists in the phone book.')
                return

        self.phonebook.append(contact)
        self.phonebook.sort()
        self.saveContacts()


    def delContact(self, forename, name):
        """Removes a contact from the phone book.
        If the specified contact is not stored in the phone book, nothing happens.

        """
        delcontact = Contact(forename, name, '-1')
        count = 0
        for c in self.phonebook:
            compare_value = delcontact.compare(c)
            if compare_value == 1:
                del self.phonebook[count]
            count += 1

        self.saveContacts()



