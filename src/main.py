# 00011rdddddrrrr
# 0 <= d,r <= 31, is just between what register we do it
ADC = 0b000111

# 00001rdddddrrrr
# 0 <= d,r <= 31, is just between what register we do it
ADD = 0b000011

# 10010110KKddKKKK
# d \in {24, 26, 28, 30}, 0 <= K <= 63
ADIW = 0b10010110

# 001000rdddddrrrr
# 0 <= d,r <= 31
AND = 0b001000

# 0111KKKKddddKKKK
ANDI = 0b0111

# 1001010ddddd0101
# 0 <= d <= 31
ASR_LOW = 0b1001010
ASR_HIGH = 0b0101

# 100101001sss1000
# 0 <= s <= 7
BCLR_LOW = 0b100101001
BCLR_HIGH = 0b1000

# 1111100ddddd0bbb
# 0 <= d <= 31, 0 <= b <= 7
BLD_LOW = 0b1111100
BLD_HIGH = 0

# 111101kkkkkkksss
# 0 <= 7 -64 <= k <= +63
# BRBC is sss and brcc is 000, brhc is 101, brge is 100, brid is 111, BRNE is 001, BRPL is 010, BRSH 000, BRTC is 110, BRVC 011
BRBC = 0b111101
BRCC = 0b111101
BRHC = 0b111101
BRGE = 0b111101
BRNE = 0b111101
BRPL = 0b111101
BRSH = 0b111101
BRTC = 0b111101
BRVC = 0b111101

# 111100kkkkkkksss
# 0 <= 7 -64 <= k <= +63
# BRBS is sss and BRCS is 000, BREQ is 001, BRHS is 101, BRIE is 1111, BRLO is 000, BRLT is 100, BRMI is 010, BRTS is 110, 011
BRBS = 0b111100
BRCS = 0b111100
BREQ = 0b111100
BRHS = 0b111100
BRIE = 0b111100
BRLO = 0b111100
BRLT = 0b111100
BRMI = 0b111100
BRTS = 0b111100
BRVS = 0b111100

# 100101000sss1000
BSET = 0b100101000
BSET_HIGH = 0b1000

# 1111101ddddd0bbb
# 0 <= d <= 31, 0 <= b <= 7
BST = 0b1111101

# 1001010kkkkk111k
# kkkkkkkkkkkkkkkk
CALL = 0b1001010

# 10011000 AAAA Abbb
CBI = 0b10011000
# 16-bit Opcode: (see ANDI with K complemented)
# CBR = 0b

CLC = 0b1001010010001000
CLH = 0b1001010011011000
CLI = 0b1001010011111000
CLN = 0b1001010010101000
CLS = 0b1001010011001000
CLT = 0b1001010011101000
CLV = 0b1001010010111000
CLZ = 0b1001010010011000

# 1001 010d dddd 0000
COM = 0b1001010

# 0b0001 01rd dddd rrrr
CP = 0b000101

# 0000 01rd dddd rrrr
CPC = 0b000001

# 0011 KKKK dddd KKKK
CPI = 0b0011

# 0001 00rd dddd rrrr
CPSE = 0b000100

# 0b1001 010d dddd 1010
DEC = 0b1001010

# 1001 0100 KKKK 1011
DES = 0b10010100

EICALL = 0b1001010100011001
EIJMP = 0b1001010000011001

# ELPM None, R0 implied
ELPM_0 = 0b1001010111011000
# 1001 000d dddd 0110
# ELPM Rd, Z
ELPM_1 = 0b1001000
# 1001 000d dddd 0111
# ELPM Rd, Z+
ELPM_2 = 0b1001000

# 0010 01dd dddd dddd
CLR = 0b001001

# 0010 01rd dddd rrrr
EOR = 0b001001

# 0000 0011 0ddd 1rrr
FMUL = 0b000000110
# 0000 0011 1ddd 0rrr
FMULS = 0b000000111

# 0000 0011 1ddd 1rrr
FMULSU = 0b000000111

ICALL = 0b1001010100001001

