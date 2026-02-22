from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtCore import Qt
from gui.app_loading import LoadingScreen
from gui.app_join import JoinScreen
from gui.app_chat import ChatScreen
from gui.app_settings import SettingsScreen
from core.session_mgr import SessionManager
from core.theme_manager import ThemeManager

class AppWindow(QMainWindow):
    def __init__(self, auth_manager):
        super().__init__()
        self.auth_manager = auth_manager
        self.session_mgr = SessionManager()
        self.theme = ThemeManager()
        
        self.setWindowTitle("RemiKickChat")
        self.resize(360, 600)
        self.refresh_styles() # İlk açılış stili
        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.loading = LoadingScreen(self.auth_manager, self.on_login_complete)
        self.join = JoinScreen(self.start_chat, on_settings=self.open_settings)
        self.settings = SettingsScreen(
            self.auth_manager, 
            on_back=lambda: self.stack.setCurrentIndex(1), 
            on_logout=self.logout
        )
        
        self.stack.addWidget(self.loading)  
        self.stack.addWidget(self.join)     
        self.stack.addWidget(self.settings) 

        if self.auth_manager.access_token:
            self.stack.setCurrentIndex(1)
        else:
            self.stack.setCurrentIndex(0)

    def refresh_styles(self):
        """Tüm uygulamanın stilini anlık olarak yeniler."""
        self.setStyleSheet(f"background-color: {self.theme.get('window_bg')};")
        # Eğer ekranlar oluşturulmuşsa onlara da bildir
        if hasattr(self, 'stack'):
            for i in range(self.stack.count()):
                widget = self.stack.widget(i)
                # Widget'ların kendi stillerini güncelleme fonksiyonu varsa çağır
                if hasattr(widget, 'update_ui_style'):
                    widget.update_ui_style()
                else:
                    widget.setStyleSheet(f"background-color: {self.theme.get('window_bg')};")

    def on_login_complete(self, user_data=None, token=None):
        self.session_mgr.save_session(self.auth_manager.user_data, self.auth_manager.access_token, getattr(self.auth_manager, 'refresh_token', None))
        self.stack.setCurrentIndex(1)

    def start_chat(self, channel_name):
        self.chat = ChatScreen(channel_name, self.auth_manager, on_back=lambda: self.stack.setCurrentIndex(1))
        if self.stack.count() > 3: 
            old_chat = self.stack.widget(3)
            self.stack.removeWidget(old_chat)
            old_chat.deleteLater()
        self.stack.addWidget(self.chat)
        self.stack.setCurrentWidget(self.chat)

    def open_settings(self):
        self.settings.update_info() 
        self.stack.setCurrentIndex(2)

    def logout(self):
        self.session_mgr.clear_session()
        self.auth_manager.access_token = None
        self.auth_manager.user_data = {}
        self.stack.setCurrentIndex(0)