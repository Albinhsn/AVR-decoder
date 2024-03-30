from enum import Enum, auto


class InstructionCode(Enum):
    ADC = auto()
    ADD = auto()
    BREAK = auto()
    LDI = auto()
    IJMP = auto()
    JMP = auto()
    ICALL = auto()
    FMUL = auto()
    FMULS = auto()
    FMULSU = auto()
    MUL = auto()
    MULS = auto()
    MULSU = auto()
    NEG = auto()
    ADIW = auto()
    AND = auto()
    ANDI = auto()
    ASR = auto()
    CALL = auto()
    CBI = auto()
    BST = auto()
    BSET = auto()
    CPI = auto()
    CPC = auto()
    CP = auto()
    DEC = auto()
    INC = auto()
    COM = auto()
    CLC = auto()
    CLZ = auto()
    CLN = auto()
    CLV = auto()
    CLS = auto()
    CLH = auto()
    CLT = auto()
    CLI = auto()
    BCLR = auto()
    BLD = auto()
    BRCC = auto()
    BRNE = auto()
    BRPL = auto()
    BRVC = auto()
    BRGE = auto()
    BRHC = auto()
    BRTC = auto()
    BRID = auto()
    BRCS = auto()
    BREQ = auto()
    BRMI = auto()
    BRVS = auto()
    BRLT = auto()
    BRHS = auto()
    BRTS = auto()
    BRIE = auto()
    CPSE = auto()
    EOR = auto()
    IN = auto()
    LD = auto()
    LDD = auto()
    LPM = auto()
    LDS = auto()
    LSR = auto()
    MOV = auto()
    MOVW = auto()
    NOP = auto()
    OR = auto()
    ORI = auto()
    OUT = auto()
    POP = auto()
    PUSH = auto()
    RCALL = auto()
    RET = auto()
    RETI = auto()
    RJMP = auto()
    ROR = auto()
    SBC = auto()
    SBCI = auto()
    SBI = auto()
    SBIC = auto()
    SBIS = auto()
    SBIW = auto()
    SBRS = auto()
    SBRC = auto()
    SEC = auto()
    SEH = auto()
    SEI = auto()
    SEN = auto()
    SER = auto()
    SES = auto()
    SET = auto()
    SEV = auto()
    SLEEP = auto()
    SEZ = auto()
    SPM = auto()
    ST = auto()
    STD = auto()
    STS = auto()
    SUB = auto()
    SUBI = auto()
    SWAP = auto()
    WDR = auto()


class Reg16(Enum):
    X = auto()
    X_MINUS = auto()
    X_PLUS = auto()
    Y = auto()
    Y_MINUS = auto()
    Y_PLUS = auto()
    Y_OFFSET = auto()
    Z = auto()
    Z_MINUS = auto()
    Z_PLUS = auto()
    Z_OFFSET = auto()


def debug_reg(x):
    match x:
        case Reg16.X:
            return "X"
        case Reg16.X_MINUS:
            return "-X"
        case Reg16.X_PLUS:
            return "X+"
        case Reg16.Y:
            return "Y"
        case Reg16.Y_MINUS:
            return "-Y"
        case Reg16.Y_PLUS:
            return "Y+"
        case Reg16.Y_OFFSET:
            return "Y+"
        case Reg16.Z:
            return "Z"
        case Reg16.Z_MINUS:
            return "-Z"
        case Reg16.Z_PLUS:
            return "Z+"
        case Reg16.Z_OFFSET:
            return "Z+"


