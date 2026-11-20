# SenDev® — Creative Developer Portfolio

Website portofolio **SenDev** dibangun ulang dari proyek Django yang dikirim, dengan tema **Obsidian / Electric Violet / Cyan / Lime**, efek interaktif, responsive layout, dan dashboard Django Admin untuk menambahkan foto maupun isi portofolio.

> **Identitas awal** diambil dari proyek asli: **Sendy Ahmad / SenDev**. Nama, email, deskripsi, dan tautan sosial bisa kamu ganti di **Admin → Profil situs**.

## 1. Jalankan proyek di Windows (VS Code)

Buka ZIP, lalu buka folder `portofolio-main` di VS Code. Buka terminal di folder yang berisi `manage.py`.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Jika PowerShell menolak aktivasi virtual environment, gunakan CMD:

```bat
.venv\Scripts\activate.bat
```

Atau panggil langsung: `.venv\Scripts\python.exe manage.py runserver`.

Lalu buka:

- **Portofolio:** http://127.0.0.1:8000/
- **Dashboard admin:** http://127.0.0.1:8000/admin/

Di Mac / Linux, buat virtual environment dengan `python3 -m venv .venv`, aktifkan dengan `source .venv/bin/activate`, kemudian jalankan perintah yang sama.

**Penting:** ZIP final tidak menyertakan database login lama (`db.sqlite3`) untuk menghindari membagikan akun admin atau password hash. Database baru dibuat otomatis dengan `migrate`, dan akun admin dibuat dengan `createsuperuser`. Setelah `migrate`, sistem otomatis menambahkan satu profil SenDev dan empat proyek awal ke database sehingga bisa langsung diedit di Admin.

## 2. Cara mengganti identitas, profil, dan foto

1. Masuk ke `/admin/`.
2. Buka **Profil situs** → klik **SenDev — Sendy Ahmad**. (Profil awal sudah dibuat otomatis saat `migrate`.)
3. Ganti nama, role, deskripsi, email, lokasi, dan URL sosial.
4. Unggah gambar `avatar` untuk tampilan utama serta `about_photo` untuk bagian Tentang.
5. Klik **Simpan** dan refresh homepage. Desain monogram akan otomatis berubah menjadi foto yang kamu unggah.

### Daftar file yang perlu kamu siapkan

| Konten | Nama field di admin | Format & ukuran yang disarankan | Fungsi |
|---|---|---|---|
| Foto profil utama | Profil situs → `avatar` | **900 × 1100 px**, portrait, JPG/WebP | Mengisi kartu visual utama hero |
| Foto pribadi / coding | Profil situs → `about_photo` | **1200 × 900 px**, landscape, JPG/WebP | Mengganti kotak kode di About |
| Screenshot proyek | Proyek → `image` | **1600 × 1000 px**, landscape, JPG/WebP/PNG | Gambar utama kartu proyek |
| Scan sertifikat | Sertifikat → `image` | **1600 × 1100 px**, landscape, JPG/PNG/WebP | Galeri sertifikat, bisa diklik fullscreen |
| Foto kegiatan | Kegiatan → `image` | **1400 × 1100 px**, landscape, JPG/WebP | Galeri kegiatan, workshop, komunitas |
| CV / resume | Profil situs → `resume` | PDF | Data CV tersimpan, siap ditautkan jika diinginkan |

**Kamu tidak perlu mengubah kode untuk foto**: upload file melalui Django Admin. File disimpan di folder `media/` dan URL-nya dipakai otomatis oleh template.

### Cara menambah proyek

Buka **Proyek → Tambah**. Isi judul, deskripsi, kategori, `tech_stack` (pisahkan dengan koma, contoh `React, Laravel, MySQL`), gambar, link GitHub/demo, urutan, lalu simpan.

Saat menjalankan `python manage.py migrate` untuk pertama kali, **empat proyek dari ZIP awal otomatis masuk database** (SPK SAW, Blogging Django, PPID BAZNAS Kaltim, dan Aplikasi Android Islamic). Kamu bisa langsung membuka salah satunya di Admin untuk mengunggah gambarnya. Konfigurasi fallback hanya disiapkan untuk data yang benar-benar kosong.

### Sertifikat & kegiatan

- **Sertifikat → Tambah**: Judul, penerbit, tanggal, gambar, link validasi (jika ada).
- **Kegiatan → Tambah**: Judul kegiatan, kategori, tanggal, deskripsi, dan foto.
- Jika belum ada konten, halaman menampilkan **desain placeholder**, bukan sertifikat atau kegiatan fiktif.

