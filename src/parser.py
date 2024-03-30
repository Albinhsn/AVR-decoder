from typing import List, Optional, Tuple

from instruction import *


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


def parse_adc(f, idx) -> Tuple[int, Optional[Instruction]]:
    ADC = 0b00011100
    mask = 0b11111100

    if (mask & f[idx]) == ADC:
        d, r = parse_ops(f, idx)
        i: Instruction = Instruction(InstructionCode.ADC, d, r)
        return 2, i

    return 0, None


def parse_break(f, idx) -> Tuple[int, Optional[Instruction]]:
    size = 2
    BREAK = 0b10010101_10011000

    # 1110 KKKK dddd KKKK
    while size != 0 and match_low_byte(BREAK >> ((size - 1) * 8), f[idx]):
        size -= 1
        idx += 1

    if size == 0:
        return 2, Instruction(InstructionCode.BREAK)
    return 0, None


def parse_ldi(f, idx) -> Tuple[int, Optional[Instruction]]:
    LDI = 0b1110
    if (f[idx] >> 4) != LDI:
        return 0, None

    K = (f[idx] & 0b1111) << 4
    idx += 1
    K |= f[idx] & 0b1111
    d = (f[idx] & 0b1111) << 4
    return 2, Instruction(InstructionCode.LDI, d, K)


def parse_ijmp(f, idx) -> Tuple[int, Optional[Instruction]]:
    IJMP_HIGH = 0b1001_0100
    IJMP_LOW = 0b0000_1001
    if f[idx] == IJMP_HIGH and f[idx + 1] == IJMP_LOW:
        return 2, Instruction(InstructionCode.IJMP)
    return 0, None


def parse_jmp(f, idx) -> Tuple[int, Optional[Instruction]]:
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
            return 11, Instruction(InstructionCode.JMP, k)

    return 0, None


def parse_icall(f, idx) -> Tuple[int, Optional[Instruction]]:
    ICALL_HIGH = 0b1001_0101
    ICALL_LOW = 0b0000_1001
    if f[idx] == ICALL_HIGH and f[idx + 1] == ICALL_LOW:
        return 2, Instruction(InstructionCode.ICALL)
    return 0, None


def parse_mul(f, idx) -> Tuple[int, Optional[Instruction]]:
    FMUL = 0b0000_0011
    MUL = 0b1001_1100
    mask_mul = 0b1111_1100
    MULS = 0b0000_0010

    if f[idx] == FMUL:
        idx += 1
        high = f[idx] & 0b1000_0000
        low = f[idx] & 0b1000
        d = (f[idx] & 0b0111_0000) >> 4
        r = f[idx] & 0b111
        i = Instruction(InstructionCode.MUL, d, r)
        if high == 0 and low != 0:
            i.code = InstructionCode.FMUL
        elif high != 0 and low == 0:
            i.code = InstructionCode.FMULS
        elif high != 0 and low != 0:
            i.code = InstructionCode.FMULSU
        elif high == 0 and low == 0:
            i.code = InstructionCode.MULSU

        return 2, i

    elif (f[idx] & mask_mul) == MUL:
        d, r = parse_ops(f, idx)
        return 2, Instruction(InstructionCode.MUL, d, r)
    elif f[idx] == MULS:
        idx += 1
        d = f[idx] >> 4
        r = f[idx] & 0b1111
        return 2, Instruction(InstructionCode.MULS, d, r)

    return 0, None


def parse_neg(f, idx) -> Tuple[int, Optional[Instruction]]:
    NEG = 0b1001_0100
    mask = 0b1111_1110

    if (f[idx] & mask) == NEG:
        d = (f[idx] & 0b1) << 4
        idx += 1
        if (f[idx] & 0b1111) == 0b0001:
            d |= f[idx] >> 4
            return 2, Instruction(InstructionCode.NEG, d)

    return 0, None


def parse_add(f, idx) -> Tuple[int, Optional[Instruction]]:
    ADD = 0b000011_00
    mask = 0b111111_00

    if f[idx] & mask == ADD:
        d, r = parse_ops(f, idx)
        i: Instruction = Instruction(InstructionCode.ADD, d, r)
        return 2, i
    return 0, None


