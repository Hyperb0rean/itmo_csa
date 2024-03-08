# Лабораторная работа № 3

- Сосновцев Григорий Алексеевич P33102
- `alg -> asm | cisc -> risc | harv | mc -> hw | tick -> instr | struct | stream | mem | pstr | prob1 | 8bit`
- С упрощением

##  YAASM - Yet Another ASM

### Синтаксис

```
program ::= <section_code> <section_data> | <section_data> <section_code> | <section_code>
<section_data> ::= "section .data:" <data>
<section_code> ::= "section .code:" <code>
<data> ::= (<comment> | <variable>) <data>
<comment> ::= "#" <text>
<code> ::= (<comment> | <label> | <instruction>) <code>
<name> ::= [a-zA-Z]+
<label> ::= "."<name> ":"
<variable> ::= <name> ":" (<int> | <string>)
<reg=> ::= "x1" | "x2" | "x3" | "x4" | "x5" | "x6" | "x7" | "x8 | "x9" | "x10" | "x11" | "x12" | "x14" | "x15""
<string> ::= '"' <character>* '"'
<character> ::= any printable ASCII character
<int> ::= <digit>+
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<bin_ops> ::= ("cmp" | "ld" | "st" | "mov" | "add" | "mod" | "div") " " ((<reg> ", " <reg>) | (<reg> ", " "(" <name> ")") | ("(" <name> ")" ", " <reg>))
<un_ops> ::= ("inc" | "dec" | "neg") " "  (<reg>)
<branch> ::= ("jmp" | "je" | "jg") " " (<label>)
<zero_arg> ::= ("hlp" | "nop")
<instruction> ::= <bin_ops> | <un_ops> | <branch> | <zero_arg>
```

### Описание

- Поддержка строковых и числовых литералов
- Поддержка комментариев и меток
- Переменные объявляются в секции `.data`, инструкции в секции `.code`
- Точка входа объявляется меткой `.start`

### Набор инструкции

| Инструкция    | Такты |
|---------------|-------|
| mov reg, reg  | 4     |
| ld reg, [reg] | 5     |
| st [reg], reg | 5     |
| inc reg       | 3     |
| dec reg       | 3     |
| neg reg       | 3     |
| add reg, reg  | 3     |
| div reg, reg  | 3     |
| mod reg, reg  | 3     |
| cmp reg, reg  | 3     |
| jmp label     | 2     |
| jg label      | 2     |
| je label      | 2     |
| in reg, port  | 4     |
| out port, reg | 4     |

### Пример программы выводящий `Hello world!`

```yaasm
section .data
# It is definitly Hello World!
    hello_str: "hello, world!"
section .code
.start:
    mov x4, 0
    mov x5, hello_str
.reload:
    ld x6, [x5]
    cmp x4, x6
    je .exit
    out 1, x6
    inc x5
    jmp .reload
.exit:
    hlt
```

Компилируется в `JSON` следующего формата:

```json
{
    "data_mem": {
        "0": 104,
        "1": 101,
        "2": 108,
        "3": 108,
        "4": 111,
        "5": 32,
        "6": 119,
        "7": 111,
        "8": 114,
        "9": 108,
        "10": 100,
        "11": 33,
        "12": 0
    },
    "start": 0,
    "code_mem": {
        "0": {
            "opcode": "mov",
            "args": [
                "x4",
                "0"
            ]
        },
        "1": {
            "opcode": "mov",
            "args": [
                "x5",
                "0"
            ]
        },
        "2": {
            "opcode": "ld",
            "args": [
                "x6",
                "x5"
            ]
        },
        "3": {
            "opcode": "cmp",
            "args": [
                "x4",
                "x6"
            ]
        },
        "4": {
            "opcode": "je",
            "args": [
                "8"
            ]
        },
        "5": {
            "opcode": "out",
            "args": [
                "1",
                "x6"
            ]
        },
        "6": {
            "opcode": "inc",
            "args": [
                "x5"
            ]
        },
        "7": {
            "opcode": "jmp",
            "args": [
                "2"
            ]
        },
        "8": {
            "opcode": "hlt",
            "args": []
        }
    }
}
```

- data_mem - память данных
- code_mem - память инструкций
- start - точка входа в памяти инструкций

## Организация памяти:

Гарвардская архитектура, память данных и память команд разделена.
Данные и инструкции располагаются в начале соответствующих себе адресных пространств.
При инициализации процессора `x2` устанавливается на последний адрес памяти данных.

### Память данных

Массив 32-х битных слов, реализуется используя `list[int]`.
При старте симуляции инициализируется нулевыми значениями.

- Строковые литералы выделяются статически при компиляции в Pascal String.

### Память команд

Реализуется с использованием `list[Instruction]`.
При старте симуляции инициализируется `nop` инструкциями.

### Регистры

`x0` - hardwared zero
`x1` - reserved
`x2` - stack pointer
`x3` - global pointer
`x4 - x15` - регистры общего назначения

## Транслятор

- Формат запуска: `./translator.py hello_user.yaasm hello_user.json`
  Реализован в [translator.py](translator.py).
  Компиляция осуществляется в 4 прохода по тексту программы: 
- Проход препроцессора: удаление пустых строк и комментариев
- Проход по секции `.data`: преобразовывает данные в словарь `переменная -> адрес в памяти данных`.
- Первый проход по секции `.code`: получает словарь `метка -> адрес в памяти команд`.
- Второй проход по секции `.code`: подставляет все переменные и метки используя словари полученные на этапах выше.

## Модель процессора

- Формат запуска: ` ./vm.py hello_user.json ./my_name`
  Реализована в [vm.py](vm.py)

### Схема

![scheme.jpg](doc%2Fscheme.jpg)

- choose port - выбор порта для работы с IO
- write io - запись в выбранное устройство
- read io чтение с выбранного устройства
- choose op - выбор операции на АЛУ
- latch reg - защелкнуть регистр
- sel regs - выбор в мультиплексорe
- sel ip - выбор в мультиплексоре регистра IP
- write data - запись в память данных
- read data - чтение памяти данных
- read instruction - чтение памяти инструкций

## Тестирование

Тестирование производится набором **golden** тестов, реализация в директории: [tests](tests).
Тестируются следующие алгоритмы:

- cat
- hello
- hello_user_name
- prob1

Исходные коды алгоритмов находятся в:
[sources](examples/sources)
