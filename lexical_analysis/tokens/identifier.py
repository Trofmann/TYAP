from collections.abc import Iterable

from lexical_analysis import const
from lexical_analysis.tokens.token import Token

__all__ = [
    'IdentifierToken',
    'identifiers_table',
]


class IdentifierToken(Token):
    """Токен идентификатора"""

    def __init__(self, value, attr_name, attr_value, type):
        super().__init__(name='id', code=25, value=value)
        # Обозначение идентификатора
        self.attr_name = attr_name
        # Значение идентификатора
        self.attr_value = attr_value
        self.type = type
        # Если идентификатор используется для типа запись, то здесь хранятся поля
        self.fields = []

    @property
    def parent_identifier_token(self):
        if not isinstance(Iterable, self.value):
            return None
        return identifiers_table[self.value[0]]

    @classmethod
    def get_or_create(cls, lexeme):
        """Находим в таблице идентификаторов токен с attr_name==lexeme или создаём его"""
        found = list(filter(lambda x: x.attr_name == lexeme, identifiers_table))
        if found:
            return found[0]
        token_value = len(identifiers_table)
        new_token = IdentifierToken(value=token_value, attr_name=lexeme, attr_value=None, type=None)
        identifiers_table.append(new_token)
        return new_token


INT_TOKEN = IdentifierToken(value=0, attr_name=const.INT, attr_value=const.INT, type=None)
FLOAT_TOKEN = IdentifierToken(value=1, attr_name=const.FLOAT, attr_value=const.FLOAT, type=None)
BOOL_TOKEN = IdentifierToken(value=2, attr_name=const.BOOL, attr_value=const.BOOL, type=None)

identifiers_table = [
    INT_TOKEN,
    FLOAT_TOKEN,
    BOOL_TOKEN,
]
