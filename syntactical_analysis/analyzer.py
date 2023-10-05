from typing import List
from tokens import Token, IdentifierToken, CLASS_TOKEN
from .custom_exceptions import IdentifierRedeclarationException


class SyntacticalAnalyzer(object):
    """Синтаксический анализатор"""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens

    @staticmethod
    def _add_identifier_category(token: IdentifierToken, category, type_=None):
        """Установка категории идентификатора"""
        if token.category is not None:
            raise IdentifierRedeclarationException()
        token.category = category
        token.type = type_

    def set_types_and_categories(self):
        """Проставление типов и категорий"""
        for index, token in enumerate(self.tokens):
            if isinstance(token, IdentifierToken):
                # Пришёл идентификатор
                prev_token = self.tokens[index - 1]
                if prev_token == CLASS_TOKEN:
                    # Предыдущий токен - ключевое слово class. Значит здесь объявление типа
                    self._add_identifier_category(token, category=IdentifierToken.CATEGORY_TYPE)
                elif isinstance(prev_token, IdentifierToken) and prev_token.category == IdentifierToken.CATEGORY_TYPE:
                    # Предыдущий токен - тип. Значит здесь объявление переменной типа
                    self._add_identifier_category(
                        token, category=IdentifierToken.CATEGORY_VAR, type_=prev_token.attr_name
                    )
