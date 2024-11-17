from behave import given, when, then
from task3.features.TherapistClass import Therapist


@given('терапевт имеет базу данных диагнозов')
def step_given_therapist_has_database(context):
    context.therapist = Therapist(database_path="task3/features/diagnoses.txt")


@when('пользователь выбирает номер пациента {patient_number}')
def step_when_user_selects_patient(context, patient_number):
    patient_number = int(patient_number)
    patients = context.therapist.list_patients()

    if 1 <= patient_number <= len(patients):
        symptoms, patient_name = patients[patient_number - 1]
        context.result = context.therapist.ask_questions(symptoms)
    else:
        context.result = "Неверный номер пациента"


@then('диагноз должен быть "{expected_diagnosis}"')
def step_then_diagnosis_should_be(context, expected_diagnosis):
    print("Captured result: ", context.result)  # Выводим текущий результат для отладки
    assert context.result == expected_diagnosis


@when('пользователь выбирает неверный номер пациента')
def step_when_user_selects_invalid_patient(context):
    context.result = "Неверный номер пациента"
