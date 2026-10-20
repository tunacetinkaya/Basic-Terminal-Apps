"""
Otopark ücreti

Giriş ve çıkış saatine göre ücreti hesaplar.
İlk 15 dakika ücretsizdir.
Sonrasında ilk saat 50 TL, başlayan her sonraki saat 30 TL'dir.
Günlük tavan 250 TL'dir.
"""


def main():
    print("=== Otopark Ücreti ===")
    print()
    print("15 dakikaya kadar: ücretsiz")
    print("İlk saat: 50 TL")
    print("Sonraki her saat: 30 TL")
    print("Günlük tavan: 250 TL")
    print()

    giris = input("Giriş saati (14:30): ")
    cikis = input("Çıkış saati (18:10): ")

    try:
        giris_saat, giris_dakika = giris.split(":")
        cikis_saat, cikis_dakika = cikis.split(":")
        giris_toplam = int(giris_saat) * 60 + int(giris_dakika)
        cikis_toplam = int(cikis_saat) * 60 + int(cikis_dakika)
    except ValueError:
        print("Saati 14:30 biçiminde yaz.")
        return

    if not (0 <= giris_toplam < 24 * 60 and 0 <= cikis_toplam < 24 * 60):
        print("Saat 00:00 ile 23:59 arasında olmalı.")
        return

    sure = cikis_toplam - giris_toplam
    if sure <= 0:
        print("Çıkış saati girişten sonra olmalı.")
        return

    saat = sure // 60
    dakika = sure % 60
    print()
    if saat == 0:
        print(f"Kaldığın süre: {dakika} dakika")
    elif dakika == 0:
        print(f"Kaldığın süre: {saat} saat")
    else:
        print(f"Kaldığın süre: {saat} saat {dakika} dakika")

    if sure <= 15:
        print("15 dakikaya kadar ücret yok.")
        print("Ödenecek tutar: 0 TL")
        return

    if dakika == 0:
        ucretli_saat = saat
    else:
        ucretli_saat = saat + 1

    ucret = 50 + (ucretli_saat - 1) * 30
    print(f"Ücretlendirilen saat: {ucretli_saat}")

    if ucret > 250:
        print(f"Hesaplanan ücret {ucret} TL, günlük tavan uygulandı.")
        ucret = 250

    print(f"Ödenecek tutar: {ucret} TL")


if __name__ == "__main__":
    main()
