
.device ATMega8

start:
  clr r17
  inc r16
  ldi r16, 15
  inc r16
  ldi r17, high($3)
  ldi r16, 15
  inc r16
  ldi r17, high($3)
  ldi r16, 15
  inc r16
  ldi r17, high($3)
  rjmp start
