import argparse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .client import get_weather

console = Console()


def main():
    parser = argparse.ArgumentParser(
        description="Live Weather Information"
    )
    parser.add_argument(
        "city",
        nargs="?",
        help="City name to check"
    )

    args = parser.parse_args()

    city = args.city or console.input(
        "[bold cyan]Enter city name: [/bold cyan]"
    )

    try:
        data = get_weather(city)

        location = data["location"]
        current = data["current"]

        table = Table(title="Current Weather Report")
        table.add_column("Information", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("City", location["name"])
        table.add_row("Country", location["country"])
        table.add_row("Temperature", f"{current['temp_c']} °C")
        table.add_row("Condition", current["condition"]["text"])
        table.add_row("Humidity", f"{current['humidity']}%")
        table.add_row("Wind Speed", f"{current['wind_kph']} km/h")

        console.print(Panel(table, title="Weather App", border_style="blue"))

    except (ValueError, RuntimeError) as error:
        console.print(f"[bold red]Error:[/bold red] {error}")


if __name__ == "__main__":
    main()