# WiFiSafe
Small utility software conceived to share WiFi connections between computers.
As the software is intended to be used on a USB drive, the WiFi profiles (the files that store the connection information) are encrypted to avoid revealing sensitive information in case the device is lost.

# Usage
Place this program on a USB device. 
Run it and choose Export profiles (or Synchronise profiles). Exit program and Remove USB device.
Plug the USB device into another computer, run it and choose Import profiles (or Synchronise profiles). 
You have successfully shared the password-protected WiFi connections from the first computer into the second one.

Warning: might override previous WiFi profiles if used improperly. 

Warning: the software will create two folders: "profiles" and "temp", do not remove those folders during use. The encrypted data will be stored within the profiles folder.

# Requirements
This program works on Windows (tested on Windows 10) and the language of the OS must be either French or English.
