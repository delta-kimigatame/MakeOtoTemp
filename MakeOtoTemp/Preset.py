import os
import os.path
import codecs

import settings

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
    under :bool
        | アンダーバーの扱い
        | Flaseだと無視、Trueだと休符扱いにします。
    begining_cv :bool
        | wavの頭のエイリアスの種類
        | Trueだと[- CV]を生成
        | Falseだと[CV]を生成
    nohead :bool
        | wavの頭のエイリアス生成の有無
        | Trueだと生成
        | Falseだとwavの頭からは生成しません。
    novcv :bool
        | [V CV]の生成規則
        | Falseで生成
        | Trueで生成しない
    only_consonant :bool
        | [C]の生成規則
        | Falseで生成しない
        | Trueで生成する
    vowel :dict
        母音のバリエーションを指定
    consonant :dict
        子音のバリエーションを指定
    consonant_time :dict
        子音の標準長さをmsで指定
    replace :list
        ファイル名とエイリアスの置換を指定
    '''

    _tempo :float
    _offset :float
    _max :int
    _under :bool
    _begining_cv :bool
    _nohead :bool
    _novcv :bool
    _only_consonant :bool
    _vowel :dict
    _consonant :dict
    _consonant_time :dict
    _replace :list

    @property
    def tempo(self) -> float:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        tempo :float
            収録のbpm
        '''
        return self._tempo
    
    @property
    def offset(self) -> float:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        offset :float
            録音の開始時間(ms)
        '''
        return self._offset

    @property
    def max(self) -> int:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        max :int
            同じエイリアスをいくつ生成するか
        '''
        return self._max
    
    @property
    def under(self) -> bool:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        under :bool
            アンダーバーの扱い
            Flaseだと無視、Trueだと休符扱いにします。
        '''
        return self._under
    
    @property
    def begining_cv(self) -> bool:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        begining_cv :bool
            | wavの頭のエイリアスの種類
            | Trueだと[- CV]を生成
            | Falseだと[CV]を生成
        '''
        return self._begining_cv

    @property
    def nohead(self) -> bool:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        nohead :bool
            | wavの頭のエイリアス生成の有無
            | Trueだと生成
            | Falseだとwavの頭からは生成しません。
        '''
        return self._nohead
    
    @property
    def novcv(self) -> bool:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        novcv :bool
            | [V CV]の生成規則
            | Falseで生成
            | Trueで生成しない
        '''
        return self._novcv

    @property
    def only_consonant(self) -> bool:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        only_consonant :bool
            | [C]の生成規則
            | Falseで生成しない
            | Trueで生成する
        '''
        return self._only_consonant
    
    @property
    def vowel(self) -> dict:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        vowel :dict
            | 母音のバリエーションを指定
            | keyはCVに後方一致する文字列
            | valueは[V CV]の前半のVに当たる文字列
        '''
        return self._vowel
    
    @property
    def consonant(self) -> dict:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        consonant :dict
            | 子音のバリエーションを指定
            | keyは[CV]に完全一致する文字列
            | valueは子音の[V C]のときのCにあたる文字列

            | valueが""のものは、連続音のみを生成する例外
            | valueが"・"のものは"・ "に置き換えて適用(eve式喉切母音の例外)
        '''
        return self._consonant
    
    @property
    def consonant_time(self) -> dict:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        consonant_time :dict
            | 子音の標準長さをmsで指定
            | keyは子音にあたる文字列
            | valueは長さ(ms)
        '''
        return self._consonant_time

    @property
    def replace(self) -> list:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        replace :list
            | ファイル名とエイリアスの置換を指定
            | keyは変換前の文字、valueは変換後の文字
        '''
        return self._replace


    def Make(self, filename :str = "mkototemp.ini"):
        '''
        デフォルト値でプリセットファイルを作成します。

        Parameters
        ----------
        filename :str ,default "mkototemp.ini"
            実行ファイルからの相対パス

        Raises
        ------
        OSError
            filenameへの書き込み権限がなかったとき
        '''

        line :list =[]
        line.append("[TEMPO]")
        line.append(str(self._tempo))

        line.append("[OFFSET]")
        line.append(str(self._offset))

        line.append("[MAXNUM]")
        line.append(str(self._max))

        line.append("[UNDER]")
        if self._under:
            line.append("1")
        else:
            line.append("0")

        line.append("[NOHEAD]")
        if self._nohead:
            line.append("2")
        elif self._begining_cv:
            line.append("0")
        else:
            line.apopend("1")

        line.append("[NOVCV]")
        if self._novcv:
            line.append("1")
        else:
            line.append("0")

        line.append("[ONLYCONSONANT]")
        if self._only_consonant:
            line.append("1")
        else:
            line.append("0")

        line.append("[VOWEL]")
        vowels :dict = {}
        for kana, vowel in self._vowel.items():
            if vowel in vowels.keys():
                vowels[vowel].append(kana)
            else:
                vowels[vowel] = [kana]

        for vowel,kanas in vowels.items():
            line.append(vowel + "=" + ",".join(kanas))

        line.append("[CONSONANT]")
        consonants :dict = {}
        for consonant in self._consonant_time.keys():
            consonants[consonant] = []
        for cv,consonant in self._consonant.items():
            consonants[consonant].append(cv)

        for consonant,cvs in consonants.items():
            line.append(consonant + "=" + ",".join(cvs) + "=" + str(self._consonant_time[consonant]))

        with codecs.open(filename, "w", "utf-8") as fw:
            fw.write("\r\n".join(line))


    def __init__(self, filename: str = "mkototemp.ini"):
        '''
        | filenameのプリセットを読み込む。
        | もしfilenameにプリセットが存在しない場合、デフォルトプリセットを作成する。

        Parameters
        ----------
        filename :str ,default "mkototemp.ini"
            実行ファイルからの相対パス
        '''

        self._tempo = settings.DEFAULT_TEMPO
        self._offset = settings.DEFAULT_OFFSET
        self._max = settings.DEFAULT_MAX
        self._under = settings.DEFAULT_UNDER
        self._begining_cv = settings.DEFAULT_BEGINING_CV
        self._nohead = settings.DEFAULT_NO_HEAD
        self._novcv = settings.DEFAULT_NO_VCV
        self._only_consonant = settings.DEFAULT_ONLY_CONSONANT
        
        if not os.path.isfile(filename):
            self._vowel = settings.DEFAULT_VOWEL
            self._consonant = settings.DEFAULT_CONSONANT
            self._consonant_time = settings.DEFAULT_CONSONANT_TIME
            self._replace = settings.DEFAULT_REPLACE
            self.Make(filename)
        else:
            self._vowel = {}
            self._consonant = {}
            self._consonant_time = {}
            self._replace = []
            self.Read(filename)


    def Read(self, filename: str = "mkototemp.ini"):
        '''
        | filenameのプリセットを読み込む。
        | filenameの有無は事前にチェック済みのものとする。
        | 各パラメータは事前に初期化済みとする。

        Parameters
        ----------
        filename :str ,default "mkototemp.ini"
            実行ファイルからの相対パス

        Raises
        ------
        UnicodeDecodeError
            プリセットの文字コードがutf-8ではなかったとき
        TypeError
            プリセットで数字を入力すべき箇所に数字以外が入力されたとき
        ValueError
            | プリセットのフォーマットが適切ではないとき。
            | 具体的には、tempoやoffsetに負の数が入力された場合と
            | vowel,consonant,replaceの区切り文字が適切ではないとき
        '''
        mode :str = ""
        data :str
        lines :str
        line : str
        entry : list

        entry = settings.ENTRIES

        try:
            with codecs.open(filename, "r", "utf-8") as fr:
                data = fr.read().replace("\ufeff","")
        except UnicodeDecodeError as e:
            e.reason = "PRESET ERROR:" + filename + "の文字コードがutf-8ではないため、読み込みに失敗しました。"
            raise e
        lines = data.replace("\r","").split("\n")

        for line in lines:
            if line == "":
                continue

            if line in entry:
                mode = line.replace("[","").replace("]","")
                continue

            if mode == "TEMPO":
                try:
                    self._tempo = float(line)
                except:
                    raise TypeError("PRESET ERROR:" + filename + "の[TEMPO]に数字以外が入力されています。\n半角数字を入力してください。\n"+line)
                if self._tempo <= 0:
                    raise ValueError("PRESET ERROR:" + filename + "の[TEMPO]に0以下の数字が入力されています。\n"+line)
            elif mode == "OFFSET":
                try:
                    self._offset = float(line)
                except:
                    raise TypeError("PRESET ERROR:" + filename + "の[OFFSET]に数字以外が入力されています。\n半角数字を入力してください。\n"+line)
                if self._offset < 0:
                    raise ValueError("PRESET ERROR:" + filename + "の[OFFSET]に負の数字が入力されています。\n"+line)
            elif mode == "MAXNUM":
                try:
                    self._max = int(line)
                except:
                    raise TypeError("PRESET ERROR:" + filename + "の[MAXNUM]に数字以外が入力されています。\n半角数字を入力してください。\n"+line)
                
            elif mode == "UNDER":
                try:
                    self._under = (1 == int(line))
                except:
                    raise TypeError("PRESET ERROR:" + filename + "の[UNDER]に数字以外が入力されています。\n0か1を入力してください。\n"+line)
                
            elif mode == "NOHEAD":
                try:
                    if int(line)==2:
                        self._nohead = True
                        self._begining_cv = False
                    else:
                        self._nohead = False
                        self._begining_cv = (0 == int(line))
                except:
                    raise TypeError("PRESET ERROR:" + filename + "の[NOHEAD]に数字以外が入力されています。\n0か1か2を入力してください。\n"+line)
            elif mode == "NOVCV":
                try:
                    self._novcv = (1 == int(line))
                except:
                    raise TypeError("PRESET ERROR:" + filename + "の[NOVCV]に数字以外が入力されています。\n0か1を入力してください。\n"+line)
            elif mode == "ONLYCONSONANT":
                try:
                    self._only_consonant = (1 == int(line))
                except:
                    raise TypeError("PRESET ERROR:" + filename + "の[ONLYCONSONANT]に数字以外が入力されています。\n0か1を入力してください。\n"+line)
            elif mode == "VOWEL":
                if "=" in line:
                    value, keys = line.split("=")
                    for k in keys.split(","):
                        self._vowel[k] = value
                else:
                    raise ValueError("PRESET ERROR:" + filename + "の[VOWELS]に\"=\"が含まれていない行があります。\n"+line)
            elif mode == "CONSONANT":
                if line.count("=")==2:
                    value, cvs, time = line.split("=")
                    self._consonant_time[value] = float(time)
                    for cv in cvs.split(","):
                        self._consonant[cv] = value
                else:
                    raise ValueError("PRESET ERROR:" + filename + "の[CONSONANT]のフォーマットが正しくない行があります。\n"+line)
            elif mode == "REPLACE":
                if "=" in line:
                    self._replace.append(line.split("="))
                else:
                    raise ValueError("PRESET ERROR:" + filename + "の[REPLACE]に\"=\"が含まれていない行があります。\n"+line)


