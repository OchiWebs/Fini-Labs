# Proyek Lab Keamanan: IDOR Labs

Selamat datang di IDOR Labs!

Aplikasi web ini dibuat menggunakan **Flask** dan dirancang khusus untuk menjadi laboratorium pembelajaran kerentanan keamanan siber, yaitu ***Insecure Direct Object Reference (IDOR)***.

Proyek ini mencakup fitur autentikasi pengguna, manajemen proyek dan catatan pribadi, serta panel admin. Seluruh aplikasi telah dikemas menggunakan **Docker** untuk memastikan proses instalasi dan penyiapan berjalan dengan mudah dan konsisten di berbagai lingkungan.

---

## 🚀 Cara Menjalankan Lab

Anda dapat menjalankan aplikasi ini melalui dua cara: menggunakan **Docker (direkomendasikan untuk kemudahan)** atau menjalankan skrip **`run.sh` (untuk pengembangan lokal)**.

### Opsi 1: Menjalankan dengan Docker (Cara yang Direkomendasikan)

Metode ini adalah cara yang paling sederhana dan andal karena menggunakan Docker untuk menciptakan lingkungan yang terisolasi dan konsisten.

1.  **Clone Repositori**
    Salin repositori ini ke mesin lokal Anda menggunakan Git.
    ```bash
    git clone <URL_REPOSITORI_ANDA>
    cd <nama-direktori-repositori>
    ```

2.  **Build dan Jalankan dengan Docker Compose**
    Di direktori utama proyek, jalankan perintah berikut. Perintah ini akan membangun *image* Docker dan memulai kontainer di latar belakang (*detached mode*).
    ```bash
    docker-compose up --build -d
    ```

3.  **Akses Aplikasi**
    Setelah kontainer berhasil berjalan, buka browser Anda dan kunjungi alamat berikut:

    ➡️ **http://localhost:5000**

4.  **Menghentikan Aplikasi**
    Untuk menghentikan dan menghapus semua sumber daya Docker (kontainer, jaringan, dll.), jalankan perintah:
    ```bash
    docker-compose down
    ```

---

### Opsi 2: Menjalankan dengan Skrip `run.sh` (Pengembangan Lokal)

Metode ini cocok jika Anda ingin menjalankan aplikasi secara langsung di mesin Anda untuk tujuan pengembangan atau *debugging* tanpa Docker.

1.  **Clone Repositori**
    Jika Anda belum melakukannya, salin repositori ini ke mesin lokal Anda.
    ```bash
    git clone <URL_REPOSITORI_ANDA>
    cd <nama-direktori-repositori>
    ```

2.  **Berikan Izin Eksekusi pada Skrip**
    Pada sistem operasi macOS atau Linux, Anda mungkin perlu memberikan izin eksekusi pada file `run.sh`.
    ```bash
    chmod +x run.sh
    ```

3.  **Jalankan Skrip**
    Eksekusi skrip `run.sh`. Skrip ini akan secara otomatis melakukan langkah-langkah berikut:
    * Menghapus database lama (jika ada) untuk reset.
    * Membuat dan mengaktifkan *virtual environment* Python.
    * Menginstal semua dependensi yang diperlukan dari `requirements.txt`.
    * Memulai server pengembangan Flask.

    ```bash
    ./run.sh
    ```
    *Catatan untuk pengguna Windows:* Anda disarankan menjalankan skrip ini melalui **Git Bash** atau **WSL (Windows Subsystem for Linux)**.

4.  **Akses Aplikasi**
    Buka browser Anda dan kunjungi alamat berikut:

    ➡️ **http://localhost:5000**

5.  **Menghentikan Server**
    Untuk menghentikan server, kembali ke terminal Anda dan tekan `Ctrl + C`.

---

## 🧪 Cara Menggunakan Laboratorium

Database secara otomatis diisi dengan dua pengguna untuk memungkinkan Anda mendemonstrasikan kerentanan IDOR:

* **Pengguna Admin**
    * **Username**: `admin`
    * **Password**: `password123`

* **Pengguna "Attacker"**
    * **Username**: `atacker`
    * **Password**: `password123`

**Misi Anda**: Masuk sebagai pengguna `atacker` dan coba akses atau ubah sumber daya (seperti proyek atau catatan) milik pengguna `admin` dengan cara memanipulasi nilai ID di URL browser Anda.