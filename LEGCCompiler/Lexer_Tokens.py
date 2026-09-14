class Lexer_Token:
    def __init__(
        self, name: str, line: int = None, col: int = None, length: int = None
    ):
        self.name = name
        self.line = line
        self.col = col - length
        self.length = length

    def __str__(self):
        return f'<Lexer_Token: "{self.name}" at line: {self.line}, col: {self.col}>'


#
# Operators
#


class Lexer_Plus(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Plus", line, col, 1)

    def __str__(self):
        return super().__str__()


class Lexer_Minus(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Minus", line, col, 1)

    def __str__(self):
        return super().__str__()


class Lexer_Star(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Star", line, col, 1)

    def __str__(self):
        return super().__str__()


class Lexer_Slash(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Slash", line, col, 1)

    def __str__(self):
        return super().__str__()


class Lexer_Amp(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Amp", line, col, 1)

    def __str__(self):
        return super().__str__()


class Lexer_Pipe(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Pipe", line, col, 1)

    def __str__(self):
        return super().__str__()


class Lexer_Greater(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Greater", line, col, 1)

    def __str__(self):
        return super().__str__()


class Lexer_Less(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Less", line, col, 1)

    def __str__(self):
        return super().__str__()


class Lexer_Equals(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Equals", line, col, 1)

    def __str__(self):
        return super().__str__()


class Lexer_Exclamation(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Exclamation", line, col, 1)

    def __str__(self):
        return super().__str__()


#
# Punctionation
#


class Lexer_LParen(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_LParen", line, col, 1)

    def __str__(self):
        return super().__str__()


class Lexer_RParen(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_RParen", line, col, 1)

    def __str__(self):
        return super().__str__()


class Lexer_LBrace(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_LBrace", line, col, 1)

    def __str__(self):
        return super().__str__()


class Lexer_RBrace(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_RBrace", line, col, 1)

    def __str__(self):
        return super().__str__()


class Lexer_Semicolon(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Semicolon", line, col, 1)

    def __str__(self):
        return super().__str__()


class Lexer_Comma(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Comma", line, col, 1)

    def __str__(self):
        return super().__str__()


#
# Keywords
#


class Lexer_Const(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Const", line, col, 5)

    def __str__(self):
        return super().__str__()


class Lexer_Continue(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Continue", line, col, 8)

    def __str__(self):
        return super().__str__()


class Lexer_Else(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Else", line, col, 4)

    def __str__(self):
        return super().__str__()


class Lexer_If(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_If", line, col, 2)

    def __str__(self):
        return super().__str__()


class Lexer_Return(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Return", line, col, 6)

    def __str__(self):
        return super().__str__()


class Lexer_Signed(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Signed", line, col, 6)

    def __str__(self):
        return super().__str__()


class Lexer_Unsigned(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Unsigned", line, col, 8)

    def __str__(self):
        return super().__str__()


class Lexer_Void(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_Void", line, col, 4)

    def __str__(self):
        return super().__str__()


class Lexer_While(Lexer_Token):
    def __init__(self, line: int = None, col: int = None):
        super().__init__("Lexer_While", line, col, 5)

    def __str__(self):
        return super().__str__()


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
