CALL 0 initVars 0



ADD | II a 0 REG0
ADD | II b 0 REG1
CALL 0 fibb 0
LOAD | IR b REG0 0

label infiniteLoop_
JMP | EQ | II 0 0 infiniteLoop

# Stores A-th fibbonacci number in B
# Usage:
# ADD A REG0
# ADD B REG1
# CALL fibb
# A-th fibbonacci number now in B
label fibb_
LOAD | RR REG0 REG2 0
JMP | EQ | RI REG2 0 zero
JMP | EQ | RI REG2 1 one

SUB | RI REG2 1 REG2
STR | RR REG0 REG2 0
PUSH | RR 0 REG2 0
CALL 0 fibb 0
POP | RR 0 REG2 0
LOAD | RR REG1 REG3 0
PUSH | RR 0 REG3 0


SUB | RI REG2 1 REG2
STR | RR REG0 REG2 0
CALL 0 fibb 0
LOAD | RR REG1 REG2 0
POP | RR 0 REG3 0
ADD | RR REG2 REG3 REG2
STR | RR REG1 REG2 0
RET 0 0 COUNTER

label zero_
STR | RI REG1 0 0
RET 0 0 COUNTER
label one_
STR | RI REG1 1 0
RET 0 0 COUNTER



# Takes two variables, adds the value of B and adds to A
# Usage:
# ADD A REG0
# ADD B REG1
# CALL addVars
label addVars_
LOAD | RR REG0 REG2 0
LOAD | RR REG1 REG1 0
ADD | RR REG1 REG2 REG2
STR | RR REG0 REG2 0
RET 0 0 COUNTER

# Moves value of B into A
# Usage:
# ADD A REG0
# ADD B REG1
# CALL moveVar
label moveVar_
LOAD | RR REG1 REG1 0
STR | RR REG0 REG1 0
RET 0 0 COUNTER

# Initialize variables
label initVars_
STR | II a 9 0
STR | II b 0 0
RET 0 0 COUNTER

# consts:
const a 255
const b 254
const infiniteLoop 5
const fibb 6
const zero 24
const one 26
const addVars 28
const moveVar 33
const initVars 36

