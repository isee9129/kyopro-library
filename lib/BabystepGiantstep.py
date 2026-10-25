# Baby-step Giant-step テンプレ
# https://github.com/isee9129/kyopro-library
# 参考文献：
#     解説 - ABC270-G https://atcoder.jp/contests/abc270/editorial/4965
# 使用例：
#     ABC270-G https://atcoder.jp/contests/abc270/submissions/40789394

def BsGs(s, g):
    """f^n(s) = g となる最小の n を求める
    
    Args:
        s (int): 初期値
        g (int): 目標値
    
    Returns:
        int: f^n(s) = g となる最小の n, 存在しない場合は -1
    """

    # ---------- settings ----------

    def f(x):  # f(x) を定義
        return x

    _N = 10**9  # f^m(x) = x なる 1 <= m <= N が必ず存在するような N

    _M = int(_N**0.5)+1
    def fM(x):  # f^M(x) も定義
        return x

    # ---------- ここまで ----------

    # Baby-step
    # f^j(g) (1 <= j <= M) を求めておく
    _X = dict()
    for j in range(_M):
        g = f(g)
        _X[g] = j+1
    
    # Giant-step
    # f^iM(s) = f^j(g) なる i, j を探す
    for i in range(-((-_N)//_M)):
        s = fM(s)
        if s in _X:
            return (i + 1) * _M - _X[s]
    return -1