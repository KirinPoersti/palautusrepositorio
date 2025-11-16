class PlayerStats:
    def __init__(self, player_reader):
        self.reader = player_reader
        self._players_cache = None
    
    def get_all_players(self):
        """Get all players with caching"""
        if self._players_cache is None:
            self._players_cache = self.reader.get_players()
        return self._players_cache
    
    def top_scorers_by_nationality(self, nationality):
        """Return players of given nationality sorted by points in descending order"""
        players = self.get_all_players()
        
        # Filter players by nationality
        filtered_players = [player for player in players if player.nationality == nationality]
        
        # Sort by points in descending order
        filtered_players.sort(key=lambda player: player.points, reverse=True)
        
        return filtered_players
    
    def get_available_nationalities(self):
        """Get all available nationalities with player counts"""
        players = self.get_all_players()
        nationalities = {}
        
        for player in players:
            nat = player.nationality
            if nat in nationalities:
                nationalities[nat] += 1
            else:
                nationalities[nat] = 1
        
        # Return sorted by nationality code
        return sorted(nationalities.items())
    
    def get_team_stats(self, nationality):
        """Get team statistics for a nationality"""
        players = self.top_scorers_by_nationality(nationality)
        
        if not players:
            return None
        
        total_goals = sum(p.goals for p in players)
        total_assists = sum(p.assists for p in players)
        total_points = sum(p.points for p in players)
        total_games = sum(p.games for p in players)
        
        return {
            'player_count': len(players),
            'total_goals': total_goals,
            'total_assists': total_assists,
            'total_points': total_points,
            'total_games': total_games,
            'top_scorer': players[0] if players else None
        }