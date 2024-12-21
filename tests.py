import unittest
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


class TestLogic(unittest.TestCase):
    def setUp(self):
        self.bookstores = [
            Bookstore(1, 'Книжный мир'),
            Bookstore(2, 'Буквоед'),
            Bookstore(3, 'Азбука-Аттикус'),
            Bookstore(4, 'Читай-город'),
            Bookstore(5, 'Дом книги'),
        ]

        self.books = [
            Book(1, 'Анна Каренина', 500.0, 1),
            Book(2, 'Преступление и наказание', 600.0, 2),
            Book(3, 'Алые паруса', 450.0, 3),
            Book(4, 'Мастер и Маргарита', 550.0, 2),
            Book(5, 'Алиса в стране чудес', 700.0, 1),
        ]

        self.book_bookstores = [
            BookBookstore(1, 1),
            BookBookstore(2, 2),
            BookBookstore(3, 3),
            BookBookstore(4, 2),
            BookBookstore(5, 1),
            BookBookstore(1, 3),
            BookBookstore(3, 2),
            BookBookstore(5, 2),
        ]

        self.store_dict = build_store_dict(self.bookstores)
        self.book_dict = build_book_dict(self.books)
        self.one_to_many = get_one_to_many(self.books, self.store_dict)
        self.many_to_many = get_many_to_many(self.book_bookstores, self.book_dict, self.store_dict)

    # -------------------------------------------------------------------------
    # Тесты для build_store_dict, build_book_dict
    # -------------------------------------------------------------------------
    def test_build_store_dict_keys(self):
        expected_keys = {1, 2, 3, 4, 5}
        self.assertEqual(set(self.store_dict.keys()), expected_keys)
        self.assertIsInstance(self.store_dict[1], Bookstore)

    def test_build_book_dict_keys(self):
        expected_keys = {1, 2, 3, 4, 5}
        self.assertEqual(set(self.book_dict.keys()), expected_keys)
        self.assertIsInstance(self.book_dict[1], Book)

    # -------------------------------------------------------------------------
    # Тесты для get_one_to_many
    # -------------------------------------------------------------------------
    def test_get_one_to_many_result_length(self):
        self.assertEqual(len(self.one_to_many), 5)

    def test_get_one_to_many_content(self):
        for book, store in self.one_to_many:
            self.assertIsInstance(book, Book)
            self.assertIsInstance(store, Bookstore)
            self.assertEqual(book.store_id, store.id)

    def test_get_one_to_many_empty_lists(self):
        result = get_one_to_many([], {})
        self.assertEqual(result, [])

    # -------------------------------------------------------------------------
    # Тесты для get_many_to_many
    # -------------------------------------------------------------------------
    def test_get_many_to_many_result_length(self):
        self.assertEqual(len(self.many_to_many), 8)

    def test_get_many_to_many_content(self):
        for book, store in self.many_to_many:
            self.assertIsInstance(book, Book)
            self.assertIsInstance(store, Bookstore)

    def test_get_many_to_many_empty(self):
        result = get_many_to_many([], self.book_dict, self.store_dict)
        self.assertEqual(result, [])

    # -------------------------------------------------------------------------
    # Тесты для get_books_starting_with_a (Задание В1)
    # -------------------------------------------------------------------------
    def test_books_starting_with_a_common(self):
        result = get_books_starting_with_a(self.one_to_many)

        self.assertIn(('Анна Каренина', 'Книжный мир'), result)
        self.assertIn(('Алиса в стране чудес', 'Книжный мир'), result)
        self.assertIn(('Алые паруса', 'Азбука-Аттикус'), result)

        for book_title, _ in result:
            self.assertTrue(book_title.startswith('А'))

    def test_books_starting_with_a_case_sensitivity(self):
        books_temp = [
            Book(6, 'anna', 111.0, 1),
            Book(7, 'Альбом', 222.0, 1),
        ]

        one_to_many_temp = get_one_to_many(books_temp, self.store_dict)
        result = get_books_starting_with_a(one_to_many_temp)

        self.assertIn(('Альбом', 'Книжный мир'), result)
        self.assertNotIn(('anna', 'Книжный мир'), result)

    def test_books_starting_with_a_empty_input(self):
        result = get_books_starting_with_a([])
        self.assertEqual(result, [])

    # -------------------------------------------------------------------------
    # Тесты для get_min_price_per_store (Задание В2)
    # -------------------------------------------------------------------------
    def test_min_price_per_store_common(self):
        result = get_min_price_per_store(self.one_to_many)

        expected = [
            ('Азбука-Аттикус', 450.0),
            ('Книжный мир', 500.0),
            ('Буквоед', 550.0),
        ]
        self.assertEqual(result, expected)

    def test_min_price_per_store_sorting(self):
        result = get_min_price_per_store(self.one_to_many)
        prices = [item[1] for item in result]
        self.assertEqual(prices, sorted(prices))

    def test_min_price_per_store_empty_input(self):
        result = get_min_price_per_store([])
        self.assertEqual(result, [])

    # -------------------------------------------------------------------------
    # Тесты для get_books_with_stores (Задание В3)
    # -------------------------------------------------------------------------
    def test_books_with_stores_common(self):
        result = get_books_with_stores(self.many_to_many)

        self.assertIn(('Анна Каренина', 500.0, 'Книжный мир'), result)
        self.assertIn(('Анна Каренина', 500.0, 'Азбука-Аттикус'), result)

        self.assertIn(('Алиса в стране чудес', 700.0, 'Книжный мир'), result)
        self.assertIn(('Алиса в стране чудес', 700.0, 'Буквоед'), result)

    def test_books_with_stores_sorting(self):
        result = get_books_with_stores(self.many_to_many)

        titles = [item[0] for item in result]

        self.assertEqual(titles, sorted(titles))

    def test_books_with_stores_empty_input(self):
        result = get_books_with_stores([])
        self.assertEqual(result, [])

    def test_books_with_stores_duplicate_check(self):
        duplicated_book_bookstores = self.book_bookstores + [
            BookBookstore(1, 1),
            BookBookstore(3, 2),
        ]

        many_to_many_dups = get_many_to_many(duplicated_book_bookstores, self.book_dict, self.store_dict)
        result = get_books_with_stores(many_to_many_dups)

        from collections import Counter
        counter_result = Counter(result)
        self.assertGreaterEqual(
            counter_result[('Анна Каренина', 500.0, 'Книжный мир')],
            2
        )
        self.assertGreaterEqual(
            counter_result[('Алые паруса', 450.0, 'Буквоед')],
            2
        )


if __name__ == '__main__':
    unittest.main()
