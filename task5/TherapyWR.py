import os
from memory_profiler import profile


class Therapist:
    def __init__(self, database_path="diagnoses.txt"):
        self.database_path = database_path
        if not os.path.exists(self.database_path):
            raise FileNotFoundError(f"Файл {self.database_path} не найден")
        self.diagnoses = self.load_diagnoses()

    @profile
    def load_diagnoses(self):
        diagnoses = {}

        # Ошибка 1: Загрузка большого списка в память, который не используется.
        unused_large_list = [x for x in range(10**6)]

        with open(self.database_path, "r", encoding="utf-8") as file:
            for line in file:
                symptoms, patient_name = line.strip().split(": ")
                symptoms_list = tuple(symptoms.split(", "))  # Сохраняем порядок симптомов
                diagnoses[symptoms_list] = patient_name

        # Ошибка 2: Создание большого списка строк в памяти, хотя можно было бы обойтись итерацией.
        debug_lines = [line.strip() for line in open(self.database_path, "r", encoding="utf-8").readlines()]

        return diagnoses

    @profile
    def get_diagnosis(self, symptoms):
        symptoms_tuple = tuple(symptoms)  # Сохраняем порядок симптомов при поиске

        # Ошибка 3: Дублирование структуры данных, что увеличивает использование памяти.
        duplicate_diagnoses = self.diagnoses.copy()

        patient_name = duplicate_diagnoses.get(symptoms_tuple)
        if patient_name:
            return f"{patient_name} — диагноз: {self.get_fixed_diagnosis(symptoms_tuple)}"
        return "Диагноз не найден"

    @staticmethod
    def get_fixed_diagnosis(symptoms):
        diagnosis_map = {
            ("головная боль", "тошнота"): "мигрень",
            ("кашель", "температура", "затрудненное дыхание"): "бронхит",
            ("кашель", "температура"): "простуда",
            ("боль в горле", "кашель", "высокая температура"): "ангина",
            ("головная боль", "светобоязнь", "тошнота"): "мигрень",
            ("боль в животе", "диарея", "тошнота"): "пищевое отравление",
            ("боль в горле", "озноб", "насморк"): "ОРВИ",
            ("сильная усталость", "лихорадка"): "грипп",
            ("кашель", "заложенность носа", "головная боль"): "простуда",
            ("температура", "ломота в теле", "слабость"): "грипп",
        }

        # Ошибка 4: Создание временного списка для ключей вместо прямого обращения.
        temp_keys = list(diagnosis_map.keys())
        return diagnosis_map.get(symptoms, "Неизвестный диагноз")

    @profile
    def list_patients(self):
        patients = []

        # Ошибка 5: Использование избыточной памяти для хранения строки с разными преобразованиями.
        for symptoms, patient_name in self.diagnoses.items():
            patient_info = f"{patient_name} ({', '.join(symptoms)})"
            patients.append((symptoms, patient_info))

        for idx, (symptoms, patient_info) in enumerate(patients, 1):
            print(f"{idx}. {patient_info}")

        return patients


def main():
    therapist = Therapist()
    patients = therapist.list_patients()

    try:
        patient_number = int(input("Выберите номер пациента для получения диагноза: "))

        if 1 <= patient_number <= len(patients):
            symptoms, patient_info = patients[patient_number - 1]
            print(therapist.get_diagnosis(symptoms))
        else:
            print("Неверный номер пациента.")
    except ValueError:
        print("Пожалуйста, введите корректный номер пациента.")


if __name__ == "__main__":
    main()
