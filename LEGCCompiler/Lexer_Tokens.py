class Lexer_Token:
    def __init__(
        self, name: str, line: int = None, col: int = None, length: int = None
    ):
        self.name = name
        self.line = line
        self.col = col
        if col is not None and length is not None:
            self.col = col - length
        self.length = length

    def __str__(self):
        return f'<Lexer_Token: "{self.name}" at line: {self.line}, col: {self.col}>'


#
# Operators
#


class Lexer_Operator(Lexer_Token):
    def __init__(
        self, name: str, line: int = None, col: int = None, length: int = None
    ):
        super().__init__(name, line, col, length)


class Lexer_Plus(Lexer_Operator):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Plus", line, col, 1)


class Lexer_Minus(Lexer_Operator):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Minus", line, col, 1)


class Lexer_Star(Lexer_Operator):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Star", line, col, 1)


class Lexer_Slash(Lexer_Operator):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Slash", line, col, 1)


class Lexer_Amp(Lexer_Operator):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Amp", line, col, 1)


class Lexer_Pipe(Lexer_Operator):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Pipe", line, col, 1)


class Lexer_Greater(Lexer_Operator):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Greater", line, col, 1)


class Lexer_Less(Lexer_Operator):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Less", line, col, 1)


class Lexer_Equals(Lexer_Operator):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Equals", line, col, 1)


class Lexer_Exclamation(Lexer_Operator):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Exclamation", line, col, 1)


#
# Punctionation
#


class Lexer_LParen(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_LParen", line, col, 1)


class Lexer_RParen(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_RParen", line, col, 1)


class Lexer_LBrace(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_LBrace", line, col, 1)


class Lexer_RBrace(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_RBrace", line, col, 1)


class Lexer_Semicolon(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Semicolon", line, col, 1)


class Lexer_Comma(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Comma", line, col, 1)


#
# Keywords
#


class Lexer_Const(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Const", line, col, 5)


class Lexer_Continue(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Continue", line, col, 8)


class Lexer_Else(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Else", line, col, 4)


class Lexer_If(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_If", line, col, 2)


class Lexer_Return(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Return", line, col, 6)


class Lexer_While(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_While", line, col, 5)


#
# Data Types
#


class Lexer_Data_Type(Lexer_Token):
    def __init__(
        self, name: str, line: int = None, col: int = None, length: int = None
    ):
        super().__init__(name, line, col, length)


class Lexer_Signed(Lexer_Data_Type):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Signed", line, col, 6)


class Lexer_Unsigned(Lexer_Data_Type):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Unsigned", line, col, 8)


class Lexer_Void(Lexer_Data_Type):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Void", line, col, 4)


#
# Other
#


class Lexer_Identifier(Lexer_Token):
    def __init__(
        self,
        id: int,
        symbol_table,
        line: int = None,
        col: int = None,
        length: int = None,
    ):
        super().__init__("Lexer_Identifier", line, col, length)
        self.id = id
        self.value = symbol_table[id]

    def __str__(self):
        return super().__str__()[:-1] + f", value: {self.value}, id: {self.id}>"


class Lexer_Literal(Lexer_Token):
    def __init__(
        self,
        value: int,
        symbol_table=None,
        line: int = None,
        col: int = None,
        length: int = None,
    ):
        super().__init__("Lexer_Literal", line, col, length)
        self.value = value

    def __str__(self):
        return super().__str__()[:-1] + f", value: {self.value}>"


class Lexer_Read(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Read", line, col, 4)


class Lexer_Write(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Write", line, col, 5)
