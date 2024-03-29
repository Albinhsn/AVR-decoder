
.device ATMega16

start:
  break
  clr r17
  adc r16, r17
loop1:
  add r16, r17
  adiw r26, 60
  and r18, r19
loop2:
  andi r18, 50
  asr r12 
  brid loop1
  brhc loop1
  brie loop1
  asr r30 
loop3:
  bclr 7
  bld r2, 4
  brbc 2,start
  brcc loop2
  brbs 4,loop1
  brcs 5,loop3
  call loop2
  call loop2
  brlo 5,loop3
  breq 5,loop3
  brge 5,loop3
  cbi $18, 7
  clc
  clh
  cli
  cln
  cls
  clt
  clv
  clz
  com r16
  cp r16, r17
  cpc r16, r17
  cpi r16,23
  cpse r16,r17
  dec r16
  inc r16
  eor r16,r17
  fmul r16,r17
  fmuls r16,r17
  fmulsu r16,r17
  icall 
  ijmp
  in r25,$16
  jmp loop1
  jmp loop1
  ld r16, X
  ld r16, X+
  ld r16, -X
