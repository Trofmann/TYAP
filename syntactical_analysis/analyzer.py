from typing import List
from tokens import (
    Token, IdentifierToken, CLASS_TOKEN, COLON_TOKEN, NL_TOKEN, TAB_TOKEN, START_PROG_TOKEN, END_PROG_TOKEN,
    BLOCK_VAR_DEF_TOKEN, ENDBLOCK_VAR_DEF_TOKEN, INT_TOKEN, FLOAT_TOKEN, BOOL_TOKEN, identifiers_table
)
from .custom_exceptions import (
    IdentifierRedeclarationException, TabExpectedException, NewLineExpectedException, TypeNameExpectedException,
    StartProgExpectedError, EndProgExpectedError, BlockVarDefExpectedError, EndBlockVarDefExpectedError,
    VarNameExpectedError, AnalysisException, FieldRedeclarationError,
)
from copy import deepcopy


class SyntacticalAnalyzer(object):
    """Синтаксический анализатор"""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens

    @staticmethod
    def _add_identifier_category(token: IdentifierToken, category, type_token=None):
        """Установка категории идентификатора"""
        if token.category is not None:
            raise IdentifierRedeclarationException()
        token.category = category
        token.type = type_token

        if category == IdentifierToken.CATEGORY_VAR:
            # Объявляем переменную
            if type_token not in [INT_TOKEN, FLOAT_TOKEN, BOOL_TOKEN]:
                # Значит имеем дело с классом.
                # Скопируем поля
                token.fields = deepcopy(type_token.fields)
                print()

    def _clean_nl_tokens(self):
        """Очистка перевода строк"""
        while len(self.tokens) and self.tokens[0] == NL_TOKEN:
            self.tokens.pop(0)

    def analyze(self):
        if self.tokens[0] != START_PROG_TOKEN:
            # Программа должна начинаться с start_prog
            raise StartProgExpectedError()
        if self.tokens[-1] != END_PROG_TOKEN:
            # И заканчиваться на end_prog
            raise EndProgExpectedError()

        # Удалим start_prog и end_prog. Они нам больше не нужны
        self.tokens.pop(0)  # Удаляем start_prog
        self.tokens.pop(-1)  # Удаляем end_prog

        # Если дошли сюда, значит ожидаем встретить перевод строки и блок объявления переменных
        self._clean_nl_tokens()  # Очистим от перевода строк

        # region Объявление переменных
        # Ожидаем начало блока объявления переменных
        if self.tokens[0] != BLOCK_VAR_DEF_TOKEN:
            raise BlockVarDefExpectedError()

        # Ожидаем, что в программе есть окончание блока объявления переменных
        if ENDBLOCK_VAR_DEF_TOKEN not in self.tokens:
            raise EndBlockVarDefExpectedError()

        # Дошли до сюда, значит есть блок описания идентификаторов
        self.tokens.pop(0)  # Удалим block_var_def
        self._clean_nl_tokens()
        self.tokens.insert(0, NL_TOKEN)  # Хак для удобства
        endblock_var_def_index = self.var_definition()
        self.tokens = self.tokens[endblock_var_def_index + 1::]

        # Очистим таблицу идентификатором от идентификаторов без категории.
        # Такие могли появиться из-за того, что поля класса вносились в таблицу идентификаторов
        global identifiers_table
        identifiers_table = list(filter(lambda x: x.category is not None, identifiers_table))
        # endregion

    def var_definition(self):
        """Разбор блока описания переменных"""
        endblock_var_def_index = None  # Индекс токена окончания блока описания переменных (endblock_var_def)

        # Флаг, показывающий, что находимся в состоянии объявления класса
        in_class_declaration_state = False
        # Токен, являющийся новым классом
        new_class_token = None
        for index, token in enumerate(self.tokens):
            if not in_class_declaration_state:
                # НЕ Находимся объявления класса. Значит ожидаем увидеть или перевод строки, или идентификатор,
                # или endblock_var_def, или class
                if token == NL_TOKEN:
                    # Пусть вначале идёт перевод строки
                    if index:
                        # Пришёл перевод строки, а значит перед этим должна быть переменная
                        # Перевод строки после имени типа недопустим
                        prev_token = self.tokens[index - 1]
                        if (not isinstance(prev_token, IdentifierToken) or
                                prev_token.category == IdentifierToken.CATEGORY_TYPE):
                            raise VarNameExpectedError()
                        else:
                            # В противном случае всё хорошо. Продолжаем.
                            pass
                elif token == ENDBLOCK_VAR_DEF_TOKEN:
                    prev_token = self.tokens[index - 1]
                    if prev_token != NL_TOKEN:
                        # Перед endblock_var_def должен быть перевод строки
                        raise AnalysisException()
                    else:
                        # Всё хорошо. Вернём индекс
                        return index
                elif token == CLASS_TOKEN:
                    prev_token = self.tokens[index - 1]
                    if prev_token != NL_TOKEN:
                        # Перед class должен быть перевод строки
                        raise AnalysisException()
                    else:
                        # Всё хорошо. Продолжаем
                        pass
                elif isinstance(token, IdentifierToken):
                    # Пришёл идентификатор
                    prev_token = self.tokens[index - 1]
                    if prev_token == NL_TOKEN:
                        # После перевода строки, а значит текущий токен обязательно должен быть именем типа
                        if token.category != IdentifierToken.CATEGORY_TYPE:
                            raise TypeNameExpectedException()
                    elif prev_token == CLASS_TOKEN:
                        # Предыдущий токен - ключевое слово class. Значит здесь объявление типа
                        self._add_identifier_category(token, category=IdentifierToken.CATEGORY_TYPE)
                        # Начинается объявление класса
                        in_class_declaration_state = True
                        new_class_token = token
                    elif isinstance(prev_token,
                                    IdentifierToken) and prev_token.category == IdentifierToken.CATEGORY_TYPE:
                        # Предыдущий токен - тип. Значит здесь объявление переменной типа
                        self._add_identifier_category(
                            token, category=IdentifierToken.CATEGORY_VAR, type_token=prev_token
                        )
                    else:
                        raise AnalysisException()
            elif in_class_declaration_state:
                # Находимся в состоянии объявления класса
                prev_token = self.tokens[index - 1]
                if token == COLON_TOKEN and prev_token == new_class_token:
                    # Двоеточие после имени класса. Всё хорошо
                    pass
                elif token == NL_TOKEN:
                    # Перевод на новую строку.
                    next_token = self.tokens[index + 1]
                    # Если предыдущий токен - двоеточие, то следующий обязательно таб
                    if prev_token == COLON_TOKEN:
                        if next_token != TAB_TOKEN:
                            # Пришёл не таб. Ошибка
                            raise TabExpectedException()
                        else:
                            # Пришёл таб, всё хорошо
                            pass
                    elif next_token == TAB_TOKEN:
                        # Всё хорошо, ничего не делаем
                        pass
                    # Если следующий токен не таб, то выходим из состояния объявления класс
                    elif next_token != TAB_TOKEN:
                        in_class_declaration_state = False
                elif token == TAB_TOKEN:
                    # Табуляция. Должна быть только после перевода на новую строку
                    if prev_token != NL_TOKEN:
                        raise NewLineExpectedException()
                elif isinstance(token, IdentifierToken):
                    # Встретили идентификатор
                    prev_token = self.tokens[index - 1]
                    # Предыдущий токен - таб
                    if prev_token == TAB_TOKEN:
                        next_token = self.tokens[index + 1]
                        # А значит текущий может быть только типом
                        if token.category != IdentifierToken.CATEGORY_TYPE:
                            raise TypeNameExpectedException()
                        # А следующий - переводом идентифкатором
                        if not isinstance(next_token, IdentifierToken):
                            raise VarNameExpectedError()
                    # Предыдущий токен - идентификатор
                    elif isinstance(prev_token, IdentifierToken):
                        # Предыдущее условие гарантирует, предыдущий токен именно имя типа
                        # А значит текущий должен быть переменной, т.е НЕ именем типа
                        if token.category == IdentifierToken.CATEGORY_TYPE:
                            raise VarNameExpectedError()
                        # Попробуем найти в полях типа объявляемого типа
                        found = list(filter(lambda x: x.attr_name == token.attr_name, new_class_token.fields))
                        if found:
                            # Поле повторно объявлять нельзя
                            raise FieldRedeclarationError()
                        else:
                            # Не нашли. Значит можем добавить в поля.
                            # Создадим новый. Этот менять нельзя, чтобы не было пересечений
                            identifier = IdentifierToken(
                                value=len(new_class_token.fields),
                                attr_name=token.attr_name,
                                attr_value=None,
                                type=prev_token.attr_name,
                                category=IdentifierToken.CATEGORY_VAR,
                            )
                            new_class_token.fields.append(identifier)
                        # TODO: а для переменных класса копировать поля
                        pass
                    else:
                        raise AnalysisException()
                else:
                    raise AnalysisException()
