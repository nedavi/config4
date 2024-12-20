import csv
import struct

# python interpreter.py example.bin result.csv 1024

class Interpreter:
    def __init__(self, memory_size=1024):
        """Инициализация интерпретатора с заданным размером памяти."""
        self.stack = []  # Стек для операций
        self.memory = [0] * memory_size  # Память

    def execute(self, binary_path, output_path):
        """
        Выполняет все инструкции из бинарного файла.
        binary_path: Путь к бинарному файлу.
        output_path: Путь к файлу результата.
        """
        with open(binary_path, "rb") as f:
            data = f.read()

        pointer = 0  # Указатель на текущую инструкцию
        while pointer < len(data):
            # Разбираем инструкцию (1 байт opcode, 4 байта operand)
            opcode = data[pointer]
            operand = struct.unpack("<I", data[pointer + 1:pointer + 5])[0]
            pointer += 5  # Переход к следующей инструкции

            # Выполняем текущую инструкцию
            self.execute_instruction(opcode, operand)

        # Записываем память в файл результата
        self.save_result(output_path)

    def execute_instruction(self, opcode, operand):
        """
        Выполняет одну инструкцию по заданным opcode и operand.
        opcode: Код операции (1 байт).
        operand: Операнд инструкции (4 байта).
        """
        if opcode == 0x00:  # LOAD_CONST
            self.stack.append(operand)
        elif opcode == 0xCE:  # READ_MEM
            if operand >= len(self.memory) or operand < 0:
                raise IndexError(f"READ_MEM: Адрес {operand} выходит за пределы памяти!")
            self.stack.append(self.memory[operand])
        elif opcode == 0xA2:  # WRITE_MEM
            if operand >= len(self.memory) or operand < 0:
                raise IndexError(f"WRITE_MEM: Адрес {operand} выходит за пределы памяти!")
            value = self.stack.pop()
            self.memory[operand] = value
        elif opcode == 0x01:  # SGN
            value = self.stack.pop()
            self.stack.append(1 if value > 0 else -1 if value < 0 else 0)
        else:
            raise ValueError(f"Unknown opcode: {opcode}")

    def execute_binary(self, binary_instruction):
        """
        Выполняет одиночную бинарную инструкцию.
        binary_instruction: Бинарные данные инструкции (5 байт).
        """
        opcode = binary_instruction[0]
        operand = struct.unpack("<I", binary_instruction[1:5])[0]
        self.execute_instruction(opcode, operand)

    def save_result(self, output_path):
        """
        Сохраняет содержимое памяти в файл в формате CSV.
        output_path: Путь к выходному файлу.
        """
        with open(output_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Address", "Value"])  # Заголовки CSV
            for address, value in enumerate(self.memory):
                if value != 0:  # Сохраняем только ненулевые значения
                    writer.writerow([address, value])


if __name__ == "__main__":
    import sys

    # Проверяем, что переданы все аргументы
    if len(sys.argv) != 4:
        print("Использование: python interpreter.py <binary_path> <output_path> <memory_size>")
        sys.exit(1)

    binary_path = sys.argv[1]
    output_path = sys.argv[2]
    memory_size = int(sys.argv[3])

    # Создаем интерпретатор и выполняем файл
    interpreter = Interpreter(memory_size)
    interpreter.execute(binary_path, output_path)
    print(f"Результат записан в {output_path}")
