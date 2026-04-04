# Variabel untuk kemudahan
APP = Home_Page.py

# Perintah default (ketik 'make' atau 'make run')
# Target 'run' sekarang bergantung pada 'check-streamlit'
run: check-streamlit
	streamlit run $(APP)

# Perintah untuk mengecek & install streamlit jika belum ada
check-streamlit:
	@echo "🔍 Mengecek instalasi Streamlit..."
	@where streamlit >nul 2>nul || (echo "📦 Streamlit tidak ditemukan, menginstal sekarang..." && pip install streamlit)

# Perintah untuk membersihkan sampah python
clean:
	@echo "🧹 Menghapus pycache..."
	powershell -Command "Get-ChildItem -Recurse -Filter __pycache__ | Remove-Item -Recurse -Force"

# Perintah untuk install semua library dari requirements
install:
	@echo "📥 Menginstal semua dependensi dari requirements.txt..."
	pip install -r requirements.txt

# Perintah untuk update git sekaligus (ketik 'make push msg="pesan commit"')
push:
	git add .
	git commit -m "$(msg)"
	git push origin main