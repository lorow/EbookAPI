import dataclasses


@dataclasses.dataclass
class Book:
    uuid: str
    file_path: str
    pages: int
    current_page: int
