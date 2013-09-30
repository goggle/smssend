import csv
from AddressException import AddressException

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

    def printPhonebook(self):
        #print('Sort by: ' + self.sortBy)
        for contact in self.phonebook:
            #print('Forename: ' + contact.getForename())
            #print('Name: ' + contact.getName())
            #print('Phone number: ' + contact.getPhonenumber())
            #print()
            print( contact.getForename() + ' ' + contact.getName() + ' (' + contact.getPhonenumber() + ')')

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
        # TODO: FileNotFoundError
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
        with open(self.contactfile, 'w', newline='') as cfile:
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
        If the specified contact is not stored in the phone book, raise an exception.

        """
        delcontact = Contact(forename, name, '-1')
        count = 0
        deleted = False
        for c in self.phonebook:
            compare_value = delcontact.compare(c)
            if compare_value == 1:
                del self.phonebook[count]
                deleted = True
                self.saveContacts()
                break
            count += 1
        if deleted == False:
            raise AddressException('No contact deleted.')

    def getNameAndNumberList(self):
        """Get a list of the names ('forename name') and phone numbers from the phone book.

        """
        names = []
        numbers = []
        for c in self.phonebook:
            forename = c.getForename()
            name = c.getName()
            fullname = forename + ' ' + name
            names.append(fullname)
            number = c.getPhonenumber()
            numbers.append(number)
        return names, numbers


    def getContact(self, forename, name):
        """Retrieves the desired contact from the phone book and raises an AddressException, 
        if the contact is not part of the phone book.

        """
        contact = Contact(forename, name, '-1')
        count = 0

        for c in self.phonebook:
            compare_value = contact.compare(c)
            if compare_value == 1:
                return c

        raise AddressException('Contact is not part of the phone book')

    def getContact(self, fullname):
        """Retrieves the desired contact from the phone book and raises an AddressException, 
        if the contact is not part of the phone book.

        """
        for contact in self.phonebook:
            cname = contact.getForename() + ' ' + contact.getName()
            if cname == fullname:
                return contact
        raise AddressException('Contact is not part of the phone book')
                




