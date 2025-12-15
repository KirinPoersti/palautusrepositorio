"""Factory for creating different game type instances."""
from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from kps_parempi_tekoaly import KPSParempiTekoaly


def luo_peli(tyyppi):
    """Create game instance based on type.
    
    Args:
        tyyppi: 'a' for player vs player, 
                'b' for player vs simple AI,
                'c' for player vs advanced AI
    
    Returns:
        Game instance or None if invalid type
    """
    if tyyppi == 'a':
        return KPSPelaajaVsPelaaja()
    if tyyppi == 'b':
        return KPSTekoaly()
    if tyyppi == 'c':
        return KPSParempiTekoaly()
    
    return None
