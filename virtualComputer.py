r=[0]*256 
mem=[0]*65536
ins=[0]*256
run=True;

def SignExtend16(hw):
    if(hw & (1<<15)): #If sign bit of 16 bit number is lit
        return 0xFFFF0000 | (hw & 0xFFFF)
    else: 
        return hw
    
def SignExtend8(hw):
    if(hw & (1<<7)): #If sign bit of 8 bit number is lit
        return 0xFFFFFF00 | (hw & 0xFF)
    else: 
        return hw
    
def make16(A,B):
    return SignExtend16((A<<8)|B)

LDRimm   =0x00
def insLDRimm(D,A,B):
    r[D]=make16(A,B)
ins[LDRimm]=insLDRimm    

LDRregimm=0x01
def insLDRregimm(D,A,B):
    r[D]=mem[r[A]+B]
ins[LDRregimm]=insLDRregimm    

LDRregreg=0x02
def insLDRregreg(D,A,B):
    r[D]=mem[r[A]+r[B]]
ins[LDRregreg]=insLDRregreg    

STRimm   =0x04
def insSTRimm(D,A,B):
    mem[make16(A,B)]=r[D]
ins[STRimm]=insSTRimm
    
STRregimm=0x05
def insSTRregimm(D,A,B):
    mem[r[A]+B]=r[D]
ins[STRregimm]=insSTRregimm    

STRregreg=0x06
def insSTRregreg(D,A,B):
    mem[r[A]+r[B]]=r[D]
ins[STRregreg]=insSTRregreg    

MOVimm   =0x08
def insMOVimm(D,A,B):
    r[D]=make16(A,B)
ins[MOVimm]=insMOVimm    

MOVreg   =0x09
def insMOVreg(D,A,B):
    r[D]=r[A]
ins[MOVimm]=insMOVimm    

SWP      =0x0A
def insSWP(D,A,B):
    temp=r[D]
    r[D]=r[A]
    r[A]=temp
ins[SWP]=insSWP    

ADDregimm=0x10
def insADDregimm(D,A,B):
    r[D]=(r[A]+SignExtend8(B)) & 0xFFFFFFFF
ins[ADDregimm]=insADDregimm    

ADDregreg=0x11
def insADDregreg(D,A,B):
    r[D]=(r[A]+r[B]) & 0xFFFFFFFF
ins[ADDregreg]=insADDregreg    

AND      =0x18
def insAND(D,A,B):
    r[D]=r[A]&r[B]
ins[AND]=insAND
    
SZ       =0x30
def insSZ(D,A,B):
    if r[D]==0:
        r[0xFF]=r[0xFF]+1
ins[SZ]=insSZ        

BRK      =0xFF
def insBRK(D,A,B):
    r[0xfb]=1; 
ins[BRK]=insBRK

def assemble(opcode,D,A,B):
    return ((opcode & 0xFF) << 24) | ((D      & 0xFF) << 16) | ((A      & 0xFF) <<  8) | ((B      & 0xFF) <<  0) 
         
def assembleAB(opcode,D,AB):
    return ((opcode & 0xFF) << 24) | ((D      & 0xFF) << 16) | ((AB      & 0xFFFF) <<  0) 

def decode(w):
    opcode=(w >> 24) & 0xFF
    D=(w >> 16) & 0xFF
    A=(w >>  8) & 0xFF
    B=(w >>  0) & 0xFF
    return (opcode,D,A,B)

def printDisasm(addr,w):
    (opcode,D,A,B)=decode(w)
    print("%08x: %s %02x, %02x, %02x"%(addr,ins[opcode],D,A,B))

def dumpMem(addr0,length):
    for addr in range(addr0,length):
        printDisasm(addr,mem[addr])
        
def printReg():
    for reg in range(0,256):
        if(r[reg]!=0):
            print("rx%02x: %08x"%(reg,r[reg]))
                                             
def ExecCycle():
    thisIns=mem[r[0xFF]]
    (opcode,D,A,B)=decode(thisIns)
    printReg()
    printDisasm(r[0xFF],thisIns)
    r[0xFF]=r[0xFF]+1
    ins[opcode](D,A,B)
    
def ExecToBrk():
    r[0xfb]=0
    while(r[0xfb]==0):
        ExecCycle()
    r[0xfb]=0

dot=0
# Problem 1
mem[dot]=assemble(ADDregreg,2,1,1) ; dot=dot+1
mem[dot]=assemble(BRK,0,0,0)       ; dot=dot+1
r[0xff]=0
r[1]=17
ExecToBrk()
print(r[2])            

#problem 2, test case 1
mem[dot]=assemble(AND,3,1,2) ; dot=dot+1
mem[dot]=assemble(BRK,0,0,0)       ; dot=dot+1
r[1]=17
r[2]=8
ExecToBrk()
print(r[3])            

