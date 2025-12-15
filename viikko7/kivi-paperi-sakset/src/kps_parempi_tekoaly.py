"""Player vs Advanced AI game implementation."""
from kivi_paperi_sakset import KiviPaperiSakset
from tekoaly_parannettu import TekoalyParannettu


class KPSParempiTekoaly(KiviPaperiSakset):
    """Human player against advanced AI that learns from moves."""
    
    def __init__(self):
        self._tekoaly = TekoalyParannettu(10)
    
    def _toisen_siirto(self, ensimmaisen_siirto):
        """Get advanced AI's move and update its memory."""
        siirto = self._tekoaly.anna_siirto()
        print(f"Tietokone valitsi: {siirto}")
        self._tekoaly.aseta_siirto(ensimmaisen_siirto)
        return siirto
