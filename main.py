"""THE PORTSIDE GAZETTE milik @kombinasisayur0566 — Akun 16, NI22 Wave 7.

Tugas berkas ini sederhana: pastikan gambar edisi pelabuhan ini sahih
sebagai PNG, ukur sisinya, kemudian teruskan salinan persisnya keluar.
Edisi ini diterbitkan apa adanya — tanpa kompres ulang, tanpa ubahan piksel.
"""

import hashlib
import os
import struct
import sys

CONCEPT = "THE PORTSIDE GAZETTE"
ACCOUNT = "@kombinasisayur0566"
ACCOUNT_LABEL = "Akun 16"
BOUNTY = "news-image-20261122"
STORIES = 36
MAX_SIDE = 1024

EXPECTED_MAGIC = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])


def abort(reason):
    print(f"gagal: {reason}", file=sys.stderr)
    sys.exit(1)


def main():
    folder = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(folder, "entry.png")
    try:
        with open(path, "rb") as fh:
            first = fh.read(33)
    except OSError as exc:
        abort(f"entry.png tidak bisa dibuka: {exc}")

    if len(first) != 33:
        abort("33 byte pertama tidak lengkap")
    if first[0:8] != EXPECTED_MAGIC:
        abort("tanda tangan PNG tidak cocok")
    if first[12:16] != b"IHDR":
        abort("IHDR tidak berada pada posisi yang diharapkan")
    lebar, tinggi = struct.unpack(">II", first[16:24])
    if lebar > MAX_SIDE or tinggi > MAX_SIDE:
        abort(f"ukuran {lebar}x{tinggi} melewati plafon {MAX_SIDE}px")

    data = open(path, "rb").read()
    total = len(data)
    fingerprint = hashlib.sha256(data).hexdigest()

    dest_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "entry.png")
    with open(dest, "wb") as fh:
        fh.write(data)

    ulang = open(dest, "rb").read()
    if hashlib.sha256(ulang).hexdigest() != fingerprint or len(ulang) != total:
        abort("hasil salinan berbeda dari berkas asal")

    print(f"Concept: {CONCEPT}")
    print(f"Account: {ACCOUNT} ({ACCOUNT_LABEL})")
    print(f"Bounty: {BOUNTY}")
    print("File: entry.png")
    print(f"Size: {total} bytes")
    print(f"Dim: {lebar}x{tinggi}")
    print(f"SHA256: {fingerprint}")
    print(f"Stories: {STORIES}")
    print("Copy verified byte-identical.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
