import customtkinter as ctk
from tkinter import messagebox, filedialog


# Функция для шифрования текста методом Цезаря
def encrypt_text(text, shift):
    encrypted = ""
    shift_amount = shift % 26  # Вычисляем сдвиг
    for char in text:
        if char.isalpha():
            code = ord(char)
            base = ord('a') if char.islower() else ord('A')
            encrypted += chr((code - base + shift_amount) % 26 + base)
        else:
            encrypted += char
    return encrypted


# Функция для шифрования текста методом замены
def substitution_encrypt_text(text):
    # Пример простой замены: меняем буквы на их замену
    substitution_dict = str.maketrans("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
                                      "nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM")
    return text.translate(substitution_dict)


# Функция для анализа файла и вывода текста
def count_file_content():
    filename = entry.get()  # Получаем имя файла из текстового поля

    try:
        # Чтение файла
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        if not lines:
            raise ValueError("Файл пуст.")

        num_lines = len(lines)
        num_words = sum(len(line.split()) for line in lines)
        num_chars = sum(len(line) for line in lines)

        # Обновляем текст в метке с результатами
        result_label.configure(text=f"Строки: {num_lines}, Слова: {num_words}, Символы: {num_chars}")

        # Отображаем содержимое файла в текстовом поле
        text_area.delete("1.0", "end")
        text_area.insert("1.0", ''.join(lines))

    except FileNotFoundError:
        messagebox.showerror("Ошибка", f"Файл {filename} не найден.")
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")


# Функция для шифрования текста из текстового поля
def encrypt_file_content():
    method = encryption_method_var.get()  # Получаем выбранный метод
    try:
        shift = int(shift_var.get()) if method == "caesar" else None  # Получаем сдвиг только для Цезаря
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректное значение сдвига.")
        return

    content = text_area.get("1.0", "end")  # Получаем текст из текстового поля

    # Шифруем текст в зависимости от метода
    if method == "caesar":
        encrypted_content = encrypt_text(content, shift)
    elif method == "substitution":
        encrypted_content = substitution_encrypt_text(content)
    else:
        messagebox.showerror("Ошибка", "Выбран неверный метод шифрования.")
        return

    # Отображаем зашифрованный текст в правом текстовом поле
    encoded_text_area.delete("1.0", "end")
    encoded_text_area.insert("1.0", encrypted_content)


# Функция для сохранения зашифрованного текста в файл
def save_file_content():
    content = encoded_text_area.get("1.0", "end").strip()  # Сохраняем зашифрованный текст

    if not content:
        messagebox.showwarning("Предупреждение", "Нет текста для сохранения.")
        return

    # Открываем диалоговое окно для выбора имени файла
    filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")])
    if filename:
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)
            messagebox.showinfo("Сохранено", f"Файл сохранен как {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при сохранении: {str(e)}")


# Функции для перемещения окна
def start_move(event):
    global x_offset, y_offset
    x_offset = event.x
    y_offset = event.y


def move_window(event):
    root.geometry(f"+{event.x_root - x_offset}+{event.y_root - y_offset}")


# Функции для управления состоянием окна
def minimize_window():
    root.iconify()  # Сворачивает окно


def maximize_window():
    root.state('zoomed')  # Разворачивает окно на полный экран


# Создаем главное окно с помощью customtkinter
ctk.set_appearance_mode("light")  # Светлая тема
ctk.set_default_color_theme("dark-blue")  # Цветовая тема

root = ctk.CTk()  # Используем Ctk вместо обычного Tk()
root.title("Анализ текстового файла")
root.geometry("1280x720")  # Устанавливаем размер окна

# Отключаем системный заголовок
root.overrideredirect(True)

# Устанавливаем окно всегда поверх остальных
root.attributes("-topmost", True)

# Добавляем кастомную область заголовка (опционально)
header_frame = ctk.CTkFrame(root, height=30)
header_frame.pack(fill="x")

