




MakeOtoTemp 1.0.0 ドキュメント

















 [MakeOtoTemp](#) 

Contents:


* [MakeOtoTemp module](index.html#document-MakeOtoTemp)
* [Oto module](index.html#document-Oto)
* [Preset module](index.html#document-Preset)







[MakeOtoTemp](#)




* »
* MakeOtoTemp 1.0.0 ドキュメント
* 




---






Welcome to MakeOtoTemp's documentation![](#welcome-to-makeototemp-s-documentation "このヘッドラインへのパーマリンク")
======================================================================================================




MakeOtoTemp module[](#module-MakeOtoTemp "このヘッドラインへのパーマリンク")
-------------------------------------------------------------




*class* MakeOtoTemp.MakeOtoTemp(*input: str*, *preset\_path: str = 'mkototemp.ini'*)[](#MakeOtoTemp.MakeOtoTemp "この定義へのパーマリンク")
ベースクラス: `object`


プリセットファイルに基づいて原音設定のテンプレートを作成します。




input[](#MakeOtoTemp.MakeOtoTemp.input "この定義へのパーマリンク")

入力ファイルのパス
テキストファイルの場合、その各行を
ディレクトリの場合、その中にあるwavファイルの名前を
reclistとして取り込む。


Type
str







reclist[](#MakeOtoTemp.MakeOtoTemp.reclist "この定義へのパーマリンク")
録音リストのファイル名文字列のリスト



Type
list of str







oto[](#MakeOtoTemp.MakeOtoTemp.oto "この定義へのパーマリンク")
出力する原音設定ファイル



Type
list of Oto.Oto







preset[](#MakeOtoTemp.MakeOtoTemp.preset "この定義へのパーマリンク")
このプロジェクトの設定ファイル



Type
[Preset.Preset](index.html#Preset.Preset "Preset.Preset")







MakeOtoParam()[](#MakeOtoTemp.MakeOtoTemp.MakeOtoParam "この定義へのパーマリンク")
self.\_presetとself.\_reclistに基づいて、原音設定データを作成する。




length[](#MakeOtoTemp.MakeOtoTemp.length "この定義へのパーマリンク")

収録tempoの4分音符1つ分の長さ(ms)
length = 60 / self.\_preset.tempo * 1000


Type
float







pre[](#MakeOtoTemp.MakeOtoTemp.pre "この定義へのパーマリンク")
lengthの1/2の長さ(ms)



Type
float







offset[](#MakeOtoTemp.MakeOtoTemp.offset "この定義へのパーマリンク")

wavの先頭では、self.\_preset.offset - pre
2音素目以降はlengthを加算する。


Type
float







ove[](#MakeOtoTemp.MakeOtoTemp.ove "この定義へのパーマリンク")
preの1/3の長さ(ms)



Type
float







consonant[](#MakeOtoTemp.MakeOtoTemp.consonant "この定義へのパーマリンク")
preの1.5倍の長さ(ms)



Type
float







blank[](#MakeOtoTemp.MakeOtoTemp.blank "この定義へのパーマリンク")
(length + ove)の長さ(ms)とし、offsetからの時間にするため、-1を乗ずる



Type
float







prev\_vowel[](#MakeOtoTemp.MakeOtoTemp.prev_vowel "この定義へのパーマリンク")
直前の母音。wavの先頭の場合"-"



Type
str







record[](#MakeOtoTemp.MakeOtoTemp.record "この定義へのパーマリンク")
収録ファイル名



Type
str








WriteOto(*otopath: str = 'oto.ini'*)[](#MakeOtoTemp.MakeOtoTemp.WriteOto "この定義へのパーマリンク")
原音設定ファイルを保存する。



パラメータ
**otopath** (*str* *,**default "oto.ini"*) -- 保存する原音設定ファイルのパス



例外
**OSError** -- filenameへの書き込み権限がなかったとき







*property* input*: str*[](#id0 "この定義へのパーマリンク")
returns: **input** -- 入力ファイルのパス
:rtype: str





*property* oto*: list*[](#id1 "この定義へのパーマリンク")
returns: **oto** -- 出力する原音設定ファイル
:rtype: Oto.Oto





*property* preset*: [Preset.Preset](index.html#Preset.Preset "Preset.Preset")*[](#id2 "この定義へのパーマリンク")
returns: **preset** -- このプロジェクトの設定ファイル
:rtype: Preset.Preset





*property* reclist*: list*[](#id3 "この定義へのパーマリンク")
returns: **reclist** -- 録音リストのファイル名文字列のリスト
:rtype: list of str






Oto module[](#module-Oto "このヘッドラインへのパーマリンク")
---------------------------------------------




*class* Oto.Oto(*filename: str*, *alias: str*, *offset: float*, *pre: float*, *ove: float*, *consonant: float*, *blank: float*)[](#Oto.Oto "この定義へのパーマリンク")
ベースクラス: `object`


UTAUの原音設定ファイルのデータを扱う




filename[](#Oto.Oto.filename "この定義へのパーマリンク")
voiceルートからのファイルの相対パス



Type
str







alias[](#Oto.Oto.alias "この定義へのパーマリンク")
エイリアス



Type
str







offset[](#Oto.Oto.offset "この定義へのパーマリンク")
オフセット(setparamでいうところの左ブランク)



Type
float







pre[](#Oto.Oto.pre "この定義へのパーマリンク")
先行発声



Type
float







ove[](#Oto.Oto.ove "この定義へのパーマリンク")
オーバーラップ



Type
float







consonant[](#Oto.Oto.consonant "この定義へのパーマリンク")
子音部(setparamでいうところの固定範囲)



Type
float







blank[](#Oto.Oto.blank "この定義へのパーマリンク")

ブランク(setparamでいうところの右ブランク)
正の値のときはwav末尾からのmsを表す。
負の値のときはオフセットからのmsの絶対値に-1をかけたものを表す。


Type
float







rounds[](#Oto.Oto.rounds "この定義へのパーマリンク")

書き出し時の各パラメータを小数何桁で丸めるかを指定する。
-1の時は丸めない。


Type
int ,default -1







alias*: str*[](#id0 "この定義へのパーマリンク")



blank*: float*[](#id1 "この定義へのパーマリンク")



consonant*: float*[](#id2 "この定義へのパーマリンク")



filename*: str*[](#id3 "この定義へのパーマリンク")



offset*: float*[](#id4 "この定義へのパーマリンク")



ove*: float*[](#id5 "この定義へのパーマリンク")



pre*: float*[](#id6 "この定義へのパーマリンク")



rounds*: int*[](#id7 "この定義へのパーマリンク")




Preset module[](#module-Preset "このヘッドラインへのパーマリンク")
---------------------------------------------------




*class* Preset.Preset(*filename: str = 'mkototemp.ini'*)[](#Preset.Preset "この定義へのパーマリンク")
ベースクラス: `object`


MakeOtoTempのプリセットファイルを扱う




tempo[](#Preset.Preset.tempo "この定義へのパーマリンク")
収録のbpm



Type
float







offset[](#Preset.Preset.offset "この定義へのパーマリンク")
録音の開始時間(ms)



Type
float







max[](#Preset.Preset.max "この定義へのパーマリンク")
同じエイリアスをいくつ生成するか



Type
int







under[](#Preset.Preset.under "この定義へのパーマリンク")

アンダーバーの扱い
Flaseだと無視、Trueだと休符扱いにします。


Type
bool







begining\_cv[](#Preset.Preset.begining_cv "この定義へのパーマリンク")

wavの頭のエイリアスの種類
Trueだと[- CV]を生成
Falseだと[CV]を生成


Type
bool







nohead[](#Preset.Preset.nohead "この定義へのパーマリンク")

wavの頭のエイリアス生成の有無
Trueだと生成
Falseだとwavの頭からは生成しません。


Type
bool







novcv[](#Preset.Preset.novcv "この定義へのパーマリンク")

[V CV]の生成規則
Falseで生成
Trueで生成しない


Type
bool







only\_consonant[](#Preset.Preset.only_consonant "この定義へのパーマリンク")

[C]の生成規則
Falseで生成しない
Trueで生成する


Type
bool







vowel[](#Preset.Preset.vowel "この定義へのパーマリンク")
母音のバリエーションを指定



Type
dict







consonant[](#Preset.Preset.consonant "この定義へのパーマリンク")
子音のバリエーションを指定



Type
dict







consonant\_time[](#Preset.Preset.consonant_time "この定義へのパーマリンク")
子音の標準長さをmsで指定



Type
dict







replace[](#Preset.Preset.replace "この定義へのパーマリンク")
ファイル名とエイリアスの置換を指定



Type
list







Make(*filename: str = 'mkototemp.ini'*)[](#Preset.Preset.Make "この定義へのパーマリンク")
デフォルト値でプリセットファイルを作成します。



パラメータ
**filename** (*str* *,**default "mkototemp.ini"*) -- 実行ファイルからの相対パス



例外
**OSError** -- filenameへの書き込み権限がなかったとき







Read(*filename: str = 'mkototemp.ini'*)[](#Preset.Preset.Read "この定義へのパーマリンク")

filenameのプリセットを読み込む。
filenameの有無は事前にチェック済みのものとする。
各パラメータは事前に初期化済みとする。


パラメータ
**filename** (*str* *,**default "mkototemp.ini"*) -- 実行ファイルからの相対パス



例外
* **UnicodeDecodeError** -- プリセットの文字コードがutf-8ではなかったとき
* **TypeError** -- プリセットで数字を入力すべき箇所に数字以外が入力されたとき
* **ValueError** -- 
プリセットのフォーマットが適切ではないとき。
 | 具体的には、tempoやoffsetに負の数が入力された場合と
 | vowel,consonant,replaceの区切り文字が適切ではないとき







*property* begining\_cv*: bool*[](#id0 "この定義へのパーマリンク")
読み込んだプリセットからパラメータを返す。



戻り値
**begining\_cv** -- | wavの頭のエイリアスの種類
| Trueだと[- CV]を生成
| Falseだと[CV]を生成



戻り値の型
bool







*property* consonant*: dict*[](#id1 "この定義へのパーマリンク")
読み込んだプリセットからパラメータを返す。



戻り値
**consonant** -- | 子音のバリエーションを指定
| keyは[CV]に完全一致する文字列
| valueは子音の[V C]のときのCにあたる文字列



valueが""のものは、連続音のみを生成する例外
valueが"・"のものは"・ "に置き換えて適用(eve式喉切母音の例外)





戻り値の型
dict







*property* consonant\_time*: dict*[](#id2 "この定義へのパーマリンク")
読み込んだプリセットからパラメータを返す。



戻り値
**consonant\_time** -- | 子音の標準長さをmsで指定
| keyは子音にあたる文字列
| valueは長さ(ms)



戻り値の型
dict







*property* max*: int*[](#id3 "この定義へのパーマリンク")
読み込んだプリセットからパラメータを返す。



戻り値
**max** -- 同じエイリアスをいくつ生成するか



戻り値の型
int







*property* nohead*: bool*[](#id4 "この定義へのパーマリンク")
読み込んだプリセットからパラメータを返す。



戻り値
**nohead** -- | wavの頭のエイリアス生成の有無
| Trueだと生成
| Falseだとwavの頭からは生成しません。



戻り値の型
bool







*property* novcv*: bool*[](#id5 "この定義へのパーマリンク")
読み込んだプリセットからパラメータを返す。



戻り値
**novcv** -- | [V CV]の生成規則
| Falseで生成
| Trueで生成しない



戻り値の型
bool







*property* offset*: float*[](#id6 "この定義へのパーマリンク")
読み込んだプリセットからパラメータを返す。



戻り値
**offset** -- 録音の開始時間(ms)



戻り値の型
float







*property* only\_consonant*: bool*[](#id7 "この定義へのパーマリンク")
読み込んだプリセットからパラメータを返す。



戻り値
**only\_consonant** -- | [C]の生成規則
| Falseで生成しない
| Trueで生成する



戻り値の型
bool







*property* replace*: list*[](#id8 "この定義へのパーマリンク")
読み込んだプリセットからパラメータを返す。



戻り値
**replace** -- | ファイル名とエイリアスの置換を指定
| keyは変換前の文字、valueは変換後の文字



戻り値の型
list







*property* tempo*: float*[](#id9 "この定義へのパーマリンク")
読み込んだプリセットからパラメータを返す。



戻り値
**tempo** -- 収録のbpm



戻り値の型
float







*property* under*: bool*[](#id10 "この定義へのパーマリンク")
読み込んだプリセットからパラメータを返す。



戻り値
**under** -- アンダーバーの扱い
Flaseだと無視、Trueだと休符扱いにします。



戻り値の型
bool







*property* vowel*: dict*[](#id11 "この定義へのパーマリンク")
読み込んだプリセットからパラメータを返す。



戻り値
**vowel** -- | 母音のバリエーションを指定
| keyはCVに後方一致する文字列
| valueは[V CV]の前半のVに当たる文字列



戻り値の型
dict










Indices and tables[](#indices-and-tables "このヘッドラインへのパーマリンク")
=============================================================


* [索引](genindex.html)
* [モジュール索引](py-modindex.html)
* [検索ページ](search.html)








---



© Copyright 2022, delta\_kimigatame.




 Built with [Sphinx](https://www.sphinx-doc.org/) using a
 [theme](https://github.com/readthedocs/sphinx_rtd_theme)
 provided by [Read the Docs](https://readthedocs.org).
 







 jQuery(function () {
 SphinxRtdTheme.Navigation.enable(true);
 });
 

