from typing import List, Dict, Tuple
from itertools import groupby

from models import Book, Bookstore, BookBookstore


def build_store_dict(bookstores: List[Bookstore]) -> Dict[int, Bookstore]:
    return {store.id: store for store in bookstores}


def build_book_dict(books: List[Book]) -> Dict[int, Book]:
    return {book.id: book for book in books}


def get_one_to_many(
        books: List[Book],
        store_dict: Dict[int, Bookstore]
) -> List[Tuple[Book, Bookstore]]:
    return [
        (book, store_dict[book.store_id])
        for book in books
        if book.store_id in store_dict
    ]


def get_many_to_many(
        book_bookstores: List[BookBookstore],
        book_dict: Dict[int, Book],
        store_dict: Dict[int, Bookstore]
) -> List[Tuple[Book, Bookstore]]:
    return [
        (book_dict[bb.book_id], store_dict[bb.store_id])
        for bb in book_bookstores
        if bb.book_id in book_dict and bb.store_id in store_dict
    ]


def get_books_starting_with_a(one_to_many: List[Tuple[Book, Bookstore]]) -> List[Tuple[str, str]]:
    """
    Задание В1:
    Получает список (название книги, название магазина) для книг, начинающихся на 'А'.
    """
    return [
        (book.title, store.name)
        for book, store in one_to_many
        if book.first_letter == 'А'
    ]


def get_min_price_per_store(one_to_many: List[Tuple[Book, Bookstore]]) -> List[Tuple[str, float]]:
    """
    Задание В2:
    Получает список (название магазина, минимальная цена книги в этом магазине),
    отсортированный по возрастанию минимальной цены.
    """

    sorted_one_to_many = sorted(one_to_many, key=lambda x: x[1].name)
    grouped = groupby(sorted_one_to_many, key=lambda x: x[1].name)

    result = [
        (store_name, min(book.price for book, _ in books_in_store))
        for store_name, books_in_store in grouped
    ]

    return sorted(result, key=lambda x: x[1])


def get_books_with_stores(
        many_to_many: List[Tuple[Book, Bookstore]]
) -> List[Tuple[str, float, str]]:
    """
    Задание В3:
    Получает список (название книги, цена, название магазина),
    отсортированный по названию книги.
    """
    return [
        (book.title, book.price, store.name)
        for book, store in sorted(many_to_many, key=lambda x: x[0].title)
    ]
