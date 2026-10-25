# Mo's algorithm
# https://github.com/isee9129/kyopro-library
# 参考文献：
#     Mo's algorithm のPython実装 (コピペ用) - 学習する天然ニューラルネット https://aotamasaki.hatenablog.com/entry/2020/08/04/Mo%27s_algorithm_python
#     Mo’s algorithm | Nyaan’s Library https://nyaannyaan.github.io/library/misc/mo.hpp.html
from math import sqrt, ceil

class Mo:
    def __init__(self, N, Q, A):
        """Mo's Algorithm
        
        Args:
            N (int): 配列長さ
            Q (int): クエリ数
            ls (List): 操作対象の数列
        
        Note:
            N, Q > 10^6 では使わない（確実に間に合わない）
            N, Q > 5*10^5 でもあやしい
        
        """
        self.A = A
        self.N = N
        self.Q = Q
        self.data = [0]*Q  # クエリ本体
        self.query = [0]*Q  # クエリソート用
        self.W = ceil(1.22474487 * N / sqrt(Q))  # 分割幅 √1.5 N/√Q
    
    def addQuery(self, i, l, r):
        """クエリ[l,r)を追加

        Args:
            i (int): クエリNo
            l (int): 下端
            r (int): 上端

        """
        self.data[i] = (l<<20)|r
        l //= self.W
        self.query[i] = (l<<40) + ((-r if l&1 else r)<<20) + i
    
    # ------------------ 問題毎に書き換える部分 ------------------
    def initProcess(self):
        """初期化"""
        self.C = [0]*(2*10**5+1)
        self.n = 0
    
    def addR(self, i):
        """要素 A[i] を右に加える"""
        x = self.C[self.A[i]]
        self.C[self.A[i]] += 1
        self.n += x * (x-1) // 2
    
    def addL(self, i):
        """要素 A[i] を左に加える"""
        self.addR(i)

    def deleteR(self, i):
        """要素 A[i] を右から除く"""
        self.C[self.A[i]] -= 1
        x = self.C[self.A[i]]
        self.n -= x * (x-1) // 2

    def deleteL(self, i):
        """要素 A[i] を左から除く"""
        self.deleteR(i)

    def ans(self):
        """クエリの答え"""
        return self.n
    # -------------- 問題毎に書き換える部分ここまで --------------

    def solve(self):
        """クエリにまとめて答える

        Returns:
            List: 各クエリの結果

        """
        self.query.sort()

        self.l = 0
        self.r = 0

        res = [-1]*self.Q

        self.initProcess()
        mask = (1<<20)-1
        for lri in self.query:
            i = lri & mask
            l, r = divmod(self.data[i], 1<<20)
            # クエリ[l,r)について計算する
            for j in range(self.r, r):  # r 伸ばす
                self.addR(j)
            for j in range(self.r - 1, r - 1, -1):  # r 縮む
                self.deleteR(j)
            for j in range(self.l, l):  # l 縮む
                self.deleteL(j)
            for j in range(self.l - 1, l - 1, -1):  # l 伸ばす
                self.addL(j)
            self.l = l
            self.r = r

            res[i] = self.ans()
        return res
