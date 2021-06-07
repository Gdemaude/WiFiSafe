import subprocess
import glob
import re
import os

class Wifi:
    def __init__(self, folder=".\\temp"):
        self.folder=folder
        if not os.path.exists(folder):
            os.mkdir(folder)

    def create_profiles(self):
        try:
            data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8',errors="backslashreplace").split('\n')
            profiles = [i.split(":")[1][1:-1] for i in data if "Profil Tous les utilisateurs" in i or "All User Profile" in i]
        except subprocess.CalledProcessError as inst:
            print("No existing profiles stored within the computer")
            profiles=[]
        for f in glob.glob(self.folder+"\\*.xml"):
            try:
                file = open(f)
                txt = file.read()
                res = re.findall("<name>(.*?)</name>", txt)
                if res[0] in profiles:
                    continue
                filename = "filename=" + f
                result = subprocess.check_output(['netsh', 'wlan', 'add', 'profile', filename])
            except Exception as inst:
                print(inst)


    def export_profiles(self):
        folder = 'folder=' + self.folder
        #profiles = [i.split(":")[1][1:-1] for i in data if "Profil Tous les utilisateurs" in i or "All User Profile" in i]
        try:
            subprocess.check_output(['netsh', 'wlan', 'export', 'profile', folder, 'key=clear'])  # netsh bug if there is a # in the name of the profile, need adminstrative right
        except Exception as e:
            print("Error when exporting WiFi profiles")
            print(e)

    def remove_irrelevant_profiles(self):
        for f in glob.glob(self.folder+"\\*.xml"):
            file = open(f)
            txt = file.read()
            file.close()
            if "passPhrase" not in txt:
                os.remove(f)

    def remove_clear_profiles(self):
        for f in glob.glob(self.folder + "\\*.xml"):
            os.remove(f)