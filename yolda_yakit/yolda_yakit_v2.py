"""
Yolda yakıt (v2)

Yolun yakıtını, depoyu ve varışta kalmasını istediğin rezervi birlikte düşünür.
Yola çıkmadan alınacak litre yetmezse, rezerv düşünce durulacak yeri de hesaplar.
Gidiş-dönüş seçilirse mesafe ikiye katlanır.
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, FloatPrompt
from rich.table import Table
from rich.text import Text

console = Console()

EPS = 1e-6


class EvetHayir(Confirm):
    """Evet/hayır sorusunu e / h ile sorar."""

    validate_error_message = "[red]Lütfen e veya h yaz.[/red]"
    choices = ["e", "h"]


def litre_gerek(km: float, tuketim: float) -> float:
    """Verilen yol için tüketilen litreyi döndürür."""
    return km * tuketim / 100


def planla(
    depo: float,
    kapasite: float,
    tuketim: float,
    yol: float,
    fiyat: float,
    rezerv: float,
) -> dict:
    """Yakıt alımlarını ve varışta kalacak litreye göre bir plan döndürür.

    Kural: varışta depoda `rezerv` litre kalsın. Sığmazsa depo doldurulur,
    araç rezerv düşünce durur ve aynı kural yeniden uygulanır.
    """
    if not (0 <= depo <= kapasite):
        raise ValueError("Depodaki yakıt 0 ile kapasite arasında olmalı.")
    if kapasite <= 0 or not (0 <= rezerv < kapasite):
        raise ValueError("Rezerv, depo kapasitesinden küçük olmalı.")
    if tuketim <= 0 or yol <= 0 or fiyat < 0:
        raise ValueError("Tüketim ve yol 0'dan büyük olmalı.")

    alimlar = []
    elde = depo
    konum = 0.0

    while True:
        kalan_km = yol - konum
        kalan_yakit = litre_gerek(kalan_km, tuketim)
        if elde + EPS >= kalan_yakit + rezerv:
            return {
                "gerekli": litre_gerek(yol, tuketim),
                "maliyet": litre_gerek(yol, tuketim) * fiyat,
                "alimlar": alimlar,
                "varis": elde - kalan_yakit,
            }

        bosluk = kapasite - elde
        if bosluk <= EPS:
            raise ValueError("Depo dolu, yine de rezerv yüzünden yol bitmiyor.")

        alinacak = min(bosluk, kalan_yakit + rezerv - elde)
        alimlar.append((konum, alinacak))
        elde += alinacak

        if elde + EPS >= kalan_yakit + rezerv:
            continue

        kullanilabilir = elde - rezerv
        if kullanilabilir <= EPS:
            raise ValueError("Rezerv bu depoda ilerlemeye yer bırakmıyor.")

        konum += kullanilabilir * 100 / tuketim
        elde = rezerv


def tl(tutar: float) -> str:
    """Tutarı 1.250 TL ya da 1.250,50 TL biçiminde döndürür."""
    kurus = round(tutar * 100)
    tam, kalan = divmod(abs(kurus), 100)
    govde = f"{tam:,}".replace(",", ".")
    if kurus < 0:
        govde = f"-{govde}"
    if kalan == 0:
        return f"{govde} TL"
    return f"{govde},{kalan:02d} TL"


def miktar(deger: float, birim: str) -> str:
    """Ölçüyü, tam sayıya çok yakınsa küsuratsız yazar."""
    if abs(deger - round(deger)) < 0.05:
        govde = f"{round(deger):,}".replace(",", ".")
    else:
        govde = f"{deger:.1f}".replace(".", ",")
    return f"{govde} {birim}"


def show_welcome() -> None:
    """Başlığı gösterir."""
    console.print()
    console.print(
        Panel(
            Text("Yolda Yakıt", justify="center", style="bold cyan"),
            subtitle="Depo, rezerv ve durak",
            border_style="cyan",
        )
    )
    console.print()
    console.print(
        "Varışta depoda rezerv kadar yakıt kalsın istersin. "
        "Tek depoya sığmazsa araç, rezerv düşünce durur."
    )
    console.print()


def sayi_iste(etiket: str, alt: float, ust: float | None = None) -> float:
    """Alt sınırın üstünde, istenirse üst sınırın içinde bir sayı okur."""
    while True:
        deger = FloatPrompt.ask(etiket)
        if deger < alt or (ust is not None and deger > ust):
            if ust is None:
                console.print(f"[red]{alt:g} veya daha büyük olmalı.[/red]")
            else:
                console.print(f"[red]{alt:g} ile {ust:g} arasında olmalı.[/red]")
            continue
        return deger


def sorular() -> dict:
    """Yolculuk bilgilerini sorar. Gidiş-dönüşte mesafeyi ikiye katlar."""
    depo = sayi_iste("[bold]Depodaki yakıt (litre)[/bold]", 0)
    kapasite = sayi_iste("[bold]Depo kapasitesi (litre)[/bold]", depo)
    tuketim = sayi_iste("[bold]100 km'de tüketim (litre)[/bold]", 0.1)
    tek_yon = sayi_iste("[bold]Yol (km)[/bold]", 0.1)
    gidis_donus = EvetHayir.ask("Gidiş-dönüş mü?")
    fiyat = sayi_iste("[bold]Litre fiyatı (TL)[/bold]", 0)
    while True:
        rezerv = FloatPrompt.ask("[bold]Varışta kalsın (litre)[/bold]", default=5)
        if 0 <= rezerv < kapasite:
            break
        console.print("[red]Rezerv 0 ile depo kapasitesi arasında olmalı.[/red]")

    return {
        "depo": depo,
        "kapasite": kapasite,
        "tuketim": tuketim,
        "yol": tek_yon * 2 if gidis_donus else tek_yon,
        "tek_yon": tek_yon,
        "gidis_donus": gidis_donus,
        "fiyat": fiyat,
        "rezerv": rezerv,
    }


def build_table(bilgi: dict, plan: dict) -> Table:
    """Yol, yakıt ve durakları tek tabloda toplar."""
    tablo = Table(
        title="Yol Planı",
        header_style="bold blue",
        border_style="blue",
    )
    tablo.add_column("Kalem", style="white")
    tablo.add_column("Değer", justify="right", style="cyan")

    if bilgi["gidis_donus"]:
        tablo.add_row("Gidiş", miktar(bilgi["tek_yon"], "km"))
        tablo.add_row("Gidiş-dönüş", miktar(bilgi["yol"], "km"))
    else:
        tablo.add_row("Yol", miktar(bilgi["yol"], "km"))

    tablo.add_row("Tüketim", f"{miktar(bilgi['tuketim'], 'L')} / 100 km")
    tablo.add_row("Depo", miktar(bilgi["depo"], "L"))
    tablo.add_row("Gereken yakıt", miktar(plan["gerekli"], "L"))
    tablo.add_row("Yolun yakıt parası", tl(plan["maliyet"]))

    if not plan["alimlar"]:
        tablo.add_row("Alınacak yakıt", "yok")
    else:
        for konum, litre in plan["alimlar"]:
            tutar = litre * bilgi["fiyat"]
            if konum <= EPS:
                yer = "Yola çıkmadan"
            else:
                yer = f"{miktar(konum, 'km')} sonra"
            tablo.add_row(yer, f"{miktar(litre, 'L')} ({tl(tutar)})")

    tablo.add_row("Varışta depo", miktar(plan["varis"], "L"))
    return tablo


def show_result(bilgi: dict) -> None:
    """Plan tablosunu ve kısa kararı basar."""
    try:
        plan = planla(
            bilgi["depo"],
            bilgi["kapasite"],
            bilgi["tuketim"],
            bilgi["yol"],
            bilgi["fiyat"],
            bilgi["rezerv"],
        )
    except ValueError as exc:
        console.print()
        console.print(Panel(f"[red]{exc}[/red]", border_style="red"))
        console.print()
        return

    console.print()
    console.print(build_table(bilgi, plan))
    console.print()

    if not plan["alimlar"]:
        karar = (
            "[bold green]Yola çıkmadan yakıt almana gerek yok.[/bold green]\n"
            f"Varışta depoda {miktar(plan['varis'], 'L')} kalır."
        )
    elif len(plan["alimlar"]) == 1 and plan["alimlar"][0][0] <= EPS:
        litre, = (plan["alimlar"][0][1],)
        karar = (
            f"[bold green]Yola çıkmadan {miktar(litre, 'L')} al.[/bold green]\n"
            "Yolda durmana gerek yok."
        )
    else:
        durak = sum(1 for konum, _ in plan["alimlar"] if konum > EPS)
        karar = (
            f"[bold yellow]Yolda {durak} kez durman gerekiyor.[/bold yellow]\n"
            "Yola çıkmadan alınan yakıt yol boyu yetmiyor. "
            "Rezerv düşünce tablodaki kilometrede yeniden alıyorsun."
        )

    console.print(Panel(karar, border_style="green"))
    console.print()


def main() -> None:
    while True:
        show_welcome()
        show_result(sorular())
        if not EvetHayir.ask("Başka bir yol bakalım mı?"):
            console.print("[dim]Görüşürüz![/dim]")
            break


if __name__ == "__main__":
    main()