#problem 2, test case 2
mem[dot]=assemble(AND,3,1,2) ; dot=dot+1
mem[dot]=assemble(BRK,0,0,0)       ; dot=dot+1
r[1]=9
r[2]=8
ExecToBrk()
print(r[3])            

mem[dot]=assembleAB(MOVimm,2, 1) ; dot=dot+1 #Original bit mask for bit 0
mem[dot]=assembleAB(MOVimm,3,-1) ; dot=dot+1 #Need this to decrement a register
mem[dot]=assemble  (SZ,    1, 0, 0) ; dot=dot+1 #If r1 is already zero, we already have the mask we need. Skip everything. Because SZ 
                                                #is weak, we need to skip a jump to get to the next jump
mem[dot]=assembleAB(MOVimm,255,dot+2); dot=dot+1 #   JMP top_of_loop      ;We only hit this if we didn't skip it above, IE only if r1 isn't already 0
mem[dot]=assembleAB(MOVimm,255,dot+5); dot=dot+1 #   JMP bottom_of_loop   ;we only hit this if we DID skip above, IE only if r1 is already 0
# top_of_loop:
top_of_loop=dot
mem[dot]=assemble  (ADDregreg,2,  2,  2); dot=dot+1 #Add r2 to r2 and write result back in r2
mem[dot]=assemble  (ADDregreg,1,  1,  3); dot=dot+1 #Decrement r1
mem[dot]=assemble  (SZ,       1,  0,  0); dot=dot+1 #If r1 has reached 0, skip out of the loop
mem[dot]=assembleAB(MOVimm,255,top_of_loop); dot=dot+1 #JMP top_of_loop
bottom_of_loop=dot
mem[dot]=assemble  (BRK,0,0,0); dot=dot+1 

r[1]=3
ExecToBrk()
print(r[2])

#This implements the "dumb" way
mem[dot]=assembleAB(MOVimm,  4, -1); dot=dot+1 # need this to decrement
mem[dot]=assembleAB(MOVimm,  3,  0); dot=dot+1 # set the product to 0
mem[dot]=assemble  (SZ,      2,0,0); dot=dot+1 # If the second factor is already 0, we are done already. Just skip the loop.
mem[dot]=assembleAB(MOVimm,255,dot+2); dot=dot+1 #    JMP top_of_loop
mem[dot]=assembleAB(MOVimm,255,dot+5); dot=dot+1 #    JMP bottom_of_loop
top_of_loop=dot
mem[dot]=assemble  (ADDregreg,3,3,1); dot=dot+1  # Add the first factor to the product, writing back to the product register
mem[dot]=assemble  (ADDregreg,2,2,4); dot=dot+1  # decrement the second factor (used as a loop counter)
mem[dot]=assemble  (SZ,       2,0,0); dot=dot+1  # If the second factor has reached 0, we are done
mem[dot]=assembleAB(MOVimm,255,top_of_loop); dot=dot+1
bottom_of_loop=dot
mem[dot]=assemble  (BRK,0,0,0); dot=dot+1 

r[1]=3
r[2]=5
ExecToBrk()
print(r[3])

#"Clever way" Solution to problem 4
mem[dot]=assembleAB(MOVimm,3,  0);dot=dot+1 # clear out the product register
mem[dot]=assembleAB(MOVimm,4,  1);dot=dot+1 # Bit mask
top_of_loop=dot
mem[dot]=assemble  (AND,5,4,2);dot=dot+1  #Check if the given bit is set in factor 2
mem[dot]=assemble  (SZ, 5,0,0);dot=dot+1  #Skip the next if the bit was cleared
mem[dot]=assembleAB(MOVimm,255,dot+2);dot=dot+1
mem[dot]=assembleAB(MOVimm,255,dot+2);dot=dot+1
bit_is_one=dot
mem[dot]=assemble  (ADDregreg,3,3,1);dot=dot+1  #Add the (shifted) factor 1 to the product
bit_is_zero=dot               #Actually this is done if the bit is 1 OR 0
mem[dot]=assemble  (ADDregreg,1,1,1);dot=dot+1  #Shift factor 1 to the left by 1 bit IE double factor 1 IE add factor 1 to itself
mem[dot]=assemble  (ADDregreg,4,4,4);dot=dot+1  #Shift the bitmask. We are done when the bit shifts off the top end
mem[dot]=assemble  (SZ,       4,0,0);dot=dot+1  #If the bit mask bit shifts all the way out, then we are done
mem[dot]=assembleAB(MOVimm,255,top_of_loop);dot=dot+1 #jump back if we are not
mem[dot]=assemble  (BRK,0,0,0); dot=dot+1 

r[1]=3
r[2]=5
ExecToBrk()
print(r[3])

