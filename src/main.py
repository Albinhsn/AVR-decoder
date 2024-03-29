def debug_byte(b0):
    print("0b", end="")
    for i in reversed(range(8)):
        print(b0 >> i & 0b1, end="")
    print()


def match_low_byte(b0, b1) -> bool:
    b0 &= 0b11111111
    b1 &= 0b11111111
    return b0 == b1


def parse_ops(f, idx):
    d = (f[idx] & 0b1) << 4
    r = (f[idx] & 0b10) << 3

    idx += 1
    d = d | ((f[idx] & 0b11110000) >> 4)
    r = r | (f[idx] & 0b1111)

    return d, r


def parse_adc(f, idx) -> int:
    ADC = 0b00011100
    mask = 0b11111100

    if (mask & f[idx]) == ADC:
        d, r = parse_ops(f, idx)
        print(f"ADC r{d}, r{r}")
        return 2

    return 0


def parse_break(f, idx) -> int:
    size = 2
    BREAK = 0b10010101_10011000

    # 1110 KKKK dddd KKKK
    while size != 0 and match_low_byte(BREAK >> ((size - 1) * 8), f[idx]):
        size -= 1
        idx += 1

    if size == 0:
        print("BREAK")
        return 2
    return 0


def parse_ldi(f, idx) -> int:
    LDI = 0b1110
    if not match_low_byte(LDI, f[idx]):
        return 0
    return 1


def parse_ijmp(f, idx):
    IJMP_HIGH = 0b1001_0100
    IJMP_LOW = 0b0000_1001
    if f[idx] == IJMP_HIGH and f[idx + 1] == IJMP_LOW:
        print("IJMP")
        return 2
    return 0


def parse_jmp(f, idx):
    JMP = 0b1001_0100
    mask = 0b1111_1110
    if (f[idx] & mask) == JMP:
        k = (f[idx] & 0b1) << 21
        idx += 1
        if (f[idx] & 0b1110) == 0b1100:
            k |= (f[idx] & 0b1111_0000) << 13
            k |= (f[idx] & 0b1) << 16
            idx += 1
            k |= f[idx] << 8
            k |= f[idx + 1] << 8
            print(f"JMP {k}")
            return 11

    return 0


def parse_icall(f, idx):
    ICALL_HIGH = 0b1001_0101
    ICALL_LOW = 0b0000_1001
    if f[idx] == ICALL_HIGH and f[idx + 1] == ICALL_LOW:
        print("ICALL")
        return 2
    return 0


def parse_mul(f, idx):
    MUL = 0b0000_0011
    if f[idx] == MUL:
        idx += 1
        high = f[idx] & 0b1000_0000
        low = f[idx] & 0b1000
        d = (f[idx] & 0b0111_0000) >> 4
        r = f[idx] & 0b111
        if high == 0 and low != 0:
            print(f"FMUL r{d+16},r{r+16}")
        elif high != 0 and low == 0:
            print(f"FMULS r{d+16},r{r+16}")
        elif high != 0 and low != 0:
            print(f"FMULSU r{d+16},r{r+16}")
        return 2

    return 0


def parse_add(f, idx) -> int:
    ADD = 0b000011_00
    mask = 0b111111_00

    if f[idx] & mask == ADD:
        d, r = parse_ops(f, idx)
        print(f"ADD r{d}, r{r}")
        return 2
    return 0


def parse_adiw(f, idx) -> int:
    REG_TABLE = [24, 26, 28, 30]
    ADIW = 0b10010110
    if f[idx] == ADIW:
        idx += 1
        d = (f[idx] & 0b00110000) >> 4

        K = (f[idx] & 0b1100_0000) >> 2
        K |= f[idx] & 0b1111

        print(f"ADIW r{REG_TABLE[d]}, {K}")

        return 2

    return 0


def parse_and(f, idx) -> int:
    AND = 0b001000_00
    mask = 0b111111_00

    if f[idx] & mask == AND:
        d, r = parse_ops(f, idx)
        print(f"AND r{d}, r{r}")

        return 2
    return 0


def parse_andi(f, idx) -> int:
    ANDI = 0b0111_0000
    mask = 0b1111_0000

    if f[idx] & mask == ANDI:
        K = (f[idx] & 0b1111) << 4
        idx += 1
        K |= f[idx] & 0b1111
        d = 16 + ((f[idx] & 0b11110000) >> 4)
        print(f"ANDI r{d}, {K}")

        return 2
    return 0


