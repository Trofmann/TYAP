from dataclasses import dataclass


@dataclass
class IdentifierInfo:
    """Основная информация об идентификаторе"""
    full_name: str
    type: str

    @property
    def name(self):
        return self.full_name
