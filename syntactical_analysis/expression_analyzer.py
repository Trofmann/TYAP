from typing import List

from lexical_analysis.const import BOOL
from tokens import (
    Token, IdentifierToken,
    ASSIGNMENT_TOKEN, POINT_TOKEN,
    EQUAL_TOKEN, NOT_EQUAL_TOKEN, LESS_TOKEN, LESS_EQUAL_TOKEN, MORE_TOKEN, MORE_EQUAL_TOKEN,
    AND_TOKEN, OR_TOKEN, NOT_TOKEN, TRUE_TOKEN, FALSE_TOKEN,
)
from .custom_exceptions import (
    WrongTokenError, AssignmentExpectedError, UnknownFieldError, WrongExpressionError, TypeIncompatibilityError,
    RelationCountError
)

__all__ = [
    'ExpressionAnalyzer',
]


class ExpressionAnalyzer(object):
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.analyze()

    def analyze(self):
        if self.tokens.count(ASSIGNMENT_TOKEN) != 1:
            # Значительно упростит дальнейший анализ
            raise AssignmentExpectedError()
        if self.tokens[-1] == ASSIGNMENT_TOKEN:
            # Гарантируем наличие правой части выражения
            raise WrongExpressionError()
        identifier_type, identifier_full_name = self.analyze_left_part()
        self.analyze_right_part(type_=identifier_type)

    def analyze_left_part(self):
        """Анализ левой части выражения"""
        # Индекс присвоения. Всё, что слева - или идентификаторы, или точка
        assignment_index = self.tokens.index(ASSIGNMENT_TOKEN)
        # Конечный идентификатор
        identifier = None
        full_name = ''
        for ind in range(assignment_index):
            token = self.tokens[ind]
            if isinstance(token, IdentifierToken):
                # Встретили идентификатор
                # Следующий токен или присвоение, или точка
                next_token = self.tokens[ind + 1]
                if next_token in [POINT_TOKEN, ASSIGNMENT_TOKEN]:
                    # Всё хорошо
                    if identifier is None:
                        # Ещё не было идентификатора. Значит запомним этот
                        identifier = token
                        full_name += identifier.attr_name
                    else:
                        # Уже был. Значит в его полях ищем идентификатор с там же именем
                        found = False
                        for field in identifier.fields:
                            if field.attr_name == token.attr_name:
                                identifier = field
                                full_name = full_name + '.' + token.attr_name
                                found = True
                        if not found:
                            # Не нашли, а должны были
                            raise UnknownFieldError()

                else:
                    raise WrongTokenError()
            elif token == POINT_TOKEN:
                # Встретили точку, а значит следующий - только идентификатор
                next_token = self.tokens[ind + 1]
                if isinstance(next_token, IdentifierToken):
                    # Всё хорошо
                    pass
                else:
                    raise WrongTokenError()
        # Вернём тип идентификатора и его полное имя
        return identifier.type, full_name

    def analyze_right_part(self, type_):
        """Анализ правой части выражения"""
        assignment_index = self.tokens.index(ASSIGNMENT_TOKEN)
        tokens = self.tokens[assignment_index::]

        # region Проверка 1: Операции сравнения, логические операции, true и false
        # допустимы, только если левая часть логического типа
        relation_count = sum([
            EQUAL_TOKEN in tokens,
            NOT_EQUAL_TOKEN in tokens,
            LESS_TOKEN in tokens,
            LESS_EQUAL_TOKEN in tokens,
            MORE_TOKEN in tokens,
            MORE_EQUAL_TOKEN in tokens
        ])
        contains_logical_operators = any([
            AND_TOKEN in tokens,
            OR_TOKEN in tokens,
            NOT_TOKEN in tokens,
        ])

        contains_true_false = any([
            TRUE_TOKEN in tokens,
            FALSE_TOKEN in tokens
        ])

        if (relation_count or contains_logical_operators or contains_true_false) and type_ != BOOL:
            raise TypeIncompatibilityError()
        # endregion

        # region Проверка 2: количество операций сравнения не должно превышать 1
        if relation_count > 1:
            raise RelationCountError()
        # endregion

        # Приоритет операций
        # 1. Сравнение
        # 2. NOT
        # 3. AND, *, /
        # 4. OR, +, -

