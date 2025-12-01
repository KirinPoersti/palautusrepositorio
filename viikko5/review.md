# Koodikatselmointi: Tennis Game Refactoring

*Huom: Koska GitHub Copilot -jäsenyys ei ole vielä myönnetty, tämä katselmointi on tehty manuaalisesti noudattaen hyviä koodikatselmointikäytäntöjä.*

---

## Katselmoinnin huomiot

### Huomio 1: `won_point()` käyttää kovakoodattuja merkkijonoja

**Ongelma:**
```python
def won_point(self, player_name):
    if player_name == "player1":
        self.player1_score += 1
    else:
        self.player2_score += 1
```

Metodi vertaa parametria kovakoodattuun merkkijonoon "player1". Tämä on virhealtis ja epäjohdonmukainen, koska konstruktorissa käytetään `player1_name` ja `player2_name` muuttujia.

**Ehdotus:**
Käytä pelaajien nimiä vertailussa tai luo vakiot/enum pelaajille.

**Arvio:** Tämä on hyvä huomio. Refaktoroinnissa olisi pitänyt korjata myös tämä.

---

### Huomio 2: `_score_to_name()` voi yksinkertaistaa dictionary-rakenteella

**Ongelma:**
```python
def _score_to_name(self, score):
    if score == self.LOVE:
        return "Love"
    elif score == self.FIFTEEN:
        return "Fifteen"
    # ...
```

Pitkä if-elif-ketju voitaisiin korvata dict-rakenteella.

**Ehdotus:**
```python
SCORE_NAMES = {
    LOVE: "Love",
    FIFTEEN: "Fifteen",
    THIRTY: "Thirty",
    FORTY: "Forty"
}

def _score_to_name(self, score):
    return self.SCORE_NAMES.get(score, "")
```

**Arvio:** Hyvä ehdotus, tekisi koodista tiiviimmän ja helpommin ylläpidettävän.

---

### Huomio 3: `_get_tied_score()` toistaa logiikkaa

**Ongelma:**
```python
def _get_tied_score(self):
    if self.player1_score == self.LOVE:
        return "Love-All"
    elif self.player1_score == self.FIFTEEN:
        return "Fifteen-All"
    # ...
```

Tässä toistetaan samanlaista logiikkaa kuin `_score_to_name()`:ssa.

**Ehdotus:**
```python
def _get_tied_score(self):
    if self.player1_score >= self.FORTY:
        return "Deuce"
    score_name = self._score_to_name(self.player1_score)
    return f"{score_name}-All"
```

**Arvio:** Erinomainen huomio! Tämä poistaisi koodin toiston ja tekisi metodista paljon lyhyemmän.

---

### Huomio 4: Dokumentaatiossa puutteita

**Ongelma:**
Luokalla ei ole docstringiä, eikä julkisilla metodeilla `__init__`, `won_point`, ja `get_score` ole dokumentaatiota.

**Ehdotus:**
Lisää docstringit ainakin julkisiin metodeihin:
```python
class TennisGame:
    """Represents a tennis game with score tracking."""
    
    def won_point(self, player_name):
        """Record that a player has won a point.
        
        Args:
            player_name: Name of the player who won the point.
        """
```

**Arvio:** Tärkeä huomio. Hyvin dokumentoitu koodi on helpompi ymmärtää ja ylläpitää.

---

### Huomio 5: `_get_endgame_score()` voisi käyttää abs() ja tuple-rakennetta

**Ongelma:**
```python
if score_difference == 1:
    return "Advantage player1"
elif score_difference == -1:
    return "Advantage player2"
```

Toisto advantage- ja win-logiikassa.

**Ehdotus:**
Voisi yksinkertaistaa käyttämällä abs() ja määrittelemällä voittavan pelaajan dynaamisesti.

**Arvio:** Kohtuullinen ehdotus, mutta nykyinen toteutus on selkeä ja helppolukuinen. Tämä on makuasia.

---

### Huomio 6: Vakiot voisivat olla luokkatason sijaan moduulitason

