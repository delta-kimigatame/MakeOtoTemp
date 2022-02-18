import os.path
import codecs
import unittest
import MakeOtoTemp

class Test_test_get_record(unittest.TestCase):
    def test_input_txtfile_cp932(self):
        makeOtoTemp = MakeOtoTemp.MakeOtoTemp(os.path.join("tests","data","reclist","cp932.txt"))
        self.assertEqual(len(makeOtoTemp.reclist), 3)
        self.assertEqual(makeOtoTemp.reclist[0], "_ああいあうえあ")
        self.assertEqual(makeOtoTemp.reclist[1], "_いいうあえいえ")
        self.assertEqual(makeOtoTemp.reclist[2], "_うういおあおい")

    def test_input_txtfile_utf8(self):
        makeOtoTemp = MakeOtoTemp.MakeOtoTemp(os.path.join("tests","data","reclist","utf-8.txt"))
        self.assertEqual(len(makeOtoTemp.reclist), 3)
        self.assertEqual(makeOtoTemp.reclist[0], "_ああいあうえあ")
        self.assertEqual(makeOtoTemp.reclist[1], "_いいうあえいえ")
        self.assertEqual(makeOtoTemp.reclist[2], "_うういおあおい")

    def test_input_txtfile_other_encode_error(self):
        with self.assertRaises(UnicodeDecodeError) as cm:
            makeOtoTemp = MakeOtoTemp.MakeOtoTemp(os.path.join("tests","data","reclist","gb18030.txt"))
        self.assertEqual(cm.exception.reason,"RECLIST ERROR:" + os.path.join("tests","data","reclist","gb18030.txt") + "の文字コードが次のどちらでもないため、読み込みに失敗しました。cp932,utf-8")
        
    def test_input_dir(self):
        makeOtoTemp = MakeOtoTemp.MakeOtoTemp(os.path.join("tests","data","dummyvb","samplevb1"))
        self.assertEqual(len(makeOtoTemp.reclist), 3)
        self.assertEqual(makeOtoTemp.reclist[0], "_ああいあうえあ")
        self.assertEqual(makeOtoTemp.reclist[1], "_いいうあえいえ")
        self.assertEqual(makeOtoTemp.reclist[2], "_うういおあおい")

    def test_input_imagefile_error(self):
        with self.assertRaises(TypeError) as cm:
            makeOtoTemp = MakeOtoTemp.MakeOtoTemp(os.path.join("tests","data","reclist","image.bmp"))
        self.assertEqual(cm.exception.args[0],"RECLIST ERROR:" + os.path.join("tests","data","reclist","image.bmp") + "はテキストファイルでもフォルダでもないため、開けませんでした")
        
        
    def test_input_ignorefile_error(self):
        with self.assertRaises(FileNotFoundError) as cm:
            makeOtoTemp = MakeOtoTemp.MakeOtoTemp(os.path.join("tests","data","reclist","ignorefile"))
        self.assertEqual(cm.exception.args[0],"INPUT ERROR:"+ os.path.join("tests","data","reclist","ignorefile") + "は存在しません。")

        
