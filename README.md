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

**multipjson** (Multiple JSON Generator) adalah CLI tool buatan `k4tedu` untuk menghasilkan array objek JSON secara otomatis dengan field yang bisa dikustomisasi. Cocok untuk testing, dummy data, atau API simulasi.

---

## 🚀 Features

- ✅ Generate ribuan objek JSON dalam 1 klik
- ✅ Dukungan multi-field (`name,email,...`)
- ✅ Auto increment value (`user1`, `user2`, dst)
- ✅ Fitur `--prefix` dan `--suffix`
- ✅ Auto-update checker
- ✅ Bash auto-completion
- ✅ ASCII CLI branding

---

## 🔧 Installation

```bash
git clone https://github.com/k4tedu/Multipjson
cd Multipjson
pipx install .
```

## 🚀 Usage
```bash
multipjson --help

multipjson --total 5 --fields name,role --values user,admin --output output.txt
```
