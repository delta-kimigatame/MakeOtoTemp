import os
import os.path
import codecs

class Preset:
    '''
    MakeOtoTempのプリセットファイルを扱う
    
    Attributes
    ----------
    tempo :float
        収録のbpm
    offset :float
        録音の開始時間(ms)
    max :int
        同じエイリアスをいくつ生成するか
    under :int
        アンダーバーの扱い
        0だと無視、1だと休符扱いにします。
    nohead :int
        wavの頭のエイリアス生成規則
        0だと[- CV]を生成
        1だと[CV]を生成
        2だとwavの頭からは生成しません。
    novcv :int
        [V CV]の生成規則
        0で生成
        1で生成しない
    only_consonant :int
        [C]の生成規則
        0で生成しない
        1で生成する
    vowel :dict
        母音のバリエーションを指定
    consonant :dict
        子音のバリエーションを指定
    consonant_time :dict
        子音の標準長さをmsで指定
    replace :list
        ファイル名とエイリアスの置換を指定
    '''

    __tempo :float
    __offset :float
    __max :int
    __under :int
    __nohead :int
    __novcv :int
    __only_consonant :int
    __vowel :dict
    __consonant :dict
    __consonant_time :dict
    __replace :list

    @property
    def tempo(self) -> float:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        tempo :float
            収録のbpm
        '''
        return self.__tempo
    
    @property
    def offset(self) -> float:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        offset :float
            録音の開始時間(ms)
        '''
        return self.__offset

    @property
    def max(self) -> int:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        max :int
            同じエイリアスをいくつ生成するか
        '''
        return self.__max
    
    @property
    def under(self) -> int:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        under :int
            アンダーバーの扱い
            0だと無視、1だと休符扱いにします。
        '''
        return self.__under
    
    @property
    def nohead(self) -> int:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        nohead :int
            wavの頭のエイリアス生成規則
            0だと[- CV]を生成
            1だと[CV]を生成
            2だとwavの頭からは生成しません。
        '''
        return self.__nohead
    
    @property
    def novcv(self) -> int:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        novcv :int
            [V CV]の生成規則
            0で生成
            1で生成しない
        '''
        return self.__novcv

    @property
    def only_consonant(self) -> int:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        only_consonant :bool
            [C]の生成規則
            0で生成しない
            1で生成する
        '''
        return self.__only_consonant
    
    @property
    def vowel(self) -> dict:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        vowel :dict
            母音のバリエーションを指定
            keyはCVに後方一致する文字列
            valueは[V CV]の前半のVに当たる文字列
        '''
        return self.__vowel
    
    @property
    def consonant(self) -> dict:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        consonant :dict
            子音のバリエーションを指定
            keyは[CV]に完全一致する文字列
            valueは子音の[V C]のときのCにあたる文字列

            valueが""のものは、連続音のみを生成する例外
            valueが"・"のものは"・ "に置き換えて適用(eve式喉切母音の例外)
        '''
        return self.__consonant
    
    @property
    def consonant_time(self) -> dict:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        consonant_time :dict
            子音の標準長さをmsで指定
            keyは子音にあたる文字列
            valueは長さ(ms)
        '''
        return self.__consonant_time

    @property
    def replace(self) -> list:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        replace :list
            ファイル名とエイリアスの置換を指定
            keyは変換前の文字、valueは変換後の文字
        '''
        return self.__replace


    @staticmethod
    def Make(filename :str = "mkototemp.ini"):
        '''
        デフォルト値でプリセットファイルを作成します。

        Parameters
        ----------
        filename :str ,default "mkototemp.ini"
            実行ファイルからの相対パス
        '''

        line :list =[]
        line.append("[TEMPO]")
        line.append("100")
        line.append("[OFFSET]")
        line.append("800")
        line.append("[MAXNUM]")
        line.append("2")
        line.append("[UNDER]")
        line.append("1")
        line.append("[NOHEAD]")
        line.append("0")
        line.append("[NOVCV]")
        line.append("0")
        line.append("[ONLYCONSONANT]")
        line.append("0")
        line.append("[VOWEL]")
        line.append("a=ぁ,あ,か,が,さ,ざ,た,だ,な,は,ば,ぱ,ま,ゃ,や,ら,わ,ァ,ア,カ,ガ,サ,ザ,タ,ダ,ナ,ハ,バ,パ,マ,ャ,ヤ,ラ,ワ")
        line.append("e=ぇ,え,け,げ,せ,ぜ,て,で,ね,へ,べ,ぺ,め,れ,ゑ,ェ,エ,ケ,ゲ,セ,ゼ,テ,デ,ネ,ヘ,ベ,ペ,メ,レ,ヱ")
        line.append("i=ぃ,い,き,ぎ,し,じ,ち,ぢ,に,ひ,び,ぴ,み,り,ゐ,ィ,イ,キ,ギ,シ,ジ,チ,ヂ,ニ,ヒ,ビ,ピ,ミ,リ,ヰ")
        line.append("o=ぉ,お,こ,ご,そ,ぞ,と,ど,の,ほ,ぼ,ぽ,も,ょ,よ,ろ,を,ォ,オ,コ,ゴ,ソ,ゾ,ト,ド,ノ,ホ,ボ,ポ,モ,ョ,ヨ,ロ,ヲ")
        line.append("n=ん,ン")
        line.append("u=ぅ,う,く,ぐ,す,ず,つ,づ,ぬ,ふ,ぶ,ぷ,む,ゅ,ゆ,る,ゥ,ウ,ク,グ,ス,ズ,ツ,ヅ,ヌ,フ,ブ,プ,ム,ュ,ユ,ル,ヴ")
        line.append("[CONSONANT]")
        line.append("=あ,い,う,え,お,ん,息,吸=0")
        line.append("ch=ch,ち,ちぇ,ちゃ,ちゅ,ちょ=150")
        line.append("gy=gy,ぎ,ぎぇ,ぎゃ,ぎゅ,ぎょ=60")
        line.append("ts=ts,つ,つぁ,つぃ,つぇ,つぉ=170")
        line.append("ty=ty,てぃ,てぇ,てゃ,てゅ,てょ=75")
        line.append("py=py,ぴ,ぴぇ,ぴゃ,ぴゅ,ぴょ=100")
        line.append("ry=ry,り,りぇ,りゃ,りゅ,りょ=70")
        line.append("ny=ny,に,にぇ,にゃ,にゅ,にょ=70")
        line.append("r=r,ら,る,れ,ろ=70")
        line.append("hy=hy,ひ,ひぇ,ひゃ,ひゅ,ひょ=100")
        line.append("dy=dy,でぃ,でぇ,でゃ,でゅ,でょ=75")
        line.append("by=by,び,びぇ,びゃ,びゅ,びょ=45")
        line.append("b=b,ば,ぶ,べ,ぼ=50")
        line.append("d=d,だ,で,ど,どぅ=60")
        line.append("g=g,が,ぐ,げ,ご=80")
        line.append("f=f,ふ,ふぁ,ふぃ,ふぇ,ふぉ=130")
        line.append("h=h,は,へ,ほ=110")
        line.append("k=k,か,く,け,こ=100")
        line.append("j=j,じ,じぇ,じゃ,じゅ,じょ=110")
        line.append("m=m,ま,む,め,も=75")
        line.append("n=n,な,ぬ,ね,の=70")
        line.append("p=p,ぱ,ぷ,ぺ,ぽ=100")
        line.append("s=s,さ,す,すぃ,せ,そ=150")
        line.append("sh=sh,し,しぇ,しゃ,しゅ,しょ=200")
        line.append("t=t,た,て,と,とぅ=100")
        line.append("w=w,うぃ,うぅ,うぇ,うぉ,わ,を=50")
        line.append("v=v,ヴ,ヴぁ,ヴぃ,ヴぅ,ヴぇ,ヴぉ=100")
        line.append("y=y,いぃ,いぇ,や,ゆ,よ,ゐ,ゑ=30")
        line.append("ky=ky,き,きぇ,きゃ,きゅ,きょ=130")
        line.append("z=z,ざ,ず,ずぃ,ぜ,ぞ=80")
        line.append("my=my,み,みぇ,みゃ,みゅ,みょ=60")
        line.append("ng=ガ,グ,ゲ,ゴ=50")
        line.append("ngy=ギャ,ギ,ギュ,ギェ,ギョ=40")
        line.append("・=・あ,・い,・う,・え,・お,・ん=50")

        with codecs.open(filename, "w", "utf-8") as fw:
            fw.write("\r\n".join(line))


    def __init__(self, filename: str = "mkototemp.ini"):
        '''
        filenameのプリセットを読み込む。
        もしfilenameにプリセットが存在しない場合、デフォルトプリセットを作成し読み込む。

        Parameters
        ----------
        filename :str ,default "mkototemp.ini"
            実行ファイルからの相対パス
        '''

        if not os.path.isfile(filename):
            self.Make(filename)

        self.__tempo = 100
        self.__offset = 800
        self.__max = 2
        self.__under = 1
        self.__nohead = 0
        self.__novcv = 0
        self.__only_consonant = 0
        self.__vowel = {}
        self.__consonant = {}
        self.__consonant_time = {}
        self.__replace = []

        self.__Read(filename)

    @staticmethod
    def __InitEntries() -> list:
        '''
        presetのエントリーを定義する

        Returns
        -------
        entries :list
            [TEMPO]、[VOWEL]などのエントリー文字列のリスト
        '''
        entries :list = []
        entries.append("[TEMPO]")
        entries.append("[OFFSET]")
        entries.append("[MAXNUM]")
        entries.append("[UNDER]")
        entries.append("[NOHEAD]")
        entries.append("[NOVCV]")
        entries.append("[ONLYCONSONANT]")
        entries.append("[VOWEL]")
        entries.append("[CONSONANT]")
        entries.append("[REPLACE]")
        return entries

    def __Read(self, filename: str = "mkototemp.ini"):
        '''
        filenameのプリセットを読み込む。
        filenameの有無は事前にチェック済みのものとする。
        各パラメータは事前に初期化済みとする。

        Parameters
        ----------
        filename :str ,default "mkototemp.ini"
            実行ファイルからの相対パス
        '''
        mode :str = ""
        data :str
        lines :str
        line : str
        entry : list

        entry = self.__InitEntries()

        with codecs.open(filename, "r", "utf-8") as fr:
            data = fr.read()
        lines = data.replace("\r","").split("\n")

        for line in lines:
            if line == "":
                continue

            if line in entry:
                mode = line.replace("[","").replace("]","")
                continue

            if mode == "TEMPO":
                self.__tempo = float(line)
            elif mode == "OFFSET":
                self.__offset = float(line)
            elif mode == "MAXNUM":
                self.__max = int(line)
            elif mode == "UNDER":
                self.__under = int(line)
            elif mode == "NOHEAD":
                self.__nohead = int(line)
            elif mode == "NOVCV":
                self.__novcv = int(line)
            elif mode == "ONLYCONSONANT":
                self.__only_consonant = int(line)
            elif mode == "VOWEL":
                value, keys = line.split("=")
                for k in keys.split(","):
                    self.__vowel[k] = value
            elif mode == "CONSONANT":
                value, cvs, time = line.split("=")
                self.__consonant_time[value] = float(time)
                for cv in cvs.split(","):
                    self.__consonant[cv] = value
            elif mode == "REPLACE":
                self.__replace = line.split("=")


