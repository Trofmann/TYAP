from typing import List

from . import const
from . import utils
from .custom_exceptions import WrongSymbolException
from .state_machine import STATE_TRANSITION_TABLE, STATE_TOKEN_MAPPING
from tokens import *

__all__ = [
    'LexicalAnalyzer'
]


class LexicalAnalyzer:
    """Лексический анализатор"""

    def __init__(self, source_file='tests/editable.txt', *args, **kwargs):
        self.source_file = source_file  # type: str
        self.data = []  # type: List[str]
        self.read()
        self.tokens = []
        # Текущее состояние автомата
        self.current_state = 0

    def read(self):
        """Считывает код из файла"""
        with open(self.source_file) as f:
            self.data = [
                utils.change_prefix_to_tabs(line)
                for line in f.readlines()
            ]

    def write(self, filename='lexical_analysis_result.txt'):
        with open(filename, 'w') as f:
            f.write(''.join(map(str, self.tokens)))


    def analyze(self):
        """Анализ файла"""
        for line in self.data:
            if line and line != '\n':
                self._analyze_line(line)
        print()

    def _analyze_line(self, line):
        """Анализ строки файла """
        left, right = 0, 0
        while right <= len(line) - 1:

            symbol_ = line[right]
            if symbol_ in const.DIGITS_STR:
                table_key = 'digits'
            elif symbol_ in const.LETTERS and not self.current_state == 10:
                table_key = 'letters'
            else:
                table_key = symbol_

            if table_key not in STATE_TRANSITION_TABLE:
                table_key = 'another'
            if self.current_state == 2 and table_key != '}':
                right += 1
                continue
            elif self.current_state == 2 and table_key == '}':
                self.current_state = 0
                right += 1
                left = right
                continue
            new_state = STATE_TRANSITION_TABLE[table_key][self.current_state]
            if new_state == const.INF:
                raise WrongSymbolException(symbol_)
            if new_state < 0:
                # Пришли в конечное состояние
                lexeme = line[left:right + (left == right)]
                # print(new_state, self.current_state, lexeme)
                # Проверим, является ли лексема ключевым словом
                if lexeme in const.KEYWORDS:
                    # Является, добавим соответствующий токен
                    self.tokens.append(WORDS_TOKENS_MAPPING[lexeme])
                else:
                    # Не является
                    # Проверим, является ли заранее определенный токеном
                    if new_state in STATE_TOKEN_MAPPING:
                        # Является
                        self.tokens.append(STATE_TOKEN_MAPPING[new_state])
                    else:
                        # Не является, а значит это или числовая константа, или идентификатор
                        # Числовую константу можно получить из конечных состояний -21 и -22
                        if new_state in [-21, -22]:
                            if new_state == -21:
                                # Числовая константа целового типа
                                token_type = const.INT
                            else:
                                # Числовая константа вещественного типа
                                token_type = const.FLOAT
                            self.tokens.append(DigitalConstToken.get_or_create(lexeme=lexeme, type=token_type))
                        else:
                            self.tokens.append(IdentifierToken.get_or_create(lexeme))

                if new_state in [-11, -12, -13, -16, -18, -20, -21, -22]:
                    # Состояния с возвратом 1.
                    left = right
                else:
                    # Состояния с возвратом 0
                    right += 1
                    left = right
                self.current_state = 0
            else:
                right += 1
                self.current_state = new_state
