import unittest
from statistics_service import StatisticsService, SortBy
from player import Player


class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]


class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # give the StatisticsService class object a "stub" class object
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_search_existing_player(self):
        # Test searching for a player that exists
        player = self.stats.search("Semenko")
        self.assertIsNotNone(player)
        self.assertEqual(player.name, "Semenko")
        self.assertEqual(player.team, "EDM")

    def test_search_existing_player_partial_name(self):
        # Test searching with partial name match
        player = self.stats.search("Gret")
        self.assertIsNotNone(player)
        self.assertEqual(player.name, "Gretzky")

    def test_search_nonexistent_player(self):
        # Test searching for a player that doesn't exist
        player = self.stats.search("Nonexistent")
        self.assertIsNone(player)

    def test_search_empty_string(self):
        # Test searching with empty string (should find first player with empty string in name)
        player = self.stats.search("")
        self.assertIsNotNone(player)  # Empty string is in every string

    def test_team_existing_team_with_multiple_players(self):
        # Test getting players from a team that has multiple players
        edm_players = self.stats.team("EDM")
        self.assertEqual(len(edm_players), 3)
        
        # Verify all players are from EDM
        for player in edm_players:
            self.assertEqual(player.team, "EDM")
        
        # Verify specific players are included
        player_names = [player.name for player in edm_players]
        self.assertIn("Semenko", player_names)
        self.assertIn("Kurri", player_names)
        self.assertIn("Gretzky", player_names)

    def test_team_existing_team_with_single_player(self):
        # Test getting players from a team that has only one player
        pit_players = self.stats.team("PIT")
        self.assertEqual(len(pit_players), 1)
        self.assertEqual(pit_players[0].name, "Lemieux")
        self.assertEqual(pit_players[0].team, "PIT")

    def test_team_nonexistent_team(self):
        # Test getting players from a team that doesn't exist
        nonexistent_players = self.stats.team("XXX")
        self.assertEqual(len(nonexistent_players), 0)
        self.assertIsInstance(nonexistent_players, list)

    def test_top_players(self):
        # Test getting top players (normal case)
        top_players = self.stats.top(2)
        
        # Should return 3 players (0, 1, 2 due to <= condition)
        self.assertEqual(len(top_players), 3)
        
        # Verify they are sorted by points (descending)
        self.assertEqual(top_players[0].name, "Gretzky")  # 124 points
        self.assertEqual(top_players[1].name, "Lemieux")  # 99 points
        self.assertEqual(top_players[2].name, "Yzerman")  # 98 points

    def test_top_zero_players(self):
        # Test getting top 0 players (edge case)
        top_players = self.stats.top(0)
        
        # Should return 1 player due to <= condition (i <= 0 means i = 0)
        self.assertEqual(len(top_players), 1)
        self.assertEqual(top_players[0].name, "Gretzky")  # Highest points

    def test_top_all_players(self):
        # Test getting more players than available
        top_players = self.stats.top(4)
        
        # Should return all 5 players due to <= condition
        self.assertEqual(len(top_players), 5)
        
        # Verify order (highest to lowest points)
        expected_order = ["Gretzky", "Lemieux", "Yzerman", "Kurri", "Semenko"]
        for i, expected_name in enumerate(expected_order):
            self.assertEqual(top_players[i].name, expected_name)

    def test_top_negative_number(self):
        # Test with negative number (edge case)
        # This should return empty list since i starts at 0 and 0 <= -1 is False
        top_players = self.stats.top(-1)
        self.assertEqual(len(top_players), 0)

    # Tests for new SortBy functionality
    def test_top_sort_by_points_explicit(self):
        # Test explicit sorting by points (same as default)
        top_players = self.stats.top(2, SortBy.POINTS)
        
        # Should return 3 players due to <= condition
        self.assertEqual(len(top_players), 3)
        
        # Verify sorted by points (descending)
        self.assertEqual(top_players[0].name, "Gretzky")  # 124 points
        self.assertEqual(top_players[1].name, "Lemieux")  # 99 points
        self.assertEqual(top_players[2].name, "Yzerman")  # 98 points

    def test_top_sort_by_goals(self):
        # Test sorting by goals
        top_players = self.stats.top(2, SortBy.GOALS)
        
        # Should return 3 players due to <= condition
        self.assertEqual(len(top_players), 3)
        
        # Verify sorted by goals (descending): Lemieux(45), Yzerman(42), Kurri(37)
        self.assertEqual(top_players[0].name, "Lemieux")   # 45 goals
        self.assertEqual(top_players[1].name, "Yzerman")   # 42 goals
        self.assertEqual(top_players[2].name, "Kurri")     # 37 goals

    def test_top_sort_by_assists(self):
        # Test sorting by assists
        top_players = self.stats.top(2, SortBy.ASSISTS)
        
        # Should return 3 players due to <= condition
        self.assertEqual(len(top_players), 3)
        
        # Verify sorted by assists (descending): Gretzky(89), Yzerman(56), Lemieux(54)
        self.assertEqual(top_players[0].name, "Gretzky")   # 89 assists
        self.assertEqual(top_players[1].name, "Yzerman")   # 56 assists
        self.assertEqual(top_players[2].name, "Lemieux")   # 54 assists

    def test_top_sort_by_goals_all_players(self):
        # Test getting all players sorted by goals
        top_players = self.stats.top(4, SortBy.GOALS)
        
        # Should return all 5 players
        self.assertEqual(len(top_players), 5)
        
        # Verify full order by goals: Lemieux(45), Yzerman(42), Kurri(37), Gretzky(35), Semenko(4)
        expected_order = ["Lemieux", "Yzerman", "Kurri", "Gretzky", "Semenko"]
        expected_goals = [45, 42, 37, 35, 4]
        
        for i, (expected_name, expected_goal_count) in enumerate(zip(expected_order, expected_goals)):
            self.assertEqual(top_players[i].name, expected_name)
            self.assertEqual(top_players[i].goals, expected_goal_count)

    def test_top_sort_by_assists_all_players(self):
        # Test getting all players sorted by assists
        top_players = self.stats.top(4, SortBy.ASSISTS)
        
        # Should return all 5 players
        self.assertEqual(len(top_players), 5)
        
        # Verify full order by assists: Gretzky(89), Yzerman(56), Lemieux(54), Kurri(53), Semenko(12)
        expected_order = ["Gretzky", "Yzerman", "Lemieux", "Kurri", "Semenko"]
        expected_assists = [89, 56, 54, 53, 12]
        
        for i, (expected_name, expected_assist_count) in enumerate(zip(expected_order, expected_assists)):
            self.assertEqual(top_players[i].name, expected_name)
            self.assertEqual(top_players[i].assists, expected_assist_count)

    def test_top_default_parameter_still_works(self):
        # Test that calling without SortBy parameter still works (backward compatibility)
        top_players_default = self.stats.top(1)
        top_players_explicit = self.stats.top(1, SortBy.POINTS)
        
        # Both should return the same result
        self.assertEqual(len(top_players_default), 2)  # Due to <= condition
        self.assertEqual(len(top_players_explicit), 2)
        
        # Both should be sorted by points
        self.assertEqual(top_players_default[0].name, top_players_explicit[0].name)
        self.assertEqual(top_players_default[1].name, top_players_explicit[1].name)

    def test_top_sort_by_zero_with_different_sorts(self):
        # Test edge case with zero and different sort criteria
        top_by_points = self.stats.top(0, SortBy.POINTS)
        top_by_goals = self.stats.top(0, SortBy.GOALS)
        top_by_assists = self.stats.top(0, SortBy.ASSISTS)
        
        # All should return 1 player each
        self.assertEqual(len(top_by_points), 1)
        self.assertEqual(len(top_by_goals), 1)
        self.assertEqual(len(top_by_assists), 1)
        
        # Different top players based on sorting criteria
        self.assertEqual(top_by_points[0].name, "Gretzky")   # Highest points (124)
        self.assertEqual(top_by_goals[0].name, "Lemieux")    # Highest goals (45)
        self.assertEqual(top_by_assists[0].name, "Gretzky")  # Highest assists (89)

    def test_top_sort_by_invalid_value(self):
        # Test with invalid sort_by value (should default to points)
        # We'll pass None as an invalid value
        top_players = self.stats.top(1, None)
        
        # Should return 2 players due to <= condition
        self.assertEqual(len(top_players), 2)
        
        # Should default to sorting by points (same as SortBy.POINTS)
        self.assertEqual(top_players[0].name, "Gretzky")  # Highest points
        self.assertEqual(top_players[1].name, "Lemieux")  # Second highest points


if __name__ == "__main__":
    unittest.main()