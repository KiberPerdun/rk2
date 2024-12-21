from pprint import pprint

from models import Book, Bookstore, BookBookstore
from src import (
    build_store_dict,
    build_book_dict,
    get_one_to_many,
    get_many_to_many,
    get_books_starting_with_a,
    get_min_price_per_store,
    get_books_with_stores
)


def main():
    bookstores = [
        Bookstore(1, 'Книжный мир'),
        Bookstore(2, 'Буквоед'),
        Bookstore(3, 'Азбука-Аттикус'),
        Bookstore(4, 'Читай-город'),
        Bookstore(5, 'Дом книги'),
    ]

    books = [
        Book(1, 'Анна Каренина', 500.0, 1),
        Book(2, 'Преступление и наказание', 600.0, 2),
        Book(3, 'Алые паруса', 450.0, 3),
        Book(4, 'Мастер и Маргарита', 550.0, 2),
        Book(5, 'Алиса в стране чудес', 700.0, 1),
    ]

    book_bookstores = [
        BookBookstore(1, 1),
        BookBookstore(2, 2),
        BookBookstore(3, 3),
        BookBookstore(4, 2),
        BookBookstore(5, 1),
        BookBookstore(1, 3),
        BookBookstore(3, 2),
        BookBookstore(5, 2),
    ]

    store_dict = build_store_dict(bookstores)
    book_dict = build_book_dict(books)

    one_to_many = get_one_to_many(books, store_dict)

    many_to_many = get_many_to_many(book_bookstores, book_dict, store_dict)

    print('Задание В1')
    res_1 = get_books_starting_with_a(one_to_many)
    pprint(res_1)

    print('\nЗадание В2')
    res_2 = get_min_price_per_store(one_to_many)
    pprint(res_2, width=60)

    print('\nЗадание В3')
    res_3 = get_books_with_stores(many_to_many)
    pprint(res_3)


if __name__ == '__main__':
    main()
