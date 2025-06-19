CALL 0 initVars 0




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
label loop_ # test
JMP | EQ | II 0 0 loop

# Add RAM[REG1] to RAM[REG0]
label add_
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
label addRet_
POP | RR 0 REG0 0
RET 0 0 COUNTER

# Increment RAM[REG0]
label inc_
LOAD | RR REG0 REG1 0
ADD | IR 1 REG1 REG2
STR | RR REG0 REG2 0
RET 0 0 COUNTER

# Decrement RAM[REG0]
label dec_
LOAD | RR REG0 REG1 0
SUB | RI REG1 1 REG2
STR | RR REG0 REG2 0
RET 0 0 COUNTER

# Initialize variables
label initVars_
STR | II a 5 0
STR | II b 9 0
STR | II c 3 0
RET 0 0 COUNTER

# consts:
const a 255
const b 254
const c 253
const loop 10
const add 11
const addRet 24
const inc 26
const dec 30
const initVars 34

