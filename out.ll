
# Read in initial state
ADD | RI IO 0 REG0
ADD | RI IO 0 REG1
ADD | RI IO 0 REG2
ADD | RI IO 0 REG3

CALL 0 MOVE 0

label infiniteLoop_
JMP | EQ | II 0 0 infiniteLoop

# Move stack of size REG0 from REG1 to REG2 using space space REG3
label MOVE_
JMP | EQ | RI REG0 0 MOVEZERO
# DISK_NR > 0

# move(disk_nr-1,source,spare,dest)
# Push order: SPARE, DEST, SOURCE, DISK_NR
# Save vars for later use
PUSH | RR 0 REG3 0
PUSH | RR 0 REG2 0
PUSH | RR 0 REG1 0
PUSH | RR 0 REG0 0

# disk_nr-=1
SUB | RI REG0 1 REG4
ADD | RI REG4 0 REG0

ADD | RI REG2 0 REG4
ADD | RI REG3 0 REG2
ADD | RI REG4 0 REG3
CALL 0 MOVE 0

# move(0,source,dest,spare)
# Push order: SPARE, DEST, SOURCE, DISK_NR
# Save vars for later use
POP | RR 0 REG0 0
POP | RR 0 REG1 0
POP | RR 0 REG2 0
POP | RR 0 REG3 0
PUSH | RR 0 REG3 0
PUSH | RR 0 REG2 0
PUSH | RR 0 REG1 0
PUSH | RR 0 REG0 0
ADD | II 0 0 REG0
CALL 0 MOVE 0

# move(0,source,dest,spare)
# Push order: SPARE, DEST, SOURCE, DISK_NR
POP | RR 0 REG0 0
POP | RR 0 REG1 0
POP | RR 0 REG2 0
POP | RR 0 REG3 0

# disk_nr-=1
SUB | RI REG0 1 REG4
ADD | RI REG4 0 REG0

ADD | RI REG3 0 REG4
ADD | RI REG1 0 REG3
ADD | RI REG4 0 REG1
CALL 0 MOVE 0
RET 0 0 COUNTER

# DISK_NR == 0
label MOVEZERO_
ADD | RI REG1 0 IO
ADD | II TOGGLE 0 IO
ADD | RI REG2 0 IO
ADD | II TOGGLE 0 IO
RET 0 0 COUNTER

# consts:
const TOGGLE 5
const infiniteLoop 5
const MOVE 6
const MOVEZERO 38

