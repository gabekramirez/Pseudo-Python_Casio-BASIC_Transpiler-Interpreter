# Pseudo-Python/Casio BASIC Transpiler & Interpreter

This is my own custom Python library ([casio_basic.py](casio_basic.py)), transpiler ([casio_transpiler.py](casio_transpiler.py)), and interpreter ([casio_interpreter.py](casio_interpreter.py)) I wrote to emulate Casio BASIC. The purpose of these programs is so that I can write my own programs for my Casio
fx-CG50 calculator in Python rather than Casio BASIC and then convert them to Casio BASIC. Although this calculator already supports programming
in Python, it is very limited compared to what you can do with Casio BASIC on it.


Table of Contents
=================
* [Casio fx-CG50 Calculator Manual](#casio-fx-cg50-calculator-manual)
* [casio_basic.py Documentation](#casio_basicpy)
  * [Constants (casio_basic.py)](#constants-casio_basicpy)
  * [Global Variables](#global-variables)
  * [Non-Casio Methods](#non-casio-methods)
  * [IO Methods](#io-methods)
  * [Math Methods](#math-methods)
  * [String Methods](#string-methods)
  * [List Methods](#list-methods)
* [casio_transpiler.py Documentation](#casio_transpilerpy)
  * [Constants (casio_transpiler.py)](#constants-casio_transpilerpy)
  * [Methods](#methods)
* [casio_interpreter.py Documentation](#casio_interpreterpy)
  * [Constants (casio_interpreter.py)](#constants-casio_interpreterpy)
* [Windows Build](#windows-build)
* [Web Build](#web-build)


## Casio fx-CG50 Calculator Manual

You can access the CASIO fx-CG50 calculator manual for reference at [www.casio.com/content/dam/casio/global/support/manuals/calculators/pdf/004-en/f/fx-CG50_Soft_v340_EN.pdf](https://www.casio.com/content/dam/casio/global/support/manuals/calculators/pdf/004-en/f/fx-CG50_Soft_v340_EN.pdf#page=297)

Pages 297 to 364 of the PDF covers the Casio BASIC programming app on the calculator.


## casio_basic.py

### Constants (casio_basic.py)
- DISPLAY_WIDTH: int = 21
- DISPLAY_HEIGHT: int = 7
- DISPLAY_SIZE: int = 147
- CHAR_W: int = 52
- CHAR_H: int = 72

### Global Variables
- A through Z: float = 0

### Non-Casio Methods
- get_keyboard_mapping_dict() -> dict\[int: int\]
- string_python_to_casio(text: str) -> str
- string_casio_to_python(text: str) -> str
- file_name_python_to_casio(text: str) -> str
- run(main: () -> None) -> None
- tick(times: int = 1) -> None
- stop() -> None

### IO Methods
- get_key() -> int
- ask(text: str, value_type: type) -> value_type
- clr_text() -> None
- show_str(text: str) -> None
- disps(text: str, *, break_up: bool = False, return_str: bool = False) -> None
- locate(x: int, y: int, text: str) -> None

### Math Methods
- frac(x: float | int) -> float
- mod(x: float | int, y: float | int) -> float

### String Methods
- get_str(str_id: int) -> str
- set_str(str_id: int, value: str) -> None
- str_mid(value: str, start: int, length: int) -> str

### List Methods
- get_dim_list(list_id: int) -> int
- set_dim_list(list_id: int, dim: int) -> None
- get_list(list_id: int, index: int) -> int | float
- set_list(list_id: int, index: int, value: float) -> None
- copy_list(list_to: int, list_from: int) -> None
- fill_list(list_id: int, value: float) -> None


## casio_transpiler.py

Transpiles Pseudo-Python to Casio BASIC.

Takes a command line argument for the source file (if none, defaults to SOURCE_FILE).

Puts the output file in the BUILD_PATH directory (creates BUILD_PATH directory if it doesn't already exist).

### Constants (casio_transpiler.py)
- SOURCE_FILE = "source/{}"  # The {} gets formatted with first file found in directory
- BUILD_PATH = "build"
- DEBUG: bool = True  # When True, main() prints preprocessed input and its transpiled output to the terminal
- COMPILE_FOR_INTERPRETER = True  # translates tick() -> Tick which aren't usually present in Casio BASIC but are accepted by the interpreter

### Methods
- compile_expression(expression: str, functions: list\[str\]) -> str | tuple\[str, int\]
- compile_line(line: str, functions: list\[str\]) -> str | tuple\[str, int\]
- python_to_casio(input_file: str) -> str


## casio_interpreter.py

Runs Casio BASIC code by interpreting it line by line.

Takes a command line argument for the Casio BASIC file (if none, defaults to BUILD_FILE).

### Constants (casio_interpreter.py)
- BUILD_FILE: str = "build/{}"  # The {} gets formatted with first file found in directory
- DEBUG: bool = True  # When True, main() prints instructions being ran and tokens as they're being processed
- INSTRUCTIONS_PER_FRAME: int = 100


## Windows Build

W.I.P. Section


## Web Build

W.I.P. Section