def parse_asr(f, idx) -> int:
    ASR_LOW = 0b1001_0100
    ASR_HIGH = 0b0101
    mask = 0b1001010_0
    if f[idx] & mask == ASR_LOW:
        d = (f[idx] & 0b1) << 4
        idx += 1
        if f[idx] & 0b1111 == ASR_HIGH:
            d |= f[idx] >> 4
            print(f"ASR r{d}")
            return 2

    return 0


def parse_call(f, idx) -> int:
    CALL = 0b1001_0100
    if (f[idx] & CALL) == CALL:
        k = (f[idx] & 1) << 21
        idx += 1

        if (f[idx] & 0b1110) == 0b1110:
            k |= (0b1111_0000 & f[idx]) << 12
            k |= (0b1 & f[idx]) << 16
            idx += 1
            k |= f[idx] << 8
            idx += 1
            k |= f[idx]
            print(f"CALL {k}")
            # Need to somehow parse an additional 8 bytes?

            return 11

    return 0


# ToDo wtf :)
def parse_cbr(f, idx) -> int:
    return 0


def parse_cbi(f, idx) -> int:
    CBI = 0b1001_1000
    if f[idx] == CBI:
        idx += 1

        A = (f[idx] & 0b1111_1000) >> 3
        b = f[idx] & 0b111
        print(f"CBI ${A:x},{b}")

        return 2

    return 0


def parse_bst(f, idx) -> int:
    BST = 0b11111010
    if f[idx] == BST:
        d = f[idx] & 1 << 4
        idx += 1
        if (f[idx] & 0b1000) != 0:
            d |= f[idx] >> 4
            b = f[idx] & 0b111
            print(f"BST r{d},{b}")

            return 2

    return 0


def parse_bset(f, idx) -> int:
    BSET_LOW = 0b1001_0100
    BSET_HIGH = 0b1000
    if f[idx] == BSET_LOW:
        idx += 1

        if (f[idx] & 0b1000_0000) == 0 and (f[idx] & 0b1111) == BSET_HIGH:
            s = (f[idx] & 0b0111_0000) >> 4
            print(f"BSET {s}")
            return 2

    return 0


def parse_cpi(f, idx) -> int:
    CPI = 0b0011_0000
    mask = 0b1111_0000

    if (f[idx] & mask) == CPI:
        K = (f[idx] & 0b1111) << 4
        idx += 1

        d = (f[idx] & 0b1111_0000) >> 4
        K |= f[idx] & 0b1111
        print(f"CPI r{d},{K}")
        return 2
    return 0


def parse_cpc(f, idx) -> int:
    CPC = 0b0000_0100
    mask = 0b1111_1100
    if f[idx] & mask == CPC:
        d, r = parse_ops(f, idx)
        print(f"cpc r{d}, r{r}")
        return 2
    return 0


def parse_cp(f, idx) -> int:
    CP = 0b0001_0100
    mask = 0b1111_1100
    if f[idx] & mask == CP:
        d, r = parse_ops(f, idx)
        print(f"cp r{d}, r{r}")
        return 2
    return 0


def parse_incdec(f, idx) -> int:
    HIGH = 0b1001_0100
    mask = 0b1111_1110

    if (f[idx] & mask) == HIGH:
        d = (f[idx] & 1) << 4
        idx += 1
        d |= (f[idx] & 0b11110000) >> 4
        LOW = f[idx] & 0b1111
        if LOW == 0b1010:
            print(f"dec r{d}")
        elif LOW == 0b0011:
            print(f"inc r{d}")
        else:
            return 0

        return 2

    return 0


def parse_com(f, idx) -> int:
    COM = 0b1001_0100

    if (f[idx] & COM) == COM:
        d = (f[idx] & 1) << 4
        idx += 1
        if (f[idx] & 0b1111) == 0:
            d |= (f[idx] & 0b1111_0000) >> 4
            print(f"COM r{d}")
            return 2

    return 0


def parse_bclr(f, idx) -> int:
    BCLR_LOW = 0b1001_0100
    BCLR_HIGH = 0b1000
    if f[idx] == BCLR_LOW:
        idx += 1

        if f[idx] & 0b1000_0000 != 0 and (f[idx] & 0b1111) == BCLR_HIGH:
            s = (f[idx] & 0b0111_0000) >> 4
            if s == 0:
                print("CLC/BCLR 0")
            if s == 1:
                print("CLZ/BCLR 1")
            elif s == 2:
                print("CLN/BCLR 2")
            elif s == 3:
                print("CLV/BCLR 3")
            elif s == 4:
                print("CLS/BCLR 4")
            elif s == 5:
                print("CLH/BCLR 5")
            elif s == 6:
                print("CLT/BCLR 6")
            elif s == 7:
                print("CLI/BCLR 7")
            else:
                print(f"BCLR {s}")
            return 2

    return 0


