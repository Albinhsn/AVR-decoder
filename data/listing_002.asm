
.device ATMega8

start:
  break
  clr r17
  adc r16, r17
  add r16, r17
  adiw r26, 60
  and r18, r19
  andi r18, 50
  asr r12 
  asr r30 
  bclr 1
  bld r1, 4
