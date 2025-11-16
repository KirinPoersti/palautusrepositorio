# NHL Player Statistics Browser 🏒

A Python application for browsing NHL player statistics with beautiful Rich formatting.

## Features

- 📊 View players by nationality sorted by points
- 🔄 Browse different NHL seasons (2024-25, 2023-24, etc.)
- 🌍 Interactive nationality selection
- 📈 Team statistics and summaries
- 🎨 Beautiful Rich formatting with tables and colors

## Usage

### Basic Usage (Original Interface)
```bash
cd src
python index.py
```
Shows Finnish players for 2024-25 season in a formatted table.

### Interactive Application
```bash
cd src
python nhl_app.py
```
Launches an interactive menu where you can:
- Select any nationality
- Change seasons
- View detailed statistics
- Browse available nationalities

### Programmatic Usage
```python
from player_reader import PlayerReader
from player_stats import PlayerStats

# Load specific season
reader = PlayerReader.create_for_season("2023-24")
stats = PlayerStats(reader)

# Get players by nationality
finnish_players = stats.top_scorers_by_nationality("FIN")
swedish_players = stats.top_scorers_by_nationality("SWE")

# Get team statistics
team_stats = stats.get_team_stats("FIN")
```

## Available Seasons
- 2024-25 (current)
- 2023-24
- 2022-23
- 2021-22
- And more...

## Dependencies
- requests>=2.31.0
- rich>=13.0.0

## Classes

### PlayerReader
Handles fetching JSON data from NHL API and converting to Player objects.

### PlayerStats  
Provides statistical analysis and filtering of player data.

### Player
Represents individual player with stats (goals, assists, points, team, etc.)