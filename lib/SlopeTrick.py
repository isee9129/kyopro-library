# slope trick
# https://github.com/isee9129/kyopro-library
# 参考文献：
#     slope trick (1) 解説編 | maspyのHP https://maspypy.com/slope-trick-1-%E8%A7%A3%E8%AA%AC%E7%B7%A8

from heapq import heappush, heappushpop

class SlopeTrick:
    """slope trick
    
    主に f(x) = Σ|x-a| を処理するやつ"""

    def __init__(self):
        """初期化"""
        self.minf = 0
        self.L = []
        self.R = []

    def getFx(self, x):
        """f(x) の値を取得する。O(N)！重い！"""
        res = self.minf
        for l in self.L:
            if -l > x:
                res += -l - x
        for r in self.R:
            if x > r:
                res += x - r
        return res
    
    def getMin(self):
        """最小値を取得する
        
        Returns:
            minf (int): f(x) の最小値
        
        """
        return self.minf

    def getArgMin(self):
        """最小値となる x の範囲を取得する
        
        Returns:
            l (int): 最小値を取る x の最小値
            r (int): 最小値を取る x の最大値
        
        """
        return (self.L[0] if self.L else -10**18), (self.R[0] if self.R else 10**18)

    def addConstant(self, a):
        """f(x) に a を足す"""
        self.minf += a
    
    def addXA(self, a):
        """f(x) に max(0, x-a) を足す"""
        if self.L:
            if -self.L[0] > a:
                self.minf += -self.L[0] - a
        heappush(self.R, -heappushpop(self.L, -a))
    
    def addAX(self, a):
        """f(x) に max(0, a-x) を足す"""
        if self.R:
            if a > self.R[0]:
                self.minf += a - self.R[0]
        heappush(self.L, -heappushpop(self.R, a))
    
    def addAbsXA(self, a):
        """f(x) に |x-a| を足す"""
        self.addXA(a)
        self.addAX(a)
    
    def cumMin(self):
        """累積min化する f(x) = min_{y<=x} f(y)"""
        self.R = []
    
    def cumMinR(self):
        """右累積min化する f(x) = min_{x<=y} f(y)"""
        self.L = []
    
