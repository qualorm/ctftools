'''
from: https://github.com/orisano/owiener/blob/master/owiener.py
'''
from typing import Tuple, Iterator, Iterable, Optional
from gmpy2 import is_square
import math

def rational_to_contfrac(x: int, y: int) -> Iterator[int]:
    """
    ref: https://en.wikipedia.org/wiki/Euclidean_algorithm#Continued_fractions
    
    >>> list(rational_to_contfrac(4, 11))
    [0, 2, 1, 3]
    """
    while y:
        a = x // y
        yield a
        x, y = y, x - a * y


def contfrac_to_rational_iter(contfrac: Iterable[int]) -> Iterator[Tuple[int, int]]:
    """
    ref: https://www.cits.ruhr-uni-bochum.de/imperia/md/content/may/krypto2ss08/shortsecretexponents.pdf (6)
    """
    n0, d0 = 0, 1
    n1, d1 = 1, 0
    for q in contfrac:
        n = q * n1 + n0
        d = q * d1 + d0
        yield n, d
        n0, d0 = n1, d1
        n1, d1 = n, d


def convergents_from_contfrac(contfrac: Iterable[int]) -> Iterator[Tuple[int, int]]:
    """
    ref: https://www.cits.ruhr-uni-bochum.de/imperia/md/content/may/krypto2ss08/shortsecretexponents.pdf Section.3
    """
    n_, d_ = 1, 0
    for i, (n, d) in enumerate(contfrac_to_rational_iter(contfrac)):
        if i % 2 == 0:
            yield n + n_, d + d_
        else:
            yield n, d
        n_, d_ = n, d


def attack(e: int, n: int) -> Optional[int]:
    """
    ref: https://www.cits.ruhr-uni-bochum.de/imperia/md/content/may/krypto2ss08/shortsecretexponents.pdf Section.4
    """
    f_ = rational_to_contfrac(e, n)
    for k, dg in convergents_from_contfrac(f_):
        edg = e * dg
        phi = edg // k

        x = n - phi + 1
        if x % 2 == 0 and is_square((x // 2) ** 2 - n):
            g = edg - phi * k
            return dg // g
    return None

if __name__ == '__main__':
    from pwn import *
    from Crypto.Util.number import long_to_bytes
    HOST = 'mercury.picoctf.net'
    PORT = 41508
    io = remote(HOST, PORT)
    io.recvline()
    e = int(io.recvline().decode().split(': ')[1])
    n = int(io.recvline().decode().split(': ')[1])
    c = int(io.recvline().decode().split(': ')[1])
    d = attack(e, n)
    if d:
        warn(f'{d=}')
        pt = pow(c,d,n)
        flag = long_to_bytes(pt)
        warn(flag.decode())
    else:
        print('Attack did not succeed')
