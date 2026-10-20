"""
Hesap bölüştürücü

Herkesin ödediği tutarı alır, hesabı kişi sayısına böler.
Kim alacaklı, kim borçlu ekrana yazar.
Toplam tam bölünmezse artan lira ilk kişilere birer lira olarak yazılır.
"""


def main():
    print("=== Hesap Bölüştürücü ===")
    print()

    kisi_sayisi = int(input("Kaç kişisiniz? "))
    if kisi_sayisi < 2:
        print("Bölüştürmek için en az 2 kişi olmalı.")
        return

    kisiler = []
    toplam = 0

    for sira in range(1, kisi_sayisi + 1):
        ad = input(f"{sira}. kişinin adı: ").strip()
        if ad == "":
            print("Ad boş olamaz.")
            return
        odeme = int(input(f"{ad} ne kadar ödedi? "))
        if odeme < 0:
            print("Ödeme 0'dan küçük olamaz.")
            return
        kisiler.append((ad, odeme))
        toplam += odeme

    kisi_basi = toplam // kisi_sayisi
    artan = toplam % kisi_sayisi

    print()
    print(f"Toplam: {toplam} TL")
    if artan == 0:
        print(f"Kişi başı: {kisi_basi} TL")
    else:
        print(
            f"Kişi başı: {kisi_basi} TL. "
            f"Artan {artan} TL ilk kişilere 1'er TL eklendi."
        )
    print()

    for sira, (ad, odeme) in enumerate(kisiler):
        if sira < artan:
            pay = kisi_basi + 1
        else:
            pay = kisi_basi
        fark = odeme - pay

        if fark > 0:
            print(f"{ad}: {pay} TL pay, {fark} TL alacaklı")
        elif fark < 0:
            print(f"{ad}: {pay} TL pay, {-fark} TL borçlu")
        else:
            print(f"{ad}: {pay} TL pay, hesap eşit")


if __name__ == "__main__":
    main()
