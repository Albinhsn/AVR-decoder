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
BRBC = 0b111101


def main() -> int:
    return 0


if __name__ == "__main__":
    exit(main())
