# ⛽ Yolda yakıt

Depodaki litre, 100 km tüketimi ve yol uzunluğu birlikte düşünülür.

```text
gereken litre = yol × tüketim / 100
menzil        = depo / tüketim × 100
```

Depo 8 L, tüketim 6 L/100 km, yol 180 km, litre 45 TL: yol 10,8 L ve 486 TL tutar. Yakıt yaklaşık 133. km'de biter; varmak için 2,8 L daha gerekir.

`yolda_yakit_v2.py` depo kapasitesini ve varışta kalmasını istediğin rezervi de sorar. Yakıt tek depoya sığmazsa rezerv düşünce durulacak kilometreyi söyler. Gidiş-dönüş seçilirse mesafe ikiye katlanır.

Kapasite 12 L ve rezerv 5 L iken: yola çıkmadan 4 L al, 116,7. km'de 3,8 L daha al. Varışta depoda 5 L kalır.

```bash
python3 yolda_yakit/yolda_yakit.py
python3 yolda_yakit/yolda_yakit_v2.py
```
