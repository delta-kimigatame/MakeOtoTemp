﻿import os
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
        アンダーバーの扱い
        Flaseだと無視、Trueだと休符扱いにします。
    begining_cv :bool
        wavの頭のエイリアスの種類
        Trueだと[- CV]を生成
        Falseだと[CV]を生成
    nohead :bool
        wavの頭のエイリアス生成の有無
        Trueだと生成
        Falseだとwavの頭からは生成しません。
    novcv :bool
        [V CV]の生成規則
        Falseで生成
        Trueで生成しない
    only_consonant :bool
        [C]の生成規則
        Falseで生成しない
        Trueで生成する
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
    __under :bool
    __begining_cv :bool
    __nohead :bool
    __novcv :bool
    __only_consonant :bool
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
    def under(self) -> bool:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        under :bool
            アンダーバーの扱い
            Flaseだと無視、Trueだと休符扱いにします。
        '''
        return self.__under
    
    @property
    def begining_cv(self) -> bool:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        begining_cv :bool
            wavの頭のエイリアスの種類
            Trueだと[- CV]を生成
            Falseだと[CV]を生成
        '''
        return self.__begining_cv

    @property
    def nohead(self) -> bool:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        nohead :bool
            wavの頭のエイリアス生成の有無
            Trueだと生成
            Falseだとwavの頭からは生成しません。
        '''
        return self.__nohead
    
    @property
    def novcv(self) -> bool:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        novcv :bool
            [V CV]の生成規則
            Falseで生成
            Trueで生成しない
        '''
        return self.__novcv

    @property
    def only_consonant(self) -> bool:
        '''
        読み込んだプリセットからパラメータを返す。

        Returns
        -------
        only_consonant :bool
            [C]の生成規則
            Falseで生成しない
            Trueで生成する
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


    def Make(self, filename :str = "mkototemp.ini"):
        '''
        デフォルト値でプリセットファイルを作成します。

        Parameters
        ----------
        filename :str ,default "mkototemp.ini"
            実行ファイルからの相対パス
        '''

        line :list =[]
        line.append("[TEMPO]")
        line.append(str(self.__tempo))

        line.append("[OFFSET]")
        line.append(str(settings.__offset))

        line.append("[MAXNUM]")
        line.append(str(settings.__max))

        line.append("[UNDER]")
        if self.__under:
            line.append("1")
        else:
            line.append("0")

        line.append("[NOHEAD]")
        if self.__nohead:
            line.append("2")
        elif self.__begining_cv:
            line.append("0")
        else:
            line.apopend("1")

        line.append("[NOVCV]")
        if self.__novcv:
            line.append("1")
        else:
            line.append("0")

        line.append("[ONLYCONSONANT]")
        if self.__only_consonant:
            line.append("1")
        else:
            line.append("0")

        line.append("[VOWEL]")
        vowels :dict = {}
        for kana, vowel in self.__vowels.items():
            if vowel in vowels.keys():
                vowels[vowel].append(kana)
            else:
                vowels[vowel] = [kana]

        for vowel,kanas in vowels.items():
            line.append(vowel + "=" + ",".join(kanas))

        line.append("[CONSONANT]")
        consonants :dict = {}
        for consonant in self.__consonant_time.keys():
            consonants[consonant] = []
        for cv,consonant in self.__consonant.items():
            consonants[consonant].append(cv)

        for consonant,cvs in consonants.items():
            line.append(consonant + "=" + ",".join(cvs) + "=" + str(self.__consonant_time[consonant]))

        with codecs.open(filename, "w", "utf-8") as fw:
            fw.write("\r\n".join(line))


    def __init__(self, filename: str = "mkototemp.ini"):
        '''
        filenameのプリセットを読み込む。
        もしfilenameにプリセットが存在しない場合、デフォルトプリセットを作成する。

        Parameters
        ----------
        filename :str ,default "mkototemp.ini"
            実行ファイルからの相対パス
        '''

        self.__tempo = settings.DEFAULT_TEMPO
        self.__offset = settings.DEFAULT_OFFSET
        self.__max = settings.DEFAULT_MAX
        self.__under = settings.DEFAULT_UNDER
        self.__begining_cv = settings.DEFAULT_BEGINING_CV
        self.__nohead = settings.DEFAULT_NO_HEAD
        self.__novcv = settings.DEFAULT_NO_VCV
        self.__only_consonant = settings.DEFAULT_ONLY_CONSONANT
        self.__vowel = settings.DEFAULT_VOWEL
        self.__consonant = settings.DEFAULT_CONSONANT
        self.__consonant_time = settings.DEFAULT_CONSONANT_TIME
        self.__replace = settings.DEFAULT_REPLACE
        
        if not os.path.isfile(filename):
            self.Make(filename)
        else:
            self.__Read(filename)


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

        entry = settings.ENTRIES

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
                self.__under = (1 == int(line))
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

