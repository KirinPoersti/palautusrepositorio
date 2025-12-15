# Kivi-Paperi-Sakset Refaktorointi

## Tehtävän kuvaus

Kurssirepositorion kivi-paperi-sakset -peli sisälsi runsaasti copy-pastea ja huonoa oliosuunnittelua. Tehtävänä oli refaktoroida koodi noudattamaan oikeaoppisia suunnittelumalleja.

---

## Toteutetut refaktoroinnit

### 1. Template Method Pattern

**Mitä tehtiin:**
Luotiin yliluokka `KiviPaperiSakset`, joka sisältää yhteisen `pelaa()`-metodin template method -patternin mukaisesti.

**Alkuperäinen ongelma:**
Kolme erillistä luokkaa (`KPSPelaajaVsPelaaja`, `KPSTekoaly`, `KPSParempiTekoaly`) sisälsivät lähes identtisen `pelaa()`-metodin. Ainoa ero oli toisen pelaajan siirron hankkimisessa.

**Ratkaisu:**

```python
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
    
    def _toisen_siirto(self, ensimmaisen_siirto):
        """Must be implemented in subclasses."""
        raise NotImplementedError("Subclass must implement _toisen_siirto")
```

**Tulokset:**
- Kaikki yhteinen logiikka on nyt yhdessä paikassa
- Aliluokat toteuttavat vain `_toisen_siirto()`-metodin
- Koodin toisto eliminoitu

---

### 2. Aliluokkien yksinkertaistaminen

**Pelaaja vs. Pelaaja:**
```python
class KPSPelaajaVsPelaaja(KiviPaperiSakset):
    """Two human players playing against each other."""
    
    def _toisen_siirto(self, ensimmaisen_siirto):
        """Get second player's move from input."""
        return input("Toisen pelaajan siirto: ")
```
- **Ennen:** 22 riviä
- **Jälkeen:** 10 riviä
- **Vähenemä:** 55%

**Pelaaja vs. Tekoäly:**
```python
class KPSTekoaly(KiviPaperiSakset):
    """Human player against simple AI."""
    
    def __init__(self):
        self._tekoaly = Tekoaly()
    
    def _toisen_siirto(self, ensimmaisen_siirto):
        """Get AI's move."""
        siirto = self._tekoaly.anna_siirto()
        print(f"Tietokone valitsi: {siirto}")
        return siirto
```
- **Ennen:** 25 riviä
- **Jälkeen:** 16 riviä
- **Vähenemä:** 36%

**Pelaaja vs. Parempi Tekoäly:**
```python
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
```
- **Ennen:** 28 riviä
- **Jälkeen:** 17 riviä
- **Vähenemä:** 39%

---

### 3. Factory Pattern

**Ongelma:**
Circular import -riski, kun pääohjelma importtaa konkreettiset luokat ja ne importtaavat yliluokan.

**Ratkaisu:**
Luotiin erillinen `peli_tehdas.py`:

```python
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
```

**Edut:**
- Välttää circular import -ongelmat
- Eristää objektien luonnin logiikan
- Helpottaa uusien pelityyppien lisäämistä

---

### 4. Pääohjelman yksinkertaistaminen

**Ennen:**
```python
from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from kps_parempi_tekoaly import KPSParempiTekoaly

# ... 40 riviä koodia if-elif-ketjuilla
```

**Jälkeen:**
```python
from peli_tehdas import luo_peli

def main():
    while True:
        print("Valitse pelataanko...")
        vastaus = input()
        
        if vastaus.endswith(("a", "b", "c")):
            print("Peli loppuu kun pelaaja antaa virheellisen siirron...")
            peli = luo_peli(vastaus[-1])
            if peli:
                peli.pelaa()
        else:
            break
```

**Parannukset:**
- Ei riippuvuuksia konkreettisista luokista
- DRY-periaate: ei toistoa tulostuksissa
- Selkeämpi kontrollivirtaus

---

## Refaktoroinnin hyödyt

### Koodin laatu

**Ennen refaktorointia:**
- 3 luokkaa × ~25 riviä = ~75 riviä toistuvaa koodia
- Copy-paste virheiden riski
- Muutokset vaativat päivityksiä kolmeen paikkaan

**Refaktoroinnin jälkeen:**
- 1 yliluokka (36 riviä) + 3 aliluokkaa (10-17 riviä) = ~79 riviä
- DRY-periaate täytetty
- Muutokset tehdään yhteen paikkaan

### SOLID-periaatteet

✅ **Single Responsibility:** Jokainen luokka vastaa vain yhdestä asiasta  
✅ **Open/Closed:** Helppo laajentaa uusilla pelityypeillä ilman muutoksia olemassa olevaan koodiin  
✅ **Liskov Substitution:** Kaikki aliluokat toimivat yliluokan paikalla  
✅ **Interface Segregation:** Pienet, selkeät rajapinnat  
✅ **Dependency Inversion:** Pääohjelma riippuu abstraktiosta (factory), ei konkreettisista luokista

### Ylläpidettävyys

- **Dokumentaatio:** Kaikissa luokissa ja metodeissa docstringit
- **Nimeäminen:** Selkeät, kuvaavat nimet
- **Rakenne:** Looginen tiedostorakenne
- **Laajennettavuus:** Uuden pelityypin lisääminen vaatii vain yhden uuden aliluokan

---

## Tekniset yksityiskohdat

**Luodut tiedostot:**
- `kivi_paperi_sakset.py` - Yliluokka (36 riviä)
- `peli_tehdas.py` - Factory-funktio (26 riviä)

**Muokatut tiedostot:**
- `index.py` - Yksinkertaistettu 40 → 29 riviä
- `kps_pelaaja_vs_pelaaja.py` - Yksinkertaistettu 22 → 10 riviä
- `kps_tekoaly.py` - Yksinkertaistettu 25 → 16 riviä
- `kps_parempi_tekoaly.py` - Yksinkertaistettu 28 → 17 riviä

**Suunnittelumallit:**
- Template Method Pattern
- Factory Pattern

**Python-ominaisuudet:**
- Perintä ja abstraktit metodit
- `NotImplementedError` abstraktille metodille
- Docstringit dokumentointiin
- Type hints puuttuu (voisi lisätä)

---

## Yhteenveto

Refaktorointi onnistui erinomaisesti. Koodi on nyt:
- ✅ Selkeämpi ja luettavampi
- ✅ Helpommin ylläpidettävä
- ✅ Paremmin testattavissa
- ✅ Helpommin laajennettavissa
- ✅ Noudattaa suunnittelumalleja
- ✅ Täyttää SOLID-periaatteet

**Oppimiskokemukset:**
1. Template Method Pattern on tehokas tapa eliminoida toistoa kun algoritmin rakenne on sama mutta yksityiskohdat vaihtelevat
2. Factory Pattern auttaa välttämään circular import -ongelmia
3. Hyvin suunniteltu perintähierarkia tekee koodista laajennettavan
4. Docstringit ja selkeä nimeäminen parantavat koodin ymmärrettävyyttä merkittävästi
