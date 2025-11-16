from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.columns import Columns
from rich.layout import Layout
from rich import box
from player_reader import PlayerReader
from player_stats import PlayerStats
import requests


class NHLApp:
    def __init__(self):
        self.console = Console()
        self.current_season = "2024-25"
        self.reader = None
        self.stats = None
        
    def show_header(self):
        """Display application header"""
        title = Text("🏒 NHL Player Statistics Browser", style="bold blue")
        subtitle = Text(f"Season: {self.current_season}", style="italic")
        
        header = Panel(
            Text.assemble(title, "\n", subtitle),
            box=box.ROUNDED,
            style="blue"
        )
        self.console.print(header)
        self.console.print()
    
    def load_season_data(self, season):
        """Load data for a specific season"""
        try:
            self.console.print(f"🔄 Loading data for season {season}...", style="yellow")
            
            self.reader = PlayerReader.create_for_season(season)
            self.stats = PlayerStats(self.reader)
            
            # Test if data is available by trying to get players
            players = self.stats.get_all_players()
            
            self.current_season = season
            self.console.print(f"✅ Successfully loaded {len(players)} players!", style="green")
            return True
            
        except requests.exceptions.RequestException:
            self.console.print(f"❌ Error: Unable to load data for season {season}", style="red")
            self.console.print("Please check if the season format is correct (e.g., '2024-25', '2023-24')", style="red")
            return False
        except Exception as e:
            self.console.print(f"❌ Unexpected error: {str(e)}", style="red")
            return False
    
    def show_nationalities_menu(self):
        """Display available nationalities in a nice format"""
        nationalities = self.stats.get_available_nationalities()
        
        # Create columns for better display
        nationality_items = []
        for i, (nat, count) in enumerate(nationalities):
            if count >= 5:  # Show only countries with 5+ players
                nationality_items.append(f"[cyan]{nat}[/cyan] ({count} players)")
        
        # Split into columns
        columns = Columns(nationality_items, equal=True, expand=True)
        
        panel = Panel(
            columns,
            title="🌍 Available Nationalities (5+ players)",
            box=box.ROUNDED
        )
        self.console.print(panel)
        self.console.print()
    
    def display_players_table(self, players, nationality):
        """Display players in a beautiful Rich table"""
        if not players:
            self.console.print(f"❌ No players found for nationality '{nationality}'", style="red")
            return
        
        # Create table
        table = Table(
            title=f"🏒 Players from {nationality} - Season {self.current_season}",
            box=box.ROUNDED,
            header_style="bold magenta"
        )
        
        table.add_column("Rank", style="dim", width=4)
        table.add_column("Player Name", style="bold cyan", min_width=20)
        table.add_column("Team", style="yellow", width=15)
        table.add_column("Goals", justify="right", style="red")
        table.add_column("Assists", justify="right", style="green")
        table.add_column("Points", justify="right", style="bold blue")
        table.add_column("Games", justify="right", style="dim")
        
        # Add rows
        for i, player in enumerate(players[:25], 1):  # Show top 25
            # Color coding for top players
            if i <= 3:
                rank_style = "bold gold1"
            elif i <= 10:
                rank_style = "bold"
            else:
                rank_style = "dim"
                
            table.add_row(
                str(i),
                player.name,
                player.team,
                str(player.goals),
                str(player.assists),
                str(player.points),
                str(player.games),
                style=rank_style if i <= 3 else None
            )
        
        self.console.print(table)
        
        if len(players) > 25:
            self.console.print(f"\n[dim]... and {len(players) - 25} more players[/dim]")
    
    def show_team_summary(self, nationality):
        """Show team statistics summary"""
        team_stats = self.stats.get_team_stats(nationality)
        
        if not team_stats:
            return
        
        # Create summary table
        summary_table = Table(
            title=f"📊 Team {nationality} Statistics",
            box=box.SIMPLE,
            show_header=False
        )
        summary_table.add_column("Metric", style="bold")
        summary_table.add_column("Value", style="cyan")
        
        summary_table.add_row("Total Players", str(team_stats['player_count']))
        summary_table.add_row("Total Goals", str(team_stats['total_goals']))
        summary_table.add_row("Total Assists", str(team_stats['total_assists']))
        summary_table.add_row("Total Points", str(team_stats['total_points']))
        summary_table.add_row("Total Games", str(team_stats['total_games']))
        
        if team_stats['top_scorer']:
            top_scorer = team_stats['top_scorer']
            summary_table.add_row("Top Scorer", f"{top_scorer.name} ({top_scorer.points} pts)")
        
        panel = Panel(summary_table, box=box.ROUNDED)
        self.console.print(panel)
    
    def run(self):
        """Main application loop"""
        self.console.clear()
        self.show_header()
        
        # Load initial data
        if not self.load_season_data(self.current_season):
            return
        
        while True:
            self.console.print("\n" + "="*60)
            self.console.print("[bold]Main Menu[/bold]")
            self.console.print("1. 📊 View players by nationality")
            self.console.print("2. 🔄 Change season")
            self.console.print("3. 🌍 Show all available nationalities")
            self.console.print("4. ❌ Exit")
            
            choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4"], default="1")
            
            if choice == "1":
                self.show_players_menu()
            elif choice == "2":
                self.change_season_menu()
            elif choice == "3":
                self.show_nationalities_menu()
            elif choice == "4":
                self.console.print("👋 Goodbye!", style="green")
                break
    
    def show_players_menu(self):
        """Show players for a selected nationality"""
        self.console.print()
        nationality = Prompt.ask(
            "[bold]Enter nationality code[/bold] (e.g., FIN, SWE, USA, CAN)",
            default="FIN"
        ).upper()
        
        players = self.stats.top_scorers_by_nationality(nationality)
        
        self.console.print()
        self.display_players_table(players, nationality)
        self.show_team_summary(nationality)
        
        if players:
            if Confirm.ask("\nWould you like to see another nationality?", default=True):
                self.show_players_menu()
    
    def change_season_menu(self):
        """Change the current season"""
        self.console.print()
        self.console.print("[bold]Available seasons:[/bold] 2024-25, 2023-24, 2022-23, 2021-22, etc.")
        
        season = Prompt.ask(
            "Enter season",
            default=self.current_season
        )
        
        if self.load_season_data(season):
            self.show_header()


def main():
    """Main entry point"""
    app = NHLApp()
    try:
        app.run()
    except KeyboardInterrupt:
        app.console.print("\n👋 Goodbye!", style="green")
    except Exception as e:
        app.console.print(f"\n❌ An error occurred: {str(e)}", style="red")


if __name__ == "__main__":
    main()