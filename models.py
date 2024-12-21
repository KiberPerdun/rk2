from dataclasses import dataclass


@dataclass(order=True)
class Book:
    """
    Книга
    """
    id: int
    title: str
    price: float
    store_id: int

    @property
    def first_letter(self) -> str:
        return self.title[0]


@dataclass(order=True)
class Bookstore:
    """
    Книжный магазин
    """
    id: int
    name: str


@dataclass
class BookBookstore:
    """
    Связи многие-ко-многим
    """
    book_id: int
    store_id: int
