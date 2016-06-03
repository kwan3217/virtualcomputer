;"Clever way" Solution to problem 4
   MOV r3,  0 ; clear out the product register
   MOV r4,  1 ; Bit mask
 top_of_loop:
   AND r5, r4, r2  ;Check if the given bit is set in factor 2
   SZ r5           ;Skip the next if the bit was cleared
   JMP bit_is_one
   JMP bit_is_zero
 bit_is_one:
   ADD r3, r3, r1  ;Add the (shifted) factor 1 to the product
 bit_is_zero:      ;Actually this is done if the bit is 1 OR 0
   ADD r1, r1, r1  ;Shift factor 1 to the left by 1 bit IE double factor 1 IE add factor 1 to itself
   ADD r4, r4, r4  ;Shift the bitmask. We are done when the bit shifts off the top end
   SZ r4           ;If the bit mask bit shifts all the way out, then we are done
   JMP top_of_loop ;jump back if we are not
