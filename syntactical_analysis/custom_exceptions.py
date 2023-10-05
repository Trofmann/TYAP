class IdentifierRedeclarationException(Exception):
    def __init__(self):
        super().__init__('Повторное объявление идентификатора')