def parse_adiw(f, idx) -> Tuple[int, Optional[Instruction]]:
    REG_TABLE = [24, 26, 28, 30]
    ADIW = 0b10010110
    if f[idx] == ADIW:
        idx += 1
        d = (f[idx] & 0b00110000) >> 4

        K = (f[idx] & 0b1100_0000) >> 2
        K |= f[idx] & 0b1111

        return 2, Instruction(InstructionCode.ADIW, REG_TABLE[d], K)

    return 0, None


def parse_and(f, idx) -> Tuple[int, Optional[Instruction]]:
    AND = 0b001000_00
    mask = 0b111111_00

    if f[idx] & mask == AND:
        d, r = parse_ops(f, idx)

        return 2, Instruction(InstructionCode.AND, d, r)
    return 0, None


def parse_andi(f, idx) -> Tuple[int, Optional[Instruction]]:
    ANDI = 0b0111_0000
    mask = 0b1111_0000

    if f[idx] & mask == ANDI:
        K = (f[idx] & 0b1111) << 4
        idx += 1
        K |= f[idx] & 0b1111
        d = 16 + ((f[idx] & 0b11110000) >> 4)

        return 2, Instruction(InstructionCode.ANDI, d, K)
    return 0, None


def parse_asr(f, idx) -> Tuple[int, Optional[Instruction]]:
    ASR_LOW = 0b1001_0100
    ASR_HIGH = 0b0101
    mask = 0b1001010_0
    if f[idx] & mask == ASR_LOW:
        d = (f[idx] & 0b1) << 4
        idx += 1
        if f[idx] & 0b1111 == ASR_HIGH:
            d |= f[idx] >> 4
            return 2, Instruction(InstructionCode.ASR, d)

    return 0, None


def parse_call(f, idx) -> Tuple[int, Optional[Instruction]]:
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
            # Need to somehow parse an additional 8 bytes?

            return 11, Instruction(InstructionCode.CALL, k)

    return 0, None


# ToDo wtf :)
def parse_cbr(f, idx) -> Tuple[int, Optional[Instruction]]:
    return 0, None


def parse_cbi(f, idx) -> Tuple[int, Optional[Instruction]]:
    CBI = 0b1001_1000
    if f[idx] == CBI:
        idx += 1

        A = (f[idx] & 0b1111_1000) >> 3
        b = f[idx] & 0b111

        return 2, Instruction(InstructionCode.CBI, A, b)

    return 0, None


def parse_bst(f, idx) -> Tuple[int, Optional[Instruction]]:
    BST = 0b11111010
    if f[idx] == BST:
        d = f[idx] & 1 << 4
        idx += 1
        if (f[idx] & 0b1000) != 0:
            d |= f[idx] >> 4
            b = f[idx] & 0b111

            return 2, Instruction(InstructionCode.BST, d, b)

    return 0, None


def parse_bset(f, idx) -> Tuple[int, Optional[Instruction]]:
    BSET_LOW = 0b1001_0100
    BSET_HIGH = 0b1000
    if f[idx] == BSET_LOW:
        idx += 1

        if (f[idx] & 0b1000_0000) == 0 and (f[idx] & 0b1111) == BSET_HIGH:
            s = (f[idx] & 0b0111_0000) >> 4
            return 2, Instruction(InstructionCode.BSET, s)

    return 0, None


def parse_cpi(f, idx) -> Tuple[int, Optional[Instruction]]:
    CPI = 0b0011_0000
    mask = 0b1111_0000

    if (f[idx] & mask) == CPI:
        K = (f[idx] & 0b1111) << 4
        idx += 1

        d = (f[idx] & 0b1111_0000) >> 4
        K |= f[idx] & 0b1111
        return 2, Instruction(InstructionCode.CPI, d, K)
    return 0, None


def parse_cpc(f, idx) -> Tuple[int, Optional[Instruction]]:
    CPC = 0b0000_0100
    mask = 0b1111_1100
    if f[idx] & mask == CPC:
        d, r = parse_ops(f, idx)
        return 2, Instruction(InstructionCode.CPC, d, r)
    return 0, None


def parse_cp(f, idx) -> Tuple[int, Optional[Instruction]]:
    CP = 0b0001_0100
    mask = 0b1111_1100
    if f[idx] & mask == CP:
        d, r = parse_ops(f, idx)
        return 2, Instruction(InstructionCode.CP, d, r)
    return 0, None


