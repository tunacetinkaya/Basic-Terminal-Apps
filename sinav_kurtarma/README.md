# 📝 Sınav kurtarma

Geçme notuna ulaşmak için kalan sınavdan kaç alınması gerektiğini hesaplar. Not tam sayı olduğu için sonuç yukarı yuvarlanır.

Vize 40 (%40), final %60, geçme notu 50:

```text
(50 × 100 − 40 × 40) / 60 = 56,67  →  finalden en az 57
```

Hesap 0'ın altındaysa finalden 0 almak yeter. 100'ün üstündeyse finalden 100 alınsa da geçilmez.

`sinav_kurtarma_v2.py` birden fazla not alır. Vize 40 (%40) ve ödev 80 (%10) girilince kalan %50 finale kalır ve eşik 52 olur.

`math`, 56,67 gibi bir sonucu tam nota yukarı yuvarlamak için kullanılır.

```bash
python3 sinav_kurtarma/sinav_kurtarma.py
python3 sinav_kurtarma/sinav_kurtarma_v2.py
```