**Huomio:**
Vakiot `LOVE`, `FIFTEEN`, jne. ovat nyt luokkamuuttujia. Ne voisivat olla moduulitason vakioita, koska ne eivät riipu luokan instanssista.

**Ehdotus:**
```python
# Moduulin alussa
LOVE = 0
FIFTEEN = 1
THIRTY = 2
FORTY = 3
WIN_THRESHOLD = 4

class TennisGame:
    # ...
```

**Arvio:** Teknisesti oikein, mutta nykyinen ratkaisu on myös hyvä. Luokkamuuttujat pitävät vakiot loogisesti osan `TennisGame`-luokkaa.

---

## Yhteenveto katselmoinnista

### Mitä huomioita tehtiin koodista?

Katselmoinnissa löytyi **6 keskeistä parannuskohdetta**:

1. **Kovakoodatut merkkijonot** `won_point()`-metodissa
2. **If-elif-ketjut** joita voisi yksinkertaistaa dictionary-rakenteella
3. **Koodin toisto** `_get_tied_score()`-metodissa
4. **Dokumentaation puute** julkisissa metodeissa
5. **Mahdollisuus yksinkertaistaa** `_get_endgame_score()`
6. **Vakioiden sijoittelu** - luokka- vs moduulitaso

### Olivatko ehdotetut muutokset hyviä?

**Erittäin hyödyllisiä:**
- Huomiot 1-4 ovat selkeitä parannuksia, jotka parantaisivat koodin laatua merkittävästi
- Erityisesti **koodin toiston poisto** (huomio 3) ja **kovakoodattujen merkkijonojen korjaus** (huomio 1) ovat tärkeitä

**Makuasioita:**
- Huomiot 5-6 ovat enemmän tyylillisiä valintoja, jotka eivät välttämättä paranna koodia merkittävästi

### Kuinka hyödylliseksi koin katselmoinnin?

Vaikka tämä oli manuaalinen katselmointi, se oli **erittäin hyödyllinen** oppimiskokemus:

**Positiiviset puolet:**
- ✅ Löysi aitoja parannuskohteita, joita ei refaktoroinnissa huomattu
- ✅ Pakotti tarkastelemaan koodia kriittisesti
- ✅ Auttoi ymmärtämään, mitä "hyvä koodi" oikeasti tarkoittaa
- ✅ Osoitti että refaktorointi on iteratiivinen prosessi

**Mitä opin:**
- Ensimmäinen refaktorointikierros paransi koodia merkittävästi (taikanumerot, metodien erottelu)
- Mutta jäi vielä parannettavaa (koodin toisto, dokumentaatio, kovakoodatut arvot)
- Koodikatselmointi on tärkeä osa laadunvarmistusta
- Hyvä katselmointi vaatii aikaa ja huolellisuutta

**Vertailu automaattiseen katselmointiin:**
- Manuaalinen katselmointi on aikaa vievää mutta opettavaista
- Automaattinen työkalu (kuten Copilot) voisi löytää nämä ongelmat nopeammin
- Kuitenkin ihmiskatselmoija ymmärtää kontekstin ja liiketoimintalogiikan paremmin

---

## Lopputulos

Refaktorointi paransi koodin laatua huomattavasti alkuperäisestä versiosta:
- ✅ Taikanumerot korvattu vakioilla
- ✅ Muuttujat nimetty selkeästi
- ✅ Pitkä metodi jaettu pienempiin osiin
- ✅ Koodi on helpommin luettavaa

Katselmointi paljasti kuitenkin, että **refaktorointia voisi vielä jatkaa**:
- ❌ Koodin toistoa voisi vähentää
- ❌ Dokumentaatio puuttuu
- ❌ Kovakoodatut merkkijonot pitäisi korjata

**Oppiminen:** Hyvä koodi syntyy iteratiivisesti. Ensimmäinen refaktorointi teki koodista paremman, mutta ei vielä täydellistä. Koodikatselmointi on arvokas työkalu jatkuvaan parantamiseen.
