import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QCursor
from core.theme_manager import ThemeManager

class JoinScreen(QWidget):
    def __init__(self, on_join, on_settings):
        super().__init__()
        self.on_join = on_join
        self.on_settings = on_settings
        self.theme = ThemeManager() 
        
        # --- DOSYA YOLLARINI AYARLA ---
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        remi_logo_path = os.path.join(base_dir, 'web', 'static', 'images', 'logo_remi.png')

        # --- ANA YERLEŞİM ---
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 🌟 KART TASARIMI
        self.card = QFrame()
        self.card.setObjectName("JoinCard")
        self.card.setFixedWidth(320)
        
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(25, 30, 25, 30)
        card_layout.setSpacing(15)

        # --- KÜÇÜK LOGO VE BAŞLIK ---
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        if os.path.exists(remi_logo_path):
            self.logo_label = QLabel()
            pixmap = QPixmap(remi_logo_path).scaledToHeight(40, Qt.TransformationMode.SmoothTransformation)
            self.logo_label.setPixmap(pixmap)
            self.logo_label.setStyleSheet("background: transparent; border: none;")
            header_layout.addWidget(self.logo_label)

        self.title_label = QLabel("Kanal Seçimi")
        header_layout.addWidget(self.title_label)
        
        # --- INPUT (GİRİŞ KUTUSU) ---
        self.input_label = QLabel("Katılmak istediğiniz kanalın adı:")
        
        self.channel_input = QLineEdit()
        self.channel_input.setPlaceholderText("Örn: NEEXcsgo")
        self.channel_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.channel_input.returnPressed.connect(self.handle_join)
        
        # --- KATIL BUTONU ---
        self.join_btn = QPushButton("Sohbete Katıl")
        self.join_btn.setFixedHeight(45)
        self.join_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.join_btn.clicked.connect(self.handle_join)

        # --- AYARLAR BUTONU ---
        self.settings_btn = QPushButton("⚙️ Ayarlar")
        self.settings_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.settings_btn.clicked.connect(self.on_settings)
        
        card_layout.addLayout(header_layout)
        card_layout.addWidget(self.input_label)
        card_layout.addWidget(self.channel_input)
        card_layout.addWidget(self.join_btn)
        card_layout.addWidget(self.settings_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(self.card)

        # 🌟 İLK STİL YÜKLEMESİNİ YAP
        self.update_ui_style()

    def showEvent(self, event):
        """Bu ekran her görünür olduğunda (örn: sohbetten veya ayarlardan dönüldüğünde) çalışır."""
        super().showEvent(event)
        self.reset_ui() # Ekranı taze ve kullanılabilir hale getir

    def reset_ui(self):
        """Buton kilidini ve yazısını sıfırlar."""
        self.join_btn.setText("Sohbete Katıl")
        self.join_btn.setEnabled(True)

    def update_ui_style(self):
        """Tema değiştiğinde veya ekran ilk açıldığında renkleri günceller."""
        self.setStyleSheet(f"background-color: {self.theme.get('window_bg')};")

        self.card.setStyleSheet(f"""
            #JoinCard {{
                background-color: {self.theme.get('card_bg')};
                border-radius: 15px;
                border-top: 5px solid {self.theme.get('card_border')};
            }}
        """)

        self.title_label.setStyleSheet(f"color: {self.theme.get('text_main')}; font-size: 20px; font-weight: bold; background: transparent; border: none;")
        self.input_label.setStyleSheet(f"color: {self.theme.get('text_secondary')}; font-size: 13px; background: transparent; border: none; margin-top: 10px;")

        self.channel_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.theme.get('input_bg')};
                color: {self.theme.get('accent')};
                border: 1px solid {self.theme.get('input_border')};
                border-radius: 8px;
                padding: 12px;
                font-size: 15px;
                font-weight: bold;
            }}
            QLineEdit:focus {{
                border: 1px solid {self.theme.get('accent')};
            }}
        """)

        self.join_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme.get('accent')};
                color: black;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
                margin-top: 5px;
            }}
            QPushButton:hover {{
                background-color: {self.theme.get('accent_hover')};
            }}
        """)

        self.settings_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {self.theme.get('text_secondary')};
                border: none;
                font-size: 13px;
                margin-top: 10px;
            }}
            QPushButton:hover {{
                color: {self.theme.get('text_main')};
            }}
        """)

    def handle_join(self):
        channel = self.channel_input.text().strip()
        if channel:
            self.join_btn.setText("Bağlanıyor...")
            self.join_btn.setEnabled(False)
            self.on_join(channel)