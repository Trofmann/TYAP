from . import const


def change_prefix_to_tabs(str_: str) -> str:
    """Заменяем пробелы в начале строки на табы"""
    while str_.startswith(const.TAB_EQUIVALENT_SPACES):
        str_ = '\t' + str_.removeprefix(const.TAB_EQUIVALENT_SPACES)
    return str_
