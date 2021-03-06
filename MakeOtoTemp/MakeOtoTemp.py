'''
| MakeOtoTemp
| プリセットファイルに基づいて原音設定のテンプレートを作成します。
| プリセットファイルが存在しない場合、デフォルトのプリセットファイルが生成されます。

Examples
--------
>>> MakeOtoTemp input_path [--preset preset_path] [--oto oto_path]

Parameters
----------
input_path :str
    以下のいずれかのパス

    * cp932でエンコードされたテキストファイル
    * utf-8でエンコードされたテキストファイル
    * wavファイルを含むディレクトリ

    テキストファイルの場合、1行を1ファイル名として読み込みます。

preset_path :str, default "mkototemp.ini"
    使用するプリセットファイルのパス

oto_path :str, default "oto.ini"
    出力される原音設定ファイルのパス
'''

import sys
import os
import os.path
import argparse
import logging
import codecs
import mimetypes
from typing import Tuple

sys.path.append(os.path.dirname(__file__)) #embeddable pythonにimpot用のパスを追加

import Oto
import Preset

BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))

class MakeOtoTemp:
    '''
    プリセットファイルに基づいて原音設定のテンプレートを作成します。
    
    Attributes
    ----------
    input :str
        | 入力ファイルのパス
        | テキストファイルの場合、その各行を
        | ディレクトリの場合、その中にあるwavファイルの名前を
        | reclistとして取り込む。
    reclist :list of str
        録音リストのファイル名文字列のリスト
    oto :list of Oto.Oto
        出力する原音設定ファイル
    preset :Preset.Preset
        このプロジェクトの設定ファイル
    '''

    _input :str
    _reclist :list
    _oto :list
    _preset :Preset.Preset

    @property
    def input(self) -> str:
        '''
        Returns
        -------
        input :str
            入力ファイルのパス
        '''
        return self._input
    
    @property
    def reclist(self) -> list:
        '''
        Returns
        -------
        reclist :list of str
            録音リストのファイル名文字列のリスト
        '''
        return self._reclist
    
    @property
    def oto(self) -> list:
        '''
        Returns
        -------
        oto :Oto.Oto
            出力する原音設定ファイル
        '''
        return self._oto
    
    @property
    def preset(self) -> Preset.Preset:
        '''
        Returns
        -------
        preset :Preset.Preset
            このプロジェクトの設定ファイル
        '''
        return self._preset

    def __init__(self, input :str, preset_path :str = "mkototemp.ini"):
        '''
        Parameters
        ----------
        input :str
            | 入力ファイルのパス
            | テキストファイルの場合、その各行を
            | ディレクトリの場合、その中にあるwavファイルの名前を
            | reclistとして取り込む。
        preset_path :str , default "mkototemp.ini"
            presetファイルのパス
            
        Raises
        ------
        FileNotFoundError
            inputファイルが存在しなかったとき
        UnicodeDecodeError
            inputファイルの文字コードがcp932かutf-8以外だったとき
        TypeError
            inputファイルがテキストかディレクトリ以外だったとき
        TypeError
            Preset読み込み時。詳細はPreset.Preset.Readを参照
        ValueError
            Preset読み込み時。詳細はPreset.Preset.Readを参照
        OSError
            Preset書き込み時。詳細はPreset.Preset.Makeを参照
        '''
        
        if not os.path.exists(input):
            raise FileNotFoundError("INPUT ERROR:"+ input + "は存在しません。")
        self._input = input
        self._GetRecList()
        self._preset = Preset.Preset(preset_path)
        logging.debug("preset loaded")
        self._oto = []
    

    def _GetRecList(self):
        '''
        | self._inputを読み込んでself._reclistを更新します。
        | テキストファイルの場合、その各行を取り込みます。
        | ディレクトリの場合、その中にあるwavファイルの名前を取り込みます。
        | inputファイルの存在は事前に確認されているものとします。

        Raises
        ------
        TypeError
            inputファイルがテキストかディレクトリ以外だったとき
        UnicodeDecodeError
            inputファイルの文字コードがcp932かutf-8以外だったとき
        '''
        if os.path.isdir(self._input):
            logging.debug("dir input")
            files :list = os.listdir(self._input)
            filter_files :list = list(filter(lambda file: file.endswith(".wav"), files))
            self._reclist = list(map(lambda file: file.replace(".wav",""), filter_files))
        else:
            logging.debug("text input")
            if mimetypes.guess_type(self._input)[0] != "text/plain":
                raise TypeError("RECLIST ERROR:" + self._input + "はテキストファイルでもフォルダでもないため、開けませんでした")
            try:
                with codecs.open(self._input, "r", "cp932") as fr:
                    data :str = fr.read()
            except:
                try:
                    with codecs.open(self._input, "r", "utf-8") as fr:
                        data :str = fr.read().replace("\ufeff","")
                except UnicodeDecodeError as e:
                    e.reason = "RECLIST ERROR:" + self._input + "の文字コードが次のどちらでもないため、読み込みに失敗しました。cp932,utf-8"
                    raise e
            self._reclist = data.replace("\r","").split("\n")
        for record in self._reclist:
            logging.debug("input_record:"+record)
        

    def MakeOtoParam(self):
        '''
        self._presetとself._reclistに基づいて、原音設定データを作成する。

        Attributes
        ----------
        length :float
            | 収録tempoの4分音符1つ分の長さ(ms)
            | length = 60 / self._preset.tempo * 1000
        pre :float
            lengthの1/2の長さ(ms)
        offset :float
            | wavの先頭では、self._preset.offset - pre
            | 2音素目以降はlengthを加算する。
        ove :float
            preの1/3の長さ(ms)
        consonant :float
            preの1.5倍の長さ(ms)
        blank :float
            (length + ove)の長さ(ms)とし、offsetからの時間にするため、-1を乗ずる
        prev_vowel :str
            直前の母音。wavの先頭の場合"-"
        record :str
            収録ファイル名
        '''
        length :float = 60 / self._preset.tempo * 1000
        pre :float = length / 2
        ove :float = pre / 3
        consonant :float = pre * 1.5
        blank :float = (length + ove) * -1
        begin :int
        end :int
        is_underbar :bool
        cv :str
        consonant_time :float
        for record in self._reclist:
            logging.debug("target record:"+record)
            offset = self.preset.offset - pre
            prev_vowel = "-"
            if record[0] == "_":
                begin = 1
            else:
                begin = 0
            while begin < len(record):
                #エイリアスの開始位置がアンダーバーか否かチェック
                begin, offset, prev_vowel, is_underbar = self._CheckUnderBar(record, begin, offset, length, prev_vowel)
                if is_underbar:
                    continue
                #エイリアスの特定
                begin, end, offset, prev_vowel= self._GetRange(record, begin, offset, length, prev_vowel)
                if begin >= len(record):
                    break
                cv = record[begin:end]
                logging.debug("target cv:"+cv)
                logging.debug("target cv index:"+str(begin))
                if self.preset.consonant[cv] == "":#連続音
                    self._MakeOtoParamVCV(offset, pre, ove, consonant, blank, record, prev_vowel, cv)
                    logging.debug("make_vcv")
                elif self.preset.consonant[cv] == "-":#onset-consonant-cluster
                    self._MakeOtoParamOnsetConsonantCluster(offset, pre, ove, consonant, blank, record, prev_vowel, cv)
                    logging.debug("make_-cc")
                elif self.preset.consonant[cv] == "*":#coda-consonant-cluster
                    self._MakeOtoParamCodaConsonantCluster(offset, pre, ove, consonant, blank, record, begin, end)
                    logging.debug("make_cc-")
                elif prev_vowel == "-":#CVのみ
                    self._MakeOtoParamHeadCV(offset, pre, blank, record, cv)
                    logging.debug("make_cv")
                else:#CVVC
                    self._MakeOtoParamCVVC(offset, pre, ove, consonant, blank, record, prev_vowel, cv)
                    logging.debug("make_cvvc")
            
                prev_vowel = self._SetVowel(cv)
                offset = offset + length
                begin = end

    def WriteOto(self, otopath :str = "oto.ini"):
        '''
        原音設定ファイルを保存する。

        Parameters
        ----------
        otopath :str ,default "oto.ini"
            保存する原音設定ファイルのパス
            
        Raises
        ------
        OSError
            filenameへの書き込み権限がなかったとき

        '''
        writed :dict = {}
        lines :list = []
        for oto in self._oto:
            if oto.alias not in writed:
                writed[oto.alias] = 1
                lines.append(str(oto))
                logging.debug("write:"+str(oto))
            elif writed[oto.alias] >= self.preset.max:
                continue
            else:
                writed[oto.alias] = writed[oto.alias] + 1
                oto.alias = oto.alias + str(writed[oto.alias])
                lines.append(str(oto))
                logging.debug("write:"+str(oto))
        with codecs.open(otopath, "w", "cp932") as fw:
            fw.write("\r\n".join(lines))

    def _MakeOtoParamVCV(self, offset :float, pre :float, ove :float, consonant :float, blank :float, record :str, prev_vowel :str, alias :str):
        '''
        連続音用の原音設定データを作成する際の処理

        Parameters
        ----------
        offset :float
            | wavの先頭では、self._preset.offset - pre
            | 2音素目以降はlengthを加算する。
        pre :float
            lengthの1/2の長さ(ms)
        ove :float
            preの1/3の長さ(ms)
        consonant :float
            preの1.5倍の長さ(ms)
        blank :float
            (length + ove)の長さ(ms)とし、offsetからの時間にするため、-1を乗ずる
        record :str
            収録ファイル名
        prev_vowel :str
            直前の母音。wavの先頭の場合"-"
        alias :str
            エイリアス
        '''
        if prev_vowel == "-" and self.preset.nohead:
            pass
        elif prev_vowel == "-" and not self.preset.begining_cv:
            self._oto.append(Oto.Oto(record+".wav", self._ReplaceAlias(alias), offset, pre, ove, consonant, blank))
        elif self.preset.novcv:
            pass
        else:
            self._oto.append(Oto.Oto(record+".wav", self._ReplaceAlias(prev_vowel + " " + alias), offset, pre, ove, consonant, blank))
            

    def _MakeOtoParamOnsetConsonantCluster(self, offset :float, pre :float, ove :float, consonant :float, blank :float,record :str, prev_vowel :str,alias :str):
        '''
        頭子音群の原音設定データを作成する際の処理

        Parameters
        ----------
        offset :float
            | wavの先頭では、self._preset.offset - pre
            | 2音素目以降はlengthを加算する。
        pre :float
            lengthの1/2の長さ(ms)
        ove :float
            preの1/3の長さ(ms)
        consonant :float
            preの1.5倍の長さ(ms)
        blank :float
            (length + ove)の長さ(ms)とし、offsetからの時間にするため、-1を乗ずる
        record :str
            収録ファイル名
        prev_vowel :str
            直前の母音。wavの先頭の場合"-"
        alias :str
            エイリアス
        '''
        if prev_vowel == "-":
            self._oto.append(Oto.Oto(record+".wav", self._ReplaceAlias("- " + alias), offset, pre, ove, consonant, blank))
        else:
            self._oto.append(Oto.Oto(record+".wav", self._ReplaceAlias(alias), offset, pre, ove, consonant, blank))
            
    def _MakeOtoParamCodaConsonantCluster(self, offset :float, pre :float, ove :float, consonant :float, blank :float,record :str, begin :int, end:int):
        '''
        |尾子音群の原音設定データを作成する際の処理
        |子音群を[単一のC 残りの子音群]の形に分割する。
        |Cは文字数が不明な1発音単位の子音

        Parameters
        ----------
        offset :float
            | wavの先頭では、self._preset.offset - pre
            | 2音素目以降はlengthを加算する。
        pre :float
            lengthの1/2の長さ(ms)
        ove :float
            preの1/3の長さ(ms)
        consonant :float
            preの1.5倍の長さ(ms)
        blank :float
            (length + ove)の長さ(ms)とし、offsetからの時間にするため、-1を乗ずる
        record :str
            収録ファイル名
        begin :int
            エイリアスが何文字目から始まるか?
        end :int
            エイリアスが何文字目で終わるか?
        '''
        parse :int=1
        while begin < end - parse:
            if record[begin:end-parse] not in self.preset.consonant:#C1の子音の種類が特定できない場合
                parse = parse + 1
            elif self.preset.consonant[record[begin:end-parse]] in ["*", "-"]:#C1が子音クラスタの場合
                parse = parse + 1
            else:#C1の子音を特定
                break
        self._oto.append(Oto.Oto(record+".wav", self._ReplaceAlias(record[begin:end-parse] + " " + record[end-parse:end]), offset, pre, ove, consonant, blank))

    def _MakeOtoParamHeadCV(self, offset :float, pre :float, blank :float, record :str, alias :str):
        '''
        休符後単独音用の原音設定データを作成する際の処理

        Parameters
        ----------
        offset :float
            | wavの先頭では、self._preset.offset - pre
            | 2音素目以降はlengthを加算する。
        pre :float
            lengthの1/2の長さ(ms)
        blank :float
            (length + ove)の長さ(ms)とし、offsetからの時間にするため、-1を乗ずる
        record :str
            収録ファイル名
        alias :str
            エイリアス
        '''
        if self.preset.nohead:
            pass
        elif not self.preset.begining_cv:
            consonant_time = self.preset.consonant_time[self.preset.consonant[alias]]
            self._oto.append(Oto.Oto(record+".wav", 
                                        self._ReplaceAlias(alias), 
                                        offset + pre - consonant_time, 
                                        consonant_time, 
                                        consonant_time/3, 
                                        consonant_time * 1.5, 
                                        blank + consonant_time))
        else:
            consonant_time = self.preset.consonant_time[self.preset.consonant[alias]]
            self._oto.append(Oto.Oto(record+".wav", 
                                        self._ReplaceAlias("- " + alias), 
                                        offset + pre - consonant_time, 
                                        consonant_time, 
                                        consonant_time/3, 
                                        consonant_time * 1.5, 
                                        blank + consonant_time))

    def _MakeOtoParamCVVC(self, offset :float, pre :float, ove :float, consonant :float, blank :float, record :str, prev_vowel :str, alias :str):
        '''
        CVVC用の原音設定データを作成する際の処理

        Parameters
        ----------
        offset :float
            | wavの先頭では、self._preset.offset - pre
            | 2音素目以降はlengthを加算する。
        pre :float
            lengthの1/2の長さ(ms)
        ove :float
            preの1/3の長さ(ms)
        consonant :float
            preの1.5倍の長さ(ms)
        blank :float
            (length + ove)の長さ(ms)とし、offsetからの時間にするため、-1を乗ずる
        record :str
            収録ファイル名
        prev_vowel :str
            直前の母音。wavの先頭の場合"-"
        alias :str
            エイリアス
        '''
        consonant_time = self.preset.consonant_time[self.preset.consonant[alias]]
        #VC
        self._oto.append(Oto.Oto(record+".wav", 
                                    self._ReplaceAlias(prev_vowel + " " + self.preset.consonant[alias]), 
                                    offset - consonant_time, 
                                    pre, 
                                    ove, 
                                    pre + consonant_time/2, 
                                    -consonant_time * 3 / 4 -pre))
        #CV
        if "・" in self.preset.consonant[alias]:
            alias = alias.replace("・","・ ")
        self._oto.append(Oto.Oto(record+".wav", 
                                    self._ReplaceAlias(alias), 
                                    offset + pre - consonant_time, 
                                    consonant_time, 
                                    consonant_time/3, 
                                    consonant_time * 1.5, 
                                    blank + consonant_time))

        #only_consonant
        if self.preset.only_consonant:
            self._oto.append(Oto.Oto(record+".wav", 
                                        self._ReplaceAlias(self.preset.consonant[alias]), 
                                        offset + pre - consonant_time, 
                                        consonant_time * 0.3, 
                                        consonant_time * 0.1, 
                                        consonant_time/2, 
                                        -consonant_time))

    def _SetVowel(self, alias :str) -> str:
        '''
        aliasについて、後方一致でself.preset.vowelを検索し、その結果を返す。

        Parameters
        ----------
        alias :str
            エイリアス

        Returns
        -------
        vowel :str
            母音、該当するものが無ければ"-"を返す
        '''
        for i in range(len(alias)):
            if alias[i:] in self.preset.vowel:
                return self.preset.vowel[alias[i:]]
        return "-"

    def _CheckUnderBar(self, record :str, begin :int, offset :float, length :float, prev_vowel :str) -> Tuple[int, float, str, bool]:
        '''
        recordのbegin文字目が"_"か否かチェックし、各パラメータを補正して返す。

        Parameters
        ----------
        record :str
            収録文字列
        begin :int
            何文字目をチェックするか
        offset :float
            原音設定のオフセット値
        lenfth :float
            原音設定の1エイリアス当たりの長さ(ms)
        prev_vowel :str
            直前の母音。wavの先頭の場合"-"

        Returns
        -------
        begin :int
            record[begin]=="_"であれば、begin + 1を、そうでなければ引数のままの値を返す。
        offset :float
            record[begin]=="_"かつ、self.perset.underがTrueであればoffset + lengthを、そうでなければ引数のままの値を返す。
        prev_vowel :str
            record[begin]=="_"かつ、self.perset.underがTrueであれば"-"を、そうでなければ引数のままの値を返す。
        is_underbar :bool
            record[begin]=="_"の結果を返す。
        '''
        is_underbar :bool = (record[begin]=="_")
        if is_underbar:
            begin = begin + 1
            if self.preset.under:
                offset = offset + length
                prev_vowel = "-"

        return begin, offset, prev_vowel, is_underbar

    def _GetRange(self, record :str, begin :int, offset :float,length :float,prev_vowel :str) -> Tuple[int, int, float, str]:
        '''
        | recordのbegin文字目以降から、self.preset.consonantに含まれる最長文字列を見つける。
        | 
        | まず、beginからrecordの末尾までの文字列が、self.preset.consonantに含まれるか調べ、
        | ヒットするまで、後方の文字を1文字ずつ減らしていく。
        | 
        | begin ～ endの間が0文字になった場合、beginに1加えて再度実行する。
        | 
        | beginに1加えた際、record[begin]が"_"出ないかのチェックも行う。

        Parameters
        ----------
        record :str
            収録文字列
        begin :int
            エイリアスが何文字目から始まるか?
        end :int
            エイリアスが何文字目で終わるか?

        offset :float
            原音設定のオフセット値
        lenfth :float
            原音設定の1エイリアス当たりの長さ(ms)
        prev_vowel :str
            直前の母音。wavの先頭の場合"-"

        Returns
        -------
        begin :int
            通常は引数のままの値を返す。endがbegin以下になってもself.preset.consonantに含まれなければ都度インクリメントする。
        end :int
            record[begin:end] in self.preset.consonantを満たす、最大の数字を返す。
        offset :float
            通常は引数のままの値を返す。beginが増加した場合_CheckUnderBarの結果に基づいて増加する。
        prev_vowel :str
            通常は引数のままの値を返す。beginが増加した場合_CheckUnderBarの結果に変更する。
        '''
        end = len(record)
        while record[begin:end] not in self.preset.consonant:
            end = end -1
            if end <= begin:
                end = len(record)
                begin = begin + 1
                if begin >= len(record):
                    break
                begin, offset, prev_vowel, is_underbar = self._CheckUnderBar(record, begin, offset, length, prev_vowel)
                while is_underbar:
                    if begin >= len(record):
                        break
                    begin, offset, prev_vowel, is_underbar = self._CheckUnderBar(record, begin, offset, length, prev_vowel)
        return begin, end, offset, prev_vowel

    def _ReplaceAlias(self, alias :str) -> str:
        '''
        与えられたaliasをpresetの設定にしたがって置換した文字列を返す

        Parameters
        ----------
        alias :str
            変換前のエイリアス

        Returns
        -------
        alias :str
            変換後のエリアス
        '''
        for replace_pattern in self.preset.replace:
            alias = alias.replace(replace_pattern[1], replace_pattern[0])
        return alias

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="録音リストもしくはwavファイルを含むフォルダに基づいて、原音設定テンプレートを生成します。")
    parser.add_argument("input_path", type=str, help="録音リストもしくはwavファイルを含むフォルダのパス。録音リストはcp932もしくはutf-8で記述されたtxtファイルでなければいけません")
    parser.add_argument("-p", "--preset", type=str, default=os.path.join(os.path.split(BASE_DIR)[0],"mkototemp.ini"),
                        help="presetファイルのパス。指定しなければ、同一ディレクトリ内のmkototemp.iniを使用します。存在しないファイルを指定した場合、標準のプリセットファイルを作成します。")
    parser.add_argument("-o", "--oto", type=str, default=os.path.join(os.path.split(BASE_DIR)[0],"oto.ini"),
                        help="出力する原音設定ファイルのパス。指定しなければ、同一ディレクトリ内にoto.iniを生成します。既に存在するファイルの場合、無警告で上書きされます。")
    args = parser.parse_args()
    logging.basicConfig(filename=os.path.join(BASE_DIR,"..",'error-log.txt'), encoding="utf-8", level=logging.ERROR, format='%(asctime)s:%(message)s')
    #logging.basicConfig(filename=os.path.join(BASE_DIR,"..",'debug-log.txt'), encoding="utf-8", level=logging.DEBUG, format='%(asctime)s:%(message)s')
    logging.debug("base_dir:"+BASE_DIR)
    logging.debug("input_path:"+args.input_path)
    logging.debug("preset:"+args.preset)
    logging.debug("oto:"+args.oto)
    #makeOtoTemp=MakeOtoTemp(args.input_path, args.preset)
    #makeOtoTemp.MakeOtoParam()
    #makeOtoTemp.WriteOto(args.oto)
    print(BASE_DIR)
    try:
        makeOtoTemp=MakeOtoTemp(args.input_path, args.preset)
        makeOtoTemp.MakeOtoParam()
        makeOtoTemp.WriteOto(args.oto)
    except Exception as e:
        for log in e.args:
            print(log)
            logging.error(log)