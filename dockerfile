# Gunakan base image Python versi 3.9
FROM python:3.9-slim

# Set direktori kerja di dalam container
WORKDIR /app

# Salin file requirements terlebih dahulu untuk caching layer
COPY requirements.txt requirements.txt

# Install semua dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file proyek ke dalam direktori kerja di container
COPY . .

# Beri tahu Docker port mana yang akan diekspos oleh aplikasi
EXPOSE 5000

# Perintah untuk menjalankan aplikasi saat container dimulai
CMD ["python", "app.py"]