class Instruction:
    def __init__(self, code: InstructionCode, op1=None, op2=None, op3=None) -> None:
        self.code: InstructionCode = code
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3

    def debug(self) -> None:
        match self.code:
            case InstructionCode.ADC:
                print(f"ADC r{self.op1},r{self.op2}")
            case InstructionCode.ADD:
                print(f"ADD r{self.op1},r{self.op2}")
            case InstructionCode.BREAK:
                print(f"BREAK")
            case InstructionCode.LDI:
                print(f"LDI r{self.op1},{self.op2}")
            case InstructionCode.IJMP:
                print(f"IJMP")
            case InstructionCode.JMP:
                print(f"JMP {self.op1}")
            case InstructionCode.ICALL:
                print(f"ICALL")
            case InstructionCode.FMUL:
                print(f"FMUL r{self.op1},r{self.op2}")
            case InstructionCode.FMULS:
                print(f"FMULS r{self.op1},r{self.op2}")
            case InstructionCode.FMULSU:
                print(f"FMULSU r{self.op1},r{self.op2}")
            case InstructionCode.MUL:
                print(f"MUL r{self.op1},r{self.op2}")
            case InstructionCode.MULS:
                print(f"MULS r{self.op1},r{self.op2}")
            case InstructionCode.MULSU:
                print(f"MULSU r{self.op1},r{self.op2}")
            case InstructionCode.NEG:
                print(f"NEG r{self.op1}")
            case InstructionCode.ADIW:
                print(f"ADIW r{self.op1},{self.op2}")
            case InstructionCode.AND:
                print(f"AND r{self.op1},r{self.op2}")
            case InstructionCode.ANDI:
                print(f"ANDI r{self.op1},{self.op2}")
            case InstructionCode.ASR:
                print(f"ASR r{self.op1}")
            case InstructionCode.CALL:
                print(f"CALL {self.op1}")
            case InstructionCode.CBI:
                print(f"CBI ${self.op1:x},{self.op2}")
            case InstructionCode.BST:
                print(f"BST r{self.op1},{self.op2}")
            case InstructionCode.BSET:
                print(f"BSET {self.op1}")
            case InstructionCode.CPI:
                print(f"CPI r{self.op1},{self.op2}")
            case InstructionCode.CPC:
                print(f"CPC r{self.op1},r{self.op2}")
            case InstructionCode.CP:
                print(f"CP r{self.op1},r{self.op2}")
            case InstructionCode.DEC:
                print(f"DEC r{self.op1}")
            case InstructionCode.INC:
                print(f"INC r{self.op1}")
            case InstructionCode.COM:
                print(f"COM r{self.op1}")
            case InstructionCode.CLC:
                print(f"CLC")
            case InstructionCode.CLZ:
                print(f"CLZ")
            case InstructionCode.CLN:
                print(f"CLN")
            case InstructionCode.CLV:
                print(f"CLV")
            case InstructionCode.CLS:
                print(f"CLS")
            case InstructionCode.CLH:
                print(f"CLH")
            case InstructionCode.CLT:
                print(f"CLT")
            case InstructionCode.CLI:
                print(f"CLI")
            case InstructionCode.BCLR:
                print(f"BCLR {self.op1}")
            case InstructionCode.BLD:
                print(f"BLD r{self.op1},{self.op2}")
            case InstructionCode.BRCC:
                print(f"BRCC {self.op1}")
            case InstructionCode.BRNE:
                print(f"BRNE {self.op1}")
            case InstructionCode.BRPL:
                print(f"BRPL {self.op1}")
            case InstructionCode.BRVC:
                print(f"BRVC {self.op1}")
            case InstructionCode.BRGE:
                print(f"BRGE {self.op1}")
            case InstructionCode.BRHC:
                print(f"BRHC {self.op1}")
            case InstructionCode.BRTC:
                print(f"BRTC {self.op1}")
            case InstructionCode.BRID:
                print(f"BRID {self.op1}")
            case InstructionCode.BRCS:
                print(f"BRCS {self.op1}")
            case InstructionCode.BREQ:
                print(f"BREQ {self.op1}")
            case InstructionCode.BRMI:
                print(f"BRMI {self.op1}")
            case InstructionCode.BRVS:
                print(f"BRVS {self.op1}")
            case InstructionCode.BRLT:
                print(f"BRLT {self.op1}")
            case InstructionCode.BRHS:
                print(f"BRHS {self.op1}")
            case InstructionCode.BRTS:
                print(f"BRTS {self.op1}")
            case InstructionCode.BRIE:
                print(f"BRIE {self.op1}")
            case InstructionCode.CPSE:
                print(f"CPSE r{self.op1},r{self.op2}")
            case InstructionCode.EOR:
                print(f"EOR r{self.op1},r{self.op2}")
            case InstructionCode.IN:
                print(f"IN r{self.op1},${self.op2:x}")
            case InstructionCode.LD:
                print(f"LD r{self.op1},{debug_reg(self.op2)}")
            case InstructionCode.LDD:
                print(f"LDD r{self.op1},{debug_reg(self.op2)}")
            case InstructionCode.LPM:
                print("LPM Z")
            case InstructionCode.LDS:
                print(f"LDS r{self.op1},${self.op2:x}")
            case InstructionCode.LSR:
                print(f"LSR r{self.op1}")
            case InstructionCode.MOV:
                print(f"MOV r{self.op1},r{self.op2}")
            case InstructionCode.MOVW:
                print(f"MOVW r{self.op1},r{self.op2}")
            case InstructionCode.NOP:
                print("NOP")
            case InstructionCode.OR:
                print(f"OR r{self.op1},r{self.op2}")
            case InstructionCode.ORI:
                print(f"ORI r{self.op1},${self.op2:x}")
            case InstructionCode.OUT:
                print(f"OUT ${self.op1:x},r{self.op2}")
            case InstructionCode.POP:
                print(f"POP r{self.op1}")
            case InstructionCode.PUSH:
                print(f"PUSH r{self.op1}")
            case InstructionCode.RCALL:
                print(f"RCALL {self.op1}")
            case InstructionCode.RET:
                print(f"RET")
            case InstructionCode.RETI:
                print(f"RETI")
            case InstructionCode.RJMP:
                print(f"RJMP")
            case InstructionCode.ROR:
                print(f"ROR r{self.op1}")
            case InstructionCode.SBC:
                print(f"SBC r{self.op1},r{self.op2}")
            case InstructionCode.SBCI:
                print(f"SBCI r{self.op1},{self.op2}")
            case InstructionCode.SBI:
                print(f"SBI ${self.op1:x},{self.op2}")
            case InstructionCode.SBIC:
                print(f"SBIC ${self.op1:x},{self.op2}")
            case InstructionCode.SBIS:
                print(f"SBIS ${self.op1:x},{self.op2}")
            case InstructionCode.SBIW:
                print(f"SBIW r{self.op1}:r{self.op2},{self.op3}")
            case InstructionCode.SBRS:
                print(f"SBRS r{self.op1},{self.op2}")
            case InstructionCode.SBRC:
                print(f"SBRC r{self.op1},{self.op2}")
            case InstructionCode.SEC:
                print(f"SEC")
            case InstructionCode.SEH:
                print(f"SEH")
            case InstructionCode.SEI:
                print(f"SEI")
            case InstructionCode.SEN:
                print(f"SEN")
            case InstructionCode.SER:
                print(f"SER r{self.op1}")
            case InstructionCode.SES:
                print(f"SES")
            case InstructionCode.SET:
                print(f"SET")
            case InstructionCode.SEV:
                print(f"SEV")
            case InstructionCode.SLEEP:
                print(f"SLEEP")
            case InstructionCode.SEZ:
                print(f"SEZ")
            case InstructionCode.SPM:
                print(f"SPM")
            case InstructionCode.ST:
                print(f"ST {debug_reg(self.op1)},r{self.op2}")
            case InstructionCode.STD:
                print(f"STD {debug_reg(self.op1)},r{self.op2}")
            case InstructionCode.STS:
                print(f"STS ${self.op1:x},r{self.op2}")
            case InstructionCode.SUB:
                print(f"SUB r{self.op1},r{self.op2}")
            case InstructionCode.SUBI:
                print(f"SUBI r{self.op1},{self.op2}")
            case InstructionCode.SWAP:
                print(f"SWAP")
            case InstructionCode.WDR:
                print(f"WDR")
