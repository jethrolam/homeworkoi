import os
import unittest
import argparse

import main


class TestMain(unittest.TestCase):


    def test_compute_token_df_simple(self):
        token_df = main.compute_token_df('This is a simple  text.one two three, \\four \ntwO  three three. \nSimp1e')
        self.assertEqual('two|twO@2', token_df.at['two', 'summary'])
        self.assertEqual('\\four@1', token_df.at['\\four', 'summary'])
        self.assertEqual('three@3', token_df.at['three', 'summary'])
        self.assertEqual((9, 3), token_df.shape)


    def test_compute_token_df_full(self):
        text = open('gettysburg.txt').read()
        token_df = main.compute_token_df(text).sort_values('freq', ascending=False)
        self.assertEqual((137, 3), token_df.shape)
        self.assertEqual("that@13", token_df.at['that', 'summary'])
        self.assertEqual("the|The@11", token_df.at['the', 'summary'])
        self.assertEqual("we|We@10", token_df.at['we', 'summary'])
        self.assertEqual("to|t0@8", token_df.at['to', 'summary'])
        self.assertEqual("here@8", token_df.at['here', 'summary'])
        self.assertEqual("a@7", token_df.at['a', 'summary'])
        self.assertEqual("and@6", token_df.at['and', 'summary'])


    def test_normalize(self):
        self.assertEqual('this', main.normalize('this'))
        self.assertEqual('but', main.normalize('8ut'))
        self.assertEqual('buio', main.normalize('8Ul0'))
        self.assertEqual('iib', main.normalize('118'))
