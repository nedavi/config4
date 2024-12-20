import csv
import struct
from instruction_set import INSTRUCTION_SET

# python assembler.py example.asm example.bin log.csv

def assemble(input_file, output_file, log_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    binary_data = bytearray()
    log = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        mnemonic, *operands = parts
        instruction = INSTRUCTION_SET.get(mnemonic)
        if not instruction:
            raise ValueError(f"Unknown instruction: {mnemonic}")

        binary = instruction["encode"](operands)
        binary_data.extend(binary)
        log.append({"mnemonic": mnemonic, "operands": operands, "binary": binary.hex()})

    with open(output_file, "wb") as f:
        f.write(binary_data)

    with open(log_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["mnemonic", "operands", "binary"])
        writer.writeheader()
        writer.writerows(log)


if __name__ == "__main__":
    import sys

    assemble(sys.argv[1], sys.argv[2], sys.argv[3])
