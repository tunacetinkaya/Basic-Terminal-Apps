"""
Banka uygulaması (v2)

Bakiye sorgulama, para yatırma, para çekme ve hesap hareketleri.
Bakiye ve hareketler hesap.json dosyasında tutulur.
Program kapanıp yeniden açılsa da kayıtlar durur.
"""

import json
import os
import select
import sys
import termios
import tty
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()

DOSYA = Path(__file__).with_name("hesap.json")
BASLANGIC_BAKIYE = 10_000
MENU = [
    "Bakiye sorgula",
    "Para yatır",
    "Para çek",
    "Hesap hareketleri",
    "Çıkış",
]
YUKARI = {"\x1b[A", "\x1bOA"}
ASAGI = {"\x1b[B", "\x1bOB"}


def tl(tutar: int) -> str:
    """Tutarı 10.000 TL biçiminde döndürür."""
    return f"{tutar:,} TL".replace(",", ".")


def load_account() -> dict:
    """Hesabı JSON dosyasından okur. Dosya yoksa başlangıç hesabını yazar."""
    if not DOSYA.exists():
        hesap = {"bakiye": BASLANGIC_BAKIYE, "hareketler": []}
        save_account(hesap)
        return hesap

    with DOSYA.open(encoding="utf-8") as dosya:
        return json.load(dosya)


def save_account(hesap: dict) -> None:
    """Hesabı JSON dosyasına yazar."""
    with DOSYA.open("w", encoding="utf-8") as dosya:
        json.dump(hesap, dosya, ensure_ascii=False, indent=2)
        dosya.write("\n")


def record(hesap: dict, tur: str, tutar: int) -> None:
    """Bakiyeyi günceller, hareketi listeye ekler ve dosyaya kaydeder."""
    if tur == "cekme":
        hesap["bakiye"] -= tutar
    else:
        hesap["bakiye"] += tutar

    hesap["hareketler"].append(
        {
            "tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "tur": tur,
            "tutar": tutar,
            "bakiye": hesap["bakiye"],
        }
    )
    save_account(hesap)


def show_welcome() -> None:
    """Başlığı gösterir."""
    console.print()
    console.print(
        Panel(
            Text("Banka", justify="center", style="bold cyan"),
            subtitle="Bakiye, yatırma, çekme, hesap hareketleri",
            border_style="cyan",
        )
    )
    console.print()


def read_byte(fd: int) -> str:
    """Terminalden tek bayt okur. sys.stdin tamponunu kullanmaz."""
    veri = os.read(fd, 1)
    if not veri:
        raise EOFError
    return veri.decode("utf-8")


def read_escape_tail(fd: int) -> str:
    """ESC'ten hemen sonra gelen diziyi okur. Yoksa boş döner."""
    if not select.select([fd], [], [], 0.05)[0]:
        return ""
    return os.read(fd, 2).decode("utf-8", "replace")


def read_key() -> str:
    """Tek bir tuş okur. Ok tuşları kaçış dizisi olarak döner."""
    fd = sys.stdin.fileno()
    ayar = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd, termios.TCSADRAIN)
        tus = read_byte(fd)
        if tus == "\x1b":
            tus += read_escape_tail(fd)
        return tus
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, ayar)


def show_menu(secili: int) -> None:
    """Seçili satırı vurgulanmış menüyü gösterir."""
    menu = Table(border_style="magenta", show_header=False, padding=(0, 1))
    menu.add_column(width=2, justify="center")
    menu.add_column()

    for sira, etiket in enumerate(MENU):
        if sira == secili:
            menu.add_row("▸", etiket, style="bold black on cyan")
        else:
            menu.add_row(" ", etiket)

    console.print(menu)
    console.print("[dim]↑ ↓ ile gez, Enter ile seç[/dim]")
    console.print()


def read_amount(etiket: str) -> int | None:
    """0'dan büyük bir tutar okur. Esc basılırsa None döner."""
    while True:
        console.print("[dim]Esc ile vazgeç[/dim]")
        console.print(f"{etiket}: ", end="")
        yazilan = ""
        vazgecti = False

        fd = sys.stdin.fileno()
        ayar = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd, termios.TCSADRAIN)
            while True:
                tus = read_byte(fd)
                if tus == "\x1b":
                    if read_escape_tail(fd):
                        continue
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    vazgecti = True
                    break
                if tus in ("\r", "\n"):
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    break
                if tus in ("\x7f", "\b"):
                    if yazilan:
                        yazilan = yazilan[:-1]
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                    continue
                if tus.isdigit():
                    yazilan += tus
                    sys.stdout.write(tus)
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, ayar)

        if vazgecti:
            return None
        if yazilan and int(yazilan) > 0:
            return int(yazilan)
        console.print("[red]Tutar 0'dan büyük olmalı.[/red]")


