"""
Sınav kurtarma

Vize notundan, finalden kaç alınması gerektiğini hesaplar.
Notlar tam sayı olduğu için sonuç yukarı yuvarlanır.
"""

import math


def main():
    print("=== Sınav Kurtarma ===")
    print()

    vize = int(input("Vize notun: "))
    vize_yuzde = int(input("Vize ağırlığı (%): "))
    final_yuzde = int(input("Final ağırlığı (%): "))
    gecme = int(input("Geçme notu: "))

    if not (0 <= vize <= 100 and 0 <= gecme <= 100):
        print("Notlar 0 ile 100 arasında olmalı.")
        return
    if vize_yuzde <= 0 or final_yuzde <= 0:
        print("Ağırlık 0'dan büyük olmalı.")
        return
    if vize_yuzde + final_yuzde != 100:
        print("Vize ve final ağırlığının toplamı 100 olmalı.")
        return

    ham = (gecme * 100 - vize * vize_yuzde) / final_yuzde
    en_yuksek = (vize * vize_yuzde + 100 * final_yuzde) / 100

    print()
    if ham <= 0:
        print("Finalden 0 alsan da geçiyorsun.")
        print(f"Vize katkın: {vize * vize_yuzde / 100:g}")
    elif ham > 100:
        print("Finalden 100 alsan da bu notla geçemiyorsun.")
        print(f"Ulaşabileceğin en yüksek ortalama: {en_yuksek:g}")
    else:
        gerekli = math.ceil(ham)
        print(f"Finalden en az {gerekli} almalısın.")
        if gerekli != ham:
            print(f"Hesap {ham:.2f} çıktı, not tam sayı olduğu için yukarı yuvarlandı.")


if __name__ == "__main__":
    main()
