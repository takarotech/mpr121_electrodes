# from IPython.utils import coloransi
# ANSI_COLORS = {k: v for k, v in coloransi.TermColors.__dict__.items() if 'A' <= k[0] <= 'Z'}
# '{Red}test'.format(**ANSI_COLORS)


class Ansi(object):
    _ESCAPE = '\033['

    def __init__(self, code):
        self.code = code

    def __or__(self, other): 
        return self.__class__(f'{self.code};{other.code}')

    def __str__(self):
        return f'{self._ESCAPE}{self.code}m'


class C():
    ESC = Ansi('0')
    BRIGHT = Ansi('1')
    FAINT = Ansi('2')

    BLACK = Ansi('30')
    RED = Ansi('31')
    GREEN = Ansi('32')
    YELLOW = Ansi('33')
    BLUE = Ansi('34')
    MAGENTA = Ansi('35')
    CYAN = Ansi('36')
    WHITE = Ansi('37')
    DEFAULT = Ansi('39')

    BLACK_BG = Ansi('40')
    RED_BG = Ansi('41')
    GREEN_BG = Ansi('42')
    YELLOW_BG = Ansi('43')
    BLUE_BG = Ansi('44')
    MAGENTA_BG = Ansi('45')
    CYAN_BG = Ansi('46')
    WHITE_BG = Ansi('47')
    DEFAULT_BG = Ansi('49')
