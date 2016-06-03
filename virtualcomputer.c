#include <stdio.h>
//Python doesn't support goto, so it is difficult to write the JMP instruction without
//actually having a memory system. We will implement in C, which does support goto

int r[256];  // 256 registers

/** Copy value A to rD */
void MOVimm(int D, int A) {
    r[D]=A;
}

/** Copy value in rA to rD */
void MOVreg(int D, int A) {
    r[D]=r[A];
}

void ADD(int D, int A, int B) {
    r[D]=r[A]+r[B];
}

void AND(int D, int A, int B) {
    r[D]=r[A]&r[B];
}

int SZ(int D) {
    return r[D]==0;
}

#define JMP(x) goto x

/** Set r2 to twice r1 */
void problem1() {
  ADD(2,1,1); /* Just add r1 to itself */
}

/** Test if the bit specified by the bitmask in r2 is set in the value in r1. Write result to r3, 0 of cleared or !0 if set */
void problem2() {
  AND(3,1,2); /* if the given bit is set, then r3 will be the bit mask for the bit that is set (IE equal to r2) */
}

/** Calculate the bitmask for the bit specified in r1. Result will be in r2, r1 will be clobbered */
void problem3() {
  MOVimm(2,  1); /* Original bit mask for bit 0 */
  MOVimm(3, -1); /* Need this to decrement a register */
  if(!SZ(1))   /* If r1 is already zero, we already have the mask we need. Skip everything. Because SZ is weak, we need to skip a jump to get to the next jump */
  JMP(top_of_loop);    /* We only hit this if we didn't skip it above, IE only if r1 isn't already 0 */
  JMP(bottom_of_loop); /* we only hit this if we DID skip above, IE only if r1 is already 0 */
top_of_loop:
  ADD(2,2,2); /* Add r2 to r2 and write result back in r2 */
  ADD(1,1,3); /* Decrement r1 */
  if(!SZ(1))  /* If r1 has reached 0, skip out of the loop */
  JMP(top_of_loop);
bottom_of_loop:
  return; /* Need a statement as a target */
}

/** Multiply the value in r1 and r2, leaving result in r3, the "dumb" way */
void problem4dumb() {
  MOVimm(4, -1); /* need this to decrement */
  MOVimm(3,  0); /* set the product to 0 */
  if(!SZ(2))     /* If the second factor is already 0, we are done already. Just skip the loop. */
  JMP(top_of_loop);
  JMP(bottom_of_loop);
top_of_loop:
  ADD(3,3,1); /* Add the first factor to the product, writing back to the product register */
  ADD(2,2,4); /* decrement the second factor (used as a loop counter) */
  if(!SZ(2))  /* If the second factor has reached 0, we are done */
  JMP(top_of_loop);
bottom_of_loop:
  ;
}

void problem4smart() {
  MOVimm(3, 0); /* clear out the product register */
  MOVimm(4,  1); /* Bit mask */
top_of_loop:
  AND(5, 4, 2); /* Check if the given bit is set in factor 2 */
  if(!SZ(5))      /* Skip the next if the bit was cleared */
  JMP(bit_is_one);
  JMP(bit_is_zero);
bit_is_one:
  ADD(3, 3, 1); /* Add the (shifted) factor 1 to the product */
bit_is_zero: /* Actually this is done if the bit is 1 OR 0 */
  ADD(1, 1, 1); /*Shift factor 1 to the left by 1 bit IE double factor 1 IE add factor 1 to itself */
  ADD(4, 4, 4); /*Shift the bitmask. We are done when the bit shifts off the top end */
  if(!SZ(4))          /* If the bit mask bit shifts all the way out, then we are done */
  JMP(top_of_loop); /*jump back if we are not */
}

int main() {
  MOVimm(1,17); /* This is the number to double */
  problem1();
  printf("%d\n",r[2]); /* Print the result, should be 34 */

  /* Run problem 2 with first example case */
  MOVimm(1,17);
  MOVimm(2, 8); /* Manually calculated bitmask for bit 3 */
  problem2();
  printf("%d\n",r[3]); /* Should be 0 */

  /* Rerun problem 2 for second example case */
  MOVimm(1,9);
  MOVimm(2,8); /* Manually calculated bitmask for bit 3 */
  problem2();
  printf("%d\n",r[3]); /* Should be 8 */

  /* Run problem 3 */
  MOVimm(1,3);
  problem3();
  printf("%d\n",r[2]); /* Should be 8 */

  /* Run problem 4, the dumb way */
  MOVimm(1,3);
  MOVimm(2,5);
  problem4dumb();
  printf("%d\n",r[3]); /* Should be 15 */

  /* Run problem 4, the smart way */
  MOVimm(1,3);
  MOVimm(2,5);
  problem4smart();
  printf("%d\n",r[3]); /* Should be 15 */
}
