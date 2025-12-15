"""Base class for all rock-paper-scissors game variants."""
from tuomari import Tuomari


class KiviPaperiSakset:
    """Template class for rock-paper-scissors games."""
    
    def pelaa(self):
        """Play the game using template method pattern."""
        tuomari = Tuomari()

        ekan_siirto = self._ensimmaisen_siirto()
        tokan_siirto = self._toisen_siirto(ekan_siirto)

        while self._onko_ok_siirto(ekan_siirto) and self._onko_ok_siirto(tokan_siirto):
            tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)
            print(tuomari)

            ekan_siirto = self._ensimmaisen_siirto()
            tokan_siirto = self._toisen_siirto(ekan_siirto)

        print("Kiitos!")
        print(tuomari)

    def _ensimmaisen_siirto(self):
        """Get first player's move."""
        return input("Ensimmäisen pelaajan siirto: ")

    def _toisen_siirto(self, ensimmaisen_siirto):
        """Get second player's move. Must be implemented in subclasses."""
        raise NotImplementedError("Subclass must implement _toisen_siirto")

    def _onko_ok_siirto(self, siirto):
        """Check if move is valid (k, p, or s)."""
        return siirto in ("k", "p", "s")
