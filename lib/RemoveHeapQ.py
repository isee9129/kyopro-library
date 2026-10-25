# 削除可能 heapq
# https://github.com/isee9129/kyopro-library
import heapq

class RemovableHeapQ:
    __slots__ = 'exists', 'removed'

    def __init__(self, A=None):
        """初期化

        Args:
            A (List[Any], optional): 初期値
        
        Returns:
            None
        """
        if A is None:
            self.exists = []
        else:
            self.exists = A[:]
        heapq.heapify(self.exists)
        self.removed = []
    
    def __rem(self):
        # 削除チェック
        while self.exists and self.removed and self.exists[0] == self.removed[0]:
            heapq.heappop(self.exists)
            heapq.heappop(self.removed)
    
    def append(self, item):
        """itemを追加する

        Args:
            item (Any): 追加する値
        
        Returns:
            None
        """
        heapq.heappush(self.exists, item)
    
    def remove(self, item):
        """itemを削除する。存在しないitemを指定してもエラーにはならないが、たぶん後々バグる
        
        Args:
            item (Any): 削除する値
        
        Returns:
            None
        """
        heapq.heappush(self.removed, item)
        self.__rem()
    
    def pop(self):
        """最小の要素を取得して、queueから削除する

        Args:
            None

        Returns:
            Any: 最小の要素
        """
        assert self.exists
        res = heapq.heappop(self.exists)
        self.__rem()
        return res

    def appendpop(self, item):
        """append -> pop の順にまとめて処理する。ちょっと速い
        
        Args:
            item (Any): 追加する値

        Returns:
            Any: 追加後の最小の要素
        """
        res = heapq.heappushpop(self.exists, item)
        self.__rem()
        return res

    def replace(self, item):
        """pop -> append の順にまとめて処理する。ちょっと速い
        
        Args:
            item (Any): 追加する値

        Returns:
            Any: 追加前の最小の要素
        """
        assert self.exists
        res = heapq.heapreplace(self.exists, item)
        self.__rem()
        return res
    
    def smallest(self):
        """現在の最小の要素を取得する

        Args:
            None
        
        Returns:
            Any: 最小の要素
        """
        assert self.exists
        return self.exists[0]

    def getExists(self):
        """現在残ってる全要素を取得する
        
        Args:
            None
        
        Returns:
            List[Any]: 残ってる要素、昇順
        """
        res = []
        while self.exists:
            res.append(self.pop())
        self.exists = res[:]
        heapq.heapify(self.exists)
        return res
    
    def __getitem__(self, key):
        # 0 以外での使用はしない方がいい
        return self.exists[key]
    
    def __len__(self):
        return len(self.exists) - len(self.removed)
    
    def __str__(self):
        # デバッグ用。残ってるものだけ知りたい場合は self.getExists()
        return f'exists: {self.exists}  removed: {self.removed}'