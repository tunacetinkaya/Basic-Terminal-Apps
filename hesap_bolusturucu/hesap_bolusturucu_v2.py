"""
Hesap bölüştürücü (v2)

Herkesin ödediğini kişi sayısına böler, artan lirayı ilk kişilere dağıtır.
Alacak ve borcu, en az sayıda ödemeyle kimden kime gideceğini bulur.
"""

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


def tl(tutar: int) -> str:
    """Tutarı 1.250 TL biçiminde döndürür."""
    return f"{tutar:,} TL".replace(",", ".")


def paylari_bol(toplam: int, adet: int) -> list[int]:
    """Toplamı kişi sayısına böler. Artan lirayı sırayla ilk kişilere verir."""
    taban = toplam // adet
    artan = toplam % adet
    return [taban + (1 if sira < artan else 0) for sira in range(adet)]


def odemeleri_eslestir(
    kisiler: list[dict], paylar: list[int]
) -> list[tuple[str, str, int]]:
    """Borçluyu alacaklıyla eşleştirip kimden kime ne kadar gideceğini döndürür.

    Her adımda iki taraftan küçük olan tutar kapanır. Böylece aynı kişi
    gereksiz yere birkaç kişiye birden bölünmez.
    """
    borclular = []
    alacaklilar = []
    for kisi, pay in zip(kisiler, paylar):
        fark = kisi["odeme"] - pay
        if fark > 0:
            alacaklilar.append([kisi["ad"], fark])
        elif fark < 0:
            borclular.append([kisi["ad"], -fark])

    odemeler = []
    borc_sira = 0
    alacak_sira = 0
    while borc_sira < len(borclular) and alacak_sira < len(alacaklilar):
        tutar = min(borclular[borc_sira][1], alacaklilar[alacak_sira][1])
        odemeler.append(
            (borclular[borc_sira][0], alacaklilar[alacak_sira][0], tutar)
        )
        borclular[borc_sira][1] -= tutar
        alacaklilar[alacak_sira][1] -= tutar
        if borclular[borc_sira][1] == 0:
            borc_sira += 1
        if alacaklilar[alacak_sira][1] == 0:
            alacak_sira += 1
    return odemeler


def show_welcome() -> None:
    """Başlığı gösterir."""
    console.print()
    console.print(
        Panel(
            Text("Hesap Bölüştürücü", justify="center", style="bold cyan"),
            subtitle="Kim ödedi, kim kime verecek",
            border_style="cyan",
        )
    )
    console.print()
    console.print(
        "Her kişi için adı ve masaya bıraktığı tutarı yaz. "
        "Bitirmek için ad sorulunca [cyan]boş Enter[/cyan] bas."
    )
    console.print()


def kisileri_al() -> list[dict]:
    """En az iki kişiyi, ad ve ödeme tekrarı olmadan toplar."""
    kisiler = []
    while True:
        ad = Prompt.ask("[bold]Ad[/bold]", default="", show_default=False).strip()
        if ad == "":
            if len(kisiler) >= 2:
                break
            console.print("[red]En az 2 kişi yaz.[/red]")
            continue
        if any(kisi["ad"] == ad for kisi in kisiler):
            console.print("[red]Bu ad zaten var.[/red]")
            continue

        while True:
            odeme = IntPrompt.ask(f"[bold]{ad} ne kadar ödedi?[/bold]")
            if odeme >= 0:
                break
            console.print("[red]Ödeme 0'dan küçük olamaz.[/red]")

        kisiler.append({"ad": ad, "odeme": odeme})
        console.print(f"[dim]{ad} eklendi. Şu ana kadar {len(kisiler)} kişi.[/dim]")
    return kisiler


def build_pay_table(kisiler: list[dict], paylar: list[int]) -> Table:
    """Ödeme, düşen pay ve alacak/borç tablosunu kurar."""
    tablo = Table(
        title="Kişiler",
        header_style="bold magenta",
        border_style="magenta",
    )
    tablo.add_column("Kişi", style="white")
    tablo.add_column("Ödedi", justify="right", style="yellow")
    tablo.add_column("Payı", justify="right")
    tablo.add_column("Durum", justify="right")

    for kisi, pay in zip(kisiler, paylar):
        fark = kisi["odeme"] - pay
        if fark > 0:
            durum = f"[green]{tl(fark)} alacak[/green]"
        elif fark < 0:
            durum = f"[red]{tl(-fark)} borç[/red]"
        else:
            durum = "[dim]eşit[/dim]"
        tablo.add_row(kisi["ad"], tl(kisi["odeme"]), tl(pay), durum)
    return tablo


def build_transfer_table(odemeler: list[tuple[str, str, int]]) -> Table:
    """Sadeleştirilmiş ödemeleri tablo olarak döndürür."""
    tablo = Table(
        title="Kim kime verecek",
        header_style="bold blue",
        border_style="blue",
    )
    tablo.add_column("Kim", style="white")
    tablo.add_column("", justify="center", style="dim")
    tablo.add_column("Kime", style="white")
    tablo.add_column("Tutar", justify="right", style="cyan")

    for kim, kime, tutar in odemeler:
        tablo.add_row(kim, "→", kime, tl(tutar))
    return tablo


def show_result(kisiler: list[dict]) -> None:
    """Toplamı, payları ve sadeleşmiş ödemeleri gösterir."""
    toplam = sum(kisi["odeme"] for kisi in kisiler)
    paylar = paylari_bol(toplam, len(kisiler))
    odemeler = odemeleri_eslestir(kisiler, paylar)
    artan = toplam % len(kisiler)

    console.print()
    console.print(f"[bold]Toplam:[/bold] [cyan]{tl(toplam)}[/cyan]")
    if artan:
        console.print(
            f"[dim]Artan {artan} TL, listedeki ilk kişilerin payına 1'er TL eklendi.[/dim]"
        )
    console.print()
    console.print(build_pay_table(kisiler, paylar))
    console.print()

    if odemeler:
        console.print(build_transfer_table(odemeler))
    else:
        console.print(
            Panel("[bold green]Herkes kendi payını ödemiş.[/bold green]", border_style="green")
        )
    console.print()


def main() -> None:
    while True:
        show_welcome()
        show_result(kisileri_al())
        if not EvetHayir.ask("Başka bir hesap bölüştürelim mi?"):
            console.print("[dim]Görüşürüz![/dim]")
            break


if __name__ == "__main__":
    main()
