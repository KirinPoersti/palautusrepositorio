"""Player vs Simple AI game implementation."""
from kivi_paperi_sakset import KiviPaperiSakset
from tekoaly import Tekoaly


class KPSTekoaly(KiviPaperiSakset):
    """Human player against simple AI."""
    
    def __init__(self):
        self._tekoaly = Tekoaly()
    
    def _toisen_siirto(self, ensimmaisen_siirto):
        """Get AI's move."""
        siirto = self._tekoaly.anna_siirto()
        print(f"Tietokone valitsi: {siirto}")
        return siirto