IJMP = 0b1001010000001001

# 1011 0AAd dddd AAAA
IN = 0b10110

# 1001 010d dddd 0011
INC = 0b1001010

# 1001 010k kkkk 110k
# kkkk kkkk kkkk kkkk
JMP = 0b1001010

# 1001 001r rrrr 0110
LAC = 0b1001001

# 1001 001r rrrr 0101
LAS = 0b1001001

# 1001 001r rrrr 0111
LAT = 0b1001001

# 1001 000d dddd 1100
# 1001 000d dddd 1101
# 1001 000d dddd 1110
LD_X = 0b1001000
LD_X_0_HIGH = 0b1100
LD_X_1_HIGH = 0b1101
LD_X_2_HIGH = 0b1110


LD_Y_0_LOW = 0b1000000
LD_Y_0_HIGH = 0b1000
LD_Y_1_LOW = 0b1001000
LD_Y_1_0_HIGH = 0b1101
LD_Y_1_1_HIGH = 0b1110
# 10q0 qq0d dddd 1qqq
LD_Y_2 = 0b10

LD_Z_0_LOW = 0b1000000
LD_Z_0_HIGH = 0b0000
LD_Z_1_LOW = 0b1001000
LD_Z_1_0_HIGH = 0b1001
LD_Z_1_1_HIGH = 0b0010
# 10q0 qq0d dddd 0qqq
LD_Y_2 = 0b10


# 1110 KKKK dddd KKKK
LDI = 0b1110

# 1001 000d dddd 0000 kkkk kkkk kkkk kkkk
LDS_0 = 0b1001000
# 1010 0kkk dddd kkkk
LDS_1 = 0b10100

LPM_0 = 0b1001010111001000
# 1001 000d dddd 0100
# 1001 000d dddd 0101 <- LPM_2
LPM_1 = 0b1001000

# 0000 11dd dddd dddd
LSL = 0b000011

# 1001 010d dddd 0110
LSR = 0b1001010

# 0010 11rd dddd rrrr
MOV = 0b001011

# 0000 0001 dddd rrrr
MOVW = 0b00000001

# 1001 11rd dddd rrrr
MUL = 0b100111

# 0000 0010 dddd rrrr
MULS = 0b00000010

# 0000 0011 0ddd 0rrr
MULSU = 0b000000110

# 1001 010d dddd 0001
NEG = 0b1001010

NOP = 0b0000_0000_0000_0000

# 0010 10rd dddd rrrr
OR = 0b001010

# 0110 KKKK dddd KKKK
ORI = 0b0110

# 1011 1AAr rrrr AAAA
OUT = 0b10111


# 1001 000d dddd 1111
POP = 0b1001000

# 10001 001d dddd 1111
PUSH = 0b1001001

# 1101 kkkk kkkk kkkk
RCALL = 0b1101

RET = 0b1001010100001000
RETI = 0b1001010100011000
# 1100 kkkk kkkk kkkk
RJMP = 0b1100

# 0001 11dd dddd dddd
ROL = 0b000111

# 1001 010d dddd 01111
ROR = 0b1001010

# 0000 10rd dddd rrrr
SBC = 0b000010

# 0100 KKKK dddd KKKK
SBCI = 0b0100

# 1001 1010 AAAA Abbb
SBI = 0b10011010
# 1001 1001 AAAA Abbb
SBIC = 0b10011001

# 1001 1011 AAAA Abbb
SBIS = 0b10011011

# 1001 0111 KKdd KKKK
SBIW = 0b10010111

# 0110 KKKK dddd KKKK
SBR = 0b0110

# 1111 110r rrrr 0bbb
SBRC = 0b1111110

# 1111 111r rrrr 0bbb
SBRS = 0b1111111

SEC = 0b1001010000001000
SEH = 0b1001010001011000
SEI = 0b1001_0100_0111_1000
SEN = 0b1001_0100_0010_1000
# 1110 1111 dddd 1111
SER = 0b1110_1111

