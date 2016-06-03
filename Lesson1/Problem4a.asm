;Write a program which multiplies two positive numbers. One factor is in r1, the other is in r2, and leave the result 
;in r3. It doesn't matter if r1 and r2 retain the factors, IE you can use r1 and r2 as scratch space, clobbering the 
;original value there. The dumb way is to set up a loop, and just add a number to itself a certain number of times. 
;But, there is a more clever way. Think about how you learned to multiply in third grade: Multiply each digit in the top
;by one digit in the bottom, and shift the answer over the same number of digits.
;    432
; x  121
; ------
;    432
;   8640
;  43200
; ------
;  52272
;You can do the same thing in binary, with one fact that makes things easier: If the digit you are multiplying by is 1, 
;then you are just adding the top number to the product. If it is zero, then you just don't add the number.

;This implements the "dumb" way
   MOV r4, -1 ; need this to decrement
   MOV r3, 0  ; set the product to 0
   SZ r2      ; If the second factor is already 0, we are done already. Just skip the loop.
   JMP top_of_loop
   JMP bottom_of_loop
 top_of_loop:
   ADD r3, r3, r1 ; Add the first factor to the product, writing back to the product register
   ADD r2, r2, r4 ; decrement the second factor (used as a loop counter)
   SZ r2          ; If the second factor has reached 0, we are done
   JMP top_of_loop
 bottom_of_loop:
