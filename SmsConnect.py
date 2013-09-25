import requests
import json
import hashlib
import time

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

    def calculateCredits(self, message, recipients_count):
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
                'fast':0,
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

    def sendSms(self, message):
        return


