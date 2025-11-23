import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        
        # palautetaan aina arvo 42
        self.viitegeneraattori_mock.uusi.return_value = 42
        
        self.varasto_mock = Mock()
        
        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 10
            if tuote_id == 3:
                return 0
        
        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "leipä", 3)
            if tuote_id == 3:
                return Tuote(3, "juusto", 10)
        
        # otetaan toteutukset käyttöön
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote
        
        # alustetaan kauppa
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan_oikeilla_parametreilla(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu oikeilla parametreilla
        # tilisiirto(nimi, viite, tili_numero, kaupan_tili, summa)
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)

    def test_kahden_eri_tuotteen_ostaminen_kutsuu_tilisiirtoa_oikeilla_parametreilla(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # maito, hinta 5
        self.kauppa.lisaa_koriin(2)  # leipä, hinta 3
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu oikeilla parametreilla
        # yhteishinta 5 + 3 = 8
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 8)

    def test_kahden_saman_tuotteen_ostaminen_kutsuu_tilisiirtoa_oikeilla_parametreilla(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # maito, hinta 5
        self.kauppa.lisaa_koriin(1)  # maito, hinta 5
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu oikeilla parametreilla
        # yhteishinta 5 + 5 = 10
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 10)

    def test_varastossa_olevan_ja_loppuneen_tuotteen_ostaminen_kutsuu_tilisiirtoa_vain_varastossa_olevan_tuotteen_hinnalla(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # maito, hinta 5, varastossa
        self.kauppa.lisaa_koriin(3)  # juusto, hinta 10, loppu
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu oikeilla parametreilla
        # yhteishinta vain 5 (juustoa ei lisätty koriin kun sitä ei ole varastossa)
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)

    def test_aloita_asiointi_nollaa_edellisen_ostoksen_tiedot(self):
        # tehdään ensimmäinen ostos
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # maito, hinta 5
        self.kauppa.tilimaksu("pekka", "12345")

        # aloitetaan uusi asiointi
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)  # leipä, hinta 3
        self.kauppa.tilimaksu("matti", "67890")

        # varmistetaan, että toinen tilisiirto tehtiin vain toisen ostoksen hinnalla
        # eli edellisen ostoksen hinta (5) ei näy tässä
        self.pankki_mock.tilisiirto.assert_called_with("matti", 42, "67890", "33333-44455", 3)

    def test_kauppa_pyytaa_uuden_viitenumeron_jokaiselle_maksutapahtumalle(self):
        # konfiguroidaan mock palauttamaan eri arvot peräkkäisille kutsuille
        self.viitegeneraattori_mock.uusi.side_effect = [1, 2, 3]

        # tehdään ensimmäinen ostos
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan että ensimmäinen ostos käytti viitettä 1
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 1, "12345", "33333-44455", 5)

        # tehdään toinen ostos
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("matti", "67890")

        # varmistetaan että toinen ostos käytti viitettä 2
        self.pankki_mock.tilisiirto.assert_called_with("matti", 2, "67890", "33333-44455", 3)

        # tehdään kolmas ostos
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("liisa", "11111")

        # varmistetaan että kolmas ostos käytti viitettä 3
        self.pankki_mock.tilisiirto.assert_called_with("liisa", 3, "11111", "33333-44455", 5)

        # varmistetaan että viitegeneraattorin metodia uusi on kutsuttu kolme kertaa
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 3)

    def test_poista_korista_poistaa_tuotteen_ostoskorista_ja_palauttaa_varastoon(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # maito, hinta 5
        self.kauppa.lisaa_koriin(2)  # leipä, hinta 3
        
        # poistetaan maito korista
        self.kauppa.poista_korista(1)
        
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että tilisiirto tehtiin vain leivän hinnalla (3)
        # koska maito poistettiin korista
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 3)
        
        # varmistetaan että varasto.palauta_varastoon kutsuttiin
        self.varasto_mock.palauta_varastoon.assert_called()
