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

    def test_param(self):
        preset = Preset.Preset()
        self.assertEqual(100,preset.tempo)
        self.assertEqual(800,preset.offset)
        self.assertEqual(2,preset.max)
        self.assertTrue(preset.under)
        self.assertTrue(preset.begining_cv)
        self.assertFalse(preset.nohead)
        self.assertFalse(preset.novcv)
        self.assertFalse(preset.only_consonant)

    def test_vowels(self):
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

    def test_consonant_time(self):
        preset = Preset.Preset()
        self.assertEqual(preset.consonant_time[""],0)
        self.assertEqual(preset.consonant_time["k"],100)
        self.assertEqual(len(preset.consonant_time.keys()),34)
        
        
class Test_test_read_preset(unittest.TestCase):
    def test_other_param(self):
        preset = Preset.Preset(os.path.join("tests","data","preset","other_param.ini"))
        self.assertEqual(120,preset.tempo)
        self.assertEqual(900,preset.offset)
        self.assertEqual(0,preset.max)
        self.assertFalse(preset.under)
        self.assertFalse(preset.begining_cv)
        self.assertFalse(preset.nohead)
        self.assertTrue(preset.novcv)
        self.assertTrue(preset.only_consonant)
        self.assertEqual(preset.vowel["a"],"a")
        self.assertEqual(len(preset.vowel),1)
        self.assertEqual(preset.consonant["a"],"a")
        self.assertEqual(len(preset.consonant),1)
        self.assertEqual(preset.consonant_time["a"],1)
        self.assertEqual(len(preset.replace),1)
        self.assertEqual(preset.replace[0][0],"あ")
        self.assertEqual(preset.replace[0][1],"a")
        
    def test_check_nohead_2(self):
        preset = Preset.Preset(os.path.join("tests","data","preset","check_nohead_2.ini"))
        self.assertFalse(preset.begining_cv)
        self.assertTrue(preset.nohead)
        
        
    def test_error_cp932(self):
        filename=os.path.join("tests","data","preset","cp932.ini")
        with self.assertRaises(UnicodeDecodeError) as cm:
            preset = Preset.Preset(filename)
        self.assertEqual(cm.exception.reason,"PRESET ERROR:" + filename + "の文字コードがutf-8ではないため、読み込みに失敗しました。")
            
    def test_error_tempo(self):
        filename=os.path.join("tests","data","preset","error_tempo.ini")
        with self.assertRaises(TypeError) as cm:
            preset = Preset.Preset(filename)
        self.assertEqual(cm.exception.args[0],"PRESET ERROR:" + filename + "の[TEMPO]に数字以外が入力されています。\n半角数字を入力してください。\n100,0")
            
    def test_error_tempo_zero(self):
        filename=os.path.join("tests","data","preset","error_tempo_zero.ini")
        with self.assertRaises(ValueError) as cm:
            preset = Preset.Preset(filename)
        self.assertEqual(cm.exception.args[0],"PRESET ERROR:" + filename + "の[TEMPO]に0以下の数字が入力されています。\n0")
        
    def test_error_offset(self):
        filename=os.path.join("tests","data","preset","error_offset.ini")
        with self.assertRaises(TypeError) as cm:
            preset = Preset.Preset(filename)
        self.assertEqual(cm.exception.args[0],"PRESET ERROR:" + filename + "の[OFFSET]に数字以外が入力されています。\n半角数字を入力してください。\n800,0")
            
    def test_error_offset_minus(self):
        filename=os.path.join("tests","data","preset","error_offset_minus.ini")
        with self.assertRaises(ValueError) as cm:
            preset = Preset.Preset(filename)
        self.assertEqual(cm.exception.args[0],"PRESET ERROR:" + filename + "の[OFFSET]に負の数字が入力されています。\n-1")
        
    def test_error_maxnum(self):
        filename=os.path.join("tests","data","preset","error_maxnum.ini")
        with self.assertRaises(TypeError) as cm:
            preset = Preset.Preset(filename)
        self.assertEqual(cm.exception.args[0],"PRESET ERROR:" + filename + "の[MAXNUM]に数字以外が入力されています。\n半角数字を入力してください。\na")
        
    def test_error_under(self):
        filename=os.path.join("tests","data","preset","error_under.ini")
        with self.assertRaises(TypeError) as cm:
            preset = Preset.Preset(filename)
        self.assertEqual(cm.exception.args[0],"PRESET ERROR:" + filename + "の[UNDER]に数字以外が入力されています。\n0か1を入力してください。\na")
        
    def test_error_nohead(self):
        filename=os.path.join("tests","data","preset","error_nohead.ini")
        with self.assertRaises(TypeError) as cm:
            preset = Preset.Preset(filename)
        self.assertEqual(cm.exception.args[0],"PRESET ERROR:" + filename + "の[NOHEAD]に数字以外が入力されています。\n0か1か2を入力してください。\na")
        
    def test_error_novcv(self):
        filename=os.path.join("tests","data","preset","error_novcv.ini")
        with self.assertRaises(TypeError) as cm:
            preset = Preset.Preset(filename)
        self.assertEqual(cm.exception.args[0],"PRESET ERROR:" + filename + "の[NOVCV]に数字以外が入力されています。\n0か1を入力してください。\na")
        
    def test_error_onlyconsonant(self):
        filename=os.path.join("tests","data","preset","error_onlyconsonant.ini")
        with self.assertRaises(TypeError) as cm:
            preset = Preset.Preset(filename)
        self.assertEqual(cm.exception.args[0],"PRESET ERROR:" + filename + "の[ONLYCONSONANT]に数字以外が入力されています。\n0か1を入力してください。\na")
        
        
    def test_error_vowel(self):
        filename=os.path.join("tests","data","preset","error_vowel.ini")
        with self.assertRaises(ValueError) as cm:
            preset = Preset.Preset(filename)
        self.assertEqual(cm.exception.args[0],"PRESET ERROR:" + filename + "の[VOWELS]に\"=\"が含まれていない行があります。\na")
        

    def test_error_consonant(self):
        filename=os.path.join("tests","data","preset","error_consonant.ini")
        with self.assertRaises(ValueError) as cm:
            preset = Preset.Preset(filename)
        self.assertEqual(cm.exception.args[0],"PRESET ERROR:" + filename + "の[CONSONANT]のフォーマットが正しくない行があります。\na=a")
        

    def test_error_replace(self):
        filename=os.path.join("tests","data","preset","error_replace.ini")
        with self.assertRaises(ValueError) as cm:
            preset = Preset.Preset(filename)
        self.assertEqual(cm.exception.args[0],"PRESET ERROR:" + filename + "の[REPLACE]に\"=\"が含まれていない行があります。\na")
        
