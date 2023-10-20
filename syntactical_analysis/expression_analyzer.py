from lexical_analysis.const import BOOL, INT, FLOAT
from tokens import (
    IdentifierToken, DigitalConstToken,
    ASSIGNMENT_TOKEN, POINT_TOKEN,
    EQUAL_TOKEN, NOT_EQUAL_TOKEN, LESS_TOKEN, LESS_EQUAL_TOKEN, MORE_TOKEN, MORE_EQUAL_TOKEN,
    AND_TOKEN, OR_TOKEN, NOT_TOKEN, TRUE_TOKEN, FALSE_TOKEN, MULT_TOKEN, DIV_TOKEN, PLUS_TOKEN, MINUS_TOKEN,
)
from .custom_exceptions import (
    WrongTokenError, AssignmentExpectedError, UnknownFieldError, WrongExpressionError, TypeIncompatibilityError,
    RelationCountError, UnknownVarError, VarNameExpectedError, AnalysisException, WrongTypeForOperator
)
from .handlers import (
    NotOperationHandler, AndOperationHandler, OrOperationHandler, ArithmeticOperationHandler, RelationOperationHandler,
    AssignmentHandler
)
from .identifier_info import IdentifierInfo
from .temp_var import TempVar

__all__ = [
    'ExpressionAnalyzer',
]

from .utils import parse_identifiers