def parse_incdec(f, idx) -> Tuple[int, Optional[Instruction]]:
    HIGH = 0b1001_0100
    mask = 0b1111_1110

    if (f[idx] & mask) == HIGH:
        d = (f[idx] & 1) << 4
        idx += 1
        d |= (f[idx] & 0b11110000) >> 4
        LOW = f[idx] & 0b1111
        if LOW == 0b1010:
            return 2, Instruction(InstructionCode.DEC, d)
        elif LOW == 0b0011:
            return 2, Instruction(InstructionCode.INC, d)
    return 0, None


def parse_com(f, idx) -> Tuple[int, Optional[Instruction]]:
    COM = 0b1001_0100
    mask = 0b1111_1110

    if (f[idx] & mask) == COM:
        d = (f[idx] & 1) << 4
        idx += 1
        if (f[idx] & 0b1111) == 0:
            d |= (f[idx] & 0b1111_0000) >> 4
            return 2, Instruction(InstructionCode.COM, d)
    return 0, None


def parse_bclr(f, idx) -> Tuple[int, Optional[Instruction]]:
    BCLR_LOW = 0b1001_0100
    BCLR_HIGH = 0b1000
    if f[idx] == BCLR_LOW:
        idx += 1

        if f[idx] & 0b1000_0000 != 0 and (f[idx] & 0b1111) == BCLR_HIGH:
            s = (f[idx] & 0b0111_0000) >> 4
            i = Instruction(InstructionCode.ADD, s)
            if s == 0:
                i.code = InstructionCode.CLC
            if s == 1:
                i.code = InstructionCode.CLZ
            elif s == 2:
                i.code = InstructionCode.CLN
            elif s == 3:
                i.code = InstructionCode.CLV
            elif s == 4:
                i.code = InstructionCode.CLS
            elif s == 5:
                i.code = InstructionCode.CLH
            elif s == 6:
                i.code = InstructionCode.CLT
            elif s == 7:
                i.code = InstructionCode.CLI
            else:
                i.code = InstructionCode.BCLR
            return 2, i
    return 0, None


def parse_bld(f, idx) -> Tuple[int, Optional[Instruction]]:
    BLD_LOW = 0b1111_1000
    mask = 0b1111_1110

    if (f[idx] & mask) == BLD_LOW:
        d = (f[idx] & 1) << 7
        idx += 1
        if (f[idx] & 0b0000_1000) == 0:
            d |= (f[idx] & 0b11110000) >> 4
            b = f[idx] & 0b111
            return 2, Instruction(InstructionCode.BLD, d, b)
    return 0, None


def parse_branch(f, idx) -> Tuple[int, Optional[Instruction]]:
    BR0 = 0b1111_0100
    mask = 0b1111_1100
    BR0_TABLE = [
        ("BRCC/BRSH", InstructionCode.BRCC),
        ("BRNE", InstructionCode.BRNE),
        ("BRPL", InstructionCode.BRPL),
        ("BRVC", InstructionCode.BRVC),
        ("BRGE", InstructionCode.BRGE),
        ("BRHC", InstructionCode.BRHC),
        ("BRTC", InstructionCode.BRTC),
        ("BRID", InstructionCode.BRID),
    ]

    BR1 = 0b1111_0000
    BR1_TABLE = [
        ("BRCS/BRLO", InstructionCode.BRCS),
        ("BREQ", InstructionCode.BREQ),
        ("BRMI", InstructionCode.BRMI),
        ("BRVS", InstructionCode.BRVS),
        ("BRLT", InstructionCode.BRLT),
        ("BRHS", InstructionCode.BRHS),
        ("BRTS", InstructionCode.BRTS),
        ("BRIE", InstructionCode.BRIE),
    ]

    if (f[idx] & mask) == BR0:
        k = (f[idx] & 0b11) << 5
        idx += 1

        s = f[idx] & 0b111
        k |= (f[idx] & 0b11111000) >> 3
        # BRCC
        return 2, Instruction(BR0_TABLE[s][1], k)
    if (f[idx] & mask) == BR1:
        k = (f[idx] & 0b11) << 5
        idx += 1
        k |= (f[idx] & 0b11111000) >> 3

        s = f[idx] & 0b111
        return 2, Instruction(BR1_TABLE[s][1], k)
    return 0, None


