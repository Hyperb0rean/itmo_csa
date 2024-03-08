from __future__ import annotations

from enum import Enum


class Opcode(str, Enum):
    HLT = "hlt"
    MOV = "mov"
    LD = "ld"
    ST = "st"
    INC = "inc"
    DEC = "dec"
    NEGR = "neg"
    ADD = "add"
    DIV = "div"
    MOD = "mod"
    CMP = "cmp"
    JUMP = "jmp"
    JG = "jg"
    JE = "je"
    IN = "in"
    OUT = "out"
    NOP = "nop"

    def __str__(self):
        return self.name


class Instruction:
    def __init__(self, opcode: Opcode, args: list[str] | None = None):
        if args is None:
            args = []
        self.opcode: Opcode = opcode
        self.args: list[str] = args

    def __str__(self):
        return f"({self.opcode} {self.args})"

    def __repr__(self):
        return self.__str__()
