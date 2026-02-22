# Ozel GUI Bileşenleri
from PyQt6.QtWidgets import QPushButton

class ModernButton(QPushButton):
    """Her yerde kullanabileceğin standart modern yeşil buton."""
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton { background-color: #53fc18; color: black; border-radius: 5px; font-size: 16px; font-weight: bold; padding: 10px; }
            QPushButton:hover { background-color: #45d613; }
        """)