SES = 0b1001_0100_0100_1000
SET = 0b1001_0100_0110_1000
SEV = 0b1001_0100_0011_1000
SEZ = 0b1001_0100_0001_1000
SLEEP = 0b1001_0101_1000_1000
SPM_0 = 0b1001_0101_1110_1000
SPM_1 = 0b1001_0101_1110_1000
SPM_1 = 0b1001_0101_1111_1000

ST_X = 0b1001_001
ST_X_HIGH_0 = 0b1100
ST_X_HIGH_1 = 0b1101
ST_X_HIGH_2 = 0b1110

# 1000 001r rrrr 1000
ST_Y_LOW_0 = 0b1000_001

ST_Y_LOW_1_0 = 0b1001_001
ST_Y_HIGH_1_0 = 0b1001
ST_Y_HIGH_1_1 = 0b1010
# 10q0 qq1r rrrr 1qqq
ST_Y_LOW_2_0 = 0b10

# 1000 001r rrrr 0000
ST_Z_LOW_0 = 0b1000_001

ST_Z_LOW_1_0 = 0b1001_001
ST_Z_HIGH_1_0 = 0b0001
ST_Z_HIGH_1_1 = 0b0010
# 10q0 qq1r rrrr 0qqq
ST_Z_LOW_2_0 = 0b10

# 1001 001d dddd 0000 kkkk kkkk kkkk kkkk
STS_32 = 0b1001001
# 1010 1kkk dddd kkkk
STS_16 = 0b10101

# 0001 10rd dddd rrrr
SUB = 0b000110

# 0101 KKKK dddd KKKK
SUBI = 0b0101

# 1001 010d dddd 0010
SWAP = 0b1001010

# 0010 00dd dddd dddd
TST = 0b001000

WDR = 0b1001_0101_1010_1000

# 1001 001r rrrr 0100
XCH = 0b1001_001


BREAK = 0b10010101_10011000


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
    # 1110 KKKK dddd KKKK
    if not match_low_byte(LDI, f[idx]):
        return 0
    return 1


def parse_clr(f, idx) -> int:
    # 0b001 001dd dddd dddd
    CLR = 0b00100100
    mask_clr = 0b11111100

    if f[idx] & mask_clr == CLR:
        high = f[idx] & 0b11
        idx += 1
        reg = (high >> 8) + f[idx]
        print(f"CLR r{reg}")

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
    ASR_LOW = 0b1001010_0
    ASR_HIGH = 0b0101
    mask = 0b1001010_0
    if f[idx] & mask == ASR_LOW:
        d = (f[idx] & 0b1) << 4
        idx += 1
        if f[idx] & 0b1111 == ASR_HIGH:
            d |= f[idx] >> 4
            print(f"ASR r{d}")

    return 0


def parse_bclr(f, idx) -> int:
    BCLR_LOW = 0b1001_0100
    BCLR_HIGH = 0b1000
    if f[idx] == BCLR_LOW:
        idx += 1
        print("BCLR ?")

        if f[idx] & 0b1000_0000 != 0 and f[idx] & 0b1111 == BCLR_HIGH:
            s = (f[idx] & 0b0111_0000) >> 4
            print(f"BCLR {s}")

    return 0


def parse_bld(f, idx) -> int:
    BLD_LOW = 0b1111_1000
    mask = 0b1111_1000

    print(bin(f[idx]), bin(f[idx] & mask))

    if (f[idx] & mask) == BLD_LOW:
        d = (f[idx] & 1) << 7
        idx += 1
        print("GOT")
        if (f[idx] & 0b0000_1000) == 0:
            d |= (f[idx] & 0b11110000) >> 1
            b = f[idx] & 0b111
            print(f"BLD r{d},{b}")
            return 2
    return 0


parsing_funcs = [
    parse_bld,
    parse_ldi,
    parse_break,
    parse_clr,
    parse_adc,
    parse_add,
    parse_adiw,
    parse_and,
    parse_andi,
    parse_asr,
    parse_bclr,
]


def main() -> int:
    f = open("./data/listing_002.obj", "rb").read().strip()
    length = f[3]
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