def parse_cpse(f, idx) -> Tuple[int, Optional[Instruction]]:
    CPSE = 0b0001_0000
    mask = 0b11111100
    if (f[idx] & mask) == CPSE:
        d, r = parse_ops(f, idx)

        return 2, Instruction(InstructionCode.CPSE, d, r)
    return 0, None


def parse_eor(f, idx) -> Tuple[int, Optional[Instruction]]:
    EOR = 0b0010_0100
    mask = 0b1111_1100
    if (f[idx] & mask) == EOR:
        d, r = parse_ops(f, idx)
        return 2, Instruction(InstructionCode.EOR, d, r)
    return 0, None


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
        return 2, Instruction(InstructionCode.IN, d, A)
    return 0, None


def parse_ld(f, idx):
    LDY = 0b1000_0000
    LD = 0b1001_0000
    mask = 0b1111_1110
    if (f[idx] & mask) == LD:
        d = (f[idx] & 0b1) << 4
        idx += 1
        d |= (f[idx] & 0b1111_0000) >> 4

        low = f[idx] & 0b1111

        i = Instruction(LD, d)
        if low == 12:
            i.op2 = Reg16.X
        elif low == 13:
            i.op2 = Reg16.X_PLUS
        elif low == 14:
            i.op2 = Reg16.X_MINUS
        elif low == 9:
            i.op2 = Reg16.Y_PLUS
        elif low == 10:
            i.op2 = Reg16.Y_MINUS
        elif low == 1:
            i.op2 = Reg16.Z_PLUS
        elif low == 2:
            i.op2 = Reg16.Z_MINUS
        else:
            return 0, None
        return 2, i
    elif (f[idx] & mask) == LDY:
        d = (f[idx] & 0b1) << 4
        idx += 1
        d |= (f[idx] & 0b1111_0000) >> 4

        low = f[idx] & 0b1111
        i = Instruction(InstructionCode.LD, d)
        if low == 0:
            i.op2 = Reg16.Z
        elif low == 8:
            i.op2 = Reg16.Y
        return 2, i
    else:
        LD_O = 0b1000_0000
        mask = 0b1101_0010

        if (f[idx] & mask) == LD_O:
            q = f[idx] & 0b10_0000
            q |= (f[idx] & 0b1100) << 1
            d = (f[idx] & 0b1) << 4
            idx += 1
            d |= f[idx] & 0b1111_0000
            q |= f[idx] & 0b111

            i = Instruction(InstructionCode.LDD, d, None, q)
            if f[idx] & 0b1000 != 0:
                i.op2 = Reg16.Y_PLUS
            else:
                i.op2 = Reg16.Z_PLUS
            return 2, i
    return 0, None


def parse_lpm(f, idx) -> Tuple[int, Optional[Instruction]]:
    LPM = 0b1001_0000
    mask = 0b1111_1110
    if f[idx] == 0b1001_0101 and f[idx + 1] == 0b1100_1000:
        return 2, Instruction(InstructionCode.LPM)
    elif (f[idx] & mask) == LPM:
        d = (f[idx] & 0b1) << 4
        idx += 1
        d |= (f[idx] & 0b1111_0000) >> 4

        i = Instruction(InstructionCode.LPM, d)
        if (f[idx] & 0b1111) == 0b0100:
            i.op2 = Reg16.Z
        elif (f[idx] & 0b1111) == 0b0101:
            i.op2 = Reg16.Z_PLUS
        else:
            return 0, None
        return 2, i
    return 0, None


def parse_lds(f, idx) -> Tuple[int, Optional[Instruction]]:
    LDS = 0b1001_0000
    mask = 0b1111_1110
    LDS_16 = 0b1010_0000
    mask_16 = 0b1111_1000

    if (f[idx] & mask) == LDS:
        d = (f[idx] & 0b1) << 4
        idx += 1
        if (f[idx] & 0b1111) == 0:
            d |= (f[idx] & 0b1111_000) >> 4
            idx += 1
            k = (f[idx] << 8) | f[idx + 1]
            return 11, Instruction(InstructionCode.LDS, d, k)
    elif (f[idx] & mask_16) == LDS_16:
        k = (f[idx] & 0b111) << 4
        idx += 1
        k |= f[idx] & 0b1111
        d = (f[idx] & 0b1111_0000) >> 4
        return 2, Instruction(InstructionCode.LDS, d, k)
    return 0, None


