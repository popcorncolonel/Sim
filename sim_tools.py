import random
import re
import sys


def bernoulli(p) -> bool:
    """
    :param p: Probability of returning True
    """
    x = random.random()
    return x < p


def clip(lo, x, hi):
    """ lo < hi """
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