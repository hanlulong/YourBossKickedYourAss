# Your Boss Kicked Your Ass

* Connect to your cam hermes email and/or gmail account.
* Check incoming mails every x minutes.
* Call/Message you if you received an email from your boss.  
* If you do not read your boss' email, the program will keep calling you every x minutes. 

# Installation 
1. Copy or clone this repository 
2. Edit your info in config.json (camid, mail list, phone number, messagebird_api_serect, etc.)
3. Run main.exe


# Voice call service 
I use messagebird as the voice call service provider and each voice call to UK numbers costs 2 pences. In config.json, I included an messagebird_api_secret worth of 15 pounds which should make approx 750 calls. You need to buy our own credit after the value of this secret is depleted. Please refer to https://www.messagebird.com/en-gb/pricing.

An alternative provider could be Twilio.

# 
1. Auto start in windows

2. Remote control over settings.
* You could save the this repository in your dropbox folder. And then edit the config.json file through your dropbox.
