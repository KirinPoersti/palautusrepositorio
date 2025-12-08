from statistics import Statistics
from player_reader import PlayerReader
from matchers import And, HasAtLeast, PlaysIn, Not, HasFewerThan, All, Or, QueryBuilder

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players.txt"
    reader = PlayerReader(url)
    stats = Statistics(reader)

    # Test original functionality
    print("Test 1: PHI players with at least 5 goals and 20 assists")
    matcher = And(
        HasAtLeast(5, "goals"),
        HasAtLeast(20, "assists"),
        PlaysIn("PHI")
    )
    for player in stats.matches(matcher):
        print(player)

    # Test Not and HasFewerThan
    print("\nTest 2: NYR players with fewer than 2 goals (using Not)")
    matcher = And(
        Not(HasAtLeast(2, "goals")),
        PlaysIn("NYR")
    )
    for player in stats.matches(matcher):
        print(player)

    print("\nTest 3: NYR players with fewer than 2 goals (using HasFewerThan)")
    matcher = And(
        HasFewerThan(2, "goals"),
        PlaysIn("NYR")
    )
    for player in stats.matches(matcher):
        print(player)

    # Test All
    print("\nTest 4: All players count")
    filtered_with_all = stats.matches(All())
    print(len(filtered_with_all))

    # Test Or
    print("\nTest 5: Players with at least 45 goals OR 70 assists")
    matcher = Or(
        HasAtLeast(45, "goals"),
        HasAtLeast(70, "assists")
    )
    for player in stats.matches(matcher):
        print(player)

    # Test complex Or with And
    print("\nTest 6: At least 70 points and plays in COL, FLA, or BOS")
    matcher = And(
        HasAtLeast(70, "points"),
        Or(
            PlaysIn("COL"),
            PlaysIn("FLA"),
            PlaysIn("BOS")
        )
    )
    for player in stats.matches(matcher):
        print(player)

    # Test QueryBuilder
    print("\nTest 7: QueryBuilder - All players")
    query = QueryBuilder()
    matcher = query.build()
    for player in stats.matches(matcher)[:5]:  # Print only first 5
        print(player)

    print("\nTest 8: QueryBuilder - NYR players")
    query = QueryBuilder()
    matcher = query.plays_in("NYR").build()
    for player in stats.matches(matcher)[:5]:  # Print only first 5
        print(player)

    print("\nTest 9: QueryBuilder - NYR players with 10-19 goals")
    query = QueryBuilder()
    matcher = (
        query
        .plays_in("NYR")
        .has_at_least(10, "goals")
        .has_fewer_than(20, "goals")
        .build()
    )
    for player in stats.matches(matcher):
        print(player)

    print("\nTest 10: QueryBuilder with one_of - Complex OR query")
    query = QueryBuilder()
    matcher = (
        query
        .one_of(
            QueryBuilder().plays_in("PHI").has_at_least(10, "assists").has_fewer_than(10, "goals"),
            QueryBuilder().plays_in("EDM").has_at_least(50, "points")
        )
        .build()
    )
    for player in stats.matches(matcher):
        print(player)


if __name__ == "__main__":
    main()
