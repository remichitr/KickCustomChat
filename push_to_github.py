import os
import subprocess

def run_command(command):
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Hata oluştu: {e}")

def github_push():
    # 1. Git'i başlat
    if not os.path.exists(".git"):
        print("🚀 Git başlatılıyor...")
        run_command("git init")

    # 2. Dosyaları ekle (.gitignore sayesinde venv gelmeyecek)
    print("📂 Dosyalar ekleniyor...")
    run_command("git add .")

    # 3. İlk Commit
    commit_msg = "Initial commit: Temalı ve Görünmezlik Modlu RemiKickChat"
    run_command(f'git commit -m "{commit_msg}"')

    # 4. Ana dalı ayarla
    run_command("git branch -M main")

    # 5. Uzak depoyu ekle ve pushla
    repo_url = input("🔗 GitHub Repo URL'sini yapıştırın (örn: https://github.com/...): ")
    if repo_url:
        run_command(f"git remote add origin {repo_url}")
        print("📤 Veriler gönderiliyor...")
        run_command("git push -u origin main")
        print("✅ İşlem başarıyla tamamlandı!")

if __name__ == "__main__":
    github_push()