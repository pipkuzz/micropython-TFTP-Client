# 1. Edit 'your_SSID', 'your_password' and 'your_tftp_server_IP'
#    to suit your network. Rename this file boot.py and upload
#    to board toghter with TFTPClient.py and test-image.svg.
#
# 2. Upload test-512-byte.txt to your network TFTP server thats
#    listening on port 69.
#
# 3. reset() your board.
#
# 4. If you dont need wifi, comment out the wifi setup section!
#
import network
import time
from TFTPClient import TFTPClient

# ***************************   wifi setup   *****************
WIFI_SSID = "your_SSID"
WIFI_PASSWORD = "your_password"
TFTP_SERVER_IP = "your_tftp_server_IP"

# setup wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

# I found that wlan.isconnected() can report True before the
# DHCP process is complete. Best wait untill the network
# definitely has an IP before moving forward.
netStatus = "Connecting"
while not wlan.status() == network.STAT_GOT_IP:
    print(netStatus, end="\r")
    netStatus += "."
    time.sleep(1)

print()
# **************************   End wifi setup   ***********

# **************************   TFTPClient   ***************

# initalise a tftp client to put and get some files...
tftp_client = TFTPClient(TFTP_SERVER_IP)

# The client returns True on successful completion and False otherwise
# We can test for that...

# PUT test-image.svg to TFTP server in default octet mode
if tftp_client.put_file("test-image.svg"):
    print("PUT 'test-image.svg' ('octet' mode) succsess.")

else:
    print("PUT 'test-image.svg' ('octet' mode) failed")

if tftp_client.put_file("test-image.svg", 'netascii'):
    print("PUT 'test-image.svg' ('netascii' mode) succsess.")

else:
    print("PUT 'test-image.svg' ('netascii' mode) failed")

# GET test-512.text from TFTP server in netascii mode
if tftp_client.get_file("test-512-byte.txt", 'netascii'):
    print("GET 'test-512-byte.txt' ('netascii' mode) succsess.")

else:
    print("GET 'test-512-byte.txt' ('netascii' mode) failed")

# GET test-512.text from TFTP server in octet mode
if tftp_client.get_file("test-512-byte.txt"):
    print("GET 'test-512-byte.txt' ('octet' mode) succsess.")

else:
    print("GET 'test-512-byte.txt' ('octet' mode) failed")

# test error handling with non-existant file
if tftp_client.get_file("no-file-here.txt"):
    print("GET 'no-file-here.txt' ('octet' mode) succsess.")

else:
    print("GET 'no-file-here.txt' ('octet' mode) failed")

print("Demo complete")
