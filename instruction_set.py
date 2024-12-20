import struct

def encode_load_constant(operands):
    """Загрузка константы (A=0, B=Константа)."""
    opcode = 0x00  # A=0
    constant = int(operands[0])  # Константа
    # Используем '<Bi' для знакового формата
    return struct.pack("<Bi", opcode, constant)

def encode_read_memory(operands):
    """Чтение значения из памяти (A=6, B=Адрес)."""
    opcode = 0xCE  # A=6
    address = int(operands[0])  # Адрес
    return struct.pack("<BI", opcode, address)

def encode_write_memory(operands):
    """Запись значения в память (A=2, B=Смещение)."""
    opcode = 0xA2  # A=2
    offset = int(operands[0])  # Смещение
    return struct.pack("<BI", opcode, offset)

def encode_sgn(operands):
    """Унарная операция sgn() (A=1)."""
    opcode = 0x01  # A=1
    return struct.pack("<BI", opcode, 0)

INSTRUCTION_SET = {
    "LOAD_CONST": {"encode": encode_load_constant},
    "READ_MEM": {"encode": encode_read_memory},
    "WRITE_MEM": {"encode": encode_write_memory},
    "SGN": {"encode": encode_sgn},
}
