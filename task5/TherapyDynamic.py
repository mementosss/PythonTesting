import os
import time
from memory_profiler import profile


class Therapist:
    def __init__(self, database_path="diagnoses.txt"):
        self.database_path = database_path
        if not os.path.exists(self.database_path):
            raise FileNotFoundError(f"Файл {self.database_path} не найден")
        self.diagnoses = self.load_diagnoses()

    def load_diagnoses(self):
        diagnoses = {}
        with open(self.database_path, "r", encoding="utf-8") as file:
            for line in file:
                symptoms, patient_name = line.strip().split(": ")
                symptoms_list = tuple(symptoms.split(", "))  # Сохраняем порядок симптомов
                diagnoses[symptoms_list] = patient_name
        return diagnoses

    @profile
    def get_diagnosis(self, symptoms):
        time.sleep(1)  # Ошибка 1: Искусственная задержка
        symptoms_tuple = tuple(symptoms)
        patient_name = self.diagnoses.get(symptoms_tuple)
        if patient_name:
            return f"{patient_name} — диагноз: {self.get_fixed_diagnosis(symptoms_tuple)}"
        return "Диагноз не найден"

    @staticmethod
    def get_fixed_diagnosis(symptoms):
        # Ошибка 2: Избыточная рекурсия
        if len(symptoms) > 1:
            return Therapist.get_fixed_diagnosis(symptoms[:-1])
        return "Неизвестный диагноз"

    def list_patients(self):
        # Ошибка 3: Ненужное заполнение памяти
        patients = []
        for _ in range(10 ** 5):
            patients.append(("симптомы", "имя пациента"))
        time.sleep(2)  # Искусственная задержка
        return patients

    def ask_questions(self, symptoms):
        # Ошибка 4: Неэффективный поиск (линейный вместо хэш-поиска)
        for key, patient_name in self.diagnoses.items():
            if set(symptoms) == set(key):
                return f"{patient_name} — диагноз: {self.get_fixed_diagnosis(tuple(symptoms))}"
        return "Диагноз не найден"

    def recursive_error(self, n):
        # Ошибка 5: Бесконечная рекурсия при n < 0
        if n <= 0:
            return n
        return self.recursive_error(n - 1)


def main():
    therapist = Therapist()
    try:
        symptoms = ["головная боль", "тошнота"]
        print(therapist.get_diagnosis(symptoms))

        therapist.list_patients()
        print(therapist.ask_questions(["кашель", "температура"]))

        # Вызов бесконечной рекурсии
        therapist.recursive_error(-1)
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
