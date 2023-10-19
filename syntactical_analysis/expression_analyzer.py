from lexical_analysis.const import BOOL
from tokens import (
    IdentifierToken,
    ASSIGNMENT_TOKEN, POINT_TOKEN,
    EQUAL_TOKEN, NOT_EQUAL_TOKEN, LESS_TOKEN, LESS_EQUAL_TOKEN, MORE_TOKEN, MORE_EQUAL_TOKEN,
    AND_TOKEN, OR_TOKEN, NOT_TOKEN, TRUE_TOKEN, FALSE_TOKEN,
)
from .custom_exceptions import (
    WrongTokenError, AssignmentExpectedError, UnknownFieldError, WrongExpressionError, TypeIncompatibilityError,
    RelationCountError, UnknownVarError, VarNameExpectedError, AnalysisException, WrongTypeForOperator
)
from .identifier_info import IdentifierInfo
from .handlers import NotOperationHandler
from .commands import commands

__all__ = [
    'ExpressionAnalyzer',
]


class ExpressionAnalyzer(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.parse_identifiers()
        self.analyze()

    def parse_identifiers(self):
        """Схлопываем идентификаторы"""
        result = []
        identifier = None
        full_name = ''
        for ind in range(len(self.tokens)):
            token = self.tokens[ind]
            if isinstance(token, IdentifierToken):
                # Встретили идентификатор
                if identifier is None:
                    if not token.category:
                        raise UnknownVarError()
                    if token.category == IdentifierToken.CATEGORY_TYPE:
                        raise VarNameExpectedError()
                    identifier = token
                    full_name += identifier.attr_name
                else:
                    prev_token = self.tokens[ind - 1]
                    if prev_token == POINT_TOKEN:
                        # Предыдущая точка, всё хорошо
                        found = False
                        for field in identifier.fields:
                            if field.attr_name == token.attr_name:
                                identifier = field
                                full_name = full_name + '.' + token.attr_name
                                found = True
                        if not found:
                            raise UnknownFieldError()
                    else:
                        raise AnalysisException()
            elif token == POINT_TOKEN:
                # Встретили точку
                # А значит предыдущий только идентификатор, и следующий идентификатор
                if ind == len(self.tokens):
                    raise AnalysisException()
                next_token = self.tokens[ind + 1]
                prev_token = self.tokens[ind - 1]
                if isinstance(next_token, IdentifierToken) and (prev_token, IdentifierToken):
                    # Всё хорошо
                    pass
                else:
                    raise WrongTokenError()
            else:
                # Встретили другой токен.
                if identifier:
                    # Если есть идентификатор, сбросим его в result
                    identifier_info = IdentifierInfo(full_name=full_name, type=identifier.type)
                    result.append(identifier_info)
                    identifier = None
                    full_name = ''
                result.append(token)
        if identifier:
            identifier_info = IdentifierInfo(full_name=full_name, type=identifier.type)
            result.append(identifier_info)
        self.tokens = result

    def analyze(self):
        if self.tokens.count(ASSIGNMENT_TOKEN) != 1:
            # Значительно упростит дальнейший анализ
            raise AssignmentExpectedError()
        if self.tokens[-1] == ASSIGNMENT_TOKEN:
            # Гарантируем наличие правой части выражения
            raise WrongExpressionError()
        # Если дошли досюда, значит с левой частью всё норм. Можно схлопнуть
        assignment_index = self.tokens.index(ASSIGNMENT_TOKEN)
        left_identifier = self.tokens[0]
        self.tokens = self.tokens[assignment_index::]
        self.analyze_right_part(type_=left_identifier.type)

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

        while NOT_TOKEN in tokens:
            not_token_index = tokens.index(NOT_TOKEN)
            identifier = tokens[not_token_index + 1]  # Берем следующий
            if identifier.type != BOOL:
                raise WrongTypeForOperator()

            identifier_name = identifier.name
            temp_var = NotOperationHandler.handle(identifier_name)
            if not_token_index + 1 == len(tokens) - 1:
                # not a находится в конце
                tokens = tokens[0:not_token_index] + [temp_var]
            else:
                tokens = tokens[0:not_token_index] + [temp_var] + tokens[not_token_index + 2::]
