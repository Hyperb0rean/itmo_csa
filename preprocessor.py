from __future__ import annotations

import re


def remove_extra_spaces(line: str) -> str:
    line = line.replace("' '", str(ord(" ")))
    return re.sub(r"\s+", " ", line)

def remove_comments(line: str) -> str:
    return line if not line.startswith('#') else ''

def remove_commas(line: str) -> str:
    line = line.replace("','", str(ord(",")))
    return line.replace(",", " ")

def preprocessing(asm_text: str) -> str:
    lines: list[str] = asm_text.splitlines()
    strip_lines = map(str.strip, lines)
    removed_comments = map(remove_comments, strip_lines)
    remove_empty_lines = filter(bool, removed_comments)
    removed_commas = map(remove_commas, remove_empty_lines)
    remove_spaces = map(remove_extra_spaces, removed_commas)
    joined: str = "\n".join(remove_spaces)
    return joined
