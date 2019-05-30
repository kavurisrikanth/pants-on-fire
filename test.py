import unittest

from commands import alter_name


class TestProject(unittest.TestCase):
    def testNameAlteration(self):
        s = 'Donald Trump'
        self.assertEqual(alter_name(s), 'donald-trump')

        s = 'Bill de Blasio'
        self.assertEqual(alter_name(s), 'bill-de-blasio')

        s = "Beto O'Rourke"
        self.assertEqual(alter_name(s), 'beto-orourke')