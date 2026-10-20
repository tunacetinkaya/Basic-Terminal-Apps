# 🅿️ Otopark

Ücret, durulan dakikaya göre çıkar. Başlayan saat yukarı yuvarlanır.

- 15 dakika ve altı ücretsizdir.
- İlk saat 50 TL.
- Sonraki her saat 30 TL.
- Günlük tavan 250 TL.

`14:30` giriş, `18:10` çıkış: 3 saat 40 dakika, 4 saat üzerinden **140 TL**.

Sade sürüm çıkışın aynı gün içinde girişten sonra olmasını ister. `otopark_v2.py` çıkış daha küçükse süreyi ertesi güne sayar. `22:00`–`02:00` dört saattir.

`math`, dakikayı ücretlendirilen saate yukarı yuvarlamak için kullanılır.

```bash
python3 otopark/otopark.py
python3 otopark/otopark_v2.py
```
