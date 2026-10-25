# 数値をハッシュ化する
# https://github.com/isee9129/kyopro-library
# 参考文献：
#     解説 - ABC346-C https://atcoder.jp/contests/abc346/editorial/9635

# AtCoderにおいては問題になることはほとんどない

from random import randrange
class HashNum:
    '''set/dictのHackを回避する
    使い方:
        初期化: HN = HashNum()
        ハッシュ化: HN.H(N)
        復元: HN.H(N)
    '''
    def __init__(self, X=None) -> None:
        if X is None:
            self.X = randrange(1, 1<<60)
        else:
            self.X = X
    def H(self, N):
        return N ^ self.X
