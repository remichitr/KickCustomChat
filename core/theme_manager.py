import json
import os

class ThemeManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ThemeManager, cls).__new__(cls)
            cls._instance.colors = {}
            
            # Yollar
            cls._instance.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            cls._instance.config_path = os.path.join(cls._instance.base_dir, 'store', 'config.json')
            
            # Başlangıçta config'den temayı oku
            saved_theme = cls._instance.get_config("theme", "kick_green.json")
            cls._instance.current_theme_file = saved_theme
            cls._instance.load_theme(cls._instance.current_theme_file, save=False)
            
        return cls._instance

    def get_config(self, key, default_value=None):
        """config.json dosyasından istenen ayarı okur. Yoksa varsayılanı döner."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get(key, default_value)
            except Exception as e:
                print(f"Config okuma hatası: {e}")
        return default_value

    def update_config(self, key, value):
        """Herhangi bir ayarı (tema, kısayol, dil) config.json dosyasına anında yazar."""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        data = {}
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except:
                pass
                
        data[key] = value # İlgili ayarı güncelle veya ekle
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"❌ Config kaydetme hatası: {e}")

    def load_theme(self, theme_file, save=True):
        theme_path = os.path.join(self.base_dir, 'themes', theme_file)
        if os.path.exists(theme_path):
            try:
                with open(theme_path, 'r', encoding='utf-8') as f:
                    self.colors = json.load(f)
                
                self.current_theme_file = theme_file
                if save:
                    self.update_config("theme", theme_file) # Temayı kaydet
                return True
            except Exception as e:
                return False
        return False

    def get_all_themes(self):
        theme_folder = os.path.join(self.base_dir, "themes")
        theme_map = {}
        if os.path.exists(theme_folder):
            for file in os.listdir(theme_folder):
                if file.endswith('.json'):
                    try:
                        with open(os.path.join(theme_folder, file), 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            display_name = data.get("name", file)
                            theme_map[display_name] = file
                    except:
                        continue
        return theme_map

    def get(self, key):
        return self.colors.get(key, "#01fb2f")