import requests
from src.player import Player

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    response = requests.get(url).json()

    print("JSON-muotoinen vastaus:")
    print(f"First player: {response[0]}")

    players = []

    for player_dict in response:
        player = Player(player_dict)
        players.append(player)

    print("Oliot:")

    for player in players[:5]:  # Show first 5 players
        print(player)
        
    # Show top 3 Finnish players by points
    finnish_players = [player for player in players if player.nationality == "FIN"]
    finnish_players.sort(key=lambda player: player.points, reverse=True)
    
    print("\nTop 3 Finnish players by points:")
    for player in finnish_players[:3]:
        print(player)

if __name__ == "__main__":
    main()