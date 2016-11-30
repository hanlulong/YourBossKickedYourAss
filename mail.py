import imaplib
import datetime
import messagebird
import email
from time import sleep
import logging

username = 'yourcamid'
password = 'yourcampassword'
yourphone = '0044XXXXXXXXXX'
message = 'Hi Lu, your boss kicked your ass!'

interval = 300 # time interval between two checks, in seconds
messagebird_secret = 'live_XXXXXXXXXXXXXXXXXXXXXXXXX'




from optparse import OptionParser

parser = OptionParser()
parser.add_option("-l", "--log", dest="loglevel", help="log level")
(options, args) = parser.parse_args()
usrloglevel = getattr(logging, options.loglevel.upper())
logging.basicConfig(level=usrloglevel, format='%(asctime)s - %(name)s [%(levelname)s]: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# note that if you want to get text content (body) and the email contains
# multiple payloads (plaintext/ html), you must parse each message separately.
# use something like the following: (taken from a stackoverflow post)
def get_first_text_block(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()




while True:
    try:
    	mail = imaplib.IMAP4_SSL('imap.hermes.cam.ac.uk',993)
    	mail.login(username, password)

        # Out: list of "folders" aka labels in gmail.
    	mail.select("inbox",readonly=True) # connect to inbox.

    	date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
    	senderList = ["giancarlo.corsetti@gmail.com","mc865@cam.ac.uk","crowley.meredith@gmail.com","zl290@cam.ac.uk","hanlulong@gmail.com"]

    	for sender in senderList:
            result, data = mail.uid('search', None, '(UNSEEN SENTSINCE {date} FROM {sender})'.format(date=date,sender=sender))

            if len(data[0]) > 0:
            	print data[0]
            	latest_email_uid = data[0].split()[-1]
            	result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')

            	raw_email = data[0][1]
            	# including headers and alternate payloads
            	email_message = email.message_from_string(raw_email)
            	print email.utils.parseaddr(email_message['From'])
            	client = messagebird.Client(messagebird_secret)

            	message = client.voice_message_create(
                            yourphone,
                            message,
                            { 'language' : 'en-gb', 'voice': 'male' }
                            )

    	logging.info('Sleeping for 5 minutes.')
    	sleep(300)
    except Exception as e:    
    	log.error("Error in %s", e)
        pass
