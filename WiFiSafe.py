# -*- coding: utf-8 -*-
import subprocess
import os
import sys
import glob
import re
from PyInquirer import prompt
from time import sleep

def createprofiles():
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8',errors="backslashreplace").split('\n')
    profiles = [i.split(":")[1][1:-1] for i in data if "Profil Tous les utilisateurs" in i or "All User Profile" in i ]
    for f in glob.glob(".\\profiles\\*.xml"):
        file=open(f)
        txt=file.read()
        res=re.findall("<name>(.*?)</name>", txt)
        if res[0] in profiles:
            continue

        filename="filename="+f
        if "passPhrase" in txt:
            result=subprocess.check_output(['netsh', 'wlan', 'add', 'profile', filename])

def exportprofiles():
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
    folder='folder='+os.getcwd()+"\\profiles"
    print(os.getcwd())
    profiles = [i.split(":")[1][1:-1] for i in data if "Profil Tous les utilisateurs" in i or "All User Profile" in i]
    for i in profiles:
        try:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode(sys.stdout.encoding,errors="backslashreplace").split('\n')
            results = [b.split(":")[1][1:-1] for b in results if "Authentification" in b]
            if "WPA2\\xff-\\xffPersonnel" in results:
                results = subprocess.check_output(['netsh', 'wlan', 'export', 'profile', i, folder])
                print(results)
        except:
            print("Error when exporting WiFi profile")


if __name__ == '__main__':
    if not os.path.exists("profiles"):
        os.mkdir("profiles")
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
    print("Welcome to WiFiSafe!")
    print("This utility program is intended to be used on a portable USB device and allows you to store and share your WiFi connections.")
    print("The data is stored within the profiles folder, do not delete it.")
    while 1:
        answers = prompt(questions)
        ans=answers['theme']
        if ans=="Export WiFi profiles":
            exportprofiles()
            print("Profiles exported successfully \n")
        elif ans == "Import WiFi profiles":
            createprofiles()
            print("Profiles Imported successfully \n")
        elif ans == "Synchronise profiles":
            exportprofiles()
            createprofiles()
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




