# 🏦 Banka

Bakiye 10.000 TL ile başlar. Para yatırılır, çekilir, hareketler listelenir. Çekilecek tutar bakiyeden büyükse işlem olmaz.

Sade sürüm her şeyi program açıkken tutar; kapanınca silinir. `banka_v2.py` bakiyeyi ve hareketleri `banka/hesap.json` dosyasına yazar, ok tuşlarıyla menüden seçtirir.

`json` hesabı dosyaya yazıp geri okur. `pathlib` bu dosyanın yolunu programın yanından bulur. `datetime` her harekete saat ekler. `sys` klavyenin dosya numarasını verir. `os` terminalden tek bayt okur. `termios` tuş ayarını geçici değiştirir. `tty` ok tuşunu satır sonunu beklemeden alır. `select` ESC'ten sonra ok tuşu dizisinin gelip gelmediğine kısa süre bakar.

```bash
python3 banka/banka.py
python3 banka/banka_v2.py
```
