# Mock-kirjaston käyttö - Yhteenveto

## Mitä Mock-oliot ovat?

Mock-oliot ovat unittest.mock-moduulin tarjoamia testauksen apuvälineitä, jotka korvaavat todelliset riippuvuudet testeissä. Ne mahdollistavat:
1. Riippuvuuksien eristämisen testeissä
2. Metodikutsujen seurannan ja varmentamisen
3. Paluuarvojen ja käyttäytymisen määrittelyn

## Peruskäyttö

```python
from unittest.mock import Mock

mock = Mock()
mock.foo.bar()  # Palauttaa uuden Mock-olion
```

## Tärkeimmät ominaisuudet

### 1. return_value
Määrittelee metodin paluuarvon:
```python
mock.foo.bar.return_value = "Foobar"
mock.foo.bar()  # Palauttaa "Foobar"
```

### 2. side_effect
Määrittelee metodin toteutuksen (funktio, lambda):
```python
mock.foo.bar.side_effect = lambda name: f"{name}: Foobar"
mock.foo.bar("Kalle")  # Palauttaa "Kalle: Foobar"
```

### 3. assert_called()
Varmistaa että metodia on kutsuttu:
```python
mock.foo.bar()
mock.foo.bar.assert_called()  # OK
mock.foo.doo.assert_called()  # AssertionError
```

### 4. assert_called_with()
Varmistaa että metodia on kutsuttu oikeilla parametreilla:
```python
pankki_mock.maksa.assert_called_with("1111", 10, 55)
# Käyttäen ANY-vakiota kun parametri ei ole oleellinen:
pankki_mock.maksa.assert_called_with(ANY, ANY, 55)
```

### 5. wraps
Käyttää oikean olion metodeja mock-olion kautta:
```python
viitegeneraattori_mock = Mock(wraps=Viitegeneraattori())
# Nyt uusi()-metodi toimii oikean toteutuksen mukaan
```

### 6. call_count
Laskee montako kertaa metodia on kutsuttu:
```python
self.assertEqual(viitegeneraattori_mock.uusi.call_count, 3)
```

## Kauppa-projektin testit

Projekti demonstroi kuinka mock-olioilla voidaan:
- Testata että Kauppa kutsuu Pankki-olion maksa-metodia oikeilla parametreilla
- Varmistaa että jokaiselle maksulle haetaan uusi viitenumero
- Kontrolloida viitegeneraattorin palauttamia arvoja testeissä
- Testata luokan käyttäytymistä eristämällä sen riippuvuudet

## Virheilmoitukset

Kun testi epäonnistuu, mock antaa selkeän virheilmoituksen:
```
AssertionError: expected call not found.
Expected: maksa(<ANY>, <ANY>, 1000)
  Actual: maksa('1111', 10, 55)
```

Tämä auttaa nopeasti tunnistamaan mikä meni vikaan.
