from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTabWidget
from PyQt6.QtCore import Qt
from gui.settings.settings_general import GeneralSettingsTab
from gui.settings.settings_kick import KickSettingsTab
from core.theme_manager import ThemeManager

class SettingsScreen(QWidget):
    def __init__(self, auth_manager, on_back, on_logout):
        super().__init__()
        self.auth_manager = auth_manager
        self.theme = ThemeManager()
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # --- ÜST BAR ---
        header_layout = QHBoxLayout()
        self.back_btn = QPushButton("←")
        self.back_btn.setFixedSize(35, 35)
        self.back_btn.clicked.connect(on_back)
        
        self.title_label = QLabel("Ayarlar")
        
        header_layout.addWidget(self.back_btn)
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        
        # --- SEKMELER (TABS) ---
        self.tabs = QTabWidget()
        self.tab_general = GeneralSettingsTab(self.auth_manager, on_logout)
        self.tab_kick = KickSettingsTab()
        
        self.tabs.addTab(self.tab_general, "Genel")
        self.tabs.addTab(self.tab_kick, "Kick")
        
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.tabs)

        # 🌟 İlk renkleri yükle
        self.update_ui_style()

    def update_ui_style(self):
        """Tema değiştiğinde ana ayarlar sayfasının renklerini yeniler"""
        # Arka planı yenile
        self.setStyleSheet(f"background-color: {self.theme.get('window_bg')};")

        # Üst barı yenile
        self.back_btn.setStyleSheet(f"""
            QPushButton {{ 
                background-color: {self.theme.get('card_bg')}; 
                color: {self.theme.get('text_main')}; 
                border-radius: 5px; 
                font-weight: bold; 
                font-size: 18px; 
                border: 1px solid {self.theme.get('input_border')};
            }}
            QPushButton:hover {{ background-color: {self.theme.get('input_border')}; }}
        """)
        self.title_label.setStyleSheet(f"color: {self.theme.get('text_main')}; font-size: 20px; font-weight: bold; margin-left: 10px; border: none; background: transparent;")

        # Sekmeleri yenile
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{ border: 1px solid {self.theme.get('input_border')}; border-radius: 5px; background: transparent; }}
            QTabBar::tab {{ 
                background: {self.theme.get('window_bg')}; 
                color: {self.theme.get('text_secondary')}; 
                padding: 10px 25px; 
                border-top-left-radius: 5px; 
                border-top-right-radius: 5px; 
                margin-right: 2px; 
                font-weight: bold; 
            }}
            QTabBar::tab:selected {{ 
                background: {self.theme.get('card_bg')}; 
                color: {self.theme.get('accent')}; 
                border-bottom: 2px solid {self.theme.get('accent')}; 
            }}
            QTabBar::tab:hover {{ color: {self.theme.get('text_main')}; }}
        """)

        # İçindeki sekmelere de yenilenme emri gönder
        if hasattr(self.tab_general, 'update_ui_style'):
            self.tab_general.update_ui_style()
        if hasattr(self.tab_kick, 'update_ui_style'):
            self.tab_kick.update_ui_style()

    def update_info(self):
        self.tab_general.update_username()