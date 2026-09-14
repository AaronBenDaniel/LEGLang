# /bin/bash/python
import io
import re
from Lexer_Tokens import *

indentation_chars = [" ", "\n", "\r", "\t", "\v", "\f"]


class symbol:
    def __init__(self, value: str, line: int, col: str):
        self.value = value
        self.line = line
        self.col = col

    def __str__(self):
        return f'<symbol: "{self.value}" defined on line: {line}, col: {col}>'


def add_symbol(name):
    id = int(len(symbol_table) / 2)
    symbol_table[id] = name
    symbol_table[name] = id
    return id


global symbol_table
symbol_table = {}


def lex(source_code: io.TextIOWrapper):
    def check(string: str, line: int, col: int):
        # Operators
        if string == "+":
            return Lexer_Plus
        if string == "-":
            return Lexer_Minus
        if string == "*":
            return Lexer_Star
        if string == "/":
            return Lexer_Slash
        if string == "&":
            return Lexer_Amp
        if string == "|":
            return Lexer_Pipe
        if string == ">":
            return Lexer_Greater
        if string == "<":
            return Lexer_Less
        if string == "=":
            return Lexer_Equals
        if string == "!":
            return Lexer_Exclamation

        # Punctuation
        if string == "(":
            return Lexer_LParen
        if string == ")":
            return Lexer_RParen
        if string == "{":
            return Lexer_LBrace
        if string == "}":
            return Lexer_RBrace
        if string == ";":
            return Lexer_Semicolon
        if string == ",":
            return Lexer_Comma

        # Keywords
        if string == "const":
            return Lexer_Const
        if string == "continue":
            return Lexer_Continue
        if string == "else":
            return Lexer_Else
        if string == "if":
            return Lexer_If
        if string == "return":
            return Lexer_Return
        if string == "signed":
            return Lexer_Signed
        if string == "unsigned":
            return Lexer_Unsigned
        if string == "void":
            return Lexer_Void
        if string == "while":
            return Lexer_While

        if re.search(r"^\d+[A-Za-z]\Z", string):
            raise (
                ValueError(
                    f"Identifier cannot begin with a number: line: {line}, col: {col-len(string)+1}"
                )
            )
        if re.search(r"^\d+\Z", string):
            return Lexer_Literal
        if re.search(r"^[A-Za-z][A-Za-z\d]*\Z", string):
            return Lexer_Identifier

        return None

    tokens = []
    lines = [line for line in source_code]
    line = 0
    last_line = len(lines)
    global paren_count
    global brace_count
    paren_count = 0
    brace_count = 0

    def paren_checker():
        global paren_count
        if paren_count != 0:
            raise (Exception(f"Expected ')': line: {line}, col: {col}"))

    def append_token(string, tokens):
        global symbol_table
        global paren_count
        global brace_count
        if not any([char not in indentation_chars for char in string]):
            return tokens
        match = check(string, line, col)
        if match == None:
            raise (
                Exception(f"Something went wrong: line: {line}, col: {col}: {buffer}")
            )
        if match in [Lexer_Literal, Lexer_Identifier]:
            length = len(string)
            if match is Lexer_Identifier:
                if string in symbol_table:
                    string = symbol_table[string]
                else:
                    string = add_symbol(string)
            tokens.append(
                match(
                    string,
                    line=line,
                    col=col,
                    length=length,
                    symbol_table=symbol_table,
                )
            )
        else:
            if match == Lexer_LParen:
                paren_count += 1
            elif match == Lexer_RParen:
                paren_count -= 1
            elif match == Lexer_LBrace:
                brace_count += 1
            elif match == Lexer_RBrace:
                brace_count -= 1
            elif match == Lexer_Semicolon:
                paren_checker()

            tokens.append(match(line, col - 1))
        return tokens

    for ln in lines:
        line += 1
        col = 0
        buffer = ""
        last_char = len(ln)
        for char in ln:
            col += 1
            buffer += char
            if char == "#":
                string = buffer[:-1]
                if string:
                    tokens = append_token(string, tokens)
                break
            match = check(buffer, line, col)
            if not match or (col == last_char and line == last_line):
                string = buffer[:-1]
                tokens = append_token(string, tokens)
                buffer = buffer[-1:]
                if buffer in indentation_chars:
                    buffer = ""

    tokens = append_token(buffer, tokens)

    paren_checker()
    if brace_count != 0:
        raise (Exception("Expected '}'"))

    return tokens


if __name__ == "__main__":
    with open("./LEGCCompiler/in.legc") as source_code:
        tokens = lex(source_code)
    for token in tokens:
        print(token)
