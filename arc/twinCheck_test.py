import json
from twinCheck import twinCheck
import unittest
import os


def add_fish_to_aquarium(fish_list):
    if len(fish_list) > 10:
        raise ValueError("A maximum of 10 fish can be added to the aquarium")
    return {"tank_a": fish_list}


testdata= json.load('negativeShell.json')
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

class TestAddFishToAquarium(unittest.TestCase):
    def test_add_fish_to_aquarium_success(self):
        actual = add_fish_to_aquarium(fish_list=["shark", "tuna"])
        expected = {"tank_a": ["shark", "tuna"]}
        self.assertEqual(actual, expected)
    
    def test_twinCheck_check1(self):
        self.assertEqual(testdata,testdata)


if __name__ == '__main__':
    print(testdata)