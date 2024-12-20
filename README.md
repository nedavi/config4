# Задание

Разработать ассемблер и интерпретатор для учебной виртуальной машины (УВМ).  
Система команд УВМ описана ниже.

**Требования:**

1. **Ассемблер**:
   - Принимает на вход текст исходной программы (ассемблерный код), путь к которой задается из командной строки.
   - Результатом работы является бинарный файл (последовательность байт), путь к которому также задается из командной строки.
   - Дополнительный ключ командной строки задает путь к файлу-логу (в формате CSV), в котором сохраняется список ассемблированных инструкций с их параметрами.
   
2. **Интерпретатор**:
   - Принимает на вход бинарный файл (результат работы ассемблера) и выполняет команды УВМ.
   - Интерпретатор должен записывать результаты выполнения (содержимое определенного диапазона памяти УВМ) в выходной файл в формате CSV.
   - Диапазон памяти задается параметрами командной строки.

3. **Форматы файлов**:
   - Лог-файл ассемблера и файл результата интерпретатора – в формате CSV.
   
4. **Команды УВМ** (приведены примеры и байтовая реализация):
   - **Загрузка константы (A=0)**:  
     Размер: 5 байт (1 байт – опкод, 4 байта – константа).  
     Пример: (A=0, B=256)  
     ```
     0x00, 0x08, 0x00, 0x00, 0x00
     ```
     Результат выполнения: новый элемент на вершине стека.
   
   - **Чтение значения из памяти (A=6)**:  
     Размер: 5 байт (1 байт – опкод, 4 байта – адрес).  
     Пример: (A=6, B=1017)  
     ```
     0xCE, 0x1F, 0x00, 0x00, 0x00
     ```
     Результат выполнения: значение из памяти по указанному адресу помещается на стек.

   - **Запись значения в память (A=2)**:  
     Размер: 5 байт (1 байт – опкод, 4 байта – смещение/адрес).  
     Пример: (A=2, B=20)  
     ```
     0xA2, 0x00, 0x00, 0x00, 0x00
     ```
     Операнд снимается со стека, записывается по указанному адресу в памяти.

   - **Унарная операция sgn() (A=1)**:  
     Размер: 5 байт (1 байт – опкод, 4 байта – зарезервированы под операнд).  
     Пример: (A=1)  
     ```
     0x01, 0x00, 0x00, 0x00, 0x00
     ```
     Снимает значение со стека, вычисляет его знак (-1, 0 или 1) и кладет результат обратно на стек.
   
5. **Тестовая программа**:
   - Задача: выполнить поэлементно операцию `sgn()` над вектором длины 4 и записать результат обратно в тот же вектор.
   
6. **Тесты**:
   - Необходимо реализовать и отладить тестовые сценарии для всех команд, а также написать тестовую программу.
   
---

## Описание проекта

Данный проект реализует ассемблер и интерпретатор для учебной виртуальной машины (УВМ). Проект позволяет:

- Транслировать ассемблерный код в бинарный формат.
- Логировать процесс ассемблирования в CSV-файл.
- Выполнять сгенерированный бинарный код с помощью интерпретатора.
- Сохранять состояние памяти после выполнения команд в CSV-файл.

Система команд поддерживает операции над стеком и памятью, а также простые арифметические и логические операции, такие как вычисление знака числа `sgn()`.

## Структура проекта

```
.
├── assembler.py        # Ассемблер: преобразует asm-код в бинарный и логирует инструкции.
├── example.asm         # Пример ассемблерного кода (тестовая программа).
├── instruction_set.py  # Набор инструкций с правилами кодирования.
├── interpreter.py      # Интерпретатор: выполняет бинарный код, формируя результат в CSV.
├── log.csv             # Пример файла лога, генерируемого ассемблером.
├── result.csv          # Пример файла с результатом работы интерпретатора.
└── tests.py            # Тесты для валидации функционала ассемблера и интерпретатора.
```

## Основной функционал

1. **Ассемблер (assembler.py)**:
   - Принимает путь к исходному ассемблерному файлу (например, `example.asm`).
   - Принимает путь к выходному бинарному файлу.
   - Принимает путь к лог-файлу CSV.
   - Пример запуска:
     ```bash
     python3 assembler.py example.asm example.bin log.csv
     ```
   - Результат:
     - `example.bin` – бинарный файл с командами.
     - `log.csv` – лог в формате CSV с информацией о командах.

2. **Интерпретатор (interpreter.py)**:
   - Принимает путь к бинарному файлу (результату ассемблера).
   - Принимает путь к выходному CSV-файлу результата.
   - Принимает размер памяти УВМ.
   - Пример запуска:
     ```bash
     python3 interpreter.py example.bin result.csv 1024
     ```
   - Результат:
     - `result.csv` – файл с содержимым памяти после выполнения программы.

3. **Команды**:
   - `LOAD_CONST`: Загрузка константы на стек.
   - `READ_MEM`: Чтение значения из памяти в стек.
   - `WRITE_MEM`: Запись значения из стека в память.
   - `SGN`: Вычисление знака верхнего элемента стека.

Все команды имеют фиксированный формат 5 байт:  
1 байт – opcode (содержит код операции A), оставшиеся 4 байта – операнд (константа, адрес и т.д.).

## Тестирование

- В `tests.py` реализованы тесты для отдельных команд (`LOAD_CONST`, `READ_MEM`, `WRITE_MEM`, `SGN`).
- Тестовая программа `example.asm` демонстрирует применение команд и преобразование массива чисел в их знаки.

Для запуска тестов:

```bash
python3 tests.py
```

При успешном прохождении тестов будут выведены сообщения о том, что каждый тест прошел успешно.

## Примечание

Данный проект служит учебным примером для отработки навыков разработки ассемблера и интерпретатора для простой виртуальной машины, а также для практики в работе с бинарными форматами, логированием и тестированием.

## Автор

Автор: *Nedavi*
