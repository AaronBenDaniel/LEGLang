const a 0
const valuea 5
const b 1
const valueb 9
const c 2
const valuec 3

# Load values into RAM
ADD | II valuea 0 REG0
STR | IR a REG0 0
ADD | II valueb 0 REG0
STR | IR b REG0 0
ADD | II valuec 0 REG0
STR | IR c REG0 0

# Run add opperation
ADD | II c 0 REG1
ADD | II b 0 REG0
CALL 0 add 0
ADD | II b 0 REG1
ADD | II a 0 REG0
CALL 0 add 0
ADD | II 0 0 REG0
STR | IR c REG0 0
STR | IR b REG0 0

# Infinite loop
label loop
JMP | EQ | II 0 0 loop

# Add RAM[REG1] to RAM[REG0]
label add
PUSH | RR 0 REG0 0
PUSH | RR 0 REG1 0
CALL 0 inc 0
POP | RR 0 REG0 0
ADD | RI REG0 0 REG1
PUSH | RR 0 REG1 0
CALL 0 dec 0
POP | RR 0 REG0 0
LOAD | RR REG0 REG1 0
JMP | EQ | IR 0 REG1 addRet
ADD | RI REG0 0 REG1
POP | RR 0 REG0 0
JMP | EQ | II 0 0 add
label addRet
POP | RR 0 REG0 0
RET 0 0 COUNTER

# Increment RAM[REG0]
label inc
LOAD | RR REG0 REG1 0
ADD | IR 1 REG1 REG2
STR | RR REG0 REG2 0
RET 0 0 COUNTER

# Decrement RAM[REG0]
label dec
LOAD | RR REG0 REG1 0
SUB | RI REG1 1 REG2
STR | RR REG0 REG2 0
RET 0 0 COUNTER

