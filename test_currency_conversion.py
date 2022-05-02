
import unittest
from main import *
import pandas as pd




class TestCurrencyConversion(unittest.TestCase):
    def test_get_exchange_rate(self):
        actual = type(get_exchange_rate('GBP','EUR'))
        expected = pd.DataFrame
        self.assertEqual(actual, expected)

    def test_get_raw_data(self):
        actual = type(get_raw_data('M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N'))
        expected = pd.DataFrame
        self.assertEqual(actual, expected)

    def test_get_data(self):
        actual = type(get_data('M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.GBP._T.T.N','EUR'))
        expected = pd.DataFrame
        self.assertEqual(actual, expected)
        
#this is remote coment
#this is remote coment
#this is remote coment

#this is remote coment
#this is remote coment

#this is remote coment
#this is remote coment
#this is remote coment

#this is remote coment

#this is remote coment



