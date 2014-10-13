import gdata.spreadsheets.client
import gdata.gauth
import ConfigParser
import os

Config = ConfigParser.ConfigParser()
cfg_file = open("credentials.ini","w")

print """
------------------------------------------------------------------------------------------------
Welcome! Let's configure connection details to the spreadsheet API.

0. First visit https://console.developers.google.com and create a new project.

1. Under "APIs & auth", pick "Credentials" and then choose "Create Client ID"

2. A dialog will pop up, choose, "Installed application" and then "Other", click "Create Client ID"

[press enter to continue]"""
a = raw_input()
os.system("clear")

print "Look at the right side of the screen, and type in these parameters: "
client_id = raw_input("What's the Client Id?\n\n (should be something along the lines of 12345678901-a3b0cdef88ghijkl92u4e6pkrl4546nk.apps.googleusercontent.com)").strip()
os.system("clear")
client_secret = raw_input("What's the client secret?").strip()
token = gdata.gauth.OAuth2Token(client_id=client_id,
                                client_secret=client_secret,
                                scope='https://spreadsheets.google.com/feeds/',
                                user_agent='Gdata test export')
os.system("clear")
print "Now open your browser at:\n\n ", token.generate_authorize_url(), "\n\n and follow instructions." 
code = raw_input("What's the code?").strip()
token.get_access_token(code)

os.system("clear")
spreadsheet = raw_input("what is the key of the spreadsheet you would like to write to?")
worksheet = raw_input("what is the worksheet you would like to write to? [od6]") or "od6"

Config.add_section("gdata")
Config.set("gdata", "client_id", client_id)
Config.set("gdata", "client_secret", client_secret)
Config.set("gdata", "access_token", token.access_token)
Config.set("gdata", "refresh_token", token.refresh_token)
Config.set("gdata", "worksheet", worksheet)
Config.set("gdata", "spreadsheet", spreadsheet)
Config.write(cfg_file)

os.system("clear")
cfg_file.close()

print "Created credentials.ini successfully."

