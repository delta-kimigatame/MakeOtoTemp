import unittest
import os
import os.path

import Preset

class Test_test_default_preset(unittest.TestCase):
    def test_make_preset(self):
        if os.path.isfile("mkototemp.ini"):
            os.remove("mkototemp.ini")
        self.assertFalse(os.path.isfile("mkototemp.ini"))
        preset = Preset.Preset()
        self.assertTrue(os.path.isfile("mkototemp.ini"))

    def test__param(self):
        preset = Preset.Preset()
        self.assertEqual(100,preset.tempo)
        self.assertEqual(800,preset.offset)
        self.assertEqual(2,preset.max)
        self.assertTrue(preset.under)
        self.assertTrue(preset.begining_cv)
        self.assertFalse(preset.nohead)
        self.assertFalse(preset.novcv)
        self.assertFalse(preset.only_consonant)

    def test__vowels(self):
        preset = Preset.Preset()
        self.assertEqual(preset.vowel["あ"],"a")
        self.assertEqual(preset.vowel["い"],"i")
        self.assertEqual(preset.vowel["う"],"u")
        self.assertEqual(preset.vowel["え"],"e")
        self.assertEqual(preset.vowel["お"],"o")
        self.assertEqual(preset.vowel["ん"],"n")
        self.assertEqual(preset.vowel["ン"],"n")
        self.assertEqual(len(preset.vowel),163)

    def test_consonants(self):
        preset = Preset.Preset()
        self.assertEqual(preset.consonant["あ"],"")
        self.assertEqual(preset.consonant["い"],"")
        self.assertEqual(preset.consonant["う"],"")
        self.assertEqual(preset.consonant["え"],"")
        self.assertEqual(preset.consonant["お"],"")
        self.assertEqual(preset.consonant["ん"],"")
        self.assertEqual(preset.consonant["息"],"")
        self.assertEqual(preset.consonant["吸"],"")
        self.assertEqual(preset.consonant["か"],"k")
        self.assertEqual(preset.consonant["さ"],"s")
        self.assertEqual(preset.consonant["た"],"t")
        self.assertEqual(preset.consonant["な"],"n")
        self.assertEqual(preset.consonant["は"],"h")
        self.assertEqual(len(preset.consonant),196)
        self.assertEqual(len(preset.consonant.keys()),34)

    def test_consonant_time(self):
        preset = Preset.Preset()
        self.assertEqual(preset.consonant_time[""],0)
        self.assertEqual(preset.consonant_time["k"],100)
        


