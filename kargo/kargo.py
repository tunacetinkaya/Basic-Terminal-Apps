"""
Kargo ücreti hesaplayıcı

Paket ağırlığına ve mesafeye göre toplam kargo ücretini hesaplar.
Sabit taban ücret üzerine ağırlık ve mesafe ücretleri eklenir.
"""


def main():
    print("=== Kargo Ücreti ===")
    print()
    print("Taban ücret: 50 TL")
    print("Ağırlık: 5 kg'a kadar 10 TL, 10 kg'a kadar 25 TL, fazlası 40 TL")
    print("Mesafe: 100 km'ye kadar 10 TL, 200 km'ye kadar 30 TL, fazlası 50 TL")
    print()

    agirlik = float(input("Paket ağırlığı (kg): "))
    mesafe = float(input("Mesafe (km): "))

    if agirlik <= 0 or mesafe <= 0:
        print("Ağırlık ve mesafe 0'dan büyük olmalı.")
        return

    if agirlik <= 5:
        agirlik_ucreti = 10
    elif agirlik <= 10:
        agirlik_ucreti = 25
    else:
        agirlik_ucreti = 40

    if mesafe <= 100:
        mesafe_ucreti = 10
    elif mesafe <= 200:
        mesafe_ucreti = 30
    else:
        mesafe_ucreti = 50

    toplam = 50 + agirlik_ucreti + mesafe_ucreti

    print()
    print("Taban ücret: 50 TL")
    print(f"Ağırlık ücreti ({agirlik:g} kg): {agirlik_ucreti} TL")
    print(f"Mesafe ücreti ({mesafe:g} km): {mesafe_ucreti} TL")
    print(f"Ödenecek tutar: {toplam} TL")


if __name__ == "__main__":
    main()
