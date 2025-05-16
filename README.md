# Multipjson
```bash
  __  __       _ _   _       _                  
 |  \/  |_   _| | |_(_)_ __ (_)___  ___  _ __   
 | |\/| | | | | | __| | '_ \| / __|/ _ \| '_ \  
 | |  | | |_| | | |_| | |_) | \__ \ (_) | | | | 
 |_|  |_|\__,_|_|\__|_| .__// |___/\___/|_| |_|  v1.0.0
                      |_| |__/                  
	    Multiple JSON Generator
               Created by k4tedu
```

**Multipjson** adalah sebuah web-based JSON generator tool yang dirancang untuk membantu kamu membuat data JSON secara cepat dan dinamis. Tool ini sangat berguna untuk keperluan testing aplikasi, pengembangan API, simulasi data, dan automation dalam bug hunting atau pentesting. Multipjson memungkinkan kamu membuat banyak data JSON dengan berbagai field dan nilai yang dapat dikustomisasi secara interaktif.

---

## 🚀 Features

- ✅ Generate banyak data JSON sekaligus berdasarkan jumlah yang diinginkan.
- ✅ Dukungan multi-field (`name,email,...`)
- ✅ Mendukung kustomisasi `field` dan `value` secara dinamis via input form.
- ✅ Fitur `--prefix` dan `--suffix`
- ✅ Output JSON yang dihasilkan dapat langsung dilihat dalam tampilan yang mudah dibaca.
- ✅ Fitur **Copy to Clipboard** untuk menyalin JSON hasil generate dengan sekali klik
- ✅ Tombol **View Raw** yang membuka JSON mentah dalam tab baru
- ✅ Mode **Dark Mode** toggle di halaman utama untuk kenyamanan penggunaan di berbagai kondisi pencahayaan.

---

## 🔧 Installation
1. Pastikan kamu sudah punya **Python 3.7+** dan **pip** atau **pipx** terinstall.
2. Clone repository ini:
```bash
git clone https://github.com/k4tedu/Multipjson.git
cd Multipjson
pipx install .
```

## 🚀 Usage

- Using without flags just type `multipjson`
```bash
multipjson
```
- or using with flags
```bash
multipjson --help

multipjson --total 5 --fields name,role --values user,admin --output output.txt
```

- or Generete `JSON Objects` via the web (your `localhost`) :
```bash
python3 webapp.py
```
```bash
* Running on http://127.0.0.1:5000
```