header_label = ctk.CTkLabel(header_frame, text="Анализ текстового файла")
header_label.pack(side="left", padx=10)

# Добавляем кнопки управления окном
minimize_button = ctk.CTkButton(header_frame,
                                fg_color="grey",
                                text="-",
                                font=("Arial", 15),
                                width=28,
                                height=14,
                                corner_radius=5,
                                command=minimize_window)
minimize_button.pack(side="right", padx=6)

maximize_button = ctk.CTkButton(header_frame,
                                fg_color="grey",
                                text="◻️",
                                font=("Arial", 15),
                                width=28,
                                height=14,
                                corner_radius=5,
                                command=maximize_window)
maximize_button.pack(side="right", padx=6)

close_button = ctk.CTkButton(header_frame,
                             fg_color="grey",
                             text="X",
                             font=("Arial", 15),
                             width=28,
                             height=14,
                             corner_radius=5,
                             command=root.quit)
close_button.pack(side="right", padx=6)

# Привязываем обработчики событий для перемещения окна
header_frame.bind("<Button-1>", start_move)  # Начало перемещения
header_frame.bind("<B1-Motion>", move_window)  # Процесс перемещения

# Создаем фрейм для остальных элементов и используем grid для его размещения
content_frame = ctk.CTkFrame(root)
content_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Добавляем элементы интерфейса
label = ctk.CTkLabel(content_frame, text="Введите имя файла (с расширением):")
label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

entry = ctk.CTkEntry(content_frame, width=160)  # Текстовое поле с шириной 160
entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

button = ctk.CTkButton(content_frame,
                       fg_color="#2b2b2b",
                       corner_radius=5,
                       width=120,
                       text="Загрузить файл",
                       command=count_file_content)
button.grid(row=1, column=0, columnspan=2, pady=10)

result_label = ctk.CTkLabel(content_frame, text="")
result_label.grid(row=2, column=0, columnspan=2, pady=10)

# Добавляем текстовое поле для отображения содержимого файла (слева)
text_area = ctk.CTkTextbox(content_frame, wrap="word", height=15)
text_area.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

# Добавляем текстовое поле для отображения зашифрованного текста (справа)
encoded_text_area = ctk.CTkTextbox(content_frame, wrap="word", height=15)
encoded_text_area.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

# Добавляем поле для ввода сдвига шифра
shift_label = ctk.CTkLabel(content_frame, text="Сдвиг для шифрования (Цезарь):")
shift_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

shift_var = ctk.StringVar(value="3")
shift_entry = ctk.CTkEntry(content_frame, textvariable=shift_var, width=160)
shift_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

# Добавляем метку и выпадающий список для выбора метода шифрования
method_label = ctk.CTkLabel(content_frame, text="Метод шифрования:")
method_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")

encryption_method_var = ctk.StringVar(value="caesar")
method_menu = ctk.CTkOptionMenu(content_frame, variable=encryption_method_var,
                                values=["caesar", "substitution"])
method_menu.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

# Добавляем кнопку для шифрования текста
encrypt_button = ctk.CTkButton(content_frame,
                               fg_color="#2b2b2b",
                               corner_radius=5,
                               width=120,
                               text="Зашифровать",
                               command=encrypt_file_content)
encrypt_button.grid(row=6, column=0, columnspan=2, pady=10)

# Добавляем кнопку для сохранения содержимого зашифрованного текста
save_button = ctk.CTkButton(content_frame,
                            fg_color="#2b2b2b",
                            corner_radius=5,
                            width=120,
                            text="Сохранить",
                            command=save_file_content)
save_button.grid(row=7, column=0, columnspan=2, pady=10)

# Настройка растягивания столбцов и строк в content_frame
content_frame.grid_columnconfigure(0, weight=1)  # Первый столбец растягивается
content_frame.grid_columnconfigure(1, weight=1)  # Второй столбец растягивается
content_frame.grid_rowconfigure(3, weight=1)  # Строка с текстовыми полями растягивается

# Запускаем главный цикл программы
root.mainloop()
