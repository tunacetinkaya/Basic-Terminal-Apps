"""
Sınav kurtarma (v2)

Vize, ödev, kısa sınav gibi birden fazla notu ağırlığıyla toplar.
Kalan yüzde, henüz girilmemiş sınavın payıdır.
O sınavdan geçmek için gereken tam sayıyı yukarı yuvarlayarak söyler.
"""

import math

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table
from rich.text import Text

console = Console()


class EvetHayir(Confirm):
    """Tekrar hesap sormasını e / h ile yapar."""

    validate_error_message = "[red]Lütfen e veya h yaz.[/red]"
    choices = ["e", "h"]


def katki(puan: int, agirlik: int) -> float:
    """Bir notun ortalamaya eklediği puanı döndürür."""
    return puan * agirlik / 100


def gerekli_puan(gecme: int, toplanan: float, kalan_agirlik: int) -> float:
    """Kalan sınavdan, geçme notuna ulaşmak için gereken puanı döndürür."""
    return (gecme - toplanan) * 100 / kalan_agirlik


def yukari_yuvarla(puan: float) -> int:
    """0 ile 100 arasında, üste yuvarlanmış tam not döndürür."""
    if puan <= 0:
        return 0
    return min(100, math.ceil(puan - 1e-9))


def virgul(deger: float) -> str:
    """Ondalığı Türkçe yazıma çevirir. 56.67 → 56,67"""
    yazi = f"{deger:.2f}".rstrip("0").rstrip(".")
    return yazi.replace(".", ",")


def show_welcome() -> None:
    """Başlığı gösterir."""
    console.print()
    console.print(
        Panel(
            Text("Sınav Kurtarma", justify="center", style="bold cyan"),
            subtitle="Kalan sınavdan kaç almalısın",
            border_style="cyan",
        )
    )
    console.print()
    console.print(
        "Elinde olan notları tek tek yaz. Ad sorulunca boş Enter'a basınca "
        "kalan yüzde, henüz girilmemiş sınava ayrılır."
    )
    console.print()


def aralik_iste(etiket: str, alt: int, ust: int) -> int:
    """Alt ve üst sınırın içinde bir tam sayı okur."""
    while True:
        deger = IntPrompt.ask(etiket)
        if alt <= deger <= ust:
            return deger
        console.print(f"[red]{alt} ile {ust} arasında olmalı.[/red]")


def notlari_al() -> list[dict]:
    """Ağırlık toplamı 100'ü geçmeyecek şekilde girilmiş notları toplar."""
    notlar = []
    agirlik_toplam = 0

    while agirlik_toplam < 100:
        ad = Prompt.ask("[bold]Not adı[/bold]", default="", show_default=False).strip()
        if ad == "":
            break
        if any(not_kaydi["ad"] == ad for not_kaydi in notlar):
            console.print("[red]Bu not zaten var.[/red]")
            continue

        puan = aralik_iste("[bold]Not[/bold]", 0, 100)
        kalan = 100 - agirlik_toplam
        agirlik = aralik_iste(f"[bold]Ağırlık %[/bold] (en fazla {kalan})", 1, kalan)
        notlar.append({"ad": ad, "puan": puan, "agirlik": agirlik})
        agirlik_toplam += agirlik
        console.print(f"[dim]Kalan ağırlık: %{100 - agirlik_toplam}[/dim]")

    return notlar


def build_table(notlar: list[dict], kalan_ad: str | None, kalan_agirlik: int) -> Table:
    """Her notun ortalamaya katkısını tablo olarak döndürür."""
    tablo = Table(
        title="Notlar",
        header_style="bold magenta",
        border_style="magenta",
    )
    tablo.add_column("Bileşen", style="white")
    tablo.add_column("Not", justify="right", style="yellow")
    tablo.add_column("Ağırlık", justify="right")
    tablo.add_column("Katkı", justify="right", style="cyan")

    for kayit in notlar:
        tablo.add_row(
            kayit["ad"],
            str(kayit["puan"]),
            f"%{kayit['agirlik']}",
            virgul(katki(kayit["puan"], kayit["agirlik"])),
        )

    if kalan_ad is not None:
        tablo.add_row(kalan_ad, "?", f"%{kalan_agirlik}", "—")
    return tablo


def show_result(gecme: int, notlar: list[dict]) -> None:
    """Geçmek için kalan sınavdan gereken notu ya da sonucu gösterir."""
    toplanan = sum(katki(kayit["puan"], kayit["agirlik"]) for kayit in notlar)
    kullanilan = sum(kayit["agirlik"] for kayit in notlar)
    kalan_agirlik = 100 - kullanilan

    kalan_ad = None
    if kalan_agirlik > 0:
        kalan_ad = Prompt.ask(
            f"[bold]Kalan %{kalan_agirlik} hangi sınav?[/bold]",
            default="Final",
        ).strip() or "Final"

    console.print()
    console.print(build_table(notlar, kalan_ad, kalan_agirlik))
    console.print()

    if kalan_agirlik == 0:
        if toplanan + 1e-9 >= gecme:
            metin = (
                f"[bold green]Ortalaman {virgul(toplanan)}. "
                f"Geçme notu {gecme}.[/bold green]"
            )
            renk = "green"
        else:
            metin = (
                f"[bold red]Ortalaman {virgul(toplanan)}. "
                f"Geçme notu {gecme}.[/bold red]"
            )
            renk = "red"
        console.print(Panel(metin, border_style=renk))
        console.print()
        return

    ham = gerekli_puan(gecme, toplanan, kalan_agirlik)
    en_yuksek = toplanan + kalan_agirlik

    if ham <= 0:
        metin = (
            f"[bold green]{kalan_ad} notundan 0 alsan da geçiyorsun.[/bold green]\n"
            f"Şu ana kadar toplanan katkı: {virgul(toplanan)}"
        )
        renk = "green"
    elif ham > 100:
        metin = (
            f"[bold red]{kalan_ad} notundan 100 alsan da geçemiyorsun.[/bold red]\n"
            f"Ulaşabileceğin en yüksek ortalama: {virgul(en_yuksek)}"
        )
        renk = "red"
    else:
        gerekli = yukari_yuvarla(ham)
        metin = f"[bold green]{kalan_ad} notundan en az {gerekli} almalısın.[/bold green]"
        if gerekli != ham:
            metin += (
                f"\n[dim]Hesap {virgul(ham)} çıktı, "
                "not tam sayı olduğu için yukarı yuvarlandı.[/dim]"
            )
        metin += f"\n100 alırsan ortalaman {virgul(en_yuksek)} olur."
        renk = "green"

    console.print(Panel(metin, border_style=renk))
    console.print()


def main() -> None:
    while True:
        show_welcome()
        gecme = aralik_iste("[bold]Geçme notu[/bold]", 0, 100)
        notlar = notlari_al()
        if not notlar and Prompt.ask(
            "[bold]Hiç not girmedin. Kalan sınav %100 olsun mu?[/bold]",
            choices=["e", "h"],
            default="e",
        ) == "h":
            console.print("[dim]Hesap iptal.[/dim]")
        else:
            show_result(gecme, notlar)
        if not EvetHayir.ask("Başka bir ders bakalım mı?"):
            console.print("[dim]Görüşürüz![/dim]")
            break


if __name__ == "__main__":
    main()
