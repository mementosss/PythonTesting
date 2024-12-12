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
        with open(self.database_path, "r", encoding="utf-8") as file:
            for line in file:
                symptoms, patient_name = line.strip().split(": ")
                symptoms_list = tuple(symptoms.split(", "))  # Сохраняем порядок симптомов
                diagnoses[symptoms_list] = patient_name
        return diagnoses

    @profile
    def get_diagnosis(self, symptoms):
        symptoms_tuple = tuple(symptoms)  # Сохраняем порядок симптомов при поиске
        patient_name = self.diagnoses.get(symptoms_tuple)
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
        return diagnosis_map.get(symptoms, "Неизвестный диагноз")

    @profile
    def list_patients(self):
        patients = []
        for symptoms, patient_name in self.diagnoses.items():
            patients.append((symptoms, patient_name))

        for idx, (symptoms, patient_name) in enumerate(patients, 1):
            print(f"{idx}. {patient_name} ({', '.join(symptoms)})")

        return patients


def main():
    therapist = Therapist()
    patients = therapist.list_patients()

    try:
        patient_number = int(input("Выберите номер пациента для получения диагноза: "))

        if 1 <= patient_number <= len(patients):
            symptoms, patient_name = patients[patient_number - 1]
            print(therapist.get_diagnosis(symptoms))
        else:
            print("Неверный номер пациента.")
    except ValueError:
        print("Пожалуйста, введите корректный номер пациента.")


if __name__ == "__main__":
    main()