def parse_lsr(f, idx) -> Tuple[int, Optional[Instruction]]:
    LSR = 0b1001_0100
    mask = 0b1111_1110

    if (f[idx] & mask) == LSR:
        d = (f[idx] & 0b1) << 4
        idx += 1
        if (f[idx] & 0b1111) == 0b0110:
            d |= (f[idx] & 0b1111_0000) >> 4
            return 2, Instruction(InstructionCode.LSR, d)
    return 0, None


def parse_mov(f, idx) -> Tuple[int, Optional[Instruction]]:
    MOV = 0b0010_1100
    mask = 0b1111_1100

    if (f[idx] & mask) == MOV:
        d, r = parse_ops(f, idx)
        return 2, Instruction(InstructionCode.MOV, d, r)
    return 0, None


def parse_movw(f, idx) -> Tuple[int, Optional[Instruction]]:
    MOVW = 0b0000_0001

    if f[idx] == MOVW:
        idx += 1
        d = f[idx] >> 4
        r = f[idx] & 0b1111

        return 2, Instruction(InstructionCode.MOVW, 2 * d, 2 * r)
    return 0, None


def parse_noop(f, idx) -> Tuple[int, Optional[Instruction]]:
    if f[idx] == 0 and f[idx + 1] == 0:
        return 2, Instruction(InstructionCode.NOP)
    return 0, None


def parse_or(f, idx) -> Tuple[int, Optional[Instruction]]:
    OR = 0b0010_1000
    mask = 0b1111_1100

    if (f[idx] & mask) == OR:
        d, r = parse_ops(f, idx)
        return 2, Instruction(InstructionCode.OR, d, r)
    return 0, None


def parse_ori(f, idx) -> Tuple[int, Optional[Instruction]]:
    if (f[idx] >> 4) == 0b0110:
        K = (f[idx] & 0b1111) << 4
        idx += 1
        K |= f[idx] & 0b1111
        d = f[idx] >> 4

        return 2, Instruction(InstructionCode.ORI, d, K)
    return 0, None


def parse_out(f, idx) -> Tuple[int, Optional[Instruction]]:
    OUT = 0b1011_1000
    mask = 0b1111_1000

    if (f[idx] & mask) == OUT:
        A = (f[idx] & 0b110) << 3
        r = (f[idx] & 0b1) << 4
        idx += 1

        r |= f[idx] >> 4
        A |= f[idx] & 0b1111
        return 2, Instruction(InstructionCode.OUT, A, r)
    return 0, None


def parse_pop(f, idx) -> Tuple[int, Optional[Instruction]]:
    POP = 0b1001_0000
    mask = 0b1111_1110

    if (f[idx] & mask) == POP:
        d = (f[idx] & 0b1) << 4
        idx += 1
        if f[idx] & 0b1111 == 0b1111:
            d |= f[idx] >> 4
            return 2, Instruction(InstructionCode.POP, d)
    return 0, None


def parse_push(f, idx) -> Tuple[int, Optional[Instruction]]:
    PUSH = 0b1001_0010
    mask = 0b1111_1110

    if (f[idx] & mask) == PUSH:
        d = (f[idx] & 0b1) << 4
        idx += 1
        if f[idx] & 0b1111 == 0b1111:
            d |= f[idx] >> 4
            return 2, Instruction(InstructionCode.PUSH, d)
    return 0, None


def parse_rcall(f, idx) -> Tuple[int, Optional[Instruction]]:
    RCALL = 0b1101

    if f[idx] >> 4 == RCALL:
        k = (f[idx] & 0b1111) << 8
        k |= f[idx + 1]

        return 2, Instruction(InstructionCode.RCALL, k)
    return 0, None


def parse_ret(f, idx) -> Tuple[int, Optional[Instruction]]:
    if f[idx] == 0b1001_0101 and f[idx + 1] == 0b0000_1000:
        return 2, Instruction(InstructionCode.RET)
    return 0, None


