import json
from enum import Enum

INT_MIN = -2147483648
INT_MAX = 2147483647

USER_REGISTERS = ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "x10", "x11", "x12", "x14", "x15"]


class Register(str, Enum):
    X0 = "x0"
    X1 = "x1"
    X2 = "x2"
    X3 = "x3"
    X4 = "x4"
    X5 = "x5"
    X6 = "x6"
    X7 = "x7"
    X8 = "x8"
    X9 = "x9"
    X10 = "x10"
    X11 = "x11"
    X12 = "x12"
    X13 = "x13"
    X14 = "x14"
    X15 = "x15"

    def __str__(self):
        return self.name

ZERO = Register.X0
SP = Register.X2
IP = Register.X3


def is_register(arg: str) -> bool:
    return arg in USER_REGISTERS


class RegisterEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Register):
            return "X" + str(obj.value)
        return super().default(obj)


def convert_to_register(arg):
    if arg and isinstance(arg, str) and arg.startswith("X"):
        return Register[arg]
    return arg


def to_hex(hx: str) -> int:
    return int(hx,16) - 2**32

class InvalidSymbolsError(Exception):
    def __init__(self, got, expected):
        self.token = got
        self.expected = expected

    def __str__(self):
        return f"Got invalid symbols or tokens: {self.token}, expected: {self.expected}"
