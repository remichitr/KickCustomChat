import sys
import os

# 🌟 KRİTİK ÇÖZÜM: Chromium'un Ekran Kartı (GPU) motorunu kapatıp zorla şeffaf yapıyoruz!
# Bu satır PyQt6 importlarından bile ÖNCE gelmeli.
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --disable-gpu-compositing --enable-transparent-visuals"

from PyQt6.QtWidgets import QApplication
from core.auth import KickAuth
from core.session_mgr import SessionManager
from gui.app_window import AppWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    auth = KickAuth()
    session = SessionManager()
    
    auth.start_server()
    
    saved_data = session.load_session()
    if saved_data:
        auth.access_token = saved_data.get("access_token")
        auth.refresh_token = saved_data.get("refresh_token")
        auth.user_data = saved_data.get("user_data")
        
        if not auth.test_token():
            print("⚠️ Token süresi dolmuş. Arka planda yenileniyor...")
            if auth.refresh_access_token():
                print("✅ Token başarıyla yenilendi! Oturum güncelleniyor.")
                session.save_session(auth.user_data, auth.access_token, auth.refresh_token)
            else:
                print("❌ Yenileme başarısız (Oturum tamamen ölmüş). Giriş ekranına yönlendiriliyor.")
                session.clear_session()
                auth.access_token = None

    win = AppWindow(auth)
    win.show()
    sys.exit(app.exec())