import unittest


class Laskin:
    def __init__(self, io):
        self._io = io

    def suorita(self):
        while True:
            luku1 = int(self._io.lue("Luku 1:"))

            if luku1 == -9999:
                return

            luku2 = int(self._io.lue("Luku 2:"))

            if luku2 == -9999:
                return

            vastaus = self._laske_summa(luku1, luku2)

            self._io.kirjoita(f"Summa: {vastaus}")

    def _laske_summa(self, luku1, luku2):
        return luku1 + luku2
class KonsoliIO:
    def lue(self, teksti):
        return input(teksti)

    def kirjoita(self, teksti):
        print(teksti)
class StubIO:
    def __init__(self, inputs):
        self.inputs = inputs
        self.outputs = []

    def lue(self, teksti):
        return self.inputs.pop(0)

    def kirjoita(self, teksti):
        self.outputs.append(teksti)

class TestLaskin(unittest.TestCase):
    def test_yksi_summa_oikein(self):
        # testissä kovakoodataan ohjelman syötteiksi 1, 3 ja -9999
        io = StubIO(["1", "3", "-9999"])  

        laskin = Laskin(io)
        laskin.suorita()

        # varmistetaan, että ohjelma tulosti oikean summan
        self.assertEqual(io.outputs[0], "Summa: 4")

def main():
    io = KonsoliIO()     # luodaan riippuvuus luokan ulkopuolella
    laskin = Laskin(io) # annetaan riippuvuus luokalle

    laskin.suorita()

if __name__ == "__main__":
    main()