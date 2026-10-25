# IndexSet
# https://github.com/isee9129/kyopro-library
# 参考文献：
#     [0,n)の整数の集合を管理する定数倍が軽いデータ構造 - TopCoderの学習のお時間 https://topcoder-tomerun.hatenablog.jp/entry/2021/06/12/134643

# import random

class IndexSet():
    '''[0, N) の整数の集合を高速に管理'''

    def __init__(self, N: int, L=[], fill=False) -> None:
        '''IndexSet
        
        Args:
            N (int): 管理する整数の個数
            L (List[int], optional): 初期値
            fill (bool, optional): 全部埋めた状態で始める？
        '''
        self.N = N
        if fill:
            self.que = list(range(N))
            self.pos = list(range(N))
        else:
            self.que = []
            self.pos = [-1]*N
            for x in L:
                self.add(x)
        
    def add(self, v: int) -> None:
        '''v を追加する。存在する値を追加してもいいが、個数は増えない
        
        Args:
            v (int): 追加する値
        
        '''
        assert 0 <= v < self.N
        if self.pos[v] != -1: return
        self.pos[v] = len(self.que)
        self.que.append(v)
    
    def remove(self, v: int) -> None:
        '''v を削除する。存在しない値を削除しようとするとError
        
        Args:
            v (int): 削除する値
        
        '''
        assert 0 <= v < self.N
        assert self.pos[v] != -1
        p = self.pos[v]
        b = self.que[-1]
        self.que[p] = b
        self.que.pop()
        self.pos[b] = p
        self.pos[v] = -1
    
    def choice(self) -> int:
        '''要素からランダムに 1 つ返す'''
        assert 0 < len(self.que)
        return self.que[random.randrange(len(self.que))]
    
    def pop(self) -> int:
        '''要素からランダムに 1 つ取り出す'''
        assert 0 < len(self.que)
        n = self.choice()
        self.remove(n)
        return n
    
    def __contains__(self, v: int) -> bool:
        assert 0 <= v < self.N
        return self.pos[v] != -1

    def __len__(self) -> int:
        return len(self.que)
    
    def __getitem__(self, idx: int) -> int:
        assert -len(self.que) <= idx < len(self.que)
        return self.que[idx]
    
    def __iter__(self):
        return self.que.__iter__()
    
    def __str__(self) -> str:
        return str(self.que)

