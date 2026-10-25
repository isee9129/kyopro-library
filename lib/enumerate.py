# 列挙する系色々
# https://github.com/isee9129/kyopro-library

def partitions(N, L=None, M=None):
    """N の最大長さ L, 最大値 M の分割を辞書昇順に列挙する
    
    Args:
        N (int): 分割される個数
        L (int, optional): 要素数の最大
        M (int, optional): 各要素の最大値
    
    Yields:
        List[int]: N の分割
    
    Examples:
        >>> for b in partitions(8, 5, 3): print(b)
        [2, 2, 2, 1, 1]
        [2, 2, 2, 2]
        [3, 2, 1, 1, 1]
        [3, 2, 2, 1]
        [3, 3, 1, 1]
        [3, 3, 2]
    
    Note:
        返値は参照渡しのため、関数の外で書き換えるとヤバい！
    
    """
    if N < 0:
        return
    if N == 0:
        yield (0,)
    if L is None:
        L = N
    if M is None:
        M = N
    stack = [0]
    limit = [M]
    X = 0
    while stack:
        if stack[-1] != limit[-1]:
            stack[-1] += 1
            X += 1
            if X == N:
                yield stack
            elif len(stack) < L:
                stack.append(0)
                limit.append(min(stack[-2], N-X, M))
        else:
            X -= stack.pop()
            limit.pop()

def comb_rep_lim_desc(N, R, LIM):
    """N 個から R 個を、重複を許して各上限 LIM 個取る組み合わせを 降順に得る
    
    Args:
        N (int): 選ぶ要素数
        R (int): 選ぶ個数
        LIM (int): 1 要素の選べる個数の最大値
    
    Yields:
        List[int]: 合法な選び方
    
    Examples:
        >>> for b in comb_rep_lim_desc(3, 3, 2): print(b)
        [2, 2, 1]
        [2, 2, 0]
        [2, 1, 1]
        [2, 1, 0]
        [2, 0, 0]
        [1, 1, 0]
        [1, 0, 0]
    
    Note:
        返値は参照渡しのため、関数の外で書き換えるとヤバい！
    
    """
    stack = [N]
    count = [0]*(N+1)
    count[N] += 1
    while stack:
        # 更新
        count[stack[-1]] -= 1
        stack[-1] -= 1
        if stack[-1] <= -1:
            stack.pop()
            continue
        else:
            count[stack[-1]] += 1
        # 出力
        if len(stack) == R:
            yield stack
        else:
            if count[stack[-1]] == LIM:
                stack.append(stack[-1])
            else:
                stack.append(stack[-1] + 1)
            count[stack[-1]] += 1
