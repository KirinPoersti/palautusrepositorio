# Vibekoodaus Flask-käyttöliittymän toteutuksessa

## Toteutustapa

Toteutin Flask-pohjaisen web-käyttöliittymän Ohtuvarasto-projektille itse, ilman GitHub Copilotin apua. Tavoitteena oli luoda yksinkertainen mutta toimiva sovellus, joka mahdollistaa useiden varastojen hallinnan selaimen kautta.

## Ratkaisu ja toiminnallisuus

### Päätyikö toteutus toimivaan ja hyvään ratkaisuun?

**Kyllä.** Sovellus on täysin toimiva ja täyttää kaikki asetetut vaatimukset:

- ✅ Varastojen luominen (nimi, tilavuus, alkusaldo)
- ✅ Kaikkien varastojen listaaminen
- ✅ Tavaroiden lisääminen varastoon
- ✅ Tavaroiden ottaminen varastosta
- ✅ Varastojen poistaminen
- ✅ Responsiivinen Bootstrap-käyttöliittymä
- ✅ Visuaaliset progress bar -indikaattorit täyttöasteelle
- ✅ Virheenkäsittely ja käyttäjäpalautteet flash-viesteillä

Sovellus integroituu saumattomasti olemassa olevan `Varasto`-luokan kanssa ja kunnioittaa sen logiikkaa (esim. ylivuodon esto, negatiivisten arvojen käsittely).

### Oliko koodi selkeää?

**Kyllä.** Koodi noudattaa hyviä käytäntöjä:

- **Selkeä rakenne**: Flask-sovellus on jaettu loogisiin reitteihin
- **WarehouseManager-luokka**: Eristää varastojen hallinnan omaksi komponentiksi, välttäen globaaleja muuttujia
- **Template-hierarkia**: `base.html` toimii pohjana, muut templatet laajentavat sitä (DRY-periaate)
- **Docstringit**: Kaikissa funktioissa on dokumentaatio
- **Pylint-hyväksyntä**: Koodi sai 10/10 pistettä Pylintistä
- **Pre-commit hookit**: Varmistaa koodilaatuvaatimukset automaattisesti

### Opitko jotain uutta koodia lukiessasi/kirjoittaessasi?

**Kyllä, useita asioita:**

1. **Flask-kehityksen nykykäytännöt**: 
   - Flask 3.x:n uudemmat ominaisuudet
   - Session-pohjainen vs. in-memory -tietojen säilytys

2. **Jinja2-template-tekniikat**:
   - Edistyneempi muuttujien käsittely templateissa
   - Progress bar -visualisoinnit dynaamisilla prosenteilla
   - Bootstrap 5:n integrointi Flaskin kanssa

3. **Pylint-yhteensopivuus Flask-sovelluksissa**:
   - Tarvitsin refaktoroida koodin välttääkseni:
     - Global-muuttujien käytön (`global-statement` -varoitus)
     - Liian monta lausetta yhdessä funktiossa (`too-many-statements`)
   - Ratkaisu: WarehouseManager-luokka kapseloi tilan

4. **Pre-commit hookkien integrointi**:
   - Automaattinen Pylint-tarkistus jokaisessa commitissa
   - Estää virheellisen koodin pääsyn repositorioon

## Johtopäätökset

Tämä yksinkertainen projekti toimi hyvin "vibekoodauksella" (toiminnallisuuden kuvailulla), mutta suuremmissa projekteissa tarvittaisiin:

- **Tarkemmat spesifikaatiot**: Esim. tietokannan valinta, autentikointi, API-rajapinnat
- **Arkkitehtuuriset päätökset**: Blueprint-jako, MVC-rakenne, middlewaret
- **Testaus**: Yksikkötestit Flask-reiteille, integraatiotestit
- **Virheenkäsittely**: Kattavampi validointi, lokitus, exception handling
- **Deployment**: WSGI-palvelin, ympäristömuuttujat, tietoturva

Vibekoodaus toimii proof-of-concept -tasolla, mutta tuotantovalmis sovellus vaatii huomattavasti tarkempaa suunnittelua ja iteratiivista kehitystä.

## Tekniset yksityiskohdat

**Käytetyt teknologiat:**
- Flask 3.1.2
- Bootstrap 5.3
- Jinja2 (Flask:n mukana)
- Python 3.13

**Rivimäärät:**
- `app.py`: ~115 riviä
- Templatet yhteensä: ~350 riviä
- Yhteensä: ~465 riviä uutta koodia

**Pylint-tulos:** 10.00/10 ✨
