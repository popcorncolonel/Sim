import random
import re
import sys


def bernoulli(p: float) -> bool:
    """
    :param p: Probability of returning True
    """
    x = random.random()
    return x < p


def binomial(n: int, p: float) -> list:
    result = []
    for i in range(n):
        result.append(bernoulli(p))
    return result


def is_n_units_away(pos1: tuple, pos2: tuple, n: int):
    """
    Returns True if pos1 is <= n units away from pos2
    """
    # Chebyshev distance metric
    max_dist = max(abs(pos1[0] - pos2[0]),
                   abs(pos1[1] - pos2[1]))
    return max_dist <= n


def clip(lo, x, hi=None):
    """ lo < hi """
    if hi == None:
        hi = float('inf')
    return max(lo, min(hi, x))


class Reprinter:
    def __init__(self):
        self.text = ''

    @staticmethod
    def moveup(lines):
        for _ in range(lines):
            sys.stdout.write("\x1b[A")

    def reprint(self, text):
        # Clear previous text by overwriting non-spaces with spaces
        self.moveup(self.text.count("\n"))
        sys.stdout.write(re.sub(r"[^\s]", " ", self.text))

        # Print new text
        lines = min(self.text.count("\n"), text.count("\n"))
        self.moveup(lines)
        sys.stdout.write(text)
        self.text = text