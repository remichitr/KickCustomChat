from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox
from PyQt6.QtCore import Qt
from core.theme_manager import ThemeManager

class KickSettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.theme = ThemeManager()
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.title_label = QLabel("Kick Sohbet Ayarları")
        
        self.cb_timestamps = QCheckBox("Mesaj Saatlerini Göster")
        self.cb_badges = QCheckBox("Kullanıcı Rozetlerini Göster (Mod, VIP)")
        self.cb_colors = QCheckBox("İsim Renklerini Göster")
        
        self.cb_badges.setChecked(True)
        self.cb_colors.setChecked(True)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.cb_timestamps)
        layout.addWidget(self.cb_badges)
        layout.addWidget(self.cb_colors)
        layout.addStretch()

        # 🌟 İlk renkleri yükle
        self.update_ui_style()

    def update_ui_style(self):
        """Tema değiştiğinde Kick sekmesinin renklerini yeniler"""
        # Arka planı yenile
        self.setStyleSheet(f"background-color: {self.theme.get('card_bg')};")
        
        self.title_label.setStyleSheet(f"color: {self.theme.get('text_main')}; font-size: 18px; font-weight: bold; margin-bottom: 10px; background: transparent; border: none;")
        
        checkbox_style = f"""
            QCheckBox {{ color: {self.theme.get('text_secondary')}; font-size: 14px; padding: 5px; background: transparent; border: none; }}
            QCheckBox::indicator {{ width: 18px; height: 18px; border: 1px solid {self.theme.get('input_border')}; border-radius: 3px; background-color: {self.theme.get('input_bg')}; }}
            QCheckBox::indicator:checked {{ background-color: {self.theme.get('accent')}; border: 1px solid {self.theme.get('accent')}; }}
        """
        
        self.cb_timestamps.setStyleSheet(checkbox_style)
        self.cb_badges.setStyleSheet(checkbox_style)
        self.cb_colors.setStyleSheet(checkbox_style)