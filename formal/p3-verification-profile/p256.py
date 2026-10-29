"""Minimal pure-Python P-256 affine arithmetic, used ONLY to construct test inputs (non-canonical encodings,
invalid-curve points, and the ECDSA key-substitution key). Never used to decide acceptance."""
P = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
A = P - 3
B = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
N = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
G = (0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
     0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)


def on_curve(pt, b=B):
    x, y = pt
    return (y * y - (x * x * x + A * x + b)) % P == 0


def add(p1, p2):
    if p1 is None: return p2
    if p2 is None: return p1
    (x1, y1), (x2, y2) = p1, p2
    if x1 == x2 and (y1 + y2) % P == 0: return None
    if p1 == p2: lam = (3 * x1 * x1 + A) * pow(2 * y1, -1, P) % P
    else: lam = (y2 - y1) * pow(x2 - x1, -1, P) % P
    x3 = (lam * lam - x1 - x2) % P
    return (x3, (lam * (x1 - x3) - y1) % P)


def mul(k, pt):
    out = None
    while k:
        if k & 1: out = add(out, pt)
        pt = add(pt, pt); k >>= 1
    return out


def neg(pt): return (pt[0], (-pt[1]) % P)


def sqrt(v):
    """P = 3 mod 4: v^((P+1)/4) is a root iff v is a square."""
    r = pow(v, (P + 1) // 4, P)
    return r if r * r % P == v % P else None


def lift_x(x, b=B):
    y = sqrt((x * x * x + A * x + b) % P)
    return None if y is None else (x, y)


def dsks_keys(e, r, s):
    """Keys Q with x(s^-1 (e G + r Q)) = r, computed from public (e, r, s) only:
    Q = r^-1 (s R - e G) for each R with x(R) = r. Returns both candidates (one is the signer's key)."""
    R = lift_x(r)
    assert R is not None
    rinv = pow(r, -1, N)
    eg = neg(mul(e % N, G))
    return [mul(rinv, add(mul(s, Rc), eg)) for Rc in (R, neg(R))]


# ---- a point with a small y (for a Y >= p encoding that still fits 32 bytes): solve x^3 - 3x + (B - y^2) = 0 mod P.
def _pmulmod(a, b, f):
    """a, b: coefficient lists (low first) of degree < 3; f: monic cubic [f0, f1, f2, 1]."""
    out = [0] * 5
    for i, x in enumerate(a):
        for j, y in enumerate(b): out[i + j] = (out[i + j] + x * y) % P
    for d in (4, 3):
        c = out[d]
        if c:
            for k in range(4): out[d - 3 + k] = (out[d - 3 + k] - c * f[k]) % P
    return out[:3]


def _pgcd(a, b):
    def trim(p):
        while p and p[-1] == 0: p = p[:-1]
        return p
    a, b = trim(a), trim(b)
    while b:
        inv = pow(b[-1], -1, P)
        while len(a) >= len(b):
            c = a[-1] * inv % P; shift = len(a) - len(b)
            a = trim([(a[i] - c * (b[i - shift] if 0 <= i - shift < len(b) else 0)) % P for i in range(len(a))])
            if not a: break
        a, b = b, a
    return a


def point_with_small_y(start=1):
    """First (x, y) on P-256 with y >= start found where the cubic in x has exactly one root."""
    for y in range(start, start + 10000):
        f = [(B - y * y) % P, A, 0, 1]
        r, base, e = [1, 0, 0], [0, 1, 0], P
        while e:
            if e & 1: r = _pmulmod(r, base, f)
            base = _pmulmod(base, base, f); e >>= 1
        r[1] = (r[1] - 1) % P  # x^p - x mod f
        g = _pgcd(f, r)
        if len(g) == 2:
            x = (-g[0]) * pow(g[1], -1, P) % P
            assert on_curve((x, y))
            return x, y
    raise ValueError('none found')
