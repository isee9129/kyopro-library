# 行列
# https://github.com/isee9129/kyopro-library

MOD = 998244353

class Matrix:
    # MODは外で宣言しておく
    __slots__ = 'rows', 'cols', 'mat'

    @staticmethod
    def list2Matrix(list):
        return Matrix(len(list), len(list[0]), list)
    
    @staticmethod
    def E(n):
        # n*n の単位行列
        res = Matrix(n, n)
        for i in range(n):
            res.mat[i][i] = 1
        return res

    def __init__(self, rows, cols, mat=None):
        self.rows = rows
        self.cols = cols
        self.mat = [[0] * self.cols for _ in range(self.rows)]
        if mat:
            for i in range(rows):
                self.mat[i] = mat[i][:]

    # 添字
    def __getitem__(self, key):
        return self.mat[key]
    
    # print
    def __str__(self):
        return '\n'.join(' '.join(map(str, self.mat[i])) for i in range(self.rows))
    __repr__ = lambda self: str(self.mat)

    def __pos__(self):
        return self
    def __neg__(self):
        return self.times(-1)

    # 加算
    def __add__(self, other):
        # assert self.rows == other.rows and self.cols == other.cols
        res = [[0] * self.cols for _ in range(self.rows)]
        for i in range(self.rows):
            si, oi, ri = self.mat[i], other.mat[i], res[i]
            for j in range(self.cols):
                ri[j] = (si[j] + oi[j]) % MOD
        return Matrix(self.rows, self.cols, res)

    # 減算
    def __sub__(self, other):
        # assert self.rows == other.rows and self.cols == other.cols
        res = [[0] * self.cols for _ in range(self.rows)]
        for i in range(self.rows):
            si, oi, ri = self.mat[i], other.mat[i], res[i]
            for j in range(self.cols):
                ri[j] = (si[j] - oi[j]) % MOD
        return Matrix(self.rows, self.cols, res)

    # 乗算
    # https://judge.yosupo.jp/submission/119798
    def times(self, other):
        # 定数倍
        res = [[0] * self.cols for _ in range(self.rows)]
        for i in range(self.rows):
            si, ri = self.mat[i], res[i]
            for j in range(self.cols):
                ri[j] = (si[j] * other) % MOD
        return Matrix(self.rows, self.cols, res)

    def __mul__(self, other):
        # 行列同士
        if other.__class__ == Matrix:
            assert self.cols == other.rows
            res = [[0] * other.cols for _ in range(self.rows)]
            for i in range(self.rows):
                ri, si = res[i], self.mat[i]
                for k in range(self.cols):
                    sik, ok = si[k], other.mat[k]
                    for j in range(other.cols):
                        ri[j] += (sik * ok[j])
                        ri[j] %= MOD
            return Matrix(self.rows, other.cols, res)
        else:
            return self.times(other)
    
    def __rmul__(self, other):
        return self.times(other)
    
    # べき乗
    def __pow__(self, other):
        tmp = Matrix(self.rows, self.cols, self.mat)
        res = Matrix.E(self.rows)
        i = abs(other)
        while i:
            if i & 1:
                res *= tmp
            tmp *= tmp
            i >>= 1
        if other < 0:
            return res.inv()
        return res

    # 行列式
    # https://judge.yosupo.jp/submission/119873
    def det(self):
        # 要：素数MOD
        A = [a.copy() for a in self.mat]
        res = 1
        for i in range(self.cols):
            Ai = A[i]
            if Ai[i] == 0:
                for j in range(i+1, self.rows):
                    if A[j][i]:
                        break
                else:
                    return 0
                A[i], A[j] = A[j], A[i]
                Ai = A[i]
                res = -res
            inv = pow(Ai[i], MOD-2, MOD)
            for j in range(i+1, self.rows):
                Aj = A[j]
                t = (Aj[i] * inv) % MOD
                for k in range(i+1, self.cols):
                    Aj[k] -= t * Ai[k]
                    Aj[k] %= MOD
        for i in range(self.rows):
            res *= A[i][i]
            res %= MOD
        return res
    
    # 逆行列
    # https://judge.yosupo.jp/submission/119884
    def inv(self):
        res = Matrix.E(self.rows)
        A = [a.copy() for a in self.mat]
        for j in range(self.cols):
            Aj, rj = A[j], res.mat[j]
            if Aj[j] == 0:
                for i in range(j+1, self.rows):
                    if A[i][j]:
                        break
                else:
                    return -1
                A[j], A[i] = A[i], A[j]
                res.mat[j], res.mat[i] = res.mat[i], res.mat[j]
            Aj, rj = A[j], res.mat[j]
            inv = pow(Aj[j], MOD-2, MOD)
            for k in range(self.cols):
                Aj[k] *= inv
                Aj[k] %= MOD
                rj[k] *= inv
                rj[k] %= MOD
            for i in range(self.rows):
                if i == j:
                    continue
                Ai, ri = A[i], res[i]
                c = Ai[j]
                for k in range(self.cols):
                    Ai[k] -= Aj[k] * c
                    Ai[k] %= MOD
                    ri[k] -= rj[k] * c
                    ri[k] %= MOD
        return res
