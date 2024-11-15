# Функция для чтения чисел из файла
def read_numbers_from_file(filename):
    try:
        with open(filename, 'r') as file:
            numbers = [float(line.strip()) for line in file]
        return numbers
    except FileNotFoundError:
        return "Ошибка: Файл не найден."
    except ValueError:
        return "Ошибка: Некорректные данные в файле."


# Функция для записи результата в файл
def write_result_to_file(filename, result):
    try:
        with open(filename, 'w') as file:
            file.write(f"Результат: {result}\n")
    except Exception as e:
        return f"Ошибка записи в файл: {e}"


# Функция для сложения всех чисел
def sum_numbers(numbers):
    return sum(numbers)


# Функция для вычитания всех чисел
def subtract_numbers(numbers):
    result = numbers[0]
    for num in numbers[1:]:
        result -= num
    return result


# Функция для умножения всех чисел
def multiply_numbers(numbers):
    result = 1
    for num in numbers:
        result *= num
    return result


# Основная программа
def file_calculator(input_file, output_file):
    numbers = read_numbers_from_file(input_file)

    if isinstance(numbers, str):
        # Если произошла ошибка, выводим сообщение
        print(numbers)
    else:
        print(f"Прочитанные числа: {numbers}")
        print("Выберите операцию:")
        print("1. Сложение")
        print("2. Вычитание")
        print("3. Умножение")

        choice = input("Введите номер операции (1/2/3): ")

        if choice == '1':
            result = sum_numbers(numbers)
            print(f"Сумма чисел: {result}")
        elif choice == '2':
            result = subtract_numbers(numbers)
            print(f"Результат вычитания: {result}")
        elif choice == '3':
            result = multiply_numbers(numbers)
            print(f"Результат умножения: {result}")
        else:
            print("Неверный ввод")
            return

        # Записываем результат в выходной файл
        write_result_to_file(output_file, result)
        print(f"Результат записан в файл: {output_file}")


# Пример использования
input_filename = 'input.txt'  # Входной файл с числами
output_filename = 'output.txt'  # Файл для записи результата
file_calculator(input_filename, output_filename)
