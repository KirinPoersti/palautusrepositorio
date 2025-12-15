"""Main program for rock-paper-scissors game."""
from peli_tehdas import luo_peli


def main():
    """Run the game loop."""
    while True:
        print("Valitse pelataanko"
              "\n (a) Ihmistä vastaan"
              "\n (b) Tekoälyä vastaan"
              "\n (c) Parannettua tekoälyä vastaan"
              "\nMuilla valinnoilla lopetetaan"
              )

        vastaus = input()

        if vastaus.endswith(("a", "b", "c")):
            print(
                "Peli loppuu kun pelaaja antaa virheellisen siirron "
                "eli jonkun muun kuin k, p tai s"
            )

            peli = luo_peli(vastaus[-1])
            if peli:
                peli.pelaa()
        else:
            break


if __name__ == "__main__":
    main()