class Test_test_make_oto_param(unittest.TestCase):
    def setUp(self) -> None:
        self.makeOtoTemp = MakeOtoTemp.MakeOtoTemp(os.path.join("tests","data","reclist","cp932.txt"))

    def test_makeoto_simple_VCV(self):
        self.makeOtoTemp.MakeOtoParam()
        self.assertEqual(len(self.makeOtoTemp.oto), 21)
        self.assertEqual(self.makeOtoTemp.oto[0].alias, "- あ")
        self.assertEqual(self.makeOtoTemp.oto[0].offset, 500)
        self.assertEqual(self.makeOtoTemp.oto[0].pre, 300)
        self.assertEqual(self.makeOtoTemp.oto[0].ove, 100)
        self.assertEqual(self.makeOtoTemp.oto[0].consonant, 450)
        self.assertEqual(self.makeOtoTemp.oto[0].blank, -700)
        self.assertEqual(self.makeOtoTemp.oto[0].filename, "_ああいあうえあ.wav")
        self.assertEqual(self.makeOtoTemp.oto[1].alias, "a あ")
        self.assertEqual(self.makeOtoTemp.oto[1].offset, 1100)
        self.assertEqual(self.makeOtoTemp.oto[1].pre, 300)
        self.assertEqual(self.makeOtoTemp.oto[1].ove, 100)
        self.assertEqual(self.makeOtoTemp.oto[1].consonant, 450)
        self.assertEqual(self.makeOtoTemp.oto[1].blank, -700)
        self.assertEqual(self.makeOtoTemp.oto[1].filename, "_ああいあうえあ.wav")
        self.assertEqual(self.makeOtoTemp.oto[7].alias, "- い")
        self.assertEqual(self.makeOtoTemp.oto[7].filename, "_いいうあえいえ.wav")
        self.assertEqual(self.makeOtoTemp.oto[7].filename, "_いいうあえいえ.wav")
        
    def test_makeoto_simple_VCV_other_tempo(self):
        self.makeOtoTemp.preset._tempo = 120
        self.makeOtoTemp.MakeOtoParam()
        self.assertEqual(len(self.makeOtoTemp.oto), 21)
        self.assertEqual(self.makeOtoTemp.oto[0].alias, "- あ")
        self.assertEqual(self.makeOtoTemp.oto[0].offset, 550)
        self.assertEqual(self.makeOtoTemp.oto[0].pre, 250)
        self.assertEqual(self.makeOtoTemp.oto[0].ove, 250/3)
        self.assertEqual(self.makeOtoTemp.oto[0].consonant, 375)
        self.assertEqual(self.makeOtoTemp.oto[0].blank, -500-250/3)
        self.assertEqual(self.makeOtoTemp.oto[0].filename, "_ああいあうえあ.wav")
        self.assertEqual(self.makeOtoTemp.oto[1].alias, "a あ")
        self.assertEqual(self.makeOtoTemp.oto[1].offset, 1050)
        self.assertEqual(self.makeOtoTemp.oto[1].pre, 250)
        self.assertEqual(self.makeOtoTemp.oto[1].ove, 250/3)
        self.assertEqual(self.makeOtoTemp.oto[1].consonant, 375)
        self.assertEqual(self.makeOtoTemp.oto[1].blank, -500-250/3)
        self.assertEqual(self.makeOtoTemp.oto[1].filename, "_ああいあうえあ.wav")

    def test_makeoto_simple_VCV_other_offset(self):
        self.makeOtoTemp.preset._offset = 1000
        self.makeOtoTemp.MakeOtoParam()
        self.assertEqual(len(self.makeOtoTemp.oto), 21)
        self.assertEqual(self.makeOtoTemp.oto[0].alias, "- あ")
        self.assertEqual(self.makeOtoTemp.oto[0].offset, 700)
        self.assertEqual(self.makeOtoTemp.oto[0].pre, 300)
        self.assertEqual(self.makeOtoTemp.oto[0].ove, 100)
        self.assertEqual(self.makeOtoTemp.oto[0].consonant, 450)
        self.assertEqual(self.makeOtoTemp.oto[0].blank, -700)
        self.assertEqual(self.makeOtoTemp.oto[0].filename, "_ああいあうえあ.wav")
        self.assertEqual(self.makeOtoTemp.oto[1].alias, "a あ")
        self.assertEqual(self.makeOtoTemp.oto[1].offset, 1300)
        self.assertEqual(self.makeOtoTemp.oto[1].pre, 300)
        self.assertEqual(self.makeOtoTemp.oto[1].ove, 100)
        self.assertEqual(self.makeOtoTemp.oto[1].consonant, 450)
        self.assertEqual(self.makeOtoTemp.oto[1].blank, -700)
        
    def test_makeoto_simple_VCV_no_begining_cv(self):
        self.makeOtoTemp.preset._begining_cv = False
        self.makeOtoTemp.MakeOtoParam()
        self.assertEqual(len(self.makeOtoTemp.oto), 21)
        self.assertEqual(self.makeOtoTemp.oto[0].alias, "あ")
        self.assertEqual(self.makeOtoTemp.oto[0].offset, 500)
        self.assertEqual(self.makeOtoTemp.oto[0].pre, 300)
        self.assertEqual(self.makeOtoTemp.oto[0].ove, 100)
        self.assertEqual(self.makeOtoTemp.oto[0].consonant, 450)
        self.assertEqual(self.makeOtoTemp.oto[0].blank, -700)
        self.assertEqual(self.makeOtoTemp.oto[0].filename, "_ああいあうえあ.wav")
        self.assertEqual(self.makeOtoTemp.oto[1].alias, "a あ")
        self.assertEqual(self.makeOtoTemp.oto[1].offset, 1100)
        self.assertEqual(self.makeOtoTemp.oto[1].pre, 300)
        self.assertEqual(self.makeOtoTemp.oto[1].ove, 100)
        self.assertEqual(self.makeOtoTemp.oto[1].consonant, 450)
        self.assertEqual(self.makeOtoTemp.oto[1].blank, -700)
        self.assertEqual(self.makeOtoTemp.oto[1].filename, "_ああいあうえあ.wav")
        self.assertEqual(self.makeOtoTemp.oto[7].alias, "い")
        self.assertEqual(self.makeOtoTemp.oto[7].filename, "_いいうあえいえ.wav")
        self.assertEqual(self.makeOtoTemp.oto[7].filename, "_いいうあえいえ.wav")
        
    def test_makeoto_simple_VCV_no_head(self):
        self.makeOtoTemp.preset._nohead = True
        self.makeOtoTemp.MakeOtoParam()
        self.assertEqual(len(self.makeOtoTemp.oto), 18)
        self.assertEqual(self.makeOtoTemp.oto[0].alias, "a あ")
        self.assertEqual(self.makeOtoTemp.oto[0].offset, 1100)
        self.assertEqual(self.makeOtoTemp.oto[0].pre, 300)
        self.assertEqual(self.makeOtoTemp.oto[0].ove, 100)
        self.assertEqual(self.makeOtoTemp.oto[0].consonant, 450)
        self.assertEqual(self.makeOtoTemp.oto[0].blank, -700)
        self.assertEqual(self.makeOtoTemp.oto[0].filename, "_ああいあうえあ.wav")
        
    def test_makeoto_simple_VCV_novcv(self):
        self.makeOtoTemp.preset._novcv = True
        self.makeOtoTemp.MakeOtoParam()
        self.assertEqual(len(self.makeOtoTemp.oto), 0)
        
    def test_makeoto_simple_VCV_novcv_no_begining_cv(self):
        self.makeOtoTemp.preset._novcv = True
        self.makeOtoTemp.preset._begining_cv = False
        self.makeOtoTemp.MakeOtoParam()
        self.assertEqual(len(self.makeOtoTemp.oto), 3)
        self.assertEqual(self.makeOtoTemp.oto[0].alias, "あ")
        self.assertEqual(self.makeOtoTemp.oto[0].offset, 500)
        self.assertEqual(self.makeOtoTemp.oto[0].pre, 300)
        self.assertEqual(self.makeOtoTemp.oto[0].ove, 100)
        self.assertEqual(self.makeOtoTemp.oto[0].consonant, 450)
        self.assertEqual(self.makeOtoTemp.oto[0].blank, -700)
        self.assertEqual(self.makeOtoTemp.oto[0].filename, "_ああいあうえあ.wav")
        self.assertEqual(self.makeOtoTemp.oto[1].alias, "い")
        self.assertEqual(self.makeOtoTemp.oto[1].filename, "_いいうあえいえ.wav")

    def test_makeoto_simple_CVVC(self):
        self.makeOtoTemp._reclist=["_かかきかくけか"]
        self.makeOtoTemp.MakeOtoParam()
        self.assertEqual(len(self.makeOtoTemp.oto), 13)
        self.assertEqual(self.makeOtoTemp.oto[0].alias, "- か")
        self.assertEqual(self.makeOtoTemp.oto[0].offset, 700)
        self.assertEqual(self.makeOtoTemp.oto[0].pre, 100)
        self.assertEqual(self.makeOtoTemp.oto[0].ove, 100/3)
        self.assertEqual(self.makeOtoTemp.oto[0].consonant, 150)
        self.assertEqual(self.makeOtoTemp.oto[0].blank, -600)
        self.assertEqual(self.makeOtoTemp.oto[0].filename, "_かかきかくけか.wav")
        self.assertEqual(self.makeOtoTemp.oto[1].alias, "a k")
        self.assertEqual(self.makeOtoTemp.oto[1].offset, 1000)
        self.assertEqual(self.makeOtoTemp.oto[1].pre, 300)
        self.assertEqual(self.makeOtoTemp.oto[1].ove, 100)
        self.assertEqual(self.makeOtoTemp.oto[1].consonant, 350)
        self.assertEqual(self.makeOtoTemp.oto[1].blank, -375)
        self.assertEqual(self.makeOtoTemp.oto[1].filename, "_かかきかくけか.wav")
        self.assertEqual(self.makeOtoTemp.oto[2].alias, "か")
        self.assertEqual(self.makeOtoTemp.oto[2].offset, 1300)
        self.assertEqual(self.makeOtoTemp.oto[2].pre, 100)
        self.assertEqual(self.makeOtoTemp.oto[2].ove, 100/3)
        self.assertEqual(self.makeOtoTemp.oto[2].consonant, 150)
        self.assertEqual(self.makeOtoTemp.oto[2].blank, -600)
        self.assertEqual(self.makeOtoTemp.oto[2].filename, "_かかきかくけか.wav")
        
    def test_makeoto_simple_CVVC_other_consonant(self):
        #各パラメータが子音の設定値を読んでいることの確認
        self.makeOtoTemp._reclist=["_ささしさすせさ"]
        self.makeOtoTemp.MakeOtoParam()
        self.assertEqual(len(self.makeOtoTemp.oto), 13)
        self.assertEqual(self.makeOtoTemp.oto[0].alias, "- さ")
        self.assertEqual(self.makeOtoTemp.oto[0].offset, 650)
        self.assertEqual(self.makeOtoTemp.oto[0].pre, 150)
        self.assertEqual(self.makeOtoTemp.oto[0].ove, 150/3)
        self.assertEqual(self.makeOtoTemp.oto[0].consonant, 150*1.5)
        self.assertEqual(self.makeOtoTemp.oto[0].blank, -550)
        self.assertEqual(self.makeOtoTemp.oto[0].filename, "_ささしさすせさ.wav")
        self.assertEqual(self.makeOtoTemp.oto[1].alias, "a s")
        self.assertEqual(self.makeOtoTemp.oto[1].offset, 950)
        self.assertEqual(self.makeOtoTemp.oto[1].pre, 300)
        self.assertEqual(self.makeOtoTemp.oto[1].ove, 100)
        self.assertEqual(self.makeOtoTemp.oto[1].consonant, 300+150/2)
        self.assertEqual(self.makeOtoTemp.oto[1].blank, -300-150/4*3)
        self.assertEqual(self.makeOtoTemp.oto[1].filename, "_ささしさすせさ.wav")
        self.assertEqual(self.makeOtoTemp.oto[2].alias, "さ")
        self.assertEqual(self.makeOtoTemp.oto[2].offset, 1250)
        self.assertEqual(self.makeOtoTemp.oto[0].pre, 150)
        self.assertEqual(self.makeOtoTemp.oto[0].ove, 150/3)
        self.assertEqual(self.makeOtoTemp.oto[0].consonant, 150*1.5)
        self.assertEqual(self.makeOtoTemp.oto[2].blank, -550)
        self.assertEqual(self.makeOtoTemp.oto[2].filename, "_ささしさすせさ.wav")
        
    def test_makeoto_simple_CVVC_no_begining_cv(self):
        self.makeOtoTemp.preset._begining_cv = False
        self.makeOtoTemp._reclist=["_かかきかくけか"]
        self.makeOtoTemp.MakeOtoParam()
        self.assertEqual(len(self.makeOtoTemp.oto), 13)
        self.assertEqual(self.makeOtoTemp.oto[0].alias, "か")
        self.assertEqual(self.makeOtoTemp.oto[0].offset, 700)
        self.assertEqual(self.makeOtoTemp.oto[0].pre, 100)
        self.assertEqual(self.makeOtoTemp.oto[0].ove, 100/3)
        self.assertEqual(self.makeOtoTemp.oto[0].consonant, 150)
        self.assertEqual(self.makeOtoTemp.oto[0].blank, -600)
        self.assertEqual(self.makeOtoTemp.oto[0].filename, "_かかきかくけか.wav")
        self.assertEqual(self.makeOtoTemp.oto[1].alias, "a k")
        self.assertEqual(self.makeOtoTemp.oto[1].offset, 1000)
        self.assertEqual(self.makeOtoTemp.oto[1].pre, 300)
        self.assertEqual(self.makeOtoTemp.oto[1].ove, 100)
        self.assertEqual(self.makeOtoTemp.oto[1].consonant, 350)
        self.assertEqual(self.makeOtoTemp.oto[1].blank, -375)
        self.assertEqual(self.makeOtoTemp.oto[1].filename, "_かかきかくけか.wav")
        self.assertEqual(self.makeOtoTemp.oto[2].alias, "か")
        self.assertEqual(self.makeOtoTemp.oto[2].offset, 1300)
        self.assertEqual(self.makeOtoTemp.oto[2].pre, 100)
        self.assertEqual(self.makeOtoTemp.oto[2].ove, 100/3)
        self.assertEqual(self.makeOtoTemp.oto[2].consonant, 150)
        self.assertEqual(self.makeOtoTemp.oto[2].blank, -600)
        self.assertEqual(self.makeOtoTemp.oto[2].filename, "_かかきかくけか.wav")

    def test_makeoto_simple_CVVC_nohead(self):
        self.makeOtoTemp.preset._nohead = True
        self.makeOtoTemp._reclist=["_かかきかくけか"]
        self.makeOtoTemp.MakeOtoParam()
        self.assertEqual(len(self.makeOtoTemp.oto), 12)
        self.assertEqual(self.makeOtoTemp.oto[0].alias, "a k")
        self.assertEqual(self.makeOtoTemp.oto[0].offset, 1000)
        self.assertEqual(self.makeOtoTemp.oto[0].pre, 300)
        self.assertEqual(self.makeOtoTemp.oto[0].ove, 100)
        self.assertEqual(self.makeOtoTemp.oto[0].consonant, 350)
        self.assertEqual(self.makeOtoTemp.oto[0].blank, -375)
        self.assertEqual(self.makeOtoTemp.oto[0].filename, "_かかきかくけか.wav")
        self.assertEqual(self.makeOtoTemp.oto[1].alias, "か")
        self.assertEqual(self.makeOtoTemp.oto[1].offset, 1300)
        self.assertEqual(self.makeOtoTemp.oto[1].pre, 100)
        self.assertEqual(self.makeOtoTemp.oto[1].ove, 100/3)
        self.assertEqual(self.makeOtoTemp.oto[1].consonant, 150)
        self.assertEqual(self.makeOtoTemp.oto[1].blank, -600)
        self.assertEqual(self.makeOtoTemp.oto[1].filename, "_かかきかくけか.wav")
        
    def test_makeoto_simple_CVVC_onlyconsonant(self):
        self.makeOtoTemp.preset._only_consonant= True
        self.makeOtoTemp._reclist=["_かかきかくけか"]
        self.makeOtoTemp.MakeOtoParam()
        self.assertEqual(len(self.makeOtoTemp.oto), 19)
        self.assertEqual(self.makeOtoTemp.oto[0].alias, "- か")
        self.assertEqual(self.makeOtoTemp.oto[0].offset, 700)
        self.assertEqual(self.makeOtoTemp.oto[0].pre, 100)
        self.assertEqual(self.makeOtoTemp.oto[0].ove, 100/3)
        self.assertEqual(self.makeOtoTemp.oto[0].consonant, 150)
        self.assertEqual(self.makeOtoTemp.oto[0].blank, -600)
        self.assertEqual(self.makeOtoTemp.oto[0].filename, "_かかきかくけか.wav")
        self.assertEqual(self.makeOtoTemp.oto[1].alias, "a k")
        self.assertEqual(self.makeOtoTemp.oto[1].offset, 1000)
        self.assertEqual(self.makeOtoTemp.oto[1].pre, 300)
        self.assertEqual(self.makeOtoTemp.oto[1].ove, 100)
        self.assertEqual(self.makeOtoTemp.oto[1].consonant, 350)
        self.assertEqual(self.makeOtoTemp.oto[1].blank, -375)
        self.assertEqual(self.makeOtoTemp.oto[1].filename, "_かかきかくけか.wav")
        self.assertEqual(self.makeOtoTemp.oto[2].alias, "か")
        self.assertEqual(self.makeOtoTemp.oto[2].offset, 1300)
        self.assertEqual(self.makeOtoTemp.oto[2].pre, 100)
        self.assertEqual(self.makeOtoTemp.oto[2].ove, 100/3)
        self.assertEqual(self.makeOtoTemp.oto[2].consonant, 150)
        self.assertEqual(self.makeOtoTemp.oto[2].blank, -600)
        self.assertEqual(self.makeOtoTemp.oto[2].filename, "_かかきかくけか.wav")
        self.assertEqual(self.makeOtoTemp.oto[3].alias, "k")
        self.assertEqual(self.makeOtoTemp.oto[3].offset, 1300)
        self.assertEqual(self.makeOtoTemp.oto[3].pre, 100*0.3)
        self.assertEqual(self.makeOtoTemp.oto[3].ove, 100*0.1)
        self.assertEqual(self.makeOtoTemp.oto[3].consonant, 100*0.5)
        self.assertEqual(self.makeOtoTemp.oto[3].blank, -100)
        self.assertEqual(self.makeOtoTemp.oto[3].filename, "_かかきかくけか.wav")
        
    def test_makeoto_nodokiri_CVVC(self):
        #喉切によるCVの置き換え例外の確認
        self.makeOtoTemp._reclist=["_あ・あ・い・あ・う・え・あ"]
        self.makeOtoTemp.MakeOtoParam()
        self.assertEqual(len(self.makeOtoTemp.oto), 13)
        self.assertEqual(self.makeOtoTemp.oto[0].alias, "- あ")
        self.assertEqual(self.makeOtoTemp.oto[0].offset, 500)
        self.assertEqual(self.makeOtoTemp.oto[0].pre, 300)
        self.assertEqual(self.makeOtoTemp.oto[0].ove, 100)
        self.assertEqual(self.makeOtoTemp.oto[0].consonant, 450)
        self.assertEqual(self.makeOtoTemp.oto[0].blank, -700)
        self.assertEqual(self.makeOtoTemp.oto[0].filename, "_あ・あ・い・あ・う・え・あ.wav")
        self.assertEqual(self.makeOtoTemp.oto[1].alias, "a ・")
        self.assertEqual(self.makeOtoTemp.oto[1].offset, 1050)
        self.assertEqual(self.makeOtoTemp.oto[1].pre, 300)
        self.assertEqual(self.makeOtoTemp.oto[1].ove, 100)
        self.assertEqual(self.makeOtoTemp.oto[1].consonant, 325)
        self.assertEqual(self.makeOtoTemp.oto[1].blank, -300-50/4*3)
        self.assertEqual(self.makeOtoTemp.oto[1].filename, "_あ・あ・い・あ・う・え・あ.wav")
        self.assertEqual(self.makeOtoTemp.oto[2].alias, "・ あ")
        self.assertEqual(self.makeOtoTemp.oto[2].offset, 1350)
        self.assertEqual(self.makeOtoTemp.oto[2].pre, 50)
        self.assertEqual(self.makeOtoTemp.oto[2].ove, 50/3)
        self.assertEqual(self.makeOtoTemp.oto[2].consonant, 75)
        self.assertEqual(self.makeOtoTemp.oto[2].blank, -650)
        self.assertEqual(self.makeOtoTemp.oto[2].filename, "_あ・あ・い・あ・う・え・あ.wav")
        
    def test_makeoto_underbar_default(self):
        self.makeOtoTemp._reclist=["_あ_あ_い_あ"]
        self.makeOtoTemp.MakeOtoParam()
        self.assertEqual(len(self.makeOtoTemp.oto), 4)
        self.assertEqual(self.makeOtoTemp.oto[0].alias, "- あ")
        self.assertEqual(self.makeOtoTemp.oto[0].offset, 500)
        self.assertEqual(self.makeOtoTemp.oto[0].pre, 300)
        self.assertEqual(self.makeOtoTemp.oto[0].ove, 100)
        self.assertEqual(self.makeOtoTemp.oto[0].consonant, 450)
        self.assertEqual(self.makeOtoTemp.oto[0].blank, -700)
        self.assertEqual(self.makeOtoTemp.oto[0].filename, "_あ_あ_い_あ.wav")
        self.assertEqual(self.makeOtoTemp.oto[1].alias, "- あ")
        self.assertEqual(self.makeOtoTemp.oto[1].offset, 1700)
        self.assertEqual(self.makeOtoTemp.oto[1].pre, 300)
        self.assertEqual(self.makeOtoTemp.oto[1].ove, 100)
        self.assertEqual(self.makeOtoTemp.oto[1].consonant, 450)
        self.assertEqual(self.makeOtoTemp.oto[1].blank, -700)
        self.assertEqual(self.makeOtoTemp.oto[1].filename, "_あ_あ_い_あ.wav")
        self.assertEqual(self.makeOtoTemp.oto[2].alias, "- い")
        self.assertEqual(self.makeOtoTemp.oto[2].offset, 2900)
        self.assertEqual(self.makeOtoTemp.oto[2].filename, "_あ_あ_い_あ.wav")
        
    def test_makeoto_underbar_pass(self):
        self.makeOtoTemp._reclist=["_あ_あ_い_あ"]
        self.makeOtoTemp.preset._under = False
        self.makeOtoTemp.MakeOtoParam()
        self.assertEqual(len(self.makeOtoTemp.oto), 4)
        self.assertEqual(self.makeOtoTemp.oto[0].alias, "- あ")
        self.assertEqual(self.makeOtoTemp.oto[0].offset, 500)
        self.assertEqual(self.makeOtoTemp.oto[0].pre, 300)
        self.assertEqual(self.makeOtoTemp.oto[0].ove, 100)
        self.assertEqual(self.makeOtoTemp.oto[0].consonant, 450)
        self.assertEqual(self.makeOtoTemp.oto[0].blank, -700)
        self.assertEqual(self.makeOtoTemp.oto[0].filename, "_あ_あ_い_あ.wav")
        self.assertEqual(self.makeOtoTemp.oto[1].alias, "a あ")
        self.assertEqual(self.makeOtoTemp.oto[1].offset, 1100)
        self.assertEqual(self.makeOtoTemp.oto[1].pre, 300)
        self.assertEqual(self.makeOtoTemp.oto[1].ove, 100)
        self.assertEqual(self.makeOtoTemp.oto[1].consonant, 450)
        self.assertEqual(self.makeOtoTemp.oto[1].blank, -700)
        self.assertEqual(self.makeOtoTemp.oto[1].filename, "_あ_あ_い_あ.wav")
        self.assertEqual(self.makeOtoTemp.oto[2].alias, "a い")
        self.assertEqual(self.makeOtoTemp.oto[2].offset, 1700)
        self.assertEqual(self.makeOtoTemp.oto[2].filename, "_あ_あ_い_あ.wav")