def parse_reti(f, idx) -> Tuple[int, Optional[Instruction]]:
    if f[idx] == 0b1001_0101 and f[idx + 1] == 0b0001_1000:
        return 2, Instruction(InstructionCode.RETI)
    return 0, None


def parse_rjmp(f, idx) -> Tuple[int, Optional[Instruction]]:
    if f[idx] >> 4 == 0b1100:
        k = ((f[idx] & 0b1111) << 8) | f[idx + 1]
        return 2, Instruction(InstructionCode.RJMP, k)
    return 0, None


def parse_ror(f, idx) -> Tuple[int, Optional[Instruction]]:
    ROR = 0b1001_0100
    mask = 0b1111_1110

    if (f[idx] & mask) == ROR:
        d = (f[idx] & 0b1) << 4
        idx += 1
        d |= f[idx] >> 4
        if f[idx] & 0b1111 == 0b0111:
            return 2, Instruction(InstructionCode.ROR, d)
    return 0, None


def parse_sbc(f, idx) -> Tuple[int, Optional[Instruction]]:
    SBC = 0b0000_1000
    mask = 0b1111_1100

    if (f[idx] & mask) == SBC:
        d, r = parse_ops(f, idx)
        return 2, Instruction(InstructionCode.SBC, d, r)
    return 0, None


def parse_sbci(f, idx) -> Tuple[int, Optional[Instruction]]:
    if (f[idx] >> 4) == 0b0100:
        K = (f[idx] & 0b1111) << 4
        idx += 1
        d = f[idx] >> 4
        K |= f[idx] & 0b1111
        return 2, Instruction(InstructionCode.SBCI, d + 16, K)
    return 0, None


def parse_sbi(f, idx) -> Tuple[int, Optional[Instruction]]:
    if f[idx] == 0b1001_1010:
        idx += 1
        A = f[idx] >> 3
        b = f[idx] & 0b111
        return 2, Instruction(InstructionCode.SBI, A, b)
    return 0, None


def parse_sbic(f, idx) -> Tuple[int, Optional[Instruction]]:
    if f[idx] == 0b1001_1001:
        idx += 1
        A = f[idx] >> 3
        b = f[idx] & 0b111

        return 2, Instruction(InstructionCode.SBIC, A, b)
    return 0, None


def parse_sbis(f, idx) -> Tuple[int, Optional[Instruction]]:
    if f[idx] == 0b1001_1011:
        idx += 1
        A = f[idx] >> 3
        b = f[idx] & 0b111

        return 2, Instruction(InstructionCode.SBIS, A, b)
    return 0, None


def parse_sbiw(f, idx) -> Tuple[int, Optional[Instruction]]:
    TABLE = [24, 26, 28, 30]
    if f[idx] == 0b1001_0111:
        idx += 1
        K = (f[idx] >> 6) << 4
        K |= f[idx] & 0b1111
        d = f[idx] >> 4
        return 2, Instruction(InstructionCode.SBIW, TABLE[d + 1], TABLE[d], K)
    return 0, None


def parse_sbrs(f, idx) -> Tuple[int, Optional[Instruction]]:
    SBRS = 0b1111_1110
    mask = 0b1111_1110

    if (f[idx] & mask) == SBRS:
        r = (f[idx] & 0b1) << 4
        idx += 1
        if (f[idx] & 0b1000) == 0:
            r |= f[idx] >> 4
            b = f[idx] & 0b111
            return 2, Instruction(InstructionCode.SBRS, r, b)
    return 0, None


def parse_sbrc(f, idx) -> Tuple[int, Optional[Instruction]]:
    SBRC = 0b1111_1100
    mask = 0b1111_1110

    if (f[idx] & mask) == SBRC:
        r = (f[idx] & 0b1) << 4
        idx += 1
        if (f[idx] & 0b1000) == 0:
            r |= f[idx] >> 4
            b = f[idx] & 0b111
            return 2, Instruction(InstructionCode.SBRC, r, b)
    return 0, None


def parse_sec(f, idx) -> Tuple[int, Optional[Instruction]]:
    if f[idx] == 0b1001_0100 and f[idx + 1] == 0b0000_1000:
        return 2, Instruction(InstructionCode.SEC)
    return 0, None


