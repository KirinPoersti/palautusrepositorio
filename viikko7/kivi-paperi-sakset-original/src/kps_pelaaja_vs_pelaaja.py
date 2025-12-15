"""Player vs Player game implementation."""
from kivi_paperi_sakset import KiviPaperiSakset


class KPSPelaajaVsPelaaja(KiviPaperiSakset):
    """Two human players playing against each other."""
    
    def _toisen_siirto(self, ensimmaisen_siirto):
        """Get second player's move from input."""
        return input("Toisen pelaajan siirto: ")
