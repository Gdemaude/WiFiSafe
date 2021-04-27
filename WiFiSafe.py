# -*- coding: utf-8 -*-
import subprocess
import os
import sys
import glob
import re
from PyInquirer import prompt
from time import sleep
import hashlib, binascii
from Crypto.Protocol.KDF import scrypt
import json
from base64 import b64encode
from Crypto.Cipher import AES
from wifi import Wifi
from encrypt import Encrypt

if __name__ == '__main__':
    print("Welcome to WiFiSafe!")
    print("This utility program is intended to be used on a portable USB device and allows you to store and share your WiFi connections.")
    print("The data is stored within the profiles folder, do not delete it. \n")

    psw=""
    E=Encrypt()
    W=Wifi()

    #Step one: Check if there is an existing password, if not: set one and store hash
    if not os.path.exists(E.passwordf):
        print("No password set. Create a new password.")
        print("This password will be used to encrypt the data. Make it strong enough.")

        questions = [
            {
                'type': 'password',
                'message': 'Enter a new password:',
                'name': 'password'
            }
        ]

        while(len(psw)<6):
            print("The password must have a length of 6 characters or more")
            answers = prompt(questions)
            psw = answers['password']

        hashd=E.create_password(psw)
        print("Password set \n")

    #Step 2: Verify password if it was previously set
    while len(psw)<6:
        questions = [
            {
                'type': 'list',
                'name': 'theme',
                'message': 'Enter the password or reset it.',
                'choices': [
                    'Enter password',
                    'Reset password',
                    'Help',
                    'Exit',
                ]
            }]
        answers = prompt(questions)
        ans = answers['theme']
        if ans == "Enter password":
            question = [
                {
                    'type': 'password',
                    'message': 'Enter your password or BACK (to go back):',
                    'name': 'password'
                }
            ]
            while True:
                epsw=prompt(question)['password']
                if epsw.upper()=="BACK":
                    break
                else:
                    checked= E.verify_password(epsw)
                    if checked:
                        psw=epsw
                        print("Password valid")
                        break
        elif ans == "Reset password":
            print("Stored WiFi profiles will be deleted when new password is set.")
            question = [
                {
                    'type': 'password',
                    'message': 'Enter your password or BACK (to go back):',
                    'name': 'password'
                }
            ]
            while (len(psw) < 6):
                print("The password must have a length equal of 6 characters or more")
                answers = prompt(question)
                epsw = answers['password']
                if epsw.upper() == "BACK":
                    break
                elif len(epsw) >= 6:
                    psw = epsw
                    W.remove_clear_profiles()
                    E.remove_crypted_profiles()
                    print("Old connections deleted")
                    hashd = E.create_password(psw)
                    print("New password set \n")


        elif ans == "Help":
            print("Select Enter Password to type in your password. It will be checked against the sotred password used to encrypt WiFi data.")
            print("Select Reset Password to type a new password. Warning: previous WiFi data will be deleted!")
            print("Info: tempering with stored password will result in bad behaviours but won't get you access to WiFi data.")
            print("Select Exit to quit this program \n")

            input("Press Enter to continue \n")

        elif ans == "Exit":
            print("Exiting... \n ")
            sleep(1)
            exit()




    questions = [
        {
            'type': 'list',
            'name': 'theme',
            'message': 'Select function:',
            'choices': [
                'Export WiFi profiles',
                'Import WiFi profiles',
                'Synchronise profiles',
                'Help',
                'Exit',
            ]
        }]
    while 1:
        answers = prompt(questions)
        ans=answers['theme']
        if ans=="Export WiFi profiles":
            print("Exporting profiles...")
            W.export_profiles()
            W.remove_irrelevant_profiles()
            E.encrypt_profiles(W.folder)
            W.remove_clear_profiles()
            print("Profiles exported successfully \n")
        elif ans == "Import WiFi profiles":
            print("Importing profiles...")
            E.decrypt_profiles(W.folder)
            W.create_profiles()
            W.remove_clear_profiles()
            print("Profiles Imported successfully \n")
        elif ans == "Synchronise profiles":
            print("Synchronising...")
            E.decrypt_profiles(W.folder)
            W.export_profiles()
            W.remove_irrelevant_profiles()
            W.create_profiles()
            E.encrypt_profiles(W.folder)
            W.remove_clear_profiles()
            print("Synchronisation completed")
        elif ans== "Help":
            print("Option Export WiFi profiles will export all relevant WiFi connections(aka profiles) to this program for later use on other computers")
            print("Option Import WiFi profiles will import all relevant WiFi connections(aka profiles) stored by this program to the computer")
            print("Synchronises profiles will do both the Export and Import options")
            print("Select Exit to quit this program \n")
            input("Press Enter to continue \n")
        elif ans=="Exit":
            print("Exiting... \n ")
            sleep(1)
            break
        else:
            print("Problem encountered... Exiting... \n")




