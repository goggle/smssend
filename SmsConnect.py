import requests
import json
import hashlib
import time
import datetime
from Phonebook import Contact

class SmsConnect:
    def __init__(self):
        self.url = 'http://api.boxis.net/'
        self.username = ''
        self.phonenumber = ''
        self.apikey = ''
        self.version = '1.0'
        self.section = 'sms'
        self.returntype = 'json'
        self.timestamp = ''
        self.authcode = ''

    def boolToInt(self, boolval):
        if boolval:
            return 1
        else:
            return 0


    def getTimestamp(self):
        ts = int(time.time())
        return str(ts)

    def getAuthcode(self, timestamp, apikey):
        concatkey = timestamp + apikey
        md = hashlib.md5(concatkey.encode('utf-8'))
        return md.hexdigest()

    def readLoginData(self):
        """
        Read the login data:

        Reads the login data (username, apikey and phone number) from the file
        'login.conf'.
        """
        f = open('login.conf', 'r') # TODO: exception handling
        self.username = f.readline()
        self.apikey = f.readline()
        self.phonenumber = f.readline()
        self.username = self.username.strip('\n')
        self.apikey = self.apikey.strip('\n')
        self.phonenumber = self.phonenumber.strip('\n')
        f.close()

    def getCreditLimit(self):
        """Get the available credit (as an integer value).


        """
        self.timestamp = self.getTimestamp()
        self.authcode = self.getAuthcode(self.timestamp, self.apikey)
        payload = {'version':self.version,
                'timestamp':self.timestamp,
                'username':self.username,
                'authcode':self.authcode,
                'returntype':self.returntype,
                'section':self.section,
                'action':'getCreditLimit'
                }
        r = requests.post(self.url, payload)
        if int(r.json()['result']) == 1: # success
            return int(r.json()['params']['credit'])
        else: # TODO: error handling
            return

    def calculateCredits(self, message, recipients_count, fast=False):
        """Calculate how many credits you need to send a message. (Returns an integer).

        Keyword arguments:
        message -- the message string
        recipients_count -- number of message recipients (as an integer)


        """
        self.timestamp = self.getTimestamp()
        self.authcode = self.getAuthcode(self.timestamp, self.apikey)
        payload = {'version':self.version,
                'timestamp':self.timestamp,
                'username':self.username,
                'authcode':self.authcode,
                'section':self.section,
                'action':'calculateCredits',
                'recipients_count':recipients_count,
                'content':message,
                'encoding':'UTF-8',
                'fast':self.boolToInt(fast),
                'returntype':self.returntype
                }
        r = requests.post(self.url, payload)
        if int(r.json()['result']) == 1: # success
            return r.json()['params']['credit']
        else: # TODO error handling
            return


#    def getSenderNames(self):
#        self.timestamp = self.getTimestamp()
#        self.authcode = self.getAuthcode(self.timestamp, self.apikey)
#        payload = {'version':self.version,
#                'timestamp':self.timestamp,
#                'username':self.username,
#                'authcode':self.authcode,
#                'section':self.section,
#                'returntype':self.returntype,
#                'action':'getSenderNames'
#                }
#        r = requests.post(self.url, payload)
#        return r

#    def getHistory(self):
#        self.timestamp = self.getTimestamp()
#        self.authcode = self.getAuthcode(self.timestamp, self.apikey)
#        payload = {'version':self.version,
#                'timestamp':self.timestamp,
#                'username':self.username,
#                'authcode':self.authcode,
#                'section':self.section,


    def sendSms(self, recipients, message, flash=False, fast=False, schedule=False,
            timesend=datetime.datetime.today()):
        """Sends a sms to all the specified recipents.

        Keywort arguments:
        recipients -- a list of contact objects
        message -- the message text as a string
        flash -- enable sending the message in flash mode (boolean)
        fast -- enable sending the message in fast mode (boolean)
        schedule -- enable message scheduling (boolean)
        timesend -- a datetime object that indicates, when the message should be send


        """
        self.timestamp = self.getTimestamp()
        self.authcode = self.getAuthcode(self.timestamp, self.apikey)

        recipients_numbers = []
        for contact in recipients:
            recipients_numbers.append(contact.getPhonenumber())

        payload = {'version':self.version,
                'timestamp':self.timestamp,
                'username':self.username,
                'sender_name':self.phonenumber,
                'authcode':self.authcode,
                'section':self.section,
                'action':'sendSMS',
                #'recipients':recipients_numbers,
                'content':message,
                'encoding':'UTF-8',
                'flash':self.boolToInt(flash),
                'fast':self.boolToInt(fast),
                'returntype':self.returntype
                }
        c = 1
        for number in recipients_numbers:
            rec = 'recipients[' + str(c) + ']'
            payload.update({rec:number})
            c += 1

        if schedule:
            year = str(timesend.year)
            month = str(timesend.month)
            if len(month) == 1:
                month = '0' + month
            day = str(timesend.day)
            if len(day) == 1:
                day = '0' + day
            hour = str(timesend.hour)
            if len(hour) == 1:
                hour = '0' + hour
            minute = str(timesend.minute)
            if len(minute) == 1:
                minute = '0' + minute
            timesend_string = year + '-' + month + '-' + day + ' ' + hour + ':' + minute
            payload.update({'schedule':1, 'timesend':timesend_string})

        print(payload)
        r = requests.post(self.url, payload)
        return r


    def splitmessage(self, message):
        """If a message is longer than 3 sms, we need to split it into several messages.
        This method returns a list of splitted sms.
        IMPORTANT: We assume, that the message contains no special characters!

        """
        msg_list = []
        max_len = 459
        msg = message
        while len(msg) > 0:
            msg_list.append(msg[:max_len])
            msg = msg[max_len:]
        return msg_list

        


