# /bin/bash/python
import io
import re
from pathlib import Path

indentation_chars = [" ", "\n", "\r", "\t", "\v", "\f"]

global symbol_table
symbol_table = {}
global constant_table
constant_table = {}


class Symbol:
    def __init__(self, name: str, line: int, col: str):
        self.id = int(len(symbol_table) / 2)
        self.name = name
        self.line = line
        self.col = col
        self.is_initialized = False
        self.is_declared = False
        self.data_type = None
        self.type = None

    def __str__(self):
        return f'<symbol: "{self.name}" defined on line: {self.line}, col: {self.col}>'


def add_symbol(name: str, line: int, col: int):
    symbol = Symbol(name, line, col)
    id = symbol.id
    symbol_table[id] = symbol
    symbol_table[name] = id
    return id


from Lexer_Tokens import *
from Parser_Objects import *


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
        if string == "&&":
            return Lexer_Double_Amp
        if string == "|":
            return Lexer_Pipe
        if string == "||":
            return Lexer_Double_Pipe
        if string == ">":
            return Lexer_Greater
        if string == ">=":
            return Lexer_Greater_Equals
        if string == "<":
            return Lexer_Less
        if string == "<=":
            return Lexer_Less_Equals
        if string == "=":
            return Lexer_Equals
        if string == "==":
            return Lexer_Double_Equals
        if string == "!=":
            return Lexer_Exclamation_Equals
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
        if string == "break":
            return Lexer_Break

        # Other
        if string == "read":
            return Lexer_Read
        if string == "write":
            return Lexer_Write
        if re.search(r"^\d+[A-Za-z]\Z", string):
            raise (
                ValueError(
                    f"Identifier cannot begin with a number: line: {line}, col: {col-len(string)+1}, value: '{string}'"
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
    col = 0
    last_line = len(lines)
    global paren_count
    global brace_count
    paren_count = 0
    brace_count = 0

    def paren_checker():
        global paren_count
        if paren_count > 0:
            raise (Exception(f"Expected ')': line: {line}, col: {col}"))
        if paren_count < 0:
            raise (Exception(f"Missing '(': line: {line}, col: {col}"))

    def append_token(string, tokens, line, col):
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
                    value = symbol_table[string]
                else:
                    if not isinstance(tokens[-1], Lexer_Data_Type):
                        raise (
                            NameError(
                                f"Symbol: {string} is not declared, line: {line}, col: {col}"
                            )
                        )
                    value = add_symbol(string, line, col - len(string))
            else:
                value = string
            tokens.append(
                match(
                    value,
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

            tokens.append(match(line, col))
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
                    tokens = append_token(string, tokens, line, col)
                break
            match = check(buffer, line, col)
            if not match:
                string = buffer[:-1]
                tokens = append_token(string, tokens, line, col)
                buffer = buffer[-1:]
                if buffer in indentation_chars:
                    buffer = ""

    tokens = append_token(buffer, tokens, last_line, col + 1)

    paren_checker()
    if brace_count != 0:
        raise (Exception("Expected '}'"))
    if "main" not in symbol_table:
        raise (NameError("Program declares no Main function"))

    return tokens


def parse(tokens):
    def pop_token():
        if len(tokens) == 0:
            return Parser_TERMINATE
        token = tokens[0]
        tokens.remove(token)
        return token

    def peek_token(n: int = 1):
        return tokens[-1 + n]

    def expect_term(binding_power=0, LHS=None):
        parsed = parse_token(binding_power, LHS)
        if not isinstance(parsed, Parser_Term):
            raise (
                ValueError(
                    f"Expected to recieve a valid Parser Term near {peek_token()}, got: {parsed}"
                )
            )
        return parsed

    def parse_token(binding_power=0, LHS=None):
        current_token = pop_token()
        if (
            binding_power != None
            and LHS != None
            and binding_power >= getattr(current_token, "binding_power", 0)
            and not isinstance(current_token, Lexer_LParen)
        ):
            return LHS

        if isinstance(current_token, Lexer_Comma):
            raise (NotImplementedError("Comma"))

        if isinstance(current_token, Lexer_Semicolon):
            return current_token

        if isinstance(current_token, Lexer_LBrace):
            children = []
            while True:
                parsed_object = parse_token()
                if isinstance(parsed_object, Lexer_RBrace):
                    break
                if not any(
                    [parsed_object == None]
                    + [
                        isinstance(parsed_object, a)
                        for a in [
                            Parser_Assignment_Expression,
                            Parser_Function_Call,
                            Parser_Variable_Declaration,
                            Lexer_Semicolon,
                        ]
                    ]
                ):
                    raise (TypeError("Parser Block contains illegal code"))
                if isinstance(
                    parsed_object, Parser_Assignment_Expression
                ) or isinstance(parsed_object, Parser_Function_Call):
                    children.append(parsed_object)
            return Parser_Block(children)

        if isinstance(current_token, Lexer_RBrace):
            return current_token

        if isinstance(current_token, Lexer_LParen):
            is_function_call = (
                LHS != None
                and isinstance(LHS, Lexer_Identifier)
                and (LHS.symbol.type is Identifier_Type.function)
            )
            if not is_function_call:
                return expect_term()
            else:
                arguments = []
                if isinstance(peek_token(), Lexer_RParen):
                    pop_token()
                    return arguments
                while True:
                    arguments.append(expect_term())
                    parsed = parse_token()
                    if not isinstance(parsed, Lexer_Semicolon):
                        if isinstance(parsed, Lexer_RParen):
                            break
                        raise (
                            ValueError(
                                f"Function call argument list expected `;`, got: {parsed}"
                            )
                        )

                return arguments

        if isinstance(current_token, Lexer_RParen):
            return current_token

        if isinstance(current_token, Lexer_Literal):
            literal = Parser_Literal(current_token.value)
            next_token = peek_token()
            if isinstance(next_token, Lexer_Operator):
                return parse_token(binding_power, literal)
            return literal

        if isinstance(current_token, Lexer_Exclamation):
            if LHS != None:
                raise (ValueError("Unary Operator `!` cannot have an LHS"))
            return Parser_Unary_Expression(
                expect_term(Lexer_Exclamation.binding_power),
                Lexer_Exclamation,
            )

        if isinstance(current_token, Lexer_Equals):
            if not isinstance(LHS, Parser_Variable):
                raise (
                    ValueError(
                        f"Assignment expression expected an LHS variable, got: {LHS}"
                    )
                )
            if LHS in constant_table:
                raise (TypeError("`{LHS}` is a `const` and changed"))
            return Parser_Assignment_Expression(LHS, expect_term())

        if isinstance(current_token, Lexer_Identifier):
            if current_token.symbol.type == Identifier_Type.variable:
                variable = Parser_Variable(current_token.symbol)
                next_token = peek_token()
                if isinstance(next_token, Lexer_Operator):
                    return parse_token(binding_power, variable)
                return variable
            else:
                function_call = Parser_Function_Call(
                    current_token.symbol, parse_token(LHS=current_token)
                )
                next_token = peek_token()
                if isinstance(next_token, Lexer_Operator):
                    return parse_token(binding_power, function_call)
                return function_call

        if isinstance(current_token, Lexer_Data_Type):
            if isinstance(peek_token(2), Lexer_Semicolon):
                next_token = peek_token()
                if isinstance(next_token, Lexer_Identifier):
                    next_token.symbol.type = Identifier_Type.variable
                return Parser_Variable_Declaration(current_token, parse_token())
            else:
                next_token = pop_token()
                next_token.symbol.type = Identifier_Type.function
                arguments = parse_token(LHS=next_token)
                if isinstance(peek_token(), Lexer_LBrace):
                    block = parse_token()
                else:
                    block = None
                Parser_Function_Declaration(
                    getattr(next_token, "symbol", None),
                    current_token,
                    arguments,
                    block,
                )
                return

        # NOT DONE IMPLEMENTING, CONTINUE WRITING IF BLOCKS FOR EACH POSSIBLE LEXER TOKEN

        if any(
            [
                isinstance(current_token, lexer_class)
                for lexer_class in [
                    Lexer_Plus,
                    Lexer_Minus,
                    Lexer_Star,
                    Lexer_Slash,
                    Lexer_Amp,
                    Lexer_Double_Amp,
                    Lexer_Pipe,
                    Lexer_Double_Pipe,
                    Lexer_Greater,
                    Lexer_Greater_Equals,
                    Lexer_Less,
                    Lexer_Less_Equals,
                    Lexer_Exclamation_Equals,
                    Lexer_Double_Equals,
                ]
            ]
        ):
            if LHS == None:
                raise (ValueError(f"{current_token} expected an LHS, got: None"))
            return Parser_Binary_Expression(
                LHS, current_token, expect_term(current_token.binding_power)
            )

    tokens = [Lexer_LBrace()] + tokens + [Lexer_RBrace()]
    parsed_tree = parse_token()
    if not isinstance(parsed_tree, Parser_Block):
        raise (TypeError(f"Parser pass expected a Parser Block, got: {parsed_tree}"))
    if parsed_tree.children != []:
        raise (TypeError("Code cannot exist outside of function declarations"))
    if symbol_table[symbol_table["main"]].type != Identifier_Type.function:
        raise (TypeError("`main` must be a function"))
    return Parser_Function_Call(symbol_table[symbol_table["main"]], None)


if __name__ == "__main__":
    tokens = []
    with open(Path(__file__).parent / "in.legc") as source_code:
        tokens = lex(source_code)
    print("TOKENS:-----------------------\n")
    for token in tokens:
        print(token)
    abtract_syntax_tree = parse(tokens)
    print("\nParsed!-----------------------\n")
