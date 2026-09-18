from __main__ import Symbol
from Lexer_Tokens import *
from enum import Enum


class Identifier_Type(Enum):
    variable = "variable"
    function = "function"


class Parser_Object:
    def __init__(self):
        self.children: list[Parser_Object] = None


class Parser_Block(Parser_Object):
    def __init__(self, children: list[Parser_Object]):
        self.children = children


class Parser_Term(Parser_Object):
    def __init__(self):
        pass


class Parser_Read(Parser_Term):
    def __init__(self):
        pass


class Parser_Literal(Parser_Term):
    def __init__(self, value: int):
        if not isinstance(value, int):
            raise (ValueError("Parser Literal must be an Integer"))
        self.value = value


class Parser_Variable(Parser_Term):
    def __init__(self, symbol: Symbol):
        if not isinstance(symbol, Symbol):
            raise (ValueError("Parser Variable symbol must be a valid Symbol"))
        self.symbol = symbol


class Parser_Binary_Expression(Parser_Term):
    def __init__(
        self, LValue: Parser_Term, operator: Lexer_Operator, RValue: Parser_Term
    ):
        if not isinstance(LValue, Parser_Term):
            raise (
                ValueError(
                    "Parser Binary Expression LValue must be a valid Parser Term"
                )
            )
        if not isinstance(operator, Lexer_Operator):
            raise (
                ValueError(
                    "Parser Binary Expression Operator must be a valid Lexer Operator"
                )
            )
        if not isinstance(RValue, Parser_Term):
            raise (
                ValueError(
                    "Parser Binary Expression RValue must be a valid Parser Term"
                )
            )
        self.LValue = LValue
        self.operator = operator
        self.RValue = RValue


class Parser_Unary_Expression(Parser_Term):
    def __init__(self, value: Parser_Term, operator: Lexer_Operator):
        if not isinstance(value, Parser_Term):
            raise (
                ValueError("Parser Unary Expression value must be a valid Parser Term")
            )
        if not isinstance(operator, Lexer_Operator):
            raise (
                ValueError(
                    "Parser Unary Expression Operator must be a valid Lexer Operator"
                )
            )
        self.value = value
        self.operator = operator


class Parser_Assignment_Expression(Parser_Binary_Expression):
    def __init__(self, variable: Parser_Variable, value: Parser_Term):
        if not isinstance(variable, Parser_Variable):
            raise (
                ValueError(
                    "Parser Assignemnt Expression variable must be a valid Parser Varaible"
                )
            )
        if not isinstance(value, Parser_Term):
            raise (
                ValueError(
                    "Parser Assignemnt Expression value must be a valid Parser Term"
                )
            )
        self.variable = variable
        self.value = value
        self.variable.symbol.is_initialized = True


class Parser_Variable_Declaration(Parser_Object):
    def __init__(self, data_type: Lexer_Data_Type, variable: Parser_Variable):
        if not isinstance(variable, Parser_Variable):
            raise (
                ValueError(
                    "Parser Variable Declaration variable must be a valid Parser Variable"
                )
            )
        if variable.symbol.is_declared == True:
            raise (NameError(f"Redeclaration of '{symbol}"))
        if not isinstance(data_type, Lexer_Data_Type):
            raise (
                ValueError(
                    "Parser Variable Declaration data type must be a valid Lexer Data Type"
                )
            )
        self.data_type = data_type
        self.variable = variable
        self.variable.symbol.is_declared = True
        self.variable.symbol.data_type = data_type
        self.variable.symbol.type = Identifier_Type.variable


class Parser_Function_Declaration(Parser_Object):
    def __init__(
        self,
        symbol: Symbol,
        data_type: Lexer_Data_Type,
        arguments: list[Parser_Variable_Declaration],
        block: Parser_Block = None,
    ):

        if not isinstance(symbol, Symbol):
            raise (
                ValueError("Parser Function Declaration symbol must be a valid Symbol")
            )
        if (symbol.is_declared and (not symbol.is_initialized)) or (
            symbol.type is Identifier_Type.variable
        ):
            raise (NameError(f"Redeclaration of '{symbol}"))
        if symbol.is_initialized == True:
            raise (NameError(f"Redefinition of '{symbol}"))
        if not isinstance(data_type, Lexer_Data_Type):
            raise (
                ValueError(
                    "Parser Function Declaration data type must be a valid Lexer Data Type"
                )
            )
        if (not isinstance(block, Parser_Block)) and (block is not None):
            raise (
                ValueError(
                    "Parser Function Declaration block must be a valid Parser Block"
                )
            )
        try:
            if not all(
                [
                    isinstance(argument, Parser_Term)
                    for argument in (arguments if arguments is not None else [])
                ]
            ):
                raise (
                    ValueError(
                        "Parser Function Declaration arguments must be valid Parser Terms"
                    )
                )
        except:
            raise (
                ValueError(
                    "Parser Function Declaration arguments must be valid Parser Terms"
                )
            )
        self.symbol = symbol
        self.symbol.block = block
        self.symbol.type = Identifier_Type.function
        self.symbol.is_declared = True
        self.symbol.data_type = data_type
        self.symbol.argument_data_types = [
            argument.variable.data_type
            for argument in (arguments if arguments is not None else [])
        ]
        if block is not None:
            self.symbol.is_initialized = True


class Parser_Function_Call(Parser_Object):
    def __init__(
        self,
        symbol: Symbol,
        arguments: list[Parser_Term],
    ):
        if not isinstance(symbol, Symbol):
            raise (ValueError("Parser Function Call symbol must a symbol"))
        if not symbol.is_initialized:
            raise (
                NameError(
                    f"Parser Function '{symbol}' must be defined before being called"
                )
            )
        if arguments == None:
            arguments = []
        if not all([isinstance(argument, Parser_Term) for argument in arguments]):
            raise (
                ValueError("Parser Function Call arguments must be valid Parser Terms")
            )
        self.symbol = symbol
        self.arguments = arguments


class Parser_Else(Parser_Object):
    def __init__(self, block: Parser_Block):
        if not isinstance(block, Parser_Block):
            raise (ValueError("Parser Else block must be a valid Parser Block"))
        self.block = block


class Parser_If(Parser_Object):
    def __init__(
        self,
        conditional: Parser_Term,
        block: Parser_Block,
        else_branch: Parser_Else = None,
    ):
        if not isinstance(conditional, Parser_Term):
            raise (ValueError("Parser If conditional must be a valid Parser Term"))
        if not isinstance(block, Parser_Block):
            raise (ValueError("Parser If block must be a valid Parser Block"))
        if else_branch is not None and not isinstance(else_branch, Parser_Else):
            raise (ValueError("Parser If else branch must be a valid Parser Else"))
        self.conditional = conditional
        self.block = block
        self.else_branch = else_branch


class Parser_TERMINATE(Parser_Object):
    def __init__(self):
        pass
