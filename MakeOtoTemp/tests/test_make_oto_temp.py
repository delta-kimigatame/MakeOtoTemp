import os.path
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
        
