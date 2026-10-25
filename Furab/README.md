# FURAB Secret Society

| | |
|---|---|
| **Category** | Web Exploitation |
| **Topic** | Unrestricted File Upload |
| **Difficulty** | Medium |
| **Event** | CSC CTF Contest 2026 |

> ⚠️ This challenge was intentionally built with a vulnerable upload handler for CTF purposes. The code/logic shown here should never be deployed in production.

## Description

Selamat datang di FURAB Recruitment Platform v2.1.3, gerbang rahasia bagi para pendukung setia kapal Arab x Fuji yang belum juga berlayar di dunia nyata. Tugas lu adalah menyelinap masuk dengan berpura-pura menjadi calon agen elit dan mengunggah bukti screenshot follow akun IG FURAB sebagai syarat verifikasi. Namun, misi sebenarnya bukan sekadar mendaftar; si Admin (Aloy) teledor menyimpan backup Chat Log rahasia Arab berisi rencana menikahi Fuji di dalam folder `/uploads/` yang sama. Lu harus membobol protokol keamanan sistem, menanamkan akses ilegal lewat `.htaccess`, dan mencuri bukti chat sakti tersebut (Flag) agar seluruh dunia tahu bahwa kapal ini FIX AKAN BERLAYAR!!!!!!!!

**Instance:** `http://20.204.32.130/` — *hosted on an Azure VM for the contest; resource has since been decommissioned, so this link is no longer live.*

### Hints given to players

1. "Header `X-HTTPS-Modified: true` adalah kunci gerbang."
2. "Lupakan Add, kita mainnya Set. `AddType` itu sudah kuno!"
3. "Apache bisa ditipu buat jalanin file non-PHP jadi PHP pakai `.htaccess`. Cari pola yang 'Match'!"

## Design notes

The app only allows `.jpg`/`.png` uploads client- and server-side, so a direct PHP or `.htaccess` upload is rejected outright. The intended path chains two separate weaknesses instead of a single obvious one:

- A custom header (`X-HTTPS-Modified: true`) silently relaxes the server's extension check — not documented anywhere in the UI, only discoverable by intercepting traffic.
- Even once that gate is bypassed, a naive `.htaccess` using `AddType`/`AddHandler` is blocked; players have to know Apache also accepts `SetHandler` with a `<FilesMatch>` pattern to force arbitrary filenames to execute as PHP.

Requiring both the hidden header *and* the less common `SetHandler` syntax was meant to keep this from being a one-shot copy-paste solve.

See [`writeup.md`](writeup.md) for the full solve walkthrough.
