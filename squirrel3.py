# ~!~ coding: utf-8 ~!~
"""
   squirrel3
   ~~~~~~~~~

   Provides a noise function which is fast and had good distribution.  It was
   introduced by Squirrel Eiserloh at 'Math for Game Programmers: Noise-based
   RNG', GDC17.

   :copyright: (c) 2017 by Heungsub Lee.
   :license: BSD, see LICENSE for more details.
"""
import random


__all__ = ['squirrel3', 'Squirrel3Random']


# The base bit-noise constants were crafted to have distinctive and interesting
# bits, and have so far produced excellent experimental test results.
NOISE1 = 0xb5297a4d  # 0b0110'1000'1110'0011'0001'1101'1010'0100
NOISE2 = 0x68e31da4  # 0b1011'0101'0010'1001'0111'1010'0100'1101
NOISE3 = 0x1b56c4e9  # 0b0001'1011'0101'0110'1100'0100'1110'1001

CAP = 1 << 32


def squirrel3(n, seed=0):
    """Returns an unsigned integer containing 32 reasonably-well-scrambled
    bits, based on a given (signed) integer input parameter `n` and optional
    `seed`.  Kind of like looking up a value in an infinitely large
    non-existent table of previously generated random numbers.
    """
    n *= NOISE1
    n += seed
    n ^= n >> 8
    n += NOISE2
    n ^= n << 8
    n *= NOISE3
    n ^= n >> 8
    # Cast into uint32 like the original `Squirrel3`.
    return n % CAP


class Squirrel3Random(random.Random):

    _n = 0

    def seed(self, a=None):
        if a is None:
            a = 0
        self._seed = a

    def random(self):
        n = self._n
        self._n += 1
        return squirrel3(n, self._seed) / float(CAP)
