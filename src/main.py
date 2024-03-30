from parser import *
from typing import List

from instruction import *


def execute_instructions(instructions: List[Instruction], memory: List[int]):
    ...



def main() -> int:
    f = open("./data/listing_002.obj", "rb").read().strip()

    instructions: List[Instruction] = parse_instructions(f)
    memory: List[int] = [0 for _ in range(512)]
    execute_instructions(instructions, memory)

    return 0


if __name__ == "__main__":
    exit(main())

# eicall
# eijmp
# des
# lac
# las
# xch