def parse_seh(f, idx) -> Tuple[int, Optional[Instruction]]:
    if f[idx] == 0b1001_0100 and f[idx + 1] == 0b0101_1000:
        return 2, Instruction(InstructionCode.SEH)
    return 0, None


def parse_sei(f, idx) -> Tuple[int, Optional[Instruction]]:
    if f[idx] == 0b1001_0100 and f[idx + 1] == 0b0111_1000:
        return 2, Instruction(InstructionCode.SEI)
    return 0, None


def parse_sen(f, idx) -> Tuple[int, Optional[Instruction]]:
    if f[idx] == 0b1001_0100 and f[idx + 1] == 0b0010_1000:
        return 2, Instruction(InstructionCode.SEN)
    return 0, None


def parse_ser(f, idx) -> Tuple[int, Optional[Instruction]]:
    if f[idx] == 0b1110_1111:
        idx += 1
        if (f[idx] & 0b1111) == 0b1111:
            d = f[idx] >> 4
            return 2, Instruction(InstructionCode.SER, d + 16)
    return 0, None


def parse_ses(f, idx) -> Tuple[int, Optional[Instruction]]:
    if f[idx] == 0b1001_0100 and f[idx + 1] == 0b0100_1000:
        return 2, Instruction(InstructionCode.SES)
    return 0, None


def parse_set(f, idx) -> Tuple[int, Optional[Instruction]]:
    if f[idx] == 0b1001_0100 and f[idx + 1] == 0b0110_1000:
        return 2, Instruction(InstructionCode.SET)
    return 0, None


def parse_sev(f, idx) -> Tuple[int, Optional[Instruction]]:
    if f[idx] == 0b1001_0100 and f[idx + 1] == 0b0011_1000:
        return 2, Instruction(InstructionCode.SEV)
    return 0, None


def parse_sleep(f, idx) -> Tuple[int, Optional[Instruction]]:
    if f[idx] == 0b1001_0101 and f[idx + 1] == 0b1000_1000:
        return 2, Instruction(InstructionCode.SLEEP)
    return 0, None


def parse_sez(f, idx) -> Tuple[int, Optional[Instruction]]:
    if f[idx] == 0b1001_0100 and f[idx + 1] == 0b0001_1000:
        return 2, Instruction(InstructionCode.SEZ)
    return 0, None


def parse_spm(f, idx) -> Tuple[int, Optional[Instruction]]:
    if f[idx] == 0b1001_0101 and f[idx + 1] == 0b1110_1000:
        ...
    elif f[idx] == 0b1001_0101 and f[idx + 1] == 0b1111_1000:
        ...
    else:
        return 0, None
    return 2, Instruction(InstructionCode.SPM)


def parse_st(f, idx) -> Tuple[int, Optional[Instruction]]:
    offset = 0b1000_0010
    mask = 0b1101_0010
    if f[idx] >> 1 == 0b1000_001:
        r = (f[idx] & 0b1) << 4
        idx += 1
        r |= f[idx] >> 4
        x = f[idx] & 0b1111
        if x == 0b1000:
            return 2, Instruction(InstructionCode.ST, Reg16.Y, r)
        elif x == 0:
            return 2, Instruction(InstructionCode.ST, Reg16.Z, r)
        idx -= 1

    if f[idx] >> 1 == 0b1001_001:
        r = (f[idx] & 0b1) << 4
        idx += 1
        r |= f[idx] >> 4

        x = f[idx] & 0b1111
        if x == 0b1100:
            return 2, Instruction(InstructionCode.ST, Reg16.X, r)
        elif x == 0b1101:
            return 2, Instruction(InstructionCode.ST, Reg16.X_PLUS, r)
        elif x == 0b1110:
            return 2, Instruction(InstructionCode.ST, Reg16.X_MINUS, r)
        elif x == 0b1001:
            return 2, Instruction(InstructionCode.ST, Reg16.Y_PLUS, r)
        elif x == 0b1010:
            return 2, Instruction(InstructionCode.ST, Reg16.Y_MINUS, r)
        elif x == 0b1:
            return 2, Instruction(InstructionCode.ST, Reg16.Z_PLUS, r)
        elif x == 0b10:
            return 2, Instruction(InstructionCode.ST, Reg16.Z_MINUS, r)
        idx -= 1

    if (f[idx] & mask) == offset:
        q = ((f[idx] >> 5) & 0b1) << 5
        q |= ((f[idx] >> 2) & 0b11) << 3

        r = (f[idx] & 0b1) << 4

        idx += 1
        r |= f[idx] >> 4
        q |= f[idx] & 0b111
        i = Instruction(InstructionCode.STD, None, q, r)
        if f[idx] & 0b1000 == 0:
            i.op1 = Reg16.Z_PLUS
        else:
            i.op1 = Reg16.Y_PLUS

        return 2, i
    return 0, None


