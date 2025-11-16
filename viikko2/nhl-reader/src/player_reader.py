import requests
from player import Player


class PlayerReader:
    def __init__(self, url):
        self.url = url
    
    @classmethod
    def create_for_season(cls, season):
        """Create PlayerReader for a specific season (e.g., '2024-25', '2023-24')"""
        url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
        return cls(url)
    
    def get_players(self):
        """Fetch players from the URL and return a list of Player objects"""
        response = requests.get(self.url).json()
        
        players = []
        for player_dict in response:
            player = Player(player_dict)
            players.append(player)
        
        return players