import os
import webbrowser
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QCursor
from core.theme_manager import ThemeManager # 🌟 Yeni import

class LoadingScreen(QWidget):
    login_success_signal = pyqtSignal()

    def __init__(self, auth_manager, on_success):
        super().__init__()
        self.auth_manager = auth_manager
        self.on_success = on_success
        self.theme = ThemeManager() # 🌟 Tema motoruna bağlan
        self.login_success_signal.connect(self.on_success)
        
        # --- ARKA PLAN (Temadan alınıyor) ---
        self.setStyleSheet(f"background-color: {self.theme.get('window_bg')};")
        
        # --- DOSYA YOLLARINI AYARLA ---
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        remi_logo_path = os.path.join(base_dir, 'web', 'static', 'images', 'logo_remi.png')
        kick_logo_path = os.path.join(base_dir, 'web', 'static', 'images', 'kick.png')

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 🌟 KART TASARIMI (Renkler temadan alınıyor)
        self.card = QFrame()
        self.card.setObjectName("LoginCard")
        self.card.setFixedWidth(320)
        self.card.setStyleSheet(f"""
            #LoginCard {{
                background-color: {self.theme.get('card_bg')};
                border-radius: 15px;
                border-top: 5px solid {self.theme.get('card_border')};
            }}
        """)
        
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(25, 35, 25, 35)
        card_layout.setSpacing(15)
        
        # --- LOGOLAR ---
        logo_layout = QHBoxLayout()
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.setSpacing(20) 

        self.remi_label = QLabel()
        if os.path.exists(remi_logo_path):
            pixmap_remi = QPixmap(remi_logo_path).scaledToHeight(60, Qt.TransformationMode.SmoothTransformation)
            self.remi_label.setPixmap(pixmap_remi)
        else:
            self.remi_label.setText("REMI")
            self.remi_label.setStyleSheet(f"color: {self.theme.get('text_main')}; font-size: 24px; font-weight: bold;")

        self.kick_label = QLabel()
        if os.path.exists(kick_logo_path):
            pixmap_kick = QPixmap(kick_logo_path).scaledToHeight(60, Qt.TransformationMode.SmoothTransformation)
            self.kick_label.setPixmap(pixmap_kick)
        else:
            self.kick_label.setText("KICK")
            self.kick_label.setStyleSheet(f"color: {self.theme.get('accent')}; font-size: 24px; font-weight: bold;")

        logo_layout.addWidget(self.remi_label)
        logo_layout.addWidget(self.kick_label)

        # --- YAZILAR ---
        title = QLabel("Giriş Yap")
        title.setStyleSheet(f"color: {self.theme.get('accent')}; font-size: 24px; font-weight: bold; background: transparent; margin-top: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Sohbete bağlanmak için\nhesabını yetkilendir.")
        subtitle.setStyleSheet(f"color: {self.theme.get('text_secondary')}; font-size: 13px; background: transparent; line-height: 1.5;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 🌟 GİRİŞ BUTONU (Dinamik Alpha Renkler)
        self.login_btn = QPushButton("Kick ile Giriş Yap")
        self.login_btn.setFixedHeight(45)
        self.login_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme.get('btn_bg_alpha')};
                color: {self.theme.get('accent')};
                border: 1px solid {self.theme.get('btn_border_alpha')};
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
                margin-top: 10px;
            }}
            QPushButton:hover {{
                background-color: {self.theme.get('btn_hover_alpha')};
                border: 1px solid {self.theme.get('accent')};
            }}
        """)
        self.login_btn.clicked.connect(self.start_login)
        
        card_layout.addLayout(logo_layout)
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(self.login_btn)
        main_layout.addWidget(self.card)

    def start_login(self):
        self.login_btn.setText("Yönlendiriliyor...")
        self.login_btn.setEnabled(False) 
        self.login_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme.get('btn_disabled')}; 
                color: {self.theme.get('text_disabled')}; 
                border: 1px solid {self.theme.get('input_border')}; 
                border-radius: 8px; 
                font-size: 15px; 
                font-weight: bold; 
                margin-top: 10px;
            }}
        """)
        self.auth_manager.login_callback = lambda u, t: self.login_success_signal.emit()
        webbrowser.open(self.auth_manager.get_auth_url())