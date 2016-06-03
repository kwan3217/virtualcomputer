; Write a program which converts a bit number to a bit mask. The bit number is in r1, leave the bit mask in r2. 
; Hint: To shift all bits in a number to the left 1 place, just multiply it by two
   MOV r2, 1    ;Original bit mask for bit 0
   MOV r3, -1   ;Need this to decrement a register
   SZ r1                ;If r1 is already zero, we already have the mask we need. Skip everything. Because SZ 
                        ;is weak, we need to skip a jump to get to the next jump
   JMP top_of_loop      ;We only hit this if we didn't skip it above, IE only if r1 isn't already 0
   JMP bottom_of_loop   ;we only hit this if we DID skip above, IE only if r1 is already 0
 top_of_loop:
   ADD r2, r2, r2       ;Add r2 to r2 and write result back in r2
   ADD r1, r1, r3       ;Decrement r1
   SZ r1                ;If r1 has reached 0, skip out of the loop
   JMP top_of_loop
 bottom_of_loop:
