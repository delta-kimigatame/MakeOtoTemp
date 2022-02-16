#preset
ENTRIES :list =["[TEMPO]",
                "[OFFSET]",
                "[MAXNUM]",
                "[UNDER]",
                "[NOHEAD]",
                "[NOVCV]",
                "[ONLYCONSONANT]",
                "[VOWEL]",
                "[CONSONANT]",
                "[REPLACE]"
                ]

DEFAULT_TEMPO :float = 100
DEFAULT_OFFSET :float = 800
DEFAULT_MAX :int = 2
DEFAULT_UNDER :bool = True
DEFAULT_BEGINING_CV :bool = True
DEFAULT_NO_HEAD :bool = False
DEFAULT_NO_VCV :bool = False
DEFAULT_ONLY_CONSONANT :bool = False

#vowel
DEFAULT_VOWEL :dict = {}
__lines :list =[]
__lines.append("a=ぁ,あ,か,が,さ,ざ,た,だ,な,は,ば,ぱ,ま,ゃ,や,ら,わ,ァ,ア,カ,ガ,サ,ザ,タ,ダ,ナ,ハ,バ,パ,マ,ャ,ヤ,ラ,ワ")
__lines.append("e=ぇ,え,け,げ,せ,ぜ,て,で,ね,へ,べ,ぺ,め,れ,ゑ,ェ,エ,ケ,ゲ,セ,ゼ,テ,デ,ネ,ヘ,ベ,ペ,メ,レ,ヱ")
__lines.append("i=ぃ,い,き,ぎ,し,じ,ち,ぢ,に,ひ,び,ぴ,み,り,ゐ,ィ,イ,キ,ギ,シ,ジ,チ,ヂ,ニ,ヒ,ビ,ピ,ミ,リ,ヰ")
__lines.append("o=ぉ,お,こ,ご,そ,ぞ,と,ど,の,ほ,ぼ,ぽ,も,ょ,よ,ろ,を,ォ,オ,コ,ゴ,ソ,ゾ,ト,ド,ノ,ホ,ボ,ポ,モ,ョ,ヨ,ロ,ヲ")
__lines.append("n=ん,ン")
__lines.append("u=ぅ,う,く,ぐ,す,ず,つ,づ,ぬ,ふ,ぶ,ぷ,む,ゅ,ゆ,る,ゥ,ウ,ク,グ,ス,ズ,ツ,ヅ,ヌ,フ,ブ,プ,ム,ュ,ユ,ル,ヴ")

for __line in __lines:
    value, keys = __line.split("=")
    for k in keys.split(","):
        DEFAULT_VOWEL[k] = value


#consonant
DEFAULT_CONSONANT :dict = {}
DEFAULT_CONSONANT_TIME :dict = {}
__lines :list =[]
__lines.append("=あ,い,う,え,お,ん,息,吸=0")
__lines.append("ch=ch,ち,ちぇ,ちゃ,ちゅ,ちょ=150")
__lines.append("gy=gy,ぎ,ぎぇ,ぎゃ,ぎゅ,ぎょ=60")
__lines.append("ts=ts,つ,つぁ,つぃ,つぇ,つぉ=170")
__lines.append("ty=ty,てぃ,てぇ,てゃ,てゅ,てょ=75")
__lines.append("py=py,ぴ,ぴぇ,ぴゃ,ぴゅ,ぴょ=100")
__lines.append("ry=ry,り,りぇ,りゃ,りゅ,りょ=70")
__lines.append("ny=ny,に,にぇ,にゃ,にゅ,にょ=70")
__lines.append("r=r,ら,る,れ,ろ=70")
__lines.append("hy=hy,ひ,ひぇ,ひゃ,ひゅ,ひょ=100")
__lines.append("dy=dy,でぃ,でぇ,でゃ,でゅ,でょ=75")
__lines.append("by=by,び,びぇ,びゃ,びゅ,びょ=45")
__lines.append("b=b,ば,ぶ,べ,ぼ=50")
__lines.append("d=d,だ,で,ど,どぅ=60")
__lines.append("g=g,が,ぐ,げ,ご=80")
__lines.append("f=f,ふ,ふぁ,ふぃ,ふぇ,ふぉ=130")
__lines.append("h=h,は,へ,ほ=110")
__lines.append("k=k,か,く,け,こ=100")
__lines.append("j=j,じ,じぇ,じゃ,じゅ,じょ=110")
__lines.append("m=m,ま,む,め,も=75")
__lines.append("n=n,な,ぬ,ね,の=70")
__lines.append("p=p,ぱ,ぷ,ぺ,ぽ=100")
__lines.append("s=s,さ,す,すぃ,せ,そ=150")
__lines.append("sh=sh,し,しぇ,しゃ,しゅ,しょ=200")
__lines.append("t=t,た,て,と,とぅ=100")
__lines.append("w=w,うぃ,うぅ,うぇ,うぉ,わ,を=50")
__lines.append("v=v,ヴ,ヴぁ,ヴぃ,ヴぅ,ヴぇ,ヴぉ=100")
__lines.append("y=y,いぃ,いぇ,や,ゆ,よ,ゐ,ゑ=30")
__lines.append("ky=ky,き,きぇ,きゃ,きゅ,きょ=130")
__lines.append("z=z,ざ,ず,ずぃ,ぜ,ぞ=80")
__lines.append("my=my,み,みぇ,みゃ,みゅ,みょ=60")
__lines.append("ng=ガ,グ,ゲ,ゴ=50")
__lines.append("ngy=ギャ,ギ,ギュ,ギェ,ギョ=40")
__lines.append("・=・あ,・い,・う,・え,・お,・ん=50")
for __line in __lines:
    value, cvs, time = __line.split("=")
    DEFAULT_CONSONANT_TIME[value] = float(time)
    for cv in cvs.split(","):
        DEFAULT_CONSONANT[cv] = value

#replace
DEFAULT_REPLACE :list = []