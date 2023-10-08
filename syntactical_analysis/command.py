from tokens import (
    Token,
    NOT_TOKEN, EQUAL_TOKEN, NOT_EQUAL_TOKEN, LESS_TOKEN, LESS_EQUAL_TOKEN, MORE_TOKEN, MORE_EQUAL_TOKEN
)
from .custom_exceptions import AnalysisException
from lexical_analysis.const import BOOL


class Command(object):
    """Команда"""

    def __init__(self, name: str, left_operand: str = None, operator: str = None, right_operand: str = None,
                 return_type: str = None):
        self.name = name  # Имя команды
        self.left_operand = left_operand  # Левый операнд. Его может не быть. Например, not A
        self.right_operand = right_operand  # Правый операнд. None для обычного присвоения
        self.operator = operator  # Оператор. None для обычного присвоения
        # Именно type только для совпадения с токенами
        self.type = return_type  # Тип, возвращаемый выражением. None для обычного присвоения

    def __repr__(self):
        return f'{self.name} ({self.left_operand}, {self.operator}, {self.right_operand}) --> {self.type}'

    def __str__(self):
        name_parts = [f'{self.name} =']
        if self.left_operand:
            name_parts.append(self.left_operand)
        if self.operator:
            name_parts.append(self.operator)
        if self.right_operand:
            name_parts.append(self.right_operand)
        return ' '.join(name_parts)


class CommandFabric(object):
    """Фабрика для создания команды"""

    @staticmethod
    def get_next_command_name() -> str:
        return f'${len(commands)}'

    @staticmethod
    def create_for_assignment(aim: str, source: str) -> Command:
        """
        Создание команды присваивания
        :param aim: Токен, которому присваивается значение.
        :param source: Токен, от которого берётся значение
        """
        name = aim
        left_operand = source
        return Command(name=name, left_operand=left_operand)

    @staticmethod
    def create_one_operand_command(operator: Token, operand: str) -> Command:
        """
        Создание однооператорной команды. (not)
        """
        # Доступно только для not
        if operator != NOT_TOKEN:
            raise AnalysisException()
        name = CommandFabric.get_next_command_name()
        command = Command(name=name, operator=operator.name, right_operand=operand, return_type=BOOL)
        commands.append(command)
        return command

    @staticmethod
    def create_two_operands_command(left_operand: str, operator: Token, right_operand: str, assumed_return_type: str):
        """
        Создание двуоператорной команды
        :param left_operand:
        :param operator:
        :param right_operand:
        :param assumed_return_type: Предполагаемый тип. Изначально равен типу операторов
        """
        name = CommandFabric.get_next_command_name()
        return_type = assumed_return_type
        if operator in [
            EQUAL_TOKEN, NOT_EQUAL_TOKEN, LESS_TOKEN, LESS_EQUAL_TOKEN, MORE_TOKEN, MORE_EQUAL_TOKEN
        ]:
            return_type = BOOL
        command = Command(
            name=name,
            left_operand=left_operand,
            operator=operator.name,
            right_operand=right_operand,
            return_type=return_type
        )
        commands.append(command)
        return command


commands = []
