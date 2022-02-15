import unittest
import Oto

class Test_test_oto(unittest.TestCase):
    def test_str_default(self):
        oto = Oto.Oto("uta\あ.wav", "あ", 100, 200.0, 300.1, 400.123456789, -500)
        self.assertEqual(str(oto),"uta\あ.wav=あ,100,200.0,300.1,400.123456789,-500")
        
    def test_str_round_minus1(self):
        oto = Oto.Oto("uta\あ.wav", "あ", 100, 200.0, 300.1, 400.123456789, -500)
        oto.rounds = -1
        self.assertEqual(str(oto),"uta\あ.wav=あ,100,200.0,300.1,400.123456789,-500")

    def test_str_round1(self):
        oto = Oto.Oto("uta\あ.wav", "あ", 100, 200.0, 300.1, 400.123456789, -500)
        oto.rounds = 1
        self.assertEqual(str(oto),"uta\あ.wav=あ,100,200.0,300.1,400.1,-500")

    def test_str_round3(self):
        oto = Oto.Oto("uta\あ.wav", "あ", 100, 200.0, 300.1, 400.123456789, -500)
        oto.rounds = 3
        self.assertEqual(str(oto),"uta\あ.wav=あ,100,200.0,300.1,400.123,-500")
        
if __name__ == '__main__':
    unittest.main()