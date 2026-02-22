import requests
import cloudscraper

class KickAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
        )

    def get_channel_info(self, channel_slug):
        print(f"\n--- @{channel_slug} İçin Kanal Bilgisi Aranıyor ---")
        url_frontend = f"https://kick.com/api/v1/channels/{channel_slug}"
        
        try:
            res = self.scraper.get(url_frontend)
            if res.status_code == 200:
                data = res.json()
                chatroom_id = data.get("chatroom", {}).get("id")
                broadcaster_user_id = data.get("user", {}).get("id") or data.get("user_id") 
                
                if chatroom_id and broadcaster_user_id:
                    print(f"✅ Kanal Bulundu! Chatroom ID: {chatroom_id} | User ID: {broadcaster_user_id}")
                    return {"broadcaster_user_id": broadcaster_user_id, "chatroom_id": chatroom_id}
            else:
                print(f"❌ Cloudflare aşılmadı. Kod: {res.status_code}")
        except Exception as e:
            print(f"Kanal bilgisi hatası: {e}")
            
        print("❌ Kanal bilgileri alınamadı.")
        return None

    def send_message(self, broadcaster_user_id, chatroom_id, message):
        """Kick Resmi API'sine scraper üzerinden mesaj gönderir."""
        url = "https://api.kick.com/public/v1/chat"
        
        try:
            b_id = int(broadcaster_user_id)
        except:
            b_id = broadcaster_user_id

        payload = {
            "broadcaster_user_id": b_id,
            "content": message,
            "type": "user"
        }
        
        print(f"\n--- MESAJ KICK'E İLETİLİYOR ---")
        print(f"-> Giden Mesaj: '{message}' | Hedef Yayıncı ID: {b_id}")
        
        try:
            # 🌟 requests YERİNE scraper KULLANIYORUZ
            res = self.scraper.post(url, json=payload, headers=self.headers)
            print(f"-> Kick'ten Gelen Yanıt Kodu: {res.status_code}")
            print(f"-> Yanıt Detayı: {res.text}")
            
            if res.status_code in [200, 204]:
                print("✅ MESAJ BAŞARIYLA KICK CHATİNE DÜŞTÜ!")
                return True
            elif res.status_code == 401:
                print("❌ HATA 401: Token geçersiz. Uygulamadan çıkıp tekrar giriş yapmalısın (session.json'ı sil).")
            elif res.status_code == 403:
                print("❌ HATA 403: Yetki reddedildi! Kick API bu token'da 'chat:write' izni bulamadı veya Cloudflare engelledi.")
        except Exception as e:
            print(f"❌ İstek sırasında çökme yaşandı: {e}")
            
        return False