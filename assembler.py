# Indentation hell if I've ever seen it
# This code feels like I completely gave in to the shoulder devil of bad coding practices
# My excuse is that it was pretty late when I wrote this

from os import remove

validDests = ["REG0", "REG1", "REG2", "REG3", "REG4", "REG5", "COUNTER", "IO"]
consts = {}
vars = {}
calls = []

try:
    # Open files
    source = open("in.lls", "r")  # LEG Lang Source
    remove("out.ll")  # LEG Lang
    output = open("out.ll", "w")

    output.write("CALL 0 initVars 0\n")
    instructionCounter = 1
    # Process lines of source code
    for lineNumber, line in enumerate(source):
        lineNumber = lineNumber + 1

        # Isolate code and comments
        if "#" in line:
            code = line[: line.index("#")].rstrip()
            comment = (" " if code else "") + line[line.index("#") - len(line) :]
        else:
            comment = ""
            code = line

        # Split code into words
        words = code.split(" ")
        words[-1] = words[-1].replace("\n", "")

        # Match first word of line to a Leg Lang word
        match (words[0]):
            case "var":
                if len(words) == 3: # var name value
                    vars[words[1]] = words[2]
                elif len(words) == 2: # var name
                    vars[words[1]] = 0
                else:
                    raise ValueError(
                        f"Line {lineNumber}: Incorrect number of arguments for `var`"
                    )
                if words[1].isdigit():
                    raise ValueError(f"Line {lineNumber}: var cannot be named a number")
                if words[1] in consts:
                    raise ValueError(f"Line {lineNumber}: Redefinition of var")
                consts[words[1]] = 0
                instructionCounter = instructionCounter - 1

            case "const":
                if len(words) != 3:
                    raise ValueError(
                        f"Line {lineNumber}: Incorrect number of arguments for `const`"
                    )
                if words[1].isdigit():
                    raise ValueError(
                        f"Line {lineNumber}: const cannot be named a number"
                    )
                if words[1] in consts:
                    raise ValueError(f"Line {lineNumber}: Redefinition of const")
                consts[words[1]] = words[2]
                instructionCounter = instructionCounter - 1

            case "label":
                if len(words) != 2:
                    raise ValueError(
                        f"Line {lineNumber}: Incorrect number of arguments for `label`"
                    )
                if words[1].isdigit():
                    raise ValueError(
                        f"Line {lineNumber}: label cannot be named a number"
                    )
                if words[1] in consts:
                    raise ValueError(f"Line {lineNumber}: Redefiniation of label")
                consts[words[1]] = instructionCounter
                instructionCounter = instructionCounter - 1
                output.write(
                    f"label {words[1]}_"
                )  # Dummy label, the real one is a const that is put at the bottom

            case "ADD":
                match (len(words)):
                    case 4:  # ADD value value reg
                        if words[1] in validDests:
                            modifier = "R"
                        elif words[1] in consts or words[1].isdigit():
                            modifier = "I"
                        else:
                            raise ValueError(
                                f"Line {lineNumber}: Invalid arugment `{words[1]}` for `ADD`"
                            )
                        if words[2] in validDests:
                            modifier = modifier + "R"
                        elif words[2] in consts or words[2].isdigit():
                            modifier = modifier + "I"
                        else:
                            raise ValueError(
                                f"Line {lineNumber}: Invalid arugment `{words[2]}` for `ADD`"
                            )
                        if words[3] not in validDests:
                            raise ValueError(
                                f"Line {lineNumber}: `{words[3]}` is not a valid destination for `ADD`"
                            )
                        output.write(
                            f"ADD | {modifier} {words[1]} {words[2]} {words[3]}"
                        )
                    case 3:  # ADD value reg
                        if words[1] in validDests:
                            modifier = "RI"
                        elif words[1] in consts or words[1].isdigit():
                            modifier = "II"
                        else:
                            raise ValueError(
                                f"Line {lineNumber}: Invalid arugment `{words[1]}` for `ADD`"
                            )
                        if words[2] not in validDests:
                            raise ValueError(
                                f"Line {lineNumber}: `{words[2]}` is not a valid destination for `ADD`"
                            )
                        output.write(f"ADD | {modifier} {words[1]} 0 {words[2]}")
                    case _:
                        raise ValueError(
                            f"Line {lineNumber}: Incorrect number of arguments for `ADD`"
                        )

            case "STR":
                if len(words) != 3:
                    raise ValueError(
                        f"Line {lineNumber}: Incorrect number of arguments for `STR`"
                    )
                if words[1] in validDests:
                    modifier = "R"
                elif words[1] in consts or words[1].isdigit():
                    modifier = "I"
                else:
                    raise ValueError(
                        f"Line {lineNumber}: Invalid arugment `{words[1]}` for `STR`"
                    )
                if words[2] in validDests:
                    modifier += "R"
                elif words[2] in consts or words[2].isdigit():
                    modifier += "I"
                else:
                    raise ValueError(
                        f"Line {lineNumber}: Invalid arugment `{words[2]}` for `STR`"
                    )
                output.write(f"STR | {modifier} {words[1]} {words[2]} 0")

            case "CALL":
                if len(words) != 2:
                    raise ValueError(
                        f"Line {lineNumber}: Incorrect number of arguments for `CALL`"
                    )
                if words[1].isdigit():
                    raise ValueError(
                        f"Line {lineNumber}: Cannot call function with number name"
                    )
                calls.append([lineNumber, words[1]])
                output.write(f"CALL 0 {words[1]} 0")

            case "JMP":
                match len(words):
                    case 2:  # JMP label
                        calls.append([lineNumber, words[1]])
                        output.write(f"JMP | EQ | II 0 0 {words[1]}")
                    case 5:  # JMP cond value value label
                        if words[2] in validDests:
                            modifier = "R"
                        elif words[2] in consts or words[2].isdigit():
                            modifier = "I"
                        else:
                            raise ValueError(
                                f"Line {lineNumber}: Invalid arugment `{words[2]}` for `ADD`"
                            )
                        if words[3] in validDests:
                            modifier = modifier + "R"
                        elif words[3] in consts or words[3].isdigit():
                            modifier = modifier + "I"
                        else:
                            raise ValueError(
                                f"Line {lineNumber}: Invalid arugment `{words[3]}` for `ADD`"
                            )

                        calls.append([lineNumber, words[4]])
                        output.write(
                            f"JMP | {words[1]} | {modifier} {words[2]} {words[3]} {words[4]}"
                        )
                    case _:
                        raise ValueError(
                            f"Line {lineNumber}: Incorrect number of arguments for `JMP`"
                        )

            case "RET":
                output.write("RET 0 0 COUNTER")

            case "PUSH":
                if len(words) != 2:
                    ValueError(
                        f"Line {lineNumber}: Incorrect number of arguments for `PUSH`"
                    )
                if words[1] in validDests:
                    modifier = "RR"
                elif words[1] in consts or words[1].isdigit():
                    modifier = "RI"
                else:
                    raise ValueError(f"Invalid arugment `{words[1]}` for `PUSH`")
                output.write(f"PUSH | {modifier} 0 {words[1]} 0")

            case "POP":
                if len(words) != 2:
                    raise ValueError(
                        f"Line {lineNumber}: Incorrect number of arguments for `POP`"
                    )
                if words[1] not in validDests:
                    raise ValueError(
                        f"Line {lineNumber}: Invalid destination `{words[1]}` for POP"
                    )
                output.write(f"POP | RR 0 {words[1]} 0")

            case "LOAD":
                if words[1] in validDests:
                    modifier = "RR"
                elif words[1] in consts or words[1].isdigit():
                    modifier = "IR"
                else:
                    raise ValueError(
                        f"Line {lineNumber}: Invalid arugment `{words[1]}` for `LOAD`"
                    )
                if words[2] not in validDests:
                    raise ValueError(
                        f"Line {lineNumber}: Invalid arugment `{words[2]}` for `LOAD`"
                    )
                output.write(f"LOAD | {modifier} {words[1]} {words[2]} 0")

            case "SUB":
                if words[1] in validDests:
                    modifier = "R"
                elif words[1] in consts or words[1].isdigit():
                    modifier = "I"
                else:
                    raise ValueError(
                        f"Line {lineNumber}: Invalid arugment `{words[1]}` for `SUB`"
                    )
                if words[2] in validDests:
                    modifier = modifier + "R"
                elif words[2] in consts or words[2].isdigit():
                    modifier = modifier + "I"
                else:
                    raise ValueError(
                        f"Line {lineNumber}: Invalid arugment `{words[2]}` for `SUB`"
                    )
                if words[3] not in validDests:
                    raise ValueError(
                        f"Line {lineNumber}: `{words[3]}` is not a valid destination for `SUB`"
                    )
                output.write(f"SUB | {modifier} {words[1]} {words[2]} {words[3]}")

            case "XOR":
                if words[1] in validDests:
                    modifier = "R"
                elif words[1] in consts or words[1].isdigit():
                    modifier = "I"
                else:
                    raise ValueError(
                        f"Line {lineNumber}: Invalid arugment `{words[1]}` for `XOR`"
                    )
                if words[2] in validDests:
                    modifier = modifier + "R"
                elif words[2] in consts or words[2].isdigit():
                    modifier = modifier + "I"
                else:
                    raise ValueError(
                        f"Line {lineNumber}: Invalid arugment `{words[2]}` for `XOR`"
                    )
                if words[3] not in validDests:
                    raise ValueError(
                        f"Line {lineNumber}: `{words[3]}` is not a valid destination for `XOR`"
                    )
                output.write(f"XOR | {modifier} {words[1]} {words[2]} {words[3]}")

            case _:
                instructionCounter = instructionCounter - 1

        instructionCounter = instructionCounter + 1

        # Write comment
        if words[0] != "const":  # Yes this removes const comments
            output.write(comment if comment else "\n")

    # Parse vars
    output.write("\n# Initialize variables\nlabel initVars_\n")
    consts["initVars"] = instructionCounter
    RAMCounter = 255
    for name, value in vars.items():
        if RAMCounter<0:
            raise ValueError("Too many variables; Not enough RAM")
        consts[name] = RAMCounter
        RAMCounter = RAMCounter - 1
        output.write(f"STR | II {name} {value} 0\n")
    output.write("RET 0 0 COUNTER\n")

    # Write out consts
    output.write("\n# consts:\n")
    for name, value in consts.items():
        output.write(f"const {name} {value}\n")

    # If there were any function calls to non-existant functions, throw an error
    for lineNumber, call in calls:
        if call not in consts:
            raise ValueError(f"Line {lineNumber}: Label `{call}` does not exist")

    if instructionCounter > 256:
        raise ValueError(
            "Program greater than 1024 bytes. Unable to store in LEGcompressed architecture"
        )

    print(
        f"Sucessfully compiled in {instructionCounter*4} bytes ({int(instructionCounter/256*100)}% of 1024 bytes)"
    )

# Close files
finally:
    source.close()
    output.write("\n")
    output.close()