class Test_test_make_oto_param_eng(unittest.TestCase):
    def setUp(self) -> None:
        self.makeOtoTemp = MakeOtoTemp.MakeOtoTemp(os.path.join("tests","data","reclist","cp932.txt"),os.path.join("tests","data","preset","delta_eng_g05.ini"))

    def test_makeoto_onset_consonant_cluster(self):
        #期待する動作ではないが、前方互換性
        #単体の@が出るのは期待する動作ではないが、前方互換性
        #maxnumで最終的にいい感じになる
        self.makeOtoTemp._reclist=["_pr@_pr@-"]
        self.makeOtoTemp.MakeOtoParam()
        self.assertEqual(len(self.makeOtoTemp.oto), 5)
        self.assertEqual(self.makeOtoTemp.oto[0].alias, "- pr")
        self.assertEqual(self.makeOtoTemp.oto[1].alias, "- @")
        self.assertEqual(self.makeOtoTemp.oto[2].alias, "pr")
        self.assertEqual(self.makeOtoTemp.oto[3].alias, "- @")
        self.assertEqual(self.makeOtoTemp.oto[4].alias, "@ -")
        
    def test_makeoto_onset_consonant_cluster_no_begining_cv(self):
        #子音群はbegining_cvの影響を受けない
        #単体の@が出るのは期待する動作ではないが、前方互換性
        #maxnumで最終的にいい感じになる
        self.makeOtoTemp._reclist=["_skr@_skr@-"]
        self.makeOtoTemp.preset._begining_cv = False
        self.makeOtoTemp.MakeOtoParam()
        self.assertEqual(len(self.makeOtoTemp.oto), 5)
        self.assertEqual(self.makeOtoTemp.oto[0].alias, "- skr")
        self.assertEqual(self.makeOtoTemp.oto[1].alias, "@")
        self.assertEqual(self.makeOtoTemp.oto[2].alias, "skr")
        self.assertEqual(self.makeOtoTemp.oto[3].alias, "@")
        self.assertEqual(self.makeOtoTemp.oto[4].alias, "@ -")
        
    def test_makeoto_onset_consonant_cluster3(self):
        #期待する動作ではないが、前方互換性
        #単体の@が出るのは期待する動作ではないが、前方互換性
        #maxnumで最終的にいい感じになる
        self.makeOtoTemp._reclist=["_pr@_pr@-"]
        self.makeOtoTemp.MakeOtoParam()
        self.assertEqual(len(self.makeOtoTemp.oto), 5)
        self.assertEqual(self.makeOtoTemp.oto[0].alias, "- pr")
        self.assertEqual(self.makeOtoTemp.oto[1].alias, "- @")
        self.assertEqual(self.makeOtoTemp.oto[2].alias, "pr")
        self.assertEqual(self.makeOtoTemp.oto[3].alias, "- @")
        self.assertEqual(self.makeOtoTemp.oto[4].alias, "@ -")

    def test_makeoto_coda_consonant_cluster(self):
        self.makeOtoTemp._reclist=["_@_bd-"]
        self.makeOtoTemp.MakeOtoParam()
        self.assertEqual(len(self.makeOtoTemp.oto), 2)
        self.assertEqual(self.makeOtoTemp.oto[0].alias, "- @")
        self.assertEqual(self.makeOtoTemp.oto[1].alias, "b d-")
        
    def test_makeoto_coda_consonant_cluster3(self):
        self.makeOtoTemp._reclist=["_@_dnt-"]
        self.makeOtoTemp.MakeOtoParam()
        self.assertEqual(len(self.makeOtoTemp.oto), 2)
        self.assertEqual(self.makeOtoTemp.oto[0].alias, "- @")
        self.assertEqual(self.makeOtoTemp.oto[1].alias, "d nt-")
        
    def test_makeoto_replace(self):
        self.makeOtoTemp._reclist=["_s+i_s+i_s+-"]
        self.makeOtoTemp.MakeOtoParam()
        self.assertEqual(len(self.makeOtoTemp.oto), 5)
        self.assertEqual(self.makeOtoTemp.oto[0].alias, "- Si")
        self.assertEqual(self.makeOtoTemp.oto[1].alias, "i S")
        self.assertEqual(self.makeOtoTemp.oto[2].alias, "Si")
        self.assertEqual(self.makeOtoTemp.oto[3].alias, "S")
        self.assertEqual(self.makeOtoTemp.oto[4].alias, "i S-")

