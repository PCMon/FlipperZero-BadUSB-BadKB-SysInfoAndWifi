## **PLEASE ONLY USE THIS ON YOUR OWN COMPUTER OR ON SOMEONE WHO CONSENTS**

### How to run:

Download raw of FlipperZero Payload.txt

Under **CUSTOMIZATION** place your discord webhook url into the line that says "PUT WEBHOOK HERE".

**DO NOT** remove any quotation marks.

Move to FlipperZero and run :D

(You may also customize what the program does by setting the variables after $webhook to "true" or "false", capitalization doesn't matter)

Default = true,true,true

--------------------------------------------------------

[Full .exe code also included.](https://github.com/PCMon/FlipperZero-BadUSB-BadKB-SysInfoAndWifi/blob/main/TempDriverUtil.py)

If the program fails in some way to collect any information as seen in the webhook embeds please comment the issue and i'll look into it.
(GPU data currently only works for NVIDIA gpus)

PAYLOAD TIME: 15.812s

What will be sent:

![alt text](https://github.com/PCMon/FlipperZero-BadUSB-BadKB-SysInfoAndWifi/blob/main/image.png?raw=true)

If errors occour in the powershell terminal, it may be due to a slow computer messing up the timing of the DELAY functions in the payload. Remember, you can always enter these powershell lines manually or change the DELAY timings.

You cannot run the .exe standalone as it requires variables present in a .txt (just a quirk of using powershell variables) but you *COULD TECHNICALLY* create the .txt file it needs including the webhook and variable data in the C:\Program Files (86x)\Temp folder.
