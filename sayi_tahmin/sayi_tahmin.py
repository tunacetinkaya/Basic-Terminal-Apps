"""
Sayı tahmin etme oyunu

Bilgisayar 1 ile 100 arasında gizli bir sayı seçer.
Sen bu sayıyı bulmaya çalışırsın.
Her tahmininden sonra "daha büyük" ya da "daha küçük" denir.
"""

import random


def main():
    print("=== Sayı Tahmin Oyunu ===")
    print()

    gizli_sayi = random.randint(1, 100)
    deneme = 0

    print("1 ile 100 arasında bir sayı tuttum.")
    print("Bakalım kaç denemede bulacaksın?")
    print()

    while True:
        tahmin = int(input("Tahminin: "))
        deneme += 1

        if tahmin < gizli_sayi:
            print("Daha büyük bir sayı dene.")
        elif tahmin > gizli_sayi:
            print("Daha küçük bir sayı dene.")
        else:
            print(f"Tebrikler! {deneme} denemede buldun.")
            break

        print()


if __name__ == "__main__":
    main()
