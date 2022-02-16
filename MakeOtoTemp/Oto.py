class Oto:
    '''
    UTAUの原音設定ファイルのデータを扱う

    Attributes
    ----------
    filename :str
        voiceルートからのファイルの相対パス
    alias :str
        エイリアス
    offset :float
        オフセット(setparamでいうところの左ブランク)
    pre :float
        先行発声
    ove :float
        オーバーラップ
    consonant :float
        子音部(setparamでいうところの固定範囲)
    blank :float
        | ブランク(setparamでいうところの右ブランク)
        | 正の値のときはwav末尾からのmsを表す。
        | 負の値のときはオフセットからのmsの絶対値に-1をかけたものを表す。
    rounds :int ,default -1
        | 書き出し時の各パラメータを小数何桁で丸めるかを指定する。
        | -1の時は丸めない。
    '''

    filename :str
    alias :str
    offset :float
    pre :float
    ove :float
    consonant :float
    blank :float
    rounds :int

    def __init__(self, filename: str, alias: str, offset: float, pre: float,
                 ove: float, consonant: float, blank: float):
        '''
        Parameters
        ----------
        filename :str
            voiceルートからのファイルの相対パス
        alias :str
            エイリアス
        offset :float
            オフセット(setparamでいうところの左ブランク)
        pre :float
            先行発声
        ove :float
            オーバーラップ
        consonant :float
            子音部(setparamでいうところの固定範囲)
        blank :float
            | ブランク(setparamでいうところの右ブランク)
            | 正の値のときはwav末尾からのmsを表す。
            | 負の値のときはオフセットからのmsの絶対値に-1をかけたものを表す。
        '''
        self.filename = filename
        self.alias = alias
        self.offset = offset
        self.pre = pre
        self.ove = ove
        self.consonant = consonant
        self.blank = blank
        self.rounds = -1

    def __str__(self) -> str:
        '''
        | oto.iniに書き出す形式の文字列を返す。
        | floatはroundsで与えられた桁数で丸める。
        
        Returns
        -------
        filename = alias,offset,pre,ove,consonant,blank
        '''

        temp :list = []
        temp.append(self.alias)

        if(self.rounds <= -1):
            temp.append(str(self.offset))
            temp.append(str(self.pre))
            temp.append(str(self.ove))
            temp.append(str(self.consonant))
            temp.append(str(self.blank))
        else:
            temp.append(str(round(self.offset, self.rounds)))
            temp.append(str(round(self.pre, self.rounds)))
            temp.append(str(round(self.ove, self.rounds)))
            temp.append(str(round(self.consonant, self.rounds)))
            temp.append(str(round(self.blank, self.rounds)))


        return (self.filename + "=" + ",".join(temp))