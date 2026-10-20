# 📦 Kargo

Her gönderiye 50 TL taban ücret eklenir. Ağırlık ve mesafe kendi tarifesinden bir kez ücretlenir; kilogram veya kilometre başı çarpılmaz.

| Ağırlık | Ücret | Mesafe | Ücret |
|---|---:|---|---:|
| ≤ 5 kg | 10 TL | ≤ 100 km | 10 TL |
| ≤ 10 kg | 25 TL | ≤ 200 km | 30 TL |
| > 10 kg | 40 TL | > 200 km | 50 TL |

7 kg ve 150 km: 50 + 25 + 30 = **105 TL**.

`kargo_v2.py` bu tabloları kodun içindeki tarife listesinden üretir. Aralık değişince hem hesap hem ekran aynı satırdan okur.

```bash
python3 kargo/kargo.py
python3 kargo/kargo_v2.py
```
