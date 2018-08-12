import smtplib
import time
import imaplib
import email
import sys
import tempfile

#Opens and reads any emails from Gmail
#In order to use fill in the required fields
#Make sure you adjust Gmail settings accordingly
#by going to settings -> forwarding and POP/IMAP -> enable IMAP
#and also allow access for less secure apps.
class Readmail:

    def read_email_from_gmail():

        FROM_EMAIL = "breakthewall72079@gmail.com" #Enter the email name
        FROM_PWD = "speechrecognition" #Enter email password
        SMTP_SERVER = "imap.gmail.com"
        NUM_TO_READ = 10 #Replace with number of earliest emails desired

        try:

            #Establish a connection and login to the Gmail account
            mail = imaplib.IMAP4_SSL(SMTP_SERVER)
            mail.login(FROM_EMAIL,FROM_PWD)

            #Look for all emails in the inbox
            mail.select('inbox')
            typ, data = mail.search(None, 'ALL')
            
            x = 0
            idList = []

            #Get a list of all the email ids, reverse it so that 
            #the newest ones are at the front of the list
            for id in data[0].rsplit():
                idList.append(id)

            idList = list(reversed(idList))



            #Fetch the first NUM_to_READ email subject lines and 
            #their recipients
            for id in idList:
                typ, data = mail.fetch(id, '(RFC822)')
                msg = email.message_from_bytes(data[0][1])
                
                
                if x >= NUM_TO_READ:
                    break
                else:
                    x += 1
                    msg = email.message_from_bytes(data[0][1])

                    print('Message #', x)
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print('From : ' + email_from)
                    print('Subject : ' + email_subject + '\n')

            #Allow the user to read the content of any emails
            while(1):
                message_to_read = 10
                message_to_read = int(message_to_read)

                #Basic error checking
                while (message_to_read < 1) or (message_to_read > NUM_TO_READ):
                    if (message_to_read == -1):
                        sys.exit()

                    print("Please enter a valid message #")    
                    message_to_read = input("Which message would you like to open?")
                    
                #Parse the desired email
                typ, data = mail.fetch(idList[message_to_read-1], '(RFC822)')
                msg = email.message_from_bytes(data[0][1])
                #print(msg)

                print('\nReading message:\n')

                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        #print(part.get_payload(decode=True).decode('utf-8'))
                        file = part.get_payload(decode=True).decode('utf-8')
                        #print(file)
                
                for line in file:
                    print(line, end = '', flush = True)
                    
                print('\n')
                #Create a temp file to write email contents to
                #and then read from the temporary file
                #Note we can replace all the file code with a print statement
                #and disregard the whole issue with the temp file
                #This was simply for the purpose of using a tempfile with python
                '''
                tmp = tempfile.NamedTemporaryFile()
                with open(tmp.name, 'w') as f:
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            #print(part.get_payload(decode=True).decode('utf-8'))
                            file = part.get_payload(decode=True).decode('utf-8')
                            print(file)
                            f.write(part.get_payload(decode=True).decode('utf-8'))
                with open(tmp.name, 'r') as f:
                    f.seek(0)
                    for line in f:
                        print(line, end = '', flush = True)
                '''

        except:
            sys.exit()

        
    read_email_from_gmail()
