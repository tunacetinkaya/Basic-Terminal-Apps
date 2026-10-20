"""
Sayı tahmin etme oyunu (v2)

Bilgisayar 1 ile 100 arasında gizli bir sayı seçer.
Her tahminden sonra sayı daha büyük mü, daha küçük mü söylenir.
"""

import random

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table
from rich.text import Text

console = Console()

ALT_SINIR = 1
UST_SINIR = 100


class EvetHayir(Confirm):
    """Tekrar oynama sorusunu e / h ile sorar."""

    validate_error_message = "[red]Lütfen e veya h yaz.[/red]"
    choices = ["e", "h"]


def show_welcome() -> None:
    """Oyunun başlığını ve kuralını gösterir."""
    console.print()
    console.print(
        Panel(
            Text("Sayı Tahmin Oyunu", justify="center", style="bold cyan"),
            subtitle=f"{ALT_SINIR} ile {UST_SINIR} arasında bir sayı",
            border_style="cyan",
        )
    )
    console.print(
        f"Bir sayı tuttum. [bold]{ALT_SINIR}[/bold] ile "
        f"[bold]{UST_SINIR}[/bold] arasında tahmin et."
    )
    console.print()


def read_guess() -> int:
    """Bir tahmin okur. Geçersizse ValueError fırlatır."""
    yazilan = console.input("[bold]Tahminin:[/bold] ").strip()
    try:
        tahmin = int(yazilan)
    except ValueError:
        raise ValueError("Lütfen bir sayı yaz.") from None

    if not ALT_SINIR <= tahmin <= UST_SINIR:
        raise ValueError(
            f"Lütfen {ALT_SINIR} ile {UST_SINIR} arasında bir sayı yaz."
        )
    return tahmin


def hint_for(tahmin: int, gizli_sayi: int) -> str:
    """Tahminin gizli sayıya göre yönünü döndürür."""
    if tahmin < gizli_sayi:
        return "Daha büyük"
    if tahmin > gizli_sayi:
        return "Daha küçük"
    return "Buldun"


def show_history(tahminler: list[tuple[int, str]]) -> None:
    """Bu turdaki tahminleri tablo olarak gösterir."""
    tablo = Table(title="Tahminlerin", header_style="bold magenta", border_style="magenta")
    tablo.add_column("#", justify="right", style="dim")
    tablo.add_column("Tahmin", justify="right", style="yellow")
    tablo.add_column("İpucu", style="white")

    for sira, (tahmin, ipucu) in enumerate(tahminler, start=1):
        tablo.add_row(str(sira), str(tahmin), ipucu)

    console.print(tablo)
    console.print()


def show_hint(ipucu: str) -> None:
    """Tek bir tahminin sonucunu renkli yazar."""
    if ipucu == "Daha büyük":
        console.print("[yellow]Daha büyük bir sayı dene.[/yellow]")
    else:
        console.print("[blue]Daha küçük bir sayı dene.[/blue]")
    console.print()


def draw_screen(
    tahminler: list[tuple[int, str]],
    ipucu: str | None = None,
    hata: str | None = None,
    gizli_sayi: int | None = None,
) -> None:
    """Ekranı temizler ve oyunu baştan çizer."""
    console.clear()
    show_welcome()

    if gizli_sayi is not None:
        console.print(
            Panel(
                f"[bold green]Tebrikler![/bold green]\n"
                f"Sayı [bold]{gizli_sayi}[/bold] idi. "
                f"[cyan]{len(tahminler)}[/cyan] denemede buldun.",
                border_style="green",
            )
        )
        console.print()

    if ipucu:
        show_hint(ipucu)
    if tahminler:
        show_history(tahminler)
    if hata:
        console.print(f"[red]{hata}[/red]")


def play_round() -> None:
    """Tek bir oyunu, sayı bulunana kadar oynatır."""
    gizli_sayi = random.randint(ALT_SINIR, UST_SINIR)
    tahminler: list[tuple[int, str]] = []
    ipucu = None
    hata = None

    while True:
        draw_screen(tahminler, ipucu, hata)
        try:
            tahmin = read_guess()
        except ValueError as exc:
            hata = str(exc)
            continue

        hata = None
        ipucu = hint_for(tahmin, gizli_sayi)
        tahminler.append((tahmin, ipucu))

        if tahmin == gizli_sayi:
            draw_screen(tahminler, gizli_sayi=gizli_sayi)
            break


def main() -> None:
    while True:
        play_round()
        if not EvetHayir.ask("Tekrar oynamak ister misin?"):
            console.print("[dim]Görüşürüz![/dim]")
            break


if __name__ == "__main__":
    main()
