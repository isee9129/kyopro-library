# Bostan-Mori のアルゴリズム
# https://github.com/isee9129/kyopro-library
# 参考文献：
#     線形漸化的数列のN項目の計算 - Qiita https://qiita.com/ryuhe1/items/da5acbcce4ac1911f47a
#     線形漸化的数列の第 K 項 - AtCoderInfo https://info.atcoder.jp/entry/algorithm_lectures/linearly_recurrent_sequence_kth_term
#     Bostan–Mori のアルゴリズム（発展） - AtCoderInfo https://info.atcoder.jp/entry/algorithm_lectures/bostan_mori_advanced

# MOD = 998244353

def even(P):
    return P[0::2]

def odd(P):
    return P[1::2]

# naiveな実装 O(NM)
# 必要に応じてconvolutionに置き換える
def mul(P, Q):
    N = len(P); M = len(Q)
    R = [0]*(N+M-1)
    for i in range(N):
        for j in range(M):
            R[i+j] += P[i]*Q[j]
            R[i+j] %= MOD
    return R

def negx(Q):
    return [(-n if i&1 else n) for i, n in enumerate(Q)]

def bostan_mori(N, P, Q):
    '''Bostan-Mori のアルゴリズム で P(x)/Q(x) の x^N の係数を求める
    Args:
        N (int): 求める項
        P (list[int]): 分子の係数
        Q (list[int]): 分母の係数
    Returns:
        int: [x^N] P(x)/Q(x)
    '''
    while N > 0:
        Qx = negx(Q)
        U = mul(P, Qx)
        if N&1: P = odd(U)
        else: P = even(U)
        Q = even(mul(Q, Qx))
        N >>= 1
    return P[0] * pow(Q[0], -1, MOD)

# # 例：フィボナッチ数列の第 100 項
# print(bostan_mori(100, [0, 1], [1, -1, -1]))