def parse_sts(f, idx) -> Tuple[int, Optional[Instruction]]:
    STS = 0b1001_0010
    STS_16 = 0b1010_1000
    mask = 0b1111_1110

    if (f[idx] & mask) == STS:
        d = f[idx] & 0b1
        idx += 1
        d |= f[idx] >> 4
        if (f[idx] & 0b1111) == 0:
            idx += 1
            k = (f[idx] << 8) | f[idx + 1]

            return 11, Instruction(InstructionCode.STS, k, d)
    elif (f[idx] & mask) == STS_16:
        k = (f[idx] & 0b111) << 4
        idx += 1
        d = f[idx] >> 4
        k |= f[idx] & 0b1111
        return 2, Instruction(InstructionCode.STS, k, d)
    return 0, None


def parse_subi(f, idx) -> Tuple[int, Optional[Instruction]]:
    SUBI = 0b0101_0000
    mask = 0b1111_0000
    if (f[idx] & mask) == SUBI:
        K = (f[idx] & 0b1111) << 4
        idx += 1
        d = f[idx] >> 4
        K |= f[idx] & 0b1111
        return 2, Instruction(InstructionCode.SUBI, d + 16, K)
    return 0, None


def parse_sub(f, idx) -> Tuple[int, Optional[Instruction]]:
    SUB = 0b0001_1000
    mask = 0b1111_1100
    if (f[idx] & mask) == SUB:
        d, r = parse_ops(f, idx)
        return 2, Instruction(InstructionCode.SUB, d, r)
    return 0, None


def parse_swap(f, idx) -> Tuple[int, Optional[Instruction]]:
    SWAP = 0b1001_0100
    mask = 0b1111_1110
    if (f[idx] & mask) == SWAP:
        d = (f[idx] & 0b1) << 4
        idx += 1
        d |= f[idx] >> 4

        if f[idx] & 0b1111 == 0b0010:
            return 2, Instruction(InstructionCode.SWAP, d)
    return 0, None


def parse_wdr(f, idx) -> Tuple[int, Optional[Instruction]]:
    if f[idx] == 0b1001_0101 and f[idx + 1] == 0b1010_1000:
        return 2, Instruction(InstructionCode.WDR)
    return 0, None


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
    parse_lds,
    parse_lpm,
    parse_lsr,
    parse_mov,
    parse_movw,
    parse_neg,
    parse_noop,
    parse_or,
    parse_ori,
    parse_out,
    parse_pop,
    parse_push,
    parse_rcall,
    parse_ret,
    parse_reti,
    parse_rjmp,
    parse_ror,
    parse_sbc,
    parse_sbci,
    parse_sbi,
    parse_sbic,
    parse_sbis,
    parse_sbiw,
    parse_sbrc,
    parse_sbrs,
    parse_sec,
    parse_seh,
    parse_ser,
    parse_ses,
    parse_set,
    parse_sleep,
    parse_spm,
    parse_st,
    parse_sts,
    parse_sub,
    parse_subi,
    parse_swap,
    parse_wdr,
]


def parse_instructions(f) -> List[Instruction]:
    length = 0
    for i in range(4):
        length = (length << 8) | f[i]

    instructions: List[Instruction] = []

    print(f"length {length} vs {len(f)}")
    idx = 29
    while idx < length:
        flag = False
        for func in parsing_funcs:
            count, instruction = func(f, idx)
            if count != 0:
                idx += count + 6  # 6 for crc?
                flag = True
                instructions.append(instruction)
                break
        if not flag:
            print(f"FOUND UNKNOWN INSTRUCTION {f[idx]}")

        idx += 1
    return instructions
