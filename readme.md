Greetings 
---------------------

![Alt text](<2024-01-31 12_55_40-DSC2 @ github.com_Elmerikh.png>)

DSC2 is a trojan that uses Discord as a c2 server 

![Alt text](<2024-01-30 05_16_51-#private-channel _ LMERIKH - Discord.png>)


![Alt text](<2024-01-30 05_16_08-#private-channel _ LMERIKH - Discord.png>)


Warning
------------------

this may ban or desactivate your Discord account you have been warned
---------------------------------

How it works ?
-------------------

the bot act as client for our discord server, when ever the programme runs in a machine the bot creates a new private channel with a webhook in the server and check for the id of the channel if it matches the current channel you are sending message to

this allows to have a session for each different client 

if programme is shutdown connexion is lost and you need to delete channel 

it needs 3 things :

-Discord bot token (create a discord bot)

-UserID token (this is to avoid bad usage)

-Guild token (your discord server id)

Setup
---------------------------------

pip install -r requirements

python DSC2.py


Features :
-----------------------

any cmd commande

!steal : steal cookies,webHistory,passwords,card bank account,downloads and then send them back via channel webhook

!screenshot : screenshot and send to server

!net : get wifi passwords and network info

!info : get system information like pc brand ,GPU ,CPU...

!startup (not added for good purpose)


DISCLAIMER :

ME The author takes NO responsibility and/or liability for how you choose to use any of the tools/source code/any files provided. ME The author and anyone affiliated with will not be liable for any losses and/or damages in connection with use of Beryl. By using Beryl or any files included, you understand that you are AGREEING TO USE AT YOUR OWN RISK. Once again Beryl is for EDUCATION and/or RESEARCH purposes ONLY.