class ExpressionAnalyzer(object):
    def __init__(self, tokens):
        self.tokens = parse_identifiers(tokens)
        self.analyze()

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
        right_part_identifier = self.analyze_right_part(type_=left_identifier.type)

        if right_part_identifier in [TRUE_TOKEN, FALSE_TOKEN]:
            right_part_type = BOOL
        else:
            right_part_type = right_part_identifier.type
        # На всякий случай проверим типы
        if left_identifier.type != right_part_type:
            raise TypeIncompatibilityError()

        if isinstance(right_part_identifier, DigitalConstToken):
            right_part_identifier_name = str(right_part_identifier.attr)
        else:
            right_part_identifier_name = right_part_identifier.name
        AssignmentHandler.handle(
            left_identifier_name=left_identifier.name, right_identifier_name=right_part_identifier_name
        )

    def analyze_right_part(self, type_):
        """Анализ правой части выражения"""
        assignment_index = self.tokens.index(ASSIGNMENT_TOKEN)
        tokens = self.tokens[assignment_index::]

        identifiers_classes = (IdentifierToken, IdentifierInfo, TempVar)
        arithmetical_identifiers_classes = (IdentifierToken, IdentifierInfo, TempVar, DigitalConstToken)
        arithmetic_types = [INT, FLOAT]
        bool_tokens = [TRUE_TOKEN, FALSE_TOKEN]

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
            if not (isinstance(identifier, identifiers_classes) or identifier in bool_tokens):
                raise WrongExpressionError()
            if identifier in bool_tokens:
                identifier_type = BOOL
            else:
                identifier_type = identifier.type
            if identifier_type != BOOL:
                raise WrongTypeForOperator()

            identifier_name = identifier.name
            temp_var = NotOperationHandler.handle(identifier_name)
            if not_token_index + 1 == len(tokens) - 1:
                # not a находится в конце
                tokens = tokens[0:not_token_index] + [temp_var]
            else:
                tokens = tokens[0:not_token_index] + [temp_var] + tokens[not_token_index + 2::]

        while AND_TOKEN in tokens:
            and_token_index = tokens.index(AND_TOKEN)
            left_identifier = tokens[and_token_index - 1]  # Берём предыдущий
            right_identifier = tokens[and_token_index + 1]  # Берём следующий

            if not (
                    (isinstance(left_identifier, identifiers_classes) or left_identifier in bool_tokens) and
                    (isinstance(right_identifier, identifiers_classes) or right_identifier in bool_tokens)
            ):
                raise WrongExpressionError()

            if left_identifier in bool_tokens:
                left_identifier_type = BOOL
            else:
                left_identifier_type = left_identifier.type

            if right_identifier in bool_tokens:
                right_identifier_type = BOOL
            else:
                right_identifier_type = right_identifier.type

            if not (left_identifier_type == BOOL and right_identifier_type == BOOL):
                raise WrongTypeForOperator()

            temp_var = AndOperationHandler.handle(
                left_identifier_name=left_identifier.name,
                right_identifier_name=right_identifier.name
            )
            if and_token_index + 1 == len(tokens) - 1:
                tokens = tokens[0:and_token_index - 1] + [temp_var]
            else:
                tokens = tokens[0:and_token_index - 1] + [temp_var] + tokens[and_token_index + 2::]

        while OR_TOKEN in tokens:
            or_token_index = tokens.index(OR_TOKEN)
            left_identifier = tokens[or_token_index - 1]  # Берём предыдущий
            right_identifier = tokens[or_token_index + 1]  # Берём следующий

            if not (
                    (isinstance(left_identifier, identifiers_classes) or left_identifier in bool_tokens) and
                    (isinstance(right_identifier, identifiers_classes) or right_identifier in bool_tokens)
            ):
                raise WrongExpressionError()

            if left_identifier in bool_tokens:
                left_identifier_type = BOOL
            else:
                left_identifier_type = left_identifier.type

            if right_identifier in bool_tokens:
                right_identifier_type = BOOL
            else:
                right_identifier_type = right_identifier.type

            if not (left_identifier_type == BOOL and right_identifier_type == BOOL):
                raise WrongTypeForOperator()

            temp_var = OrOperationHandler.handle(
                left_identifier_name=left_identifier.name,
                right_identifier_name=right_identifier.name
            )
            if or_token_index + 1 == len(tokens) - 1:
                tokens = tokens[0:or_token_index - 1] + [temp_var]
            else:
                tokens = tokens[0:or_token_index - 1] + [temp_var] + tokens[or_token_index + 2::]

        while (MULT_TOKEN in tokens) or (DIV_TOKEN in tokens):
            mult_token_index = float('inf')
            div_token_index = float('inf')

            if MULT_TOKEN in tokens:
                mult_token_index = tokens.index(MULT_TOKEN)
            if DIV_TOKEN in tokens:
                div_token_index = tokens.index(DIV_TOKEN)

            token_index = min(mult_token_index, div_token_index)  # Операции равного приоритета. Возьмём самый первый
            operation = '*' if token_index == mult_token_index else '/'
            left_identifier = tokens[token_index - 1]  # Берём предыдущий
            right_identifier = tokens[token_index + 1]  # Берём следующий

            if not (
                    isinstance(left_identifier, arithmetical_identifiers_classes) and
                    isinstance(right_identifier, arithmetical_identifiers_classes)
            ):
                raise WrongExpressionError()
            if not (left_identifier.type in arithmetic_types and right_identifier.type in arithmetic_types):
                raise WrongTypeForOperator()

            if left_identifier.type != right_identifier.type:
                raise TypeIncompatibilityError()

            if isinstance(left_identifier, DigitalConstToken):
                left_identifier_name = str(left_identifier.attr)
            else:
                left_identifier_name = left_identifier.name

            if isinstance(right_identifier, DigitalConstToken):
                right_identifier_name = str(right_identifier.attr)
            else:
                right_identifier_name = right_identifier.name

            temp_var = ArithmeticOperationHandler.handle(
                left_identifier_name=left_identifier_name,
                right_identifier_name=right_identifier_name,
                operation=operation,
                type_=left_identifier.type
            )

            if token_index + 1 == len(tokens) - 1:
                tokens = tokens[0:token_index - 1] + [temp_var]
            else:
                tokens = tokens[0:token_index - 1] + [temp_var] + tokens[token_index + 2::]

        while (PLUS_TOKEN in tokens) or (MINUS_TOKEN in tokens):
            plus_token_index = float('inf')
            minus_token_index = float('inf')

            if PLUS_TOKEN in tokens:
                plus_token_index = tokens.index(PLUS_TOKEN)
            if MINUS_TOKEN in tokens:
                minus_token_index = tokens.index(MINUS_TOKEN)

            token_index = min(plus_token_index, minus_token_index)  # Операции равного приоритета. Возьмём самый первый
            operation = '+' if token_index == plus_token_index else '-'
            left_identifier = tokens[token_index - 1]  # Берём предыдущий
            right_identifier = tokens[token_index + 1]  # Берём следующий

            if not (
                    isinstance(left_identifier, arithmetical_identifiers_classes) and
                    isinstance(right_identifier, arithmetical_identifiers_classes)
            ):
                raise WrongExpressionError()
            if not (left_identifier.type in arithmetic_types and right_identifier.type in arithmetic_types):
                raise WrongTypeForOperator()

            if left_identifier.type != right_identifier.type:
                raise TypeIncompatibilityError()

            if isinstance(left_identifier, DigitalConstToken):
                left_identifier_name = str(left_identifier.attr)
            else:
                left_identifier_name = left_identifier.name

            if isinstance(right_identifier, DigitalConstToken):
                right_identifier_name = str(right_identifier.attr)
            else:
                right_identifier_name = right_identifier.name

            temp_var = ArithmeticOperationHandler.handle(
                left_identifier_name=left_identifier_name,
                right_identifier_name=right_identifier_name,
                operation=operation,
                type_=left_identifier.type
            )

            if token_index + 1 == len(tokens) - 1:
                tokens = tokens[0:token_index - 1] + [temp_var]
            else:
                tokens = tokens[0:token_index - 1] + [temp_var] + tokens[token_index + 2::]

        if relation_count == 1:
            token = None
            operation = ''
            if EQUAL_TOKEN in tokens:
                token = EQUAL_TOKEN
                operation = '=='
            elif NOT_EQUAL_TOKEN in tokens:
                token = NOT_EQUAL_TOKEN
                operation = '!='
            elif LESS_TOKEN in tokens:
                token = LESS_TOKEN
                operation = '<'
            elif LESS_EQUAL_TOKEN in tokens:
                token = LESS_EQUAL_TOKEN
                operation = '<='
            elif MORE_TOKEN in tokens:
                token = MORE_TOKEN
                operation = '>'
            elif MORE_EQUAL_TOKEN in tokens:
                token = MORE_EQUAL_TOKEN
                operation = '>='

            rel_token_index = tokens.index(token)

            left_identifier = tokens[rel_token_index - 1]
            right_identifier = tokens[rel_token_index + 1]

            if not (
                    isinstance(left_identifier, arithmetical_identifiers_classes) and
                    isinstance(right_identifier, arithmetical_identifiers_classes)
            ):
                raise WrongExpressionError()

            if left_identifier.type != right_identifier.type:
                raise TypeIncompatibilityError()

            temp_var = RelationOperationHandler.handle(
                left_identifier_name=left_identifier.name,
                right_identifier_name=right_identifier.name,
                operation=operation,
                type_=left_identifier.type
            )
            if rel_token_index + 1 == len(tokens) - 1:
                tokens = tokens[0:rel_token_index - 1] + [temp_var]
            else:
                tokens = tokens[0:rel_token_index - 1] + [temp_var] + tokens[rel_token_index + 2::]

        # Удалим токен присвоения, его обработаем потом
        if len(tokens) and tokens[0] == ASSIGNMENT_TOKEN:
            tokens.pop(0)
        else:
            raise WrongExpressionError()
        # К этому моменту справа должен остаться только 1 токен
        if len(tokens) != 1:
            raise WrongExpressionError()
        return tokens[0]