class Test_test_write_oto(unittest.TestCase):
    def setUp(self) -> None:
        self.makeOtoTemp = MakeOtoTemp.MakeOtoTemp(os.path.join("tests","data","reclist","cp932.txt"))

    def test_write_oto(self):
        self.makeOtoTemp.MakeOtoParam()
        self.makeOtoTemp.WriteOto()
        with codecs.open("oto.ini", "r", "cp932") as fr:
            writed_data = fr.read().split("\r\n")
        self.assertEqual(len(writed_data),21)
        self.assertEqual(writed_data[0], str(self.makeOtoTemp.oto[0]))

    def test_write_oto_maxnum2(self):
        self.makeOtoTemp._reclist=["_ああいあうえあ","_ああいあうえあ","_ああいあうえあ"]
        self.makeOtoTemp.MakeOtoParam()
        self.makeOtoTemp.WriteOto()
        with codecs.open("oto.ini", "r", "cp932") as fr:
            writed_data = fr.read().split("\r\n")
        self.assertEqual(len(writed_data),14)
        self.assertEqual(writed_data[0], str(self.makeOtoTemp.oto[0]))
        self.assertTrue("- あ2" in writed_data[7])
        

    def test_write_oto_maxnum1(self):
        self.makeOtoTemp._reclist=["_ああいあうえあ","_ああいあうえあ","_ああいあうえあ"]
        self.makeOtoTemp.preset._max = 1
        self.makeOtoTemp.MakeOtoParam()
        self.makeOtoTemp.WriteOto()
        with codecs.open("oto.ini", "r", "cp932") as fr:
            writed_data = fr.read().split("\r\n")
        self.assertEqual(len(writed_data),7)
        self.assertEqual(writed_data[0], str(self.makeOtoTemp.oto[0]))

    def test_write_oto_maxnum3(self):
        self.makeOtoTemp._reclist=["_ああいあうえあ","_ああいあうえあ","_ああいあうえあ"]
        self.makeOtoTemp.preset._max = 3
        self.makeOtoTemp.MakeOtoParam()
        self.makeOtoTemp.WriteOto()
        with codecs.open("oto.ini", "r", "cp932") as fr:
            writed_data = fr.read().split("\r\n")
        self.assertEqual(len(writed_data),21)
        self.assertEqual(writed_data[0], str(self.makeOtoTemp.oto[0]))
        self.assertTrue("- あ2" in writed_data[7])
        self.assertTrue("- あ3" in writed_data[14])