### Pesan masuk

Form kontak menggunakan metode **POST**, **CSRF protection**, validasi email, dan anti-spam honeypot sederhana. Pesan disimpan sebagai **Pesan masuk** di dashboard admin.

**Form tidak mengirim email otomatis**. Pesan tersimpan di database, jadi buka Admin untuk membacanya. Jika kelak ingin notifikasi ke email, tambahkan layanan email dari server Django.

## 3. Fitur visual dan interaktif

- Hero visual dengan **monogram 3D, orbit rings, neon aura, floating cards**.
- **Canvas particle system** yang ringan, menghentikan animasi ketika tab tidak aktif.
- **Scroll reveal**, progress bar scroll, active navigation, marquee ticker.
- **Cursor ambient glow, tilt cards, spotlight hover, magnetic buttons** (desktop).
- **Filter proyek** All/Web/Backend/Mobile.
- **Galeri fullscreen** untuk sertifikat dan kegiatan asli yang diunggah.
- **Command palette**: tekan `Ctrl + K` atau `⌘ + K` untuk cari navigasi.
- **Copy email**, form kontak backend, menu mobile, interaksi keyboard, reduced-motion support.
- Responsif untuk desktop, tablet, dan ponsel.

## 4. Tampilan demo tanpa instalasi Django

Folder **`demo/`** berisi tampilan pratinjau statis yang dibuat dari template yang sama dengan contoh data. Buka `demo/index.html` di browser, atau jalankan server lokal:

```powershell
cd demo
py -m http.server 8001
```

Lalu kunjungi `http://127.0.0.1:8001/`.

**Batas demo:** data admin, upload, dan pengiriman kontak **tidak aktif** di versi statis. Jalankan Django untuk menggunakan fitur tersebut. `demo/index.html` adalah hasil ekspor pratinjau, jadi tidak otomatis memperbarui ketika kamu mengubah database Django.

## 5. Struktur utama

```text
portofolio-main/
├── manage.py
├── requirements.txt
├── .env.example
├── porto/                     # Settings, URL, ASGI, WSGI
├── portofolio/
│   ├── models.py              # Profil, proyek, sertifikat, kegiatan, pesan, dll.
│   ├── admin.py               # Dashboard pengelolaan
│   ├── views.py               # Data, fallback, dan kontak
│   ├── urls.py
│   └── migrations/
├── templates/
│   ├── base.html              # Navbar, dialog, footer, metadata
│   └── portofolio/home.html   # Seluruh section homepage
├── static/
│   ├── css/portfolio.css      # Desain & animasi
│   ├── js/portfolio.js        # Semua interaksi frontend
│   └── images/brand/favicon.svg
├── media/                     # Gambar hasil upload (otomatis)
└── demo/                      # Preview statis (tanpa Django)
```

## 6. Deployment (penting)

Ini adalah **Django dinamis**, bukan proyek React/Vite statis. Untuk deploy dengan admin dan upload foto, gunakan hosting yang mendukung Python/Django dan penyimpanan media persisten (misalnya Render, Railway, VPS, atau hosting Python yang setara).

Sebelum deploy ke publik:

1. Buat `DJANGO_SECRET_KEY` acak dan rahasia.
2. Set `DJANGO_DEBUG=0` dan `DJANGO_ALLOWED_HOSTS=domainkamu.com`.
3. Jalankan `python manage.py collectstatic` dan layani `staticfiles/` di server.
4. Konfigurasikan direktori **media** yang persisten atau object storage; jangan mengandalkan filesystem sementara untuk upload.
5. Pakai database persisten untuk produksi, misalnya PostgreSQL (butuh pengaturan database terpisah).
6. Aktifkan HTTPS dan set `DJANGO_CSRF_TRUSTED_ORIGINS=https://domainkamu.com`.
7. Pertimbangkan rate limiting / CAPTCHA dan notifikasi email untuk form kontak publik.

**Tidak cukup** hanya mengunggah folder Django ke Vercel sebagai file HTML statis untuk mendapatkan admin dan fitur upload.

## 7. Penyesuaian warna

Buka `static/css/portfolio.css` pada bagian `:root`. Ubah `--purple`, `--violet`, `--cyan`, `--lime`, dan `--pink`. UI akan otomatis mengikuti variabel warna tersebut.

---

**SenDev** — *Built with logic. Designed with feeling.*
