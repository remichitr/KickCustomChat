import json, os

class SessionManager:
    def __init__(self, file_path="session.json"):
        self.file_path = file_path

    def save_session(self, user_data, access_token, refresh_token=None):
        """Oturum bilgilerini (Yenileme anahtarıyla birlikte) dosyaya kaydeder."""
        data = {
            "user_data": user_data, 
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_session(self):
        """Varsa eski oturumu yükler."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return None
        return None

    def clear_session(self):
        """Oturum dosyasını siler (Çıkış yapıldığında veya token tamamen öldüğünde)."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)