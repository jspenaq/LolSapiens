class Rune:
    def __init__(self, id: int, name: str, name_es: str):
        self.id = id
        self.name = name # English name (en_US)
        self.name_es = name_es # Spanish name (es_MX)

    def __str__(self) -> str:
        return f"Rune: {self.name}, id: {self.id}"