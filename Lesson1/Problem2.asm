;Write a program which determines if a bit in a number is set (bit has value 1) or cleared (bit has value 0).
;For instance, is bit 3 set in the number 17? The number 17 in binary is 0b10001, so bit 3 is cleared. But, 
;bit 3 is set is in number 9, binary 0b01001. It is acceptable to precalculate (on paper, for instance) a 
;number which has the bit we care about set. This is called the bit mask. For instance if we are testing bit 3,
;then the bit mask is the value 8 (0b1000). The number we are checking is in r1, and the bit mask is in r2. 
;Your code should set r3 to 0 if the bit is cleared, and any nonzero value if it is set.
  AND r3, r1, r2 ;if the given bit is set, then r3 will be the bit mask for the bit that is set (IE equal to r2)
