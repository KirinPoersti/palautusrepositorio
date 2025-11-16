from rich.console import Console
from rich.table import Table
from rich import box
from player_reader import PlayerReader
from player_stats import PlayerStats

def main():
    console = Console()
    
    # Original functionality with Rich formatting
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    players = stats.top_scorers_by_nationality("FIN")

    # Create a simple Rich table
    table = Table(
        title="🇫🇮 Finnish Players - 2024-25 Season",
        box=box.SIMPLE_HEAD,
        show_header=True,
        header_style="bold blue"
    )
    
    table.add_column("Player", style="cyan", min_width=20)
    table.add_column("Team", style="yellow", width=15)
    table.add_column("Points", justify="right", style="bold green")
    
    for player in players:
        table.add_row(
            player.name,
            player.team,
            f"{player.goals} + {player.assists} = {player.points}"
        )
    
    console.print(table)

if __name__ == "__main__":
    main()
