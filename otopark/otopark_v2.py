"""
Otopark ücreti (v2)

Giriş ve çıkış saatinden süreyi, ücretlendirilen saati ve tutarı çıkarır.
Çıkış girişten küçükse süre ertesi güne sayılır.
Tarife listeden okunur; tavan, hesabın üstüne sonradan uygulanır.
"""

import math

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.text import Text

console = Console()

TOLERANS_DAKIKA = 15
ILK_SAAT = 50
SONRAKI_SAAT = 30
GUNLUK_TAVAN = 250
GUN_DAKIKA = 24 * 60


class EvetHayir(Confirm):
    """Tekrar hesap sormasını e / h ile yapar."""

    validate_error_message = "[red]Lütfen e veya h yaz.[/red]"
    choices = ["e", "h"]


def parse_saat(yazi: str) -> int:
    """'14:30' yazısını gece yarısından itibaren dakikaya çevirir."""
    parcalar = yazi.strip().split(":")
    if len(parcalar) != 2 or not all(parca.isdigit() for parca in parcalar):
        raise ValueError("Saati 14:30 biçiminde yaz.")

    saat, dakika = (int(parca) for parca in parcalar)
    if not (0 <= saat <= 23 and 0 <= dakika <= 59):
        raise ValueError("Saat 00:00 ile 23:59 arasında olmalı.")
    return saat * 60 + dakika


def sure_dakika(giris: int, cikis: int) -> tuple[int, bool]:
    """Park süresini dakika olarak döndürür.

    Çıkış, girişle aynı ya da daha küçükse araç ertesi güne kalmış sayılır.
    """
    if cikis <= giris:
        return cikis + GUN_DAKIKA - giris, True
    return cikis - giris, False


def ucretlendirilen_saat(dakika: int) -> int:
    """Toleransın üstündeki süreyi, başlayan saati de sayarak yukarı yuvarlar."""
    if dakika <= TOLERANS_DAKIKA:
        return 0
    return math.ceil(dakika / 60)


def ucret_hesapla(saat: int) -> tuple[int, int]:
    """Ücretlendirilen saatten ara toplamı ve tavanlı tutarı döndürür."""
    if saat <= 0:
        return 0, 0
    ara_toplam = ILK_SAAT + (saat - 1) * SONRAKI_SAAT
    return ara_toplam, min(ara_toplam, GUNLUK_TAVAN)


def sure_yaz(dakika: int) -> str:
    """Dakikayı '3 saat 40 dakika' biçiminde döndürür."""
    saat, kalan = divmod(dakika, 60)
    if saat == 0:
        return f"{kalan} dakika"
    if kalan == 0:
        return f"{saat} saat"
    return f"{saat} saat {kalan} dakika"


def tl(tutar: int) -> str:
    """Tutarı 1.250 TL biçiminde döndürür."""
    return f"{tutar:,} TL".replace(",", ".")


def build_tarife_table() -> Table:
    """Otopark tarifesini tablo olarak döndürür."""
    tablo = Table(
        title="Tarife",
        header_style="bold magenta",
        border_style="magenta",
    )
    tablo.add_column("Kural", style="yellow")
    tablo.add_column("Ücret", justify="right", style="green")
    tablo.add_row(f"≤ {TOLERANS_DAKIKA} dk", "ücretsiz")
    tablo.add_row("İlk saat", tl(ILK_SAAT))
    tablo.add_row("Sonraki her saat", tl(SONRAKI_SAAT))
    tablo.add_row("Günlük tavan", tl(GUNLUK_TAVAN))
    return tablo


def show_welcome() -> None:
    """Başlığı ve tarife tablosunu gösterir."""
    console.print()
    console.print(
        Panel(
            Text("Otopark Ücreti", justify="center", style="bold cyan"),
            subtitle="Giriş ve çıkış saatinden tutar",
            border_style="cyan",
        )
    )
    console.print()
    console.print(
        "Başlayan saat yukarı yuvarlanır. "
        "Çıkış, girişten erken görünüyorsa süre [cyan]ertesi güne[/cyan] sayılır."
    )
    console.print()
    console.print(build_tarife_table())
    console.print()


def saat_iste(etiket: str) -> int:
    """Geçerli bir saat yazılana kadar sorar."""
    while True:
        try:
            return parse_saat(Prompt.ask(etiket))
        except ValueError as exc:
            console.print(f"[red]{exc}[/red]")


def show_result(giris: int, cikis: int) -> None:
    """Süre dökümünü ve ödenecek tutarı tablo olarak basar."""
    dakika, ertesi_gun = sure_dakika(giris, cikis)
    saat = ucretlendirilen_saat(dakika)
    ara_toplam, tutar = ucret_hesapla(saat)

    ozet = Table(
        title="Hesap Özeti",
        header_style="bold blue",
        border_style="blue",
    )
    ozet.add_column("Kalem", style="white")
    ozet.add_column("Detay", style="dim")
    ozet.add_column("Tutar", justify="right", style="green")

    gun_notu = "ertesi güne sarktı" if ertesi_gun else "aynı gün"
    ozet.add_row("Süre", f"{sure_yaz(dakika)} ({gun_notu})", "")

    if saat == 0:
        ozet.add_row("Tolerans", f"{TOLERANS_DAKIKA} dk ve altı", tl(0))
    else:
        ozet.add_row("İlk saat", "sabit", tl(ILK_SAAT))
        if saat > 1:
            ozet.add_row(
                "Sonraki saatler",
                f"{saat - 1} × {tl(SONRAKI_SAAT)}",
                tl((saat - 1) * SONRAKI_SAAT),
            )
        if ara_toplam > GUNLUK_TAVAN:
            ozet.add_row("Ara toplam", f"{saat} saat", tl(ara_toplam))
            ozet.add_row("Günlük tavan", "uygulandı", f"-{tl(ara_toplam - tutar)}")

    ozet.add_row("[bold]Toplam[/bold]", "", f"[bold cyan]{tl(tutar)}[/bold cyan]")

    console.print()
    console.print(ozet)
    console.print()
    console.print(
        Panel(
            f"[bold green]Ödenecek tutar: {tl(tutar)}[/bold green]",
            border_style="green",
        )
    )
    console.print()


def main() -> None:
    while True:
        show_welcome()
        giris = saat_iste("[bold]Giriş saati[/bold]")
        cikis = saat_iste("[bold]Çıkış saati[/bold]")
        show_result(giris, cikis)
        if not EvetHayir.ask("Başka bir süre hesaplansın mı?"):
            console.print("[dim]Görüşürüz![/dim]")
            break


if __name__ == "__main__":
    main()
