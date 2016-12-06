# Your Boss Kicked Your Ass

* Connect to your Cambridge Hermes email and/or Gmail account.
* Check incoming mails every x minutes.
* Call/message you if you received an email from your boss.  
* If you do not read your boss' email, the program will keep calling you every x minutes. 

## Installation 
1. Copy or clone this repository to your local directory.
2. Edit your info in config.json (username, password, etc.)
    * messagebird_secret: no need to change for initial trials.
    * greetings: please DIY.
    * mybosses: a list of your bosses' emails.
    * phonenumbers: a list of phone numbers to be called.
    * interval: the time interval between two checks. Measured in minutes.
    * run_on_windows_startup: if you want the program auto start after each reboot. Only tested on Windows 7.    
3. Run mail_checker.exe


## Voice call service 
I use Messagebird as the voice call service provider and each voice call to UK numbers costs 2 pences. In config.json, I included a messagebird_api_secret worth 15 pounds (approx 750 calls). You need to buy our own credit for regular usages. Please refer to https://www.messagebird.com/en-gb/pricing.

An alternative message api provider is Twilio.

## Remote control
* You could save the this repository into your Dropbox folder. And then edit config.json file through your Dropbox. The program will use your new settings in its next check.
