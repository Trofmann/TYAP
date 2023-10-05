from lexical_analysis.const import INF
from tokens import *

__all__ = [
    'STATE_TRANSITION_TABLE',
    'STATE_TOKEN_MAPPING',
]

STATE_TRANSITION_TABLE = {
    '(': [-1, -11, 2, -13, INF, -16, -18, -20, -21, INF, INF, -22, INF, -22],
    ')': [-2, -11, 2, -13, INF, -16, -18, -20, -21, INF, INF, -22, INF, -22],
    ':': [-3, -11, 2, -13, INF, -16, -18, -20, -21, INF, INF, -22, INF, -22],
    ',': [-4, -11, 2, -13, INF, -16, -18, -20, -21, INF, INF, -22, INF, -22],
    '_': [-5, -11, 2, -13, INF, -16, -18, 7, -21, INF, INF, -22, INF, -22],
    '+': [-6, -11, 2, -13, INF, -16, -18, -20, -21, INF, 12, -22, INF, -22],
    '-': [-7, -11, 2, -13, INF, -16, -18, -20, -21, INF, 12, -22, INF, -22],
    '*': [-8, -11, 2, -13, INF, -16, -18, -20, -21, INF, INF, -22, INF, -22],
    '/': [-9, -11, 2, -13, INF, -16, -18, -20, -21, INF, INF, -22, INF, -22],
    '.': [-25, -11, 2, -13, INF, -16, -18, -20, 9, INF, INF, -22, INF, -22],
    ' ': [1, 1, 2, -13, INF, -16, -18, -20, -21, INF, INF, -22, INF, -22],
    '{': [2, -11, 2, -13, INF, -16, -18, -20, -21, INF, INF, -22, INF, -22],
    '}': [INF, -11, -12, -13, INF, -16, -18, -20, -21, INF, INF, -22, INF, -22],
    'digits': [8, -11, 2, -13, INF, -16, -18, 7, 8, 11, 13, 11, 13, 13],
    'e': [INF, -11, 2, -13, INF, -16, -18, -20, 10, INF, INF, -22, INF, -22],
    '=': [3, -11, 2, -14, -15, -17, -19, -20, -21, INF, INF, -22, INF, -22],
    '!': [4, -11, 2, -13, INF, -16, -18, -20, -21, INF, INF, -22, INF, -22],
    '>': [5, -11, 2, -13, INF, -16, -18, -20, -21, INF, INF, -22, INF, -22],
    '<': [6, -11, 2, -13, INF, -16, -18, -20, -21, INF, INF, -22, INF, -22],
    'letters': [7, -11, 2, -13, INF, -16, -18, 7, -21, INF, INF, -22, INF, -22],
    '\n': [-23, -11, 2, -13, INF, -16, -18, -20, -21, INF, INF, -22, INF, -22],
    '\t': [-24, -11, 2, -13, INF, -16, -18, -20, -21, INF, INF, -22, INF, -22],
    'another': [INF, INF, 2, INF, INF, INF, INF, INF, INF, INF, INF, INF, INF, INF],
}

STATE_TOKEN_MAPPING = {
    -1: OPEN_BRACKET_TOKEN,
    -2: CLOSE_BRACKET_TOKEN,
    -3: COLON_TOKEN,
    -4: COMMA_TOKEN,
    -5: UNDERSCORE_TOKEN,
    -6: PLUS_TOKEN,
    -7: MINUS_TOKEN,
    -8: MULT_TOKEN,
    -9: DIV_TOKEN,
    -13: ASSIGNMENT_TOKEN,
    -14: EQUAL_TOKEN,
    -15: NOT_EQUAL_TOKEN,
    -16: MORE_TOKEN,
    -17: MORE_EQUAL_TOKEN,
    -18: LESS_TOKEN,
    -19: LESS_EQUAL_TOKEN,
    -25: POINT_TOKEN,
}
