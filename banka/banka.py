"""
Basit banka uygulaması

Bakiye sorgulama, para yatırma, para çekme ve hesap hareketleri.
Bakiye ve hareketler program çalışırken değişkenlerde tutulur.
Program kapanınca bu bilgiler silinir.
"""


def main():
    print("=== Basit Banka ===")
    print()

    bakiye = 10_000
    hareketler = []

    while True:
        print("1) Bakiye sorgula")
        print("2) Para yatır")
        print("3) Para çek")
        print("4) Hesap hareketleri")
        print("5) Çıkış")
        print()

        secim = input("Seçimin: ")

        if secim == "1":
            print(f"Bakiyen: {bakiye} TL")
        elif secim == "2":
            tutar = int(input("Yatırılacak tutar: "))
            if tutar <= 0:
                print("Tutar 0'dan büyük olmalı.")
            else:
                bakiye += tutar
                hareketler.append(f"Yatırma: {tutar} TL")
                print(f"{tutar} TL yatırıldı. Yeni bakiye: {bakiye} TL")
        elif secim == "3":
            tutar = int(input("Çekilecek tutar: "))
            if tutar <= 0:
                print("Tutar 0'dan büyük olmalı.")
            elif tutar > bakiye:
                print("Yetersiz bakiye.")
            else:
                bakiye -= tutar
                hareketler.append(f"Çekme: {tutar} TL")
                print(f"{tutar} TL çekildi. Yeni bakiye: {bakiye} TL")
        elif secim == "4":
            if len(hareketler) == 0:
                print("Henüz işlem yok.")
            else:
                for hareket in hareketler:
                    print(hareket)
        elif secim == "5":
            print("Görüşürüz!")
            break
        else:
            print("Geçersiz seçim.")

        print()


if __name__ == "__main__":
    main()
