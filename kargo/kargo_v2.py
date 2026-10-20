"""
Kargo ücreti hesaplayıcı

Paket ağırlığına ve mesafeye göre toplam kargo ücretini hesaplar.
Sabit taban ücret üzerine ağırlık ve mesafe ücretleri eklenir.
"""

from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.prompt import FloatPrompt
from rich.table import Table
from rich.text import Text

console = Console()

BASE_PRICE = 50


WEIGHT_PRICING = [
    (5, 10),  # 0-5 kg: 10 TL
    (10, 25),  # >5-10 kg: 25 TL
    (float("inf"), 40),  # >10 kg: 40 TL
]

DISTANCE_PRICING = [
    (100, 10),  # 0-100 km: 10 TL
    (200, 30),  # >100-200 km: 30 TL
    (float("inf"), 50),  # >200 km: 50 TL
]


def price_for(value: float, bands: list[tuple[float, float]]) -> float:
    """
    Verilen değer (ör. ağırlık veya mesafe) için uygun tarifeyi bulup, o tarifeye ait ücreti döndürür.
    """
    for limit, price in bands:
        if value <= limit:
            return price
    raise ValueError("Geçersiz değer")


def calculate_total_cost(weight: float, distance: float) -> float:
    """Ağırlık, mesafe ve taban ücreti toplayarak toplam tutarı döndürür."""
    shipping_cost = price_for(weight, WEIGHT_PRICING)
    distance_cost = price_for(distance, DISTANCE_PRICING)
    return shipping_cost + distance_cost + BASE_PRICE


def band_label(previous: float, limit: float, unit: str) -> str:
    """Tarife sınırını '≤ 5 kg' veya '> 10 kg' biçiminde döndürür."""
    if limit == float("inf"):
        return f"> {previous:g} {unit}"
    return f"≤ {limit:g} {unit}"


def build_pricing_table(
    title: str,
    bands: list[tuple[float, float]],
    unit: str,
    color: str,
) -> Table:
    """Tarife listesinden aralık tablosu kurar."""
    table = Table(
        title=title,
        show_header=True,
        header_style=f"bold {color}",
        border_style=color,
    )
    table.add_column("Aralık", style="yellow")
    table.add_column("Ücret", justify="right", style="green")

    previous = 0.0
    for limit, price in bands:
        table.add_row(band_label(previous, limit, unit), f"{price:g} TL")
        previous = limit
    return table


def build_weight_table() -> Table:
    """Ağırlık tarifesini tablo olarak döndürür."""
    return build_pricing_table("Ağırlık Tarifesi", WEIGHT_PRICING, "kg", "magenta")


def build_distance_table() -> Table:
    """Mesafe tarifesini tablo olarak döndürür."""
    return build_pricing_table("Mesafe Tarifesi", DISTANCE_PRICING, "km", "blue")


def show_welcome() -> None:
    """Başlık ve tarife bilgisini gösterir."""
    console.print()
    console.print(
        Panel(
            Text("Kargo Ücreti Hesaplayıcı", justify="center", style="bold cyan"),
            subtitle="Ağırlık + mesafe + taban ücret",
            border_style="cyan",
        )
    )
    console.print()
    console.print(
        f"[bold]Taban ücret:[/bold] Her gönderi için sabit "
        f"[cyan]{BASE_PRICE} TL[/cyan] alınır. "
        "Bunun üzerine aşağıdaki ağırlık ve mesafe ücretleri eklenir."
    )
    console.print()
    console.print(Columns([build_weight_table(), build_distance_table()], equal=True))
    console.print()


def ask_inputs() -> tuple[float, float]:
    """Kullanıcıdan ağırlık ve mesafe alır."""
    while True:
        weight = FloatPrompt.ask("[bold]Paket ağırlığı (kg)[/bold]")
        if weight > 0:
            break
        console.print("[red]Ağırlık 0'dan büyük olmalı.[/red]")

    while True:
        distance = FloatPrompt.ask("[bold]Mesafe (km)[/bold]")
        if distance > 0:
            break
        console.print("[red]Mesafe 0'dan büyük olmalı.[/red]")

    return weight, distance


def show_result(weight: float, distance: float) -> None:
    """Hesap özetini ve toplam tutarı gösterir."""
    shipping_cost = price_for(weight, WEIGHT_PRICING)
    distance_cost = price_for(distance, DISTANCE_PRICING)
    total = calculate_total_cost(weight, distance)

    summary = Table(
        title="Hesap Özeti",
        show_header=True,
        header_style="bold blue",
        border_style="blue",
    )
    summary.add_column("Kalem", style="white")
    summary.add_column("Detay", style="dim")
    summary.add_column("Tutar", justify="right", style="green")

    summary.add_row("Taban ücret", "sabit", f"{BASE_PRICE} TL")
    summary.add_row("Ağırlık ücreti", f"{weight:g} kg", f"{shipping_cost} TL")
    summary.add_row("Mesafe ücreti", f"{distance:g} km", f"{distance_cost} TL")
    summary.add_row("[bold]Toplam[/bold]", "", f"[bold cyan]{total} TL[/bold cyan]")

    console.print()
    console.print(summary)
    console.print()
    console.print(
        Panel(
            f"[bold green]Ödenecek tutar: {total} TL[/bold green]",
            border_style="green",
        )
    )
    console.print()


def main() -> None:
    show_welcome()
    weight, distance = ask_inputs()
    show_result(weight, distance)


if __name__ == "__main__":
    main()
