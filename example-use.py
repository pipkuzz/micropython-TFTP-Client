# 1. Edit 'your_SSID', 'your_password' and 'your_tftp_server_IP'
#    to suit your network. Rename this file boot.py and upload
#    to board toghter with TFTPClient.py and image.svg.
#
# 2. Upload test-512.txt to your network TFTP server thats
#    listening on port 69.
#
# 3. reset() your board.
#
import network
import time
from TFTPClient import TFTPClient


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

# initalise a tftp client to put and get some files...
tftp_client = TFTPClient(TFTP_SERVER_IP)

# The client returns True on successful completion and False otherwise
# We can test for that...

# PUT image.svg to TFTP server
if tftp_client.put_file("image.svg"):
    print("File transfer image.svg succsess.")

else:
    print("File transfer image.svg failed")

# GET test-512.text from TFTP server
if tftp_client.get_file("test-512.txt"):
    print("File transfer test-512.txt succsess.")

else:
    print("File transfer test-512.txt failed")

# test error handling
if tftp_client.put_file("no-file.txt"):
    print("File transfer no-file.txt succsess.")

else:
    print("File transfer no-file.txt failed")

if tftp_client.get_file("no-file.txt"):
    print("File transfer no-file.txt succsess.")

else:
    print("File transfer no-file.txt failed")

# close the socket when we're done.
tftp_client.close()

print("Opperation completed")
