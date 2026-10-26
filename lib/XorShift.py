# XorShift による高速な乱数生成
# https://github.com/isee9129/kyopro-library
# 参考文献：
#     https://ei1333.github.io/library/other/xor-shift.hpp.html
#     https://www.cepstrum.co.jp/hobby/xorshift/xorshift.html
# 整数はやや低い値が出やすい。具体的には randrange(X) で 0 は X-1 の 1 + X / 2**32 倍くらい出やすい。

class XorShift32:
    """簡易 32 bit RNG
    
    非常に高速に動作する乱数生成器
    random = XorShift32() と宣言しておくことで、import random とほぼ同じ使い方が可能
    実数分布は一様分布 random(), uniform(a, b) のみ対応
    """
    MASK = (1 << 32) - 1
    R = 1 / (1 << 32)
    val: int

    def __init__(self, seed: int = 998244353) -> None:
        """初期 seed を指定して初期化
        
        Args:
            seed (int, optional): 初期 seed 、必ず非負整数にする
        """
        self.val = seed & XorShift32.MASK
    
    def _gen(self) -> int:
        # 乱数を更新し、現在の値を返す
        # # ↓ 超高速・短周期 (16,777,215)。質の保証はできない。
        # self.val ^= self.val << 7
        # self.val &= RNG.MASK
        # self.val ^= self.val >> 9
        # ↓ 高速・長周期 4,294,967,295 (2^32 - 1)
        self.val ^= self.val << 13
        self.val &= XorShift32.MASK
        self.val ^= self.val >> 17
        self.val ^= self.val << 5
        self.val &= XorShift32.MASK
        return self.val
    
    def randrange(self, start: int, stop: int=None, step: int=1) -> int:
        """range(start) / range(start, stop[, step]) 内の整数を 1 つ得る
        
        Args:
            start (int): 上限 または 下限
            stop (int, optional): 上限
            step (int, optional): 間隔
        
        Returns:
            int: 0 以上 start 未満 / start 以上 stop 未満 (step 間隔) のランダム整数
        """
        if stop is None:
            return self._gen() % start
        else:
            return start - self._gen() % ((start - stop) // step) * step
    
    def randint(self, a: int, b: int) -> int:
        """a 以上 b 以下の整数を 1 つ得る
        
        Args:
            a (int): 下限
            b (int): 上限
        
        Returns:
            int: a 以上 b 以下の乱数
        """
        return a + self._gen() % (b - a + 1)
    
    def random(self) -> float:
        """0 以上 1 未満の浮動小数点数を 1 つ得る

        Returns:
            float: 0 以上 1 未満の実数
        """
        return self._gen() * XorShift32.R
    
    def uniform(self, a: float, b: float) -> float:
        """a 以上 b 未満の浮動小数点数を 1 つ得る

        Returns:
            float: a 以上 b 未満の実数
        """
        return a + (b - a) * (self._gen() * XorShift32.R)
    
    def choice(self, seq):
        """seq からランダムに 1 つ要素を得る
        
        Args:
            seq (Sequence): 対象となる sequence
        
        Returns:
            Any: 選ばれた要素
        """
        return seq[self._gen() % (len(seq))]
    
    def choices(self, population, weights=None, cum_weights=None, k:int=1):
        """population からランダムに k 個要素を得る。各試行は独立。
        
        Args:
            population (Sequence): 対象となる sequence
            weight (List[float], optional): 各要素の出現率の重み
            cum_weight (List[float], optional): 各要素の出現率の重みの累積和
            k (int, optional): 選ぶ回数
        
        Returns:
            Any: 選ばれた要素のリスト
        """
        n = len(population)
        if weights is None and cum_weights is None:
            res = [population[0]] * k
            for i in range(k):
                res[i] = population[self._gen() % n]
            return res
        if cum_weights is None:
            cum_weights = list(weights)
            for i in range(1, n):
                cum_weights[i] += cum_weights[i - 1]
        total = cum_weights[n - 1]
        res = [population[0]] * k
        for i in range(k):
            r = (self._gen() * XorShift32.R) * total
            ok = n - 1
            ng = -1
            while ok - ng > 1:
                mid = (ok + ng) // 2
                if r < cum_weights[mid]:
                    ok = mid
                else:
                    ng = mid
            res[i] = population[ok]
        return res

    def shuffle(self, seq) -> None:
        """seq を直接書き換える形で混ぜる
        
        Args:
            seq (Sequence): 対象となる sequence
        """
        for i in range(len(seq)-1, 0, -1):
            n = self._gen() % (i+1)
            seq[i], seq[n] = seq[n], seq[i]
    
    def sample(self, population, k: int, counts=None):
        """poplation からランダムに重複なく k 個要素を得る

        count を使う場合、総和が 2^32 以上にならないように注意
        
        Args:
            population (Sequence): 対象となる sequence
            k (int): 抜き出す個数
            count (List[int], optional): 各要素の重複回数
        
        Returns:
            Any: 選ばれた要素のリスト
        """
        N = len(population)
        if counts is None:
            L = N - k
            S = set()
            for i in range(L, N):
                r = self._gen() % (i + 1)
                if r in S:
                    S.add(i)
                else:
                    S.add(r)
            idx = list(S)
            for i in range(k-1, 0, -1):
                j = self._gen() % (i + 1)
                idx[i], idx[j] = idx[j], idx[i]
            return [population[i] for i in idx]
        else:
            cum_counts = counts[:]
            for i in range(N-1):
                cum_counts[i+1] += cum_counts[i]
            M = cum_counts[-1]
            L = M - k
            S = set()
            for i in range(L, M):
                r = self._gen() % (i + 1)
                if r in S:
                    S.add(i)
                else:
                    S.add(r)
            idx = list(S)
            for i in range(k-1, 0, -1):
                j = self._gen() % (i + 1)
                idx[i], idx[j] = idx[j], idx[i]
            res = [population[0]]*k
            for i in range(k):
                r = idx[i]
                ok = N - 1
                ng = -1
                while ok - ng > 1:
                    mid = (ok + ng) // 2
                    if r < cum_counts[mid]:
                        ok = mid
                    else:
                        ng = mid
                res[i] = population[ok]
            return res
