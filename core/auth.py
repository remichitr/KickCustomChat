import hashlib, base64, secrets, urllib.parse, requests, time, json, threading, os
from flask import Flask, request, render_template, Response
from dotenv import load_dotenv

load_dotenv()

class KickAuth:
    def __init__(self):
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.redirect_uri = os.getenv("REDIRECT_URI")
        self.access_token = None
        self.refresh_token = None # YENİ: Yenileme anahtarı
        self.user_data = {}
        self.chat_messages = [] 
        self.processed_ids = set() 
        self.login_callback = None
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.app = Flask(__name__, 
                         template_folder=os.path.join(base_dir, 'web', 'templates'),
                         static_folder=os.path.join(base_dir, 'web', 'static'))
        self.server_thread = None

    def test_token(self):
        """Mevcut access_token'ın hala geçerli olup olmadığını test eder."""
        if not self.access_token: return False
        res = requests.get("https://api.kick.com/public/v1/users", 
                           headers={"Authorization": f"Bearer {self.access_token}"})
        return res.status_code == 200

    def refresh_access_token(self):
        """Refresh Token kullanarak yeni bir Access Token alır."""
        if not self.refresh_token: return False
        
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token
        }
        try:
            res = requests.post("https://id.kick.com/oauth/token", data=data)
            if res.status_code == 200:
                token_data = res.json()
                self.access_token = token_data.get("access_token")
                self.refresh_token = token_data.get("refresh_token") # Yeni refresh token'ı da al
                return True
        except Exception as e:
            print(f"Token yenileme hatası: {e}")
        return False

    def add_to_pool(self, sender, content, is_me=False, msg_id=None):
        my_username = self.user_data.get('username', '').lower()
        sender_lower = sender.lower()
        clean_content = content.strip()

        if msg_id and msg_id in self.processed_ids: return
        fingerprint = f"{clean_content}"
        if not is_me and sender_lower == my_username and fingerprint in self.processed_ids:
            return

        self.chat_messages.append({"sender": sender, "content": clean_content, "is_me": is_me})
        if msg_id: self.processed_ids.add(msg_id)
        if is_me: self.processed_ids.add(fingerprint)
        if len(self.processed_ids) > 100: self.processed_ids.clear()

    def start_server(self, initial_callback=None):
        if self.server_thread: return
        self.login_callback = initial_callback

        @self.app.route('/callback')
        def callback():
            code = request.args.get('code')
            res = requests.post("https://id.kick.com/oauth/token", data={
                "grant_type": "authorization_code", "client_id": self.client_id, 
                "client_secret": self.client_secret, "redirect_uri": self.redirect_uri, 
                "code": code, "code_verifier": self.pkce_verifier})
            
            if res.status_code == 200:
                token_data = res.json()
                self.access_token = token_data.get("access_token")
                self.refresh_token = token_data.get("refresh_token") # YENİ: Callback'ten de kaydet
                
                u_res = requests.get("https://api.kick.com/public/v1/users", headers={"Authorization": f"Bearer {self.access_token}"})
                user_info = u_res.json().get('data', [{}])[0]
                self.user_data = {'id': str(user_info.get('user_id', '')), 'username': user_info.get('name', '')}
                
                if self.login_callback:
                    self.login_callback(self.user_data, self.access_token)
                return render_template('success.html', username=self.user_data.get('username', 'Yayıncı'))
            return render_template('error.html', error_message="Giriş başarısız.")

        @self.app.route('/chat')
        def chat_page(): return render_template('chat.html')

        @self.app.route('/stream')
        def stream():
            def event_stream():
                idx = 0
                while True:
                    if idx < len(self.chat_messages):
                        yield f"data: {json.dumps(self.chat_messages[idx])}\n\n"
                        idx += 1
                    else: time.sleep(0.1)
            return Response(event_stream(), mimetype="text/event-stream")

        threading.Thread(target=lambda: self.app.run(port=5000, debug=False, use_reloader=False), daemon=True).start()
        self.server_thread = True

    def get_auth_url(self):
        self.pkce_verifier = secrets.token_urlsafe(64)
        challenge = base64.urlsafe_b64encode(hashlib.sha256(self.pkce_verifier.encode()).digest()).decode().replace('=', '')
        params = {"response_type": "code", "client_id": self.client_id, "redirect_uri": self.redirect_uri,
                  "scope": "user:read channel:read chat:write", "state": secrets.token_urlsafe(16),
                  "code_challenge": challenge, "code_challenge_method": "S256"}
        return f"https://id.kick.com/oauth/authorize?{urllib.parse.urlencode(params)}"