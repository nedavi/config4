from assembler import assemble
from interpreter import Interpreter
import os

# python tests.py

def test_load_constant():
    """Тест команды LOAD_CONST."""
    assemble("example.asm", "example.bin", "log.csv")
    with open("example.bin", "rb") as f:
        binary = f.read()
    # Ожидаемая команда: 0x00 + 256 (как 4-байтовое знаковое целое)
    expected_binary = b"\x00\x00\x01\x00\x00"  # opcode = 0x00, constant = 256
    assert binary.startswith(expected_binary), f"LOAD_CONST не прошел тест: {binary.hex()}"


def test_read_memory():
    """Тест команды READ_MEM."""
    interpreter = Interpreter(memory_size=1024)
    interpreter.memory[1017] = 42  # Устанавливаем значение в памяти
    instruction = b"\xCE\xF9\x03\x00\x00"  # READ_MEM для адреса 1017
    interpreter.execute_binary(instruction)
    assert interpreter.stack[-1] == 42, "READ_MEM не прошел тест"


def test_write_memory():
    """Тест команды WRITE_MEM."""
    interpreter = Interpreter(memory_size=1024)
    interpreter.stack.append(123)  # Значение для записи
    instruction = b"\xA2\x00\x00\x00\x00"  # WRITE_MEM для адреса 0
    interpreter.execute_binary(instruction)
    assert interpreter.memory[0] == 123, "WRITE_MEM не прошел тест"


def test_sgn():
    """Тест команды SGN."""
    interpreter = Interpreter()
    interpreter.stack.append(-10)  # Входное значение
    instruction = b"\x01\x00\x00\x00\x00"  # SGN
    interpreter.execute_binary(instruction)
    assert interpreter.stack[-1] == -1, "SGN не прошел тест"


if __name__ == "__main__":
    try:
        test_load_constant()
        print("test_load_constant: Passed")
        test_read_memory()
        print("test_read_memory: Passed")
        test_write_memory()
        print("test_write_memory: Passed")
        test_sgn()
        print("test_sgn: Passed")
        print("Все тесты прошли успешно!")
    except AssertionError as e:
        print(f"Ошибка: {e}")