def parse_bld(f, idx) -> int:
    BLD_LOW = 0b1111_1000

    if (f[idx] & BLD_LOW) == BLD_LOW:
        d = (f[idx] & 1) << 7
        idx += 1
        if (f[idx] & 0b0000_1000) == 0:
            d |= (f[idx] & 0b11110000) >> 4
            b = f[idx] & 0b111
            print(f"BLD r{d},{b}")
            return 2
    return 0


def parse_branch(f, idx) -> int:
    BR0 = 0b1111_0100
    BR0_TABLE = [
        "BRCC/BRSH",
        "BRNE",
        "BRPL",
        "BRVC",
        "BRGE",
        "BRHC",
        "BRTC",
        "BRID",
    ]

    BR1 = 0b1111_0000
    BR1_TABLE = [
        "BRCS/BRLO",
        "BREQ",
        "BRMI",
        "BRVS",
        "BRLT",
        "BRHS",
        "BRTS",
        "BRIE",
    ]

    if (f[idx] & BR0) == BR0:
        k = (f[idx] & 0b11) << 5
        idx += 1

        s = f[idx] & 0b111
        k |= (f[idx] & 0b11111000) >> 3
        # BRCC
        print(f"{BR0_TABLE[s]} {k}")
        return 2

    if (f[idx] & BR1) == BR1:
        k = (f[idx] & 0b11) << 5
        idx += 1
        k |= (f[idx] & 0b11111000) >> 3

        s = f[idx] & 0b111
        print(f"{BR1_TABLE[s]} {k}")
        return 2
    return 0


def parse_cpse(f, idx) -> int:
    CPSE = 0b0001_0000
    mask = 0b11111100
    if (f[idx] & mask) == CPSE:
        d, r = parse_ops(f, idx)

        print(f"cpse r{d}, r{r}")
        return 2
    return 0


def parse_eor(f, idx) -> int:
    EOR = 0b0010_0100
    mask = 0b1111_1100
    if (f[idx] & mask) == EOR:
        d, r = parse_ops(f, idx)
        if d == r:
            print(f"CLR r{d}")
        else:
            print(f"EOR r{d},r{r}")
        return 2
    return 0


def parse_in(f, idx):
    IN = 0b1011_0000
    mask = 0b1111_1000

    if (f[idx] & mask) == IN:
        A = (f[idx] & 0b110) << 3
        d = (f[idx] & 0b1) << 4
        idx += 1

        A |= f[idx] & 0b1111
        d |= f[idx] >> 4
        print(f"IN r{d},{A:x}")
        return 2
    return 0


def parse_ld(f, idx):
    LDY = 0b1000_0000
    LD = 0b1001_0000
    mask = 0b1111_1110
    if (f[idx] & mask) == LD:
        d = (f[idx] & 0b1) << 4
        idx += 1
        d |= (f[idx] & 0b1111_0000) >> 4

        low = f[idx] & 0b1111
        if low == 12:
            print(f"LD r{d}, X")
        elif low == 13:
            print(f"LD r{d}, X+")
        elif low == 14:
            print(f"LD r{d}, -X")
        elif low == 9:
            print(f"LD r{d}, Y+")
        elif low == 10:
            print(f"LD r{d}, -Y")
        else:
            return 0

        return 2
    if (f[idx] & mask) == LDY:
        d = (f[idx] & 0b1) << 4
        idx += 1
        d |= (f[idx] & 0b1111_0000) >> 4

        low = f[idx] & 0b1111
        if low == 8:
            print("LD r{d}, Y")
            return 2

    return 0


parsing_funcs = [
    parse_bld,
    parse_ldi,
    parse_break,
    parse_adc,
    parse_add,
    parse_adiw,
    parse_and,
    parse_andi,
    parse_asr,
    parse_bclr,
    parse_branch,
    parse_call,
    parse_cbi,
    parse_com,
    parse_cp,
    parse_cpc,
    parse_cpi,
    parse_cpse,
    parse_incdec,
    parse_eor,
    parse_mul,
    parse_icall,
    parse_ijmp,
    parse_jmp,
    parse_in,
    parse_ld,
]


def main() -> int:
    f = open("./data/listing_002.obj", "rb").read().strip()
    length = f[2] << 8
    length |= f[3]

    print(f"length {length} vs {len(f)}")
    idx = 29
    while idx < length:
        flag = False
        for func in parsing_funcs:
            count = func(f, idx)
            if count != 0:
                idx += count + 6  # 6 for crc?
                flag = True
                break
        if not flag:
            print(f[idx])

        idx += 1

    return 0


if __name__ == "__main__":
    exit(main())

# eicall
# eijmp
# des
# lac
# las
