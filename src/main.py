import imaplib
import datetime
import email
from time import sleep
import logging
import argparse
import os, sys
import json
import getpass

import messagebird
# Messagebird is a message api service provider. see https://www.messagebird.com/en-gb/,
# Each voice call cost you 2 pence.
# An alternative is twilio.



sys.path.append(os.path.dirname(os.path.realpath(__file__)))


def load_config():
    config_file = "config.json"

    # If config file exists, load variables from json
    load   = {}
    if os.path.isfile(config_file):
        with open(config_file) as data:
            load.update(json.load(data))
    return load

def init_config(account_index):

    parser = argparse.ArgumentParser()
    load = load_config()

    # Read passed in Arguments
    required = lambda x: not x in load['accounts'][account_index].keys()

    parser.add_argument("-a", "--auth_service", help="Auth Service ('cam' or 'gmail')",
        required=required("auth_service"))
    parser.add_argument("-u", "--username", help="Username", required=required("username"))
    parser.add_argument("-p", "--password", help="Password", required=required("password"))
    parser.add_argument("-s", "--messagebird_secret", help="Messagebird API Secret")
    parser.add_argument("-b", "--mybosses", help="Email List")
    parser.add_argument("-n", "--phonenumbers", help="List of My Phone Numbers")
    parser.add_argument("-m", "--greetings", help="Your Greetings")
    parser.add_argument("-t", "--interval", help="Time Interval Between 2 Checks")
    config = parser.parse_args()

    config.__dict__["messagebird_secret"] = load['messagebird_secret']
    config.__dict__["mybosses"] = load['mybosses']
    config.__dict__["phonenumbers"] = load['phonenumbers']
    config.__dict__["greetings"] = load['greetings']
    config.__dict__["interval"] = load['interval']

    load = load['accounts'][account_index]
    # Passed in arguments shoud trump
    for key in config.__dict__:
        if key in load and config.__dict__[key] == None:
            config.__dict__[key] = load[key]

    if config.__dict__["password"] is None:
        logging.info("Secure Password Input (if there is no password prompt, use --password <pw>):")
        config.__dict__["password"] = getpass.getpass()

    if config.auth_service not in ['cam', 'gmail']:
      logging.error("Invalid Auth service specified! ('cam' or 'gmail')")
      return None


    return config




logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s[%(levelname)s]: %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S')


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

def main():
    load = load_config()
    for i in range(len(load['accounts'])):
        config = init_config(i)

        if not config:
            return

        logging.info("Checking for %s server: USERNAME %s." % (config.auth_service, config.username))

        try:
            if config.auth_service == 'cam':
                mail = imaplib.IMAP4_SSL('imap.hermes.cam.ac.uk', 993)
            else:
                mail = imaplib.IMAP4_SSL('imap.gmail.com')

            mail.login(config.username, config.password)

            # Out: list of "folders" aka labels in gmail.
            mail.select("inbox", readonly=True)  # connect to inbox.

            date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
            senderList = config.mybosses

            for sender in senderList:
                result, data = mail.uid('search', None,
                                        '(UNSEEN SENTSINCE {date} FROM {sender})'.format(date=date, sender=sender))

                if len(data[0]) > 0:
                    print data[0]
                    latest_email_uid = data[0].split()[-1]
                    result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')

                    raw_email = data[0][1]
                    # including headers and alternate payloads
                    email_message = email.message_from_string(raw_email)
                    boss = email.utils.parseaddr(email_message['From'])
                    voicemessage = "You received an email from %s, %s" % (boss[0], boss[1])
                    logging.info(voicemessage)
                    client = messagebird.Client(config.messagebird_secret)
                    for number in config.phonenumbers:
                        message = client.voice_message_create(
                            number,
                            ' '.join([config.greetings,voicemessage]),
                            {'language': 'en-gb', 'voice': 'male'}
                        )
                        # you can overwrite the setting for message and voice. For details, please refer to
                        # https://developers.messagebird.com/docs/voice
            logging.info("Check completed. No important email found.")

        except Exception as e:
            logging.error("Error in %s", e)
            pass



if __name__ == '__main__':

    config = init_config(0)
    print " "
    print "Mail Checker Written by Lu Han"
    print "Read your boss' emails or the program will keep calling you every %s minutes." % config.interval
    print "Mail list of your bosses:"
    print "%s"  % ", ".join(config.mybosses)
    print " "
    print " "
    sleep(5)

    while True:
        main()
        logging.info('Sleeping for %s minutes.' % config.interval)
        sleep(config.interval * 60)
