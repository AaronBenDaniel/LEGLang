Valid registers are: \
- REG0 \
- REG1 \
- REG2 \
- REG3 \
- REG4 \
- REG5 \
- COUNTER (This is the program counter) \
- IO (This allows for communication outside the computer)

# Pseudo-operations 

## CONST \
`CONST {name} {value}` \
Defines a constant value that may be referenced by name. \
Value must be a literal

## LABEL \
`LABEL {name}` \
Defines a label that indicates a jump point or function.

# Arithmetic Operations \
NOTE: LEG architecture supports additional arithmetic operations that I have not implemented (yet) into LEGLang. I will implement them if I end up needing to use them.

## ADD \
`ADD {addend} {addend} {register}` \
`ADD {addend} {register}` (Second value is implictly `0`) \
Add values together and saves the output into the specificied register. \
Values may be literals, consts, or registers.

## SUB \
`SUB {minuend} {subtrahend} {register} \
Subtracts the values and saves the output into the specificied register. \
Values may be literals, consts, or registers.

## XOR
`XOR {value} {value} {register} \
Performs a bitwise XOR operation on the specificied values and saves the output into the specificied register. \
Values may be literals, consts, or registers.

# Memory Operations

## STR \
`STR {address} {value}` \
Stores the specificied value into RAM at the specificied memory address. \
Address and value may be literals, consts, or registers.

## LOAD \
`LOAD {address} {register}` \
Loads the value in RAM at the specificied memory address into the specificied register. \
Address may be a literal, const, or register.

## PUSH \
`PUSH {value}` \
Pushes the value onto the stack. \
Value may be a literal, const, or register.

## POP \
`POP {register}` \
Pops the top of the stack into the specificied register.

# Control Flow Operations

## JMP \
`JMP {label}` (Implicit `EQ 0 0`) \
`JMP {condition} {value} {value} {label}` \
Valid conditions: \
- EQ (equal to) \
- NEQ (not equal to) \
- LESS (less than) \
- LESSEQ (less than or equal to) \
- GREAT (greater than) \
- GREATEQ (greater than or equal to) \
Values may be literals, consts, or registers. \
Evaluated left to right (EG `JMP LESS a b label` jumps if `a` is less than `b`)

## CALL \
`CALL {label}` \
Pushes `counter` value +1 onto the stack and jumps to the specificied label.

## RET \
`RET` \
Pops the top of the stack into the `counter`.