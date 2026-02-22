import os, threading, json, websocket
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QShortcut, QKeySequence
from core.kick_api import KickAPI
from core.theme_manager import ThemeManager

class OverlayWindow(QWidget):
    """Sadece Görünmez Mod için yaratılmış, doğuştan şeffaf özel pencere"""
    def __init__(self):
        super().__init__()
        # 🌟 Arka planı siyah yapmayan, görev çubuğunda görünmeyen, tam şeffaf mod!
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setStyleSheet("background: transparent;")
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # 🌟 Bu pencereye özel yepyeni bir WebView açıyoruz
        self.web_view = QWebEngineView()
        self.web_view.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.web_view.page().setBackgroundColor(Qt.GlobalColor.transparent)
        self.web_view.setStyleSheet("background: transparent; border: none;")
        
        self.layout.addWidget(self.web_view)

class ChatScreen(QWidget):
    def __init__(self, channel_name, auth_manager, on_back):
        super().__init__()
        self.channel_name = channel_name
        self.auth_manager = auth_manager
        self.on_back = on_back 
        self.theme = ThemeManager()
        self.api = KickAPI(auth_manager.access_token)
        self.is_active = True 
        self.is_invisible = False
        self.overlay_win = None 
        
        self.my_user_id = str(self.auth_manager.user_data.get('id', ''))

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # --- ÜST BAR (HEADER) ---
        self.header_widget = QWidget()
        header_layout = QHBoxLayout(self.header_widget)
        header_layout.setContentsMargins(10, 5, 10, 5)

        self.back_btn = QPushButton("←")
        self.back_btn.setFixedSize(35, 35)
        self.back_btn.clicked.connect(self.leave_chat)

        self.header_label = QLabel(f"🔴 @{channel_name} bağlanıyor...")
        
        header_layout.addWidget(self.back_btn)
        header_layout.addWidget(self.header_label)
        header_layout.addStretch()

        # --- WEBVIEW (ANA PENCERE İÇİN) ---
        self.web_view = QWebEngineView()
        self.web_view.page().setBackgroundColor(Qt.GlobalColor.transparent)
        self.web_view.setUrl(QUrl("http://localhost:5000/chat"))
        
        # --- MESAJ GİRİŞ ALANI ---
        self.input_container = QWidget()
        input_bar = QHBoxLayout(self.input_container)
        input_bar.setContentsMargins(10, 10, 10, 10)
        
        self.msg_input = QLineEdit()
        self.msg_input.setPlaceholderText("Mesaj gönder...")
        self.msg_input.returnPressed.connect(self.send_msg)
        
        self.btn_send = QPushButton("Gön")
        self.btn_send.setFixedWidth(60)
        self.btn_send.setFixedHeight(38)
        self.btn_send.clicked.connect(self.send_msg)
        
        input_bar.addWidget(self.msg_input)
        input_bar.addWidget(self.btn_send)
        
        # Elemanları ana layout'a ekle
        self.main_layout.addWidget(self.header_widget)
        self.main_layout.addWidget(self.web_view)
        self.main_layout.addWidget(self.input_container)
        
        # 🌟 AYARLARDAN KISAYOLU OKU VE BAĞLA
        self.shortcut_key = self.theme.get_config("shortcut", "Ctrl+I")
        self.shortcut = QShortcut(QKeySequence(self.shortcut_key), self)
        self.shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut.activated.connect(self.toggle_invisibility)

        self.update_ui_style()
        threading.Thread(target=self.init_kick, daemon=True).start()

    def toggle_invisibility(self):
        """Kusursuz Şeffaflık Geçişi - Taşıma yapmadan yeni pencere açar."""
        self.is_invisible = not self.is_invisible
        main_win = self.window()

        if self.is_invisible:
            # 1. Ana penceredeki sohbeti durdur (Veriler çakışmasın)
            self.web_view.setUrl(QUrl("about:blank"))

            # 2. Yepyeni, doğuştan şeffaf pencereyi yarat
            self.overlay_win = OverlayWindow()
            
            # 3. Kısayolu overlay penceresine de bağla ki geri dönebilelim!
            self.overlay_shortcut = QShortcut(QKeySequence(self.shortcut_key), self.overlay_win)
            self.overlay_shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)
            self.overlay_shortcut.activated.connect(self.toggle_invisibility)

            # 4. Sayfa yüklendiğinde HTML arkaplanını zorla şeffaf yap
            js_code = """
                document.body.style.setProperty('background', 'transparent', 'important');
                document.documentElement.style.setProperty('background', 'transparent', 'important');
            """
            self.overlay_win.web_view.loadFinished.connect(lambda: self.overlay_win.web_view.page().runJavaScript(js_code))

            # 5. Sohbet kutusuna tıklanmayı kapat (Dokunulmazlık)
            self.overlay_win.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
            
            # 6. Boyutlandır, Sohbeti Başlat ve Göster
            self.overlay_win.setGeometry(main_win.geometry())
            self.overlay_win.web_view.setUrl(QUrl("http://localhost:5000/chat"))
            
            main_win.hide()
            self.overlay_win.show()
            
        else:
            # 1. Şeffaf penceredeki sohbeti kapat ve pencereyi yok et
            self.overlay_win.web_view.setUrl(QUrl("about:blank"))
            main_win.setGeometry(self.overlay_win.geometry())
            self.overlay_win.close()
            self.overlay_win = None

            # 2. Ana penceredeki sohbeti tekrar uyandır
            self.web_view.setUrl(QUrl("http://localhost:5000/chat"))
            
            main_win.show()

    def update_ui_style(self):
        if self.is_invisible:
            return 

        self.setStyleSheet(f"background-color: {self.theme.get('window_bg')};")
        self.header_widget.setStyleSheet(f"background-color: {self.theme.get('card_bg')}; border-bottom: 1px solid {self.theme.get('input_border')};")
        
        self.back_btn.setStyleSheet(f"""
            QPushButton {{ background-color: {self.theme.get('input_bg')}; color: {self.theme.get('text_main')}; border-radius: 5px; font-size: 18px; font-weight: bold; border: 1px solid {self.theme.get('input_border')};}}
            QPushButton:hover {{ background-color: {self.theme.get('danger_hover')}; color: white; }}
        """)

        if "🟢" in self.header_label.text():
            self.header_label.setStyleSheet(f"color: {self.theme.get('accent')}; font-weight: bold; font-size: 14px; margin-left: 10px; border: none;")
        else:
            self.header_label.setStyleSheet(f"color: {self.theme.get('text_main')}; font-weight: bold; font-size: 14px; margin-left: 10px; border: none;")

        self.input_container.setStyleSheet(f"background-color: {self.theme.get('card_bg')}; border-top: 1px solid {self.theme.get('input_border')};")
        
        self.msg_input.setStyleSheet(f"""
            QLineEdit {{ background-color: {self.theme.get('input_bg')}; color: {self.theme.get('text_main')}; border: 1px solid {self.theme.get('input_border')}; border-radius: 8px; padding: 10px; font-size: 14px;}}
            QLineEdit:focus {{ border: 1px solid {self.theme.get('accent')}; }}
        """)
        
        self.btn_send.setStyleSheet(f"""
            QPushButton {{ background-color: {self.theme.get('accent')}; color: black; border-radius: 8px; font-weight: bold; border: none;}}
            QPushButton:hover {{ background-color: {self.theme.get('accent_hover')}; }}
        """)

    def init_kick(self):
        info = self.api.get_channel_info(self.channel_name)
        if info and self.is_active:
            self.chatroom_id, self.b_id = info['chatroom_id'], info['broadcaster_user_id']
            self.header_label.setText(f"🟢 @{self.channel_name}")
            self.header_label.setStyleSheet(f"color: {self.theme.get('accent')}; font-weight: bold; font-size: 14px; margin-left: 10px; border: none;")
            threading.Thread(target=self.run_pusher, daemon=True).start()

    def run_pusher(self):
        def on_msg(ws, message):
            if not self.is_active: return
            try:
                d = json.loads(message)
                if "ChatMessageEvent" in str(d.get("event", "")):
                    r = json.loads(d.get("data", "{}"))
                    sender_id = str(r['sender']['id'])
                    if sender_id != self.my_user_id:
                        self.auth_manager.add_to_pool(r['sender']['username'], r['content'], is_me=False)
            except: pass

        ws_url = "wss://ws-us2.pusher.com/app/32cbd69e4b950bf97679?protocol=7&client=js&version=7.6.0&flash=false"
        self.ws = websocket.WebSocketApp(ws_url, on_message=on_msg)
        self.ws.on_open = lambda ws: ws.send(json.dumps({"event":"pusher:subscribe","data":{"channel":f"chatrooms.{self.chatroom_id}.v2"}}))
        self.ws.run_forever()

    def send_msg(self):
        txt = self.msg_input.text().strip()
        if txt and hasattr(self, 'b_id'):
            self.msg_input.clear()
            self.auth_manager.add_to_pool("Sen", txt, is_me=True)
            threading.Thread(target=self.api.send_message, args=(self.b_id, self.chatroom_id, txt), daemon=True).start()

    def leave_chat(self):
        self.is_active = False
        if hasattr(self, 'ws'):
            self.ws.close()
        
        # Bug önleyici: Çıkarken overlay açıksa kapat
        if self.is_invisible and self.overlay_win:
            self.overlay_win.close()
            self.overlay_win = None
            self.is_invisible = False

        self.auth_manager.chat_messages = []
        self.auth_manager.processed_ids.clear()
        self.on_back()