import unittest
from unittest.mock import patch, mock_open
from TherapistClass import Therapist


class TestTherapist(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open,
           read_data="головная боль, тошнота: Иван Иванов\nкашель, температура, затрудненное дыхание: Мария Петрова")
    def test_load_diagnoses(self, mock_file):
        therapist = Therapist(database_path="diagnoses.txt")
        # Проверяем, что загруженные диагнозы соответствуют ожиданиям
        expected_diagnoses = {
            ("головная боль", "тошнота"): "Иван Иванов",
            ("кашель", "температура", "затрудненное дыхание"): "Мария Петрова"
        }
        self.assertEqual(therapist.diagnoses, expected_diagnoses)

    @patch("builtins.open", new_callable=mock_open,
           read_data="головная боль, тошнота: Иван Иванов\nкашель, температура, затрудненное дыхание: Мария Петрова")
    def test_get_diagnosis(self, mock_file):
        therapist = Therapist(database_path="diagnoses.txt")

        # Тестируем диагноз для известного пациента
        result = therapist.get_diagnosis(["головная боль", "тошнота"])
        self.assertEqual(result, "Иван Иванов — диагноз: мигрень")

        # Тестируем диагноз для неизвестного набора симптомов
        result = therapist.get_diagnosis(["головная боль", "кашель"])
        self.assertEqual(result, "Диагноз не найден")

    def test_get_fixed_diagnosis(self):
        # Тестируем известные симптомы
        self.assertEqual(Therapist.get_fixed_diagnosis(("головная боль", "тошнота")), "мигрень")
        self.assertEqual(Therapist.get_fixed_diagnosis(("кашель", "температура", "затрудненное дыхание")), "бронхит")

        # Тестируем неизвестные симптомы
        self.assertEqual(Therapist.get_fixed_diagnosis(("кашель", "насморк")), "Неизвестный диагноз")

    @patch("builtins.open", new_callable=mock_open,
           read_data="головная боль, тошнота: Иван Иванов\nкашель, температура, затрудненное дыхание: Мария Петрова")
    def test_list_patients(self, mock_file):
        therapist = Therapist(database_path="diagnoses.txt")
        patients = therapist.list_patients()
        # Проверяем, что метод list_patients правильно выводит пациентов
        self.assertEqual(len(patients), 2)
        self.assertEqual(patients[0], (("головная боль", "тошнота"), "Иван Иванов"))
        self.assertEqual(patients[1], (("кашель", "температура", "затрудненное дыхание"), "Мария Петрова"))

    def test_invalid_file_path(self):
        # Проверяем, что будет выброшена ошибка при отсутствии файла
        with self.assertRaises(FileNotFoundError):
            therapist = Therapist(database_path="non_existent_file.txt")


if __name__ == "__main__":
    unittest.main()
