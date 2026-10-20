"""
Yolda yakıt

Depodaki yakıt, tüketim ve mesafeye göre yolun tutarını hesaplar.
Yakıt yetmezse kaçıncı kilometrede biteceğini de söyler.
"""


def main():
    print("=== Yolda Yakıt ===")
    print()

    depo = float(input("Depodaki yakıt (litre): "))
    tuketim = float(input("100 km'de tüketim (litre): "))
    yol = float(input("Yol (km): "))
    fiyat = float(input("Litre fiyatı (TL): "))

    if depo < 0 or fiyat < 0:
        print("Yakıt ve fiyat 0'dan küçük olamaz.")
        return
    if tuketim <= 0 or yol <= 0:
        print("Tüketim ve yol 0'dan büyük olmalı.")
        return

    gereken = yol * tuketim / 100
    masraf = gereken * fiyat
    menzil = depo / tuketim * 100

    print()
    print(f"Gereken yakıt: {gereken:.1f} L")
    print(f"Yolun yakıt parası: {masraf:.0f} TL")
    print(f"Bu depoyla gidebileceğin yol: {menzil:.0f} km")

    if menzil < yol:
        eksik = gereken - depo
        print(f"Yakıt yaklaşık {menzil:.0f}. km'de biter.")
        print(f"Varmak için {eksik:.1f} L daha lazım ({eksik * fiyat:.0f} TL).")
    else:
        kalan = depo - gereken
        print(f"Yakıt yeter. Varışta depoda yaklaşık {kalan:.1f} L kalır.")


if __name__ == "__main__":
    main()
