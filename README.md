# MakeOtoTemp(原音設定テンプレ吐き出す君)

ダウンロードはこちら(https://github.com/delta-kimigatame/MakeOtoTemp/releases)

### これは何?

* 飴屋／菖蒲氏によって公開されている、Windows向けに作成された歌声合成ソフトウェア「UTAU」の、
音声ライブラリ作成支援ツールです。

    UTAU公式サイト(http://utau2008.web.fc2.com/)
* 録音リスト又は音源フォルダからCVVCの原音設定の叩き台を生成することができます。
* 生成されるものは、あくまでも叩き台です。詳細な設定には別のツールが必要です。
* このソフトは、2015年3月ごろのUTAU界隈の動向に合わせて作成したものを、オープンソースで作り直したものです。
* 使用するには「.NET 6.0 ランタイム」が必要です。必要に応じて下記urlからインストールしてください。

    「.NET 6.0 ランタイム」(https://dotnet.microsoft.com/ja-jp/download/dotnet/6.0/runtime?cid=getdotnetcore)

---

### 使い方
* 音源フォルダ又は録音リストをmkototemp.exeにD&Dしてください。

    mkototemp.exeと同じフォルダにoto.iniが生成されます。

* 設定ファイルとして、mkototemp.iniを参照します。

    存在しない場合は初期化して生成します。いじりすぎてわからなくなったら削除してください。

---

### プリセットの仕様

###### [TEMPO]
収録時のBPMです。

###### [OFFSETT]
wavの頭から発声の開始までの時間です。
msec(1000分の1秒)単位で指定してください。

###### [MAXNUM]
重複エイリアスをいくつまで許容するかです。
2未満に設定しても意味がありません。

###### [UNDER]
_の扱いです。
0だと区切り文字とみなして無視し、1だと休符扱いにします。

主に日本語の録音リストでは1、アルファベットで作成する録音リストでは0を推奨します。

###### [NOHEAD]
ファイル頭や休符後の[- CV]の生成規則を指定します。
0の場合通常通り生成
1の場合-が付かない単独音を生成
2の場合エイリアスを生成しなくなります。

通常の場合は0、文頭と文中を区別しないCVVCの場合1を指定します。

###### [NOVCV]
連続音用のエイリアスを生成するか?を指定します。
0の場合通常通り生成
1の場合生成しなくなります。

###### [ONLYCONSONANT]
VC音素を生成した時に，子音単体音素を生成するか選択します。
0で通常通り。
1で生成されます。

日本語音源ではほとんどの場合0で問題ありません。外国語の場合1を推奨します。

###### [VOWEL]
母音のバリエーションを指定します。

`[母音の種類]=[CV1],[CV2],[CV3]`のように指定します。

CVは後方一致で検索します。

###### [CONSONANT]
子音のバリエーションを指定します。

`[子音の種類]=[CV1],[CV2],[CV3]=[子音の平均長さms]`のように指定します。

CVは完全一致で検索します。

* 子音の種類欄を空欄にすると、連続音のみ生成します。
* 子音部分に"・"を指定した場合のみエイリアスを"・ "に置換します。(eve式喉切り例外)
* 子音の種類を"-"に指定すると、頭子音群として認識します。(外国語音源用例外)
* 子音の種類を"*"に指定すると、尾子音群として認識します。(外国語音源用例外)

###### [REPLACE]
ファイル名とエイリアスの置換を指定します。
`置換後のエイリアス=元のファイル名`

ファイル名通りエイリアスを生成したくない場合に使います。

windowsではファイル名の大文字と小文字の区別がないことなどを原因で、英語音源等で必要になります。

---

### 免責事項
* 本ソフトウェアを使用して生じたいかなる不具合についても、作者は責任を負いません。
* 作者は、本ソフトウェアの不具合を修正する責任を負いません。

---

### 技術仕様

APIについては(https://delta-kimigatame.github.io/MakeOtoTemp/)

---

### リンク

twitter(https://twitter.com/delta_kuro)
github(https://github.com/delta-kimigatame/MakeOtoTemp)
