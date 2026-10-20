# Terminal Uygulamaları

Küçük konsol programları. Her biri günlük bir hesabı soruya çevirir: kaç lira, kaç km, kaç not.

Bir klasöre girince aynı fikrin iki hâli durur. Sade dosya hesabı tek akışta yapar. İkinci sürüm aynı sonucu daha düzenli kodla, kontrollü girdiyle ve tabloyla basar.

| Dosya | Ne işe yarar |
|---|---|
| `uygulama.py` | Sade sürüm. `input` ve `print` ile tek akışta hesaplar. |
| `uygulama_v2.py` | Aynı hesap. Girdi kontrol edilir, sonuç tabloyla gösterilir. |

İkinci sürümler [Rich](https://github.com/Textualize/rich) kullanır. Onun dışında kurulan bir paket yoktur.

```bash
pip install rich
```

Komutlar proje klasöründen çalışır:

```bash
python3 kargo/kargo.py
python3 kargo/kargo_v2.py
```

## Uygulamalar

Hesabın ayrıntısı her klasörün kendi README dosyasında.

| Uygulama | Kısaca | Ayrıntı |
|---|---|---|
| Sayı tahmin 🎯 | 1 ile 100 arasında tutulan sayıyı, yön ipuçlarıyla bul. | [README](sayi_tahmin/README.md) |
| Banka 🏦 | Yatır, çek, hareketleri gör. İkinci sürüm kaydı dosyada tutar. | [README](banka/README.md) |
| Kargo 📦 | Taban ücretin üstüne ağırlık ve mesafe tarifesini ekle. | [README](kargo/README.md) |
| Otopark 🅿️ | Giriş ve çıkış saatinden, tavanlı otopark ücretini çıkar. | [README](otopark/README.md) |
| Hesap bölüştürücü 🍽️ | Masadaki parayı böl, kimin kime vereceğini söyle. | [README](hesap_bolusturucu/README.md) |
| Sınav kurtarma 📝 | Geçmek için kalan sınavdan kaç almak gerektiğini bul. | [README](sinav_kurtarma/README.md) |
| Yolda yakıt ⛽ | Depo bu yola yeter mi, yetmezse nerede biter? | [README](yolda_yakit/README.md) |

## İkinci sürümde ne değişir

Hesap kuralı aynı kalır. Değişen, programın bu kuralı nasıl taşıdığıdır.

- **Ekran.** Düz satırların yerini panel ve tablo alır.
- **Girdi.** Boş ad, eksi tutar veya bozuk saat geri çevrilir.
- **Tekrar.** Bir hesap bitince yenisi sorulur.
- **Kayıt.** Bankada bakiye `hesap.json` içinde durur; program kapanınca silinmez.

Bazı ikinci sürümler kurala küçük bir gerçek hayat payı da ekler. Otopark gece yarısını ertesi güne sayar. Sınav birden fazla not alır. Yakıt, varışta kalmasını istediğin rezervi hesaba katar.
