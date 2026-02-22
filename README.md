# 🟢 RemiKickChat

RemiKickChat, Kick.com yayıncıları ve izleyicileri için geliştirilmiş, **Canlı Tema Desteği** ve **Şeffaf Overlay (Görünmezlik)** moduna sahip gelişmiş bir masaüstü sohbet uygulamasıdır.

## ✨ Özellikler

* **Canlı Tema Motoru:** Uygulama kapanmadan Pink, Dark Green gibi temalar arasında anlık geçiş.
* **Görünmezlik (Hayalet) Modu:** Tek bir kısayol ile sohbeti tamamen şeffaf, çerçevesiz ve tıklanabilir (click-through) bir overlay moduna sokun.
* **Kick API Entegrasyonu:** Resmi Kick protokolleri üzerinden hızlı ve güvenli mesaj iletimi.
* **Özel Kısayollar:** Görünmezlik modunu kendi belirlediğiniz tuş kombinasyonuyla yönetin.
* **Modern Arayüz:** PyQt6 ve WebEngine teknolojileriyle pürüzsüz kullanıcı deneyimi.

## 🚀 Kurulum

1.  **Depoyu Klonlayın:**
    ```bash
    git clone [https://github.com/kullanici-adiniz/RemiKickChat.git](https://github.com/kullanici-adiniz/RemiKickChat.git)
    cd RemiKickChat
    ```

2.  **Sanal Ortamı Oluşturun:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows için: .venv\Scripts\activate
    ```

3.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install flask PyQt6 PyQt6-WebEngine websocket-client requests python-dotenv
    ```

4.  **Uygulamayı Çalıştırın:**
    ```bash
    python main.py
    ```

## ⌨️ Kısayollar

* **Görünmezlik Modu:** `Ctrl + I` (Ayarlardan değiştirilebilir).

## 🎨 Tema Ekleme

`themes/` klasörüne yeni `.json` dosyaları ekleyerek kendi temanızı yaratabilirsiniz.