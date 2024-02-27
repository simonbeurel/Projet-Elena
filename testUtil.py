import unittest
from util import *

class MyTestCase(unittest.TestCase):
    def test_retrieve_swiatek(self):
        '''Unit test for a player with a simple lastName'''
        self.assertEqual(retrieve_player_id("iga","swiatek"), "jNyZsXZe")

    def test_retrieve_beatriz(self):
        '''Unit test for a player with a composed lastName'''
        self.assertEqual(retrieve_player_id("beatriz", 'haddad maia'), "lSABz6E8")

if __name__ == '__main__':
    unittest.main()
