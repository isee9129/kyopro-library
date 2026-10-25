# mex を効率的に管理する構造
# https://github.com/isee9129/kyopro-library
# verify: ABC330-E https://atcoder.jp/contests/abc330/submissions/80392354
import heapq

class Mex:
    '''
    多重集合 S の mex を効率的に計算する構造
    '''
    __slots__ = 'exists', 'removed', 'count', 'N'

    def __init__(self, N, A=[]):
        '''初期化  O(NlogN)

        Args:
            N (int): 要素の最大値+1。[0, N)外の要素の追加・削除は無視される
            A (List[int]): 数列の初期値
        
        Returns:
            None
        '''
        self.N = N
        self.count = [0]*N
        self.exists = set(range(N))
        for a in A:
            if not(0 <= a < N): continue
            self.exists.discard(a)
            self.count[a] += 1
        self.exists = list(self.exists)
        heapq.heapify(self.exists)
        self.removed = []
    
    def __rem(self):
        # 削除チェック
        while self.exists and self.removed and self.exists[0] == self.removed[0]:
            heapq.heappop(self.exists)
            heapq.heappop(self.removed)
    
    def append(self, i):
        '''i を追加する  O(logN)

        Args:
            i (int): 追加する値
        
        Returns:
            None
        '''
        if not(0 <= i < self.N): return
        if self.count[i] == 0:
            heapq.heappush(self.removed, i)
            self.__rem()
        self.count[i] += 1
    
    def remove(self, i):
        '''i を削除する  O(logN)  存在しない i を指定するとエラーになる
        
        Args:
            i (int): 削除する値
        
        Returns:
            None
        '''
        if not(0 <= i < self.N): return
        assert self.count[i] > 0
        if self.count[i] == 1:
            heapq.heappush(self.exists, i)
        self.count[i] -= 1
    
    def get_mex(self):
        '''現在の集合の mex を得る  O(1)
        
        Args:
            None
        
        Returns:
            int: 現在の mex
        '''
        assert self.exists
        return self.exists[0]
    
    def __len__(self):
        return self.N - len(self.exists) + len(self.removed)
