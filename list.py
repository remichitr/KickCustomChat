import os

def list_files(startpath):
    # Dışarıda tutulacak klasörler (dosya kalabalığı yapmasınlar)
    exclude_dirs = {'.git', 'node_modules', 'dist', 'out', 'build', '.vscode'}
    
    print(f"--- Proje Ağacı: {startpath} ---")
    for root, dirs, files in os.walk(startpath):
        # Gereksiz klasörleri atla
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f'{indent}{os.path.basename(root)}/')
        
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            # Sadece önemli dosya tiplerini göster (isteğe bağlı)
            if f.endswith(('.ts', '.vue', '.json', '.html', '.js')):
                print(f'{sub_indent}{f}')

# Senin yolun
project_path = r"D:\RemiTools\RemiKickChat"

if os.path.exists(project_path):
    list_files(project_path)
else:
    print("Yol bulunamadı! Lütfen yolu kontrol et.")