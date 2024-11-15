import unittest
from unittest.mock import patch, mock_open
import main  # Импортируем основной модуль с функциями


class TestFileCalculator(unittest.TestCase):

    # Тест для функции read_numbers_from_file
    @patch("builtins.open", new_callable=mock_open, read_data="1\n2\n3\n")
    def test_read_numbers_from_file(self, mock_file):
        result = main.read_numbers_from_file("input.txt")
        self.assertEqual(result, [1.0, 2.0, 3.0])

    @patch("builtins.open", new_callable=mock_open, read_data="invalid\n2\n3\n")
    def test_read_numbers_from_file_invalid_data(self, mock_file):
        result = main.read_numbers_from_file("input.txt")
        self.assertEqual(result, "Ошибка: Некорректные данные в файле.")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_read_numbers_from_file_not_found(self, mock_file):
        result = main.read_numbers_from_file("non_existent.txt")
        self.assertEqual(result, "Ошибка: Файл не найден.")

    # Тест для функции write_result_to_file
    @patch("builtins.open", new_callable=mock_open)
    def test_write_result_to_file(self, mock_file):
        result = main.write_result_to_file("output.txt", 30.0)
        self.assertIsNone(result)
        mock_file().write.assert_called_with("Результат: 30.0\n")

    @patch("builtins.open", side_effect=OSError("Ошибка ввода/вывода."))
    def test_write_result_to_file_error(self, mock_file):
        result = main.write_result_to_file("output.txt", 30.0)
        self.assertIn("Ошибка записи в файл:", result)

    # Тест для функции sum_numbers
    def test_sum_numbers(self):
        result = main.sum_numbers([1.0, 2.0, 3.0])
        self.assertEqual(result, 6.0)

    # Тест для функции subtract_numbers
    def test_subtract_numbers(self):
        result = main.subtract_numbers([10.0, 2.0, 3.0])
        self.assertEqual(result, 5.0)

    # Тест для функции multiply_numbers
    def test_multiply_numbers(self):
        result = main.multiply_numbers([2.0, 3.0, 4.0])
        self.assertEqual(result, 24.0)


if __name__ == '__main__':
    unittest.main()