def build_history_table(hareketler: list[dict]) -> Table:
    """Hesap hareketlerini tablo olarak döndürür."""
    tablo = Table(
        title="Hesap Hareketleri",
        header_style="bold magenta",
        border_style="magenta",
    )
    tablo.add_column("#", justify="right", style="dim")
    tablo.add_column("Tarih", style="dim")
    tablo.add_column("İşlem")
    tablo.add_column("Tutar", justify="right")
    tablo.add_column("Bakiye", justify="right", style="cyan")

    for sira, hareket in enumerate(hareketler, start=1):
        if hareket["tur"] == "yatirma":
            islem = "[green]Yatırma[/green]"
            tutar = f"[green]+{tl(hareket['tutar'])}[/green]"
        else:
            islem = "[red]Çekme[/red]"
            tutar = f"[red]-{tl(hareket['tutar'])}[/red]"

        tablo.add_row(
            str(sira),
            hareket["tarih"],
            islem,
            tutar,
            tl(hareket["bakiye"]),
        )

    return tablo


def draw_screen(
    secili: int,
    mesaj: str | None = None,
    hata: str | None = None,
    tablo: Table | None = None,
) -> None:
    """Ekranı temizler, menüyü ve son işlemin sonucunu çizer."""
    console.clear()
    show_welcome()
    show_menu(secili)
    if hata:
        console.print(Panel(hata, border_style="red"))
        console.print()
    if mesaj:
        console.print(Panel(mesaj, border_style="green"))
        console.print()
    if tablo is not None:
        console.print(tablo)
        console.print()


def choose(secili: int, mesaj: str | None, hata: str | None, tablo: Table | None) -> int:
    """Ok tuşlarıyla menüde gezip Enter ile bir satır seçtirir."""
    while True:
        draw_screen(secili, mesaj, hata, tablo)
        tus = read_key()
        if tus in YUKARI:
            secili = (secili - 1) % len(MENU)
        elif tus in ASAGI:
            secili = (secili + 1) % len(MENU)
        elif tus in ("\r", "\n"):
            return secili


def main() -> None:
    hesap = load_account()
    mesaj = None
    hata = None
    tablo = None
    secili = 0

    while True:
        secili = choose(secili, mesaj, hata, tablo)
        mesaj = None
        hata = None
        tablo = None

        if secili == 0:
            mesaj = f"Güncel bakiye: [bold cyan]{tl(hesap['bakiye'])}[/bold cyan]"
        elif secili == 1:
            tutar = read_amount("[bold]Yatırılacak tutar[/bold]")
            if tutar is None:
                mesaj = "[dim]Yatırma iptal edildi.[/dim]"
            else:
                record(hesap, "yatirma", tutar)
                mesaj = (
                    f"[green]{tl(tutar)} yatırıldı.[/green]\n"
                    f"Yeni bakiye: [bold]{tl(hesap['bakiye'])}[/bold]"
                )
        elif secili == 2:
            tutar = read_amount("[bold]Çekilecek tutar[/bold]")
            if tutar is None:
                mesaj = "[dim]Çekme iptal edildi.[/dim]"
            elif tutar > hesap["bakiye"]:
                hata = "[red]Yetersiz bakiye.[/red]"
            else:
                record(hesap, "cekme", tutar)
                mesaj = (
                    f"[yellow]{tl(tutar)} çekildi.[/yellow]\n"
                    f"Yeni bakiye: [bold]{tl(hesap['bakiye'])}[/bold]"
                )
        elif secili == 3:
            if len(hesap["hareketler"]) == 0:
                mesaj = "[dim]Henüz işlem yok.[/dim]"
            else:
                tablo = build_history_table(hesap["hareketler"])
        else:
            console.print("[dim]Görüşürüz![/dim]")
            break


if __name__ == "__main__":
    main()
