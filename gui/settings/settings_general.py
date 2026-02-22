import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent, QKeySequence
from core.theme_manager import ThemeManager

class ShortcutInput(QLineEdit):
    """Klavyeden basılan tuş kombinasyonlarını algılayan, boyanan ve KAYDEDEN kutu"""
    def __init__(self, default_text="Ctrl+I"):
        super().__init__()
        self.theme = ThemeManager()
        
        # 🌟 Başlangıçta config.json'dan kayıtlı kısayolu oku
        saved_shortcut = self.theme.get_config("shortcut", default_text)
        self.setText(saved_shortcut)
        self.update_ui_style()
        
        # 🌟 Metin değiştiği an kaydetmeye başla
        self.textChanged.connect(self.save_shortcut)

    def save_shortcut(self, text):
        if text: # Kutu boş değilse kaydet
            self.theme.update_config("shortcut", text)
            print(f"✅ Yeni Kısayol Kaydedildi: {text}")

    def update_ui_style(self):
        self.setStyleSheet(f"""
            QLineEdit {{ 
                background-color: {self.theme.get('input_bg')}; 
                color: {self.theme.get('text_main')}; 
                padding: 10px; 
                border: 1px solid {self.theme.get('input_border')}; 
                border-radius: 5px; 
                font-size: 14px; 
            }}
            QLineEdit:focus {{ border: 1px solid {self.theme.get('accent')}; }}
        """)

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        if key in (Qt.Key.Key_Control, Qt.Key.Key_Shift, Qt.Key.Key_Alt, Qt.Key.Key_Meta): return
        if key in (Qt.Key.Key_Backspace, Qt.Key.Key_Escape):
            self.setText("")
            return
        combination = event.keyCombination()
        self.setText(QKeySequence(combination).toString(QKeySequence.SequenceFormat.NativeText))

class GeneralSettingsTab(QWidget):
    def __init__(self, auth_manager, on_logout):
        super().__init__()
        self.auth_manager = auth_manager
        self.on_logout = on_logout
        self.theme = ThemeManager()
        self.theme_map = {} 
        
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setup_ui()

    def setup_ui(self):
        self.user_label = QLabel(f"@{self.auth_manager.user_data.get('username', 'izzoremi')}")
        self.status_box = QLabel("✅ Kick Oturumu Açık")
        
        # TEMA SEÇİMİ 
        self.theme_label = QLabel("Uygulama Teması")
        self.theme_combo = QComboBox()
        self.theme_map = self.theme.get_all_themes()
        self.theme_combo.addItems(self.theme_map.keys()) 
        
        current_file = self.theme.get_config("theme", "kick_green.json")
        for name, file in self.theme_map.items():
            if file == current_file:
                self.theme_combo.setCurrentText(name)
                break
        
        self.theme_combo.currentTextChanged.connect(self.change_theme)

        # 🌟 DİL SEÇİMİ (Artık bu da kaydediliyor)
        self.lang_label = QLabel("Tercih ettiğiniz dili seçin")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Türkçe", "English"])
        
        saved_lang = self.theme.get_config("language", "Türkçe")
        self.lang_combo.setCurrentText(saved_lang)
        self.lang_combo.currentTextChanged.connect(lambda text: self.theme.update_config("language", text))
        
        # KISAYOL SEÇİMİ
        self.shortcut_label = QLabel("Görünmezlik Kısayolunu Değiştir (Tıkla ve Tuşa Bas)")
        self.shortcut_input = ShortcutInput("Ctrl+I") # Varsayılan Ctrl+I
        
        # ÇIKIŞ YAP BUTONU 
        self.logout_btn = QPushButton("Çıkış Yap")
        self.logout_btn.setFixedHeight(45)
        self.logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.logout_btn.clicked.connect(self.on_logout)
        
        self.layout.addWidget(self.user_label)
        self.layout.addWidget(self.status_box)
        self.layout.addWidget(self.theme_label)
        self.layout.addWidget(self.theme_combo)
        self.layout.addWidget(self.lang_label)
        self.layout.addWidget(self.lang_combo)
        self.layout.addWidget(self.shortcut_label)
        self.layout.addWidget(self.shortcut_input)
        self.layout.addStretch()
        self.layout.addWidget(self.logout_btn)

        self.update_ui_style()

    def update_ui_style(self):
        self.setStyleSheet(f"background-color: {self.theme.get('window_bg')};")
        self.user_label.setStyleSheet(f"color: {self.theme.get('text_main')}; font-size: 18px; font-weight: bold; background: transparent; border: none;")
        
        title_style = f"color: {self.theme.get('text_main')}; font-size: 14px; font-weight: bold; background: transparent; border: none;"
        self.theme_label.setStyleSheet(title_style + " margin-top: 10px;")
        self.lang_label.setStyleSheet(title_style)
        self.shortcut_label.setStyleSheet(title_style)

        self.status_box.setStyleSheet(f"""
            background-color: rgba(13, 43, 5, 0.4); 
            color: {self.theme.get('accent')}; 
            padding: 12px; 
            border-radius: 5px; 
            border: 1px solid {self.theme.get('accent')};
            font-weight: bold; font-size: 14px;
        """)

        combo_style = f"""
            QComboBox {{ 
                background-color: {self.theme.get('input_bg')}; 
                color: {self.theme.get('text_main')}; 
                padding: 10px; 
                border: 1px solid {self.theme.get('input_border')}; 
                border-radius: 5px; 
            }}
            QComboBox::drop-down {{ border: none; }}
        """
        self.theme_combo.setStyleSheet(combo_style)
        self.lang_combo.setStyleSheet(combo_style)
        
        self.logout_btn.setStyleSheet("""
            QPushButton { background-color: #ffffff; color: #000000; border-radius: 8px; font-size: 15px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #e0e0e0; }
        """)
        
        self.shortcut_input.update_ui_style()

    def change_theme(self, display_name):
        theme_file = self.theme_map.get(display_name)
        if theme_file and self.theme.load_theme(theme_file):
            main_win = self.window()
            if main_win and hasattr(main_win, "refresh_styles"):
                main_win.refresh_styles()

    def update_username(self):
        username = self.auth_manager.user_data.get('username', 'izzoremi')
        self.user_label.setText(f"@{username}")