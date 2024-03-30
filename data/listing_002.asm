
.device ATMega16

start:
  break
  clr r17
  ldi r16,5
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
  mul r16,r17
  muls r16,r17
  mulsu r16,r17
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

  ld r16, Y
  ld r16, Y+
  ld r16, -Y
  ldd r16, Y+10
  
  lds r16,$FF
  lds r16,$00
  ld r16, Z
  ld r16, Z+
  ld r16, -Z
  ldd r16, Z+10

  lpm 
  lpm r5,Z
  lpm r5,Z+

  lsl r16
  lsr r16

  mov r16, r17
  mov r4, r31

  movw r0,r30
  movw r8,r14

  neg r10

  nop

  or r16,r17
  ori r16,5
  out $10,R12
  pop r12
  push r12
  rcall loop1

  ret
  reti
  rjmp loop1
  rol r15
  ror r15

  sbc r15, r16
  sbci r16, 10
  sbi $1C, 0
  sbic $1C, 0
  sbis $1C, 0
  sbiw r25:r24, 1
  sbr r17,244
  sbrc r0, 7
  sbrs r0, 7
  sec
  spm
  spm Z+

  st X,r16
  st X+,r16
  st -X,r16


  st Y,r16
  st Y+,r16
  st -Y,r16
  std Y+5,r16

  st Z,r16
  st Z+,r16
  st -Z,r16
  std Z+5,r16
  sts $10,r2

  sub r16,r17
  subi r16,100
  swap r16

  tst r16

  wdr

