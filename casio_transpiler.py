from casio_basic import disps, string_python_to_casio, file_name_python_to_casio
import os
import sys


SOURCE_FILE = "source/{}"  # {} gets formatted with first file found in directory
BUILD_PATH = "build"
DEBUG = False
COMPILE_FOR_INTERPRETER = True  # adds Tick statements which aren't usually present in Casio BASIC


_LABELS = "0123456789ABCDEFGHIJKLMNOPQRRSTUVWXYZ"
_COMPILE_OPERATORS = {" == ": "=",
                      " != ": "<>",
                      " < ": "<",
                      " > ": ">",
                      " <= ": "<=",
                      " >= ": ">=",
                      " + ": "+",
                      " - ": "-",
                      " * ": "*",
                      " / ": "/",
                      " ** ": "^",
                      " and ": " And ",
                      " or ": " Or ",
                      "int(": "Int (",
                      "frac(": "Frac (",
                      "abs(": "Abs (",
                      "get_key()": "Getkey"}
_COMPILE_FUNCTIONS = ["mod(", "ask(", "str_mid(", "get_str(", "get_list(", "get_dim_list("]


def compile_expression(expression: str, functions: list[str]) -> str | tuple[str, int]:
    expression = expression.strip()
    if expression == "True":
        return "1=1"
    elif expression == "False":
            return "0=1"
    elif expression.isdigit():
        return expression
    elif expression.startswith("\"") and expression[-1] == "\"":
        return string_python_to_casio(expression)
    elif expression.startswith("r\"") and expression[-1] == "\"":
        return compile_expression(expression[1:].replace("\\", "\\\\"), functions)
    else:
        for x, y in _COMPILE_OPERATORS.items():
            expression = expression.replace(x, y)
    for x in _COMPILE_FUNCTIONS:
        while x in expression:
            y = expression.find(x)
            i = y + len(x)
            j = 1
            while j > 0 and i < len(expression) - 1:
                i += 1
                if expression[i] == "(": j += 1
                if expression[i] == ")": j -= 1
            i += 1
            c = compile_line(expression[y:i], functions)
            if isinstance(c, tuple):
                c = c[0]
            expression = expression[:y] + c[:-1] + expression[i:]
    return expression


def compile_line(line: str, functions: list[str]) -> str | tuple[str, int]:
    line = line.lstrip().rstrip()

    if line.startswith("def "):
        prep = ""
        if functions.index(line[4:-1]) > 1:
            prep = "Goto Z\n"
        label = _LABELS[functions.index(line[4:-1])]
        return f"{prep}Lbl {label}\n", 0
    elif line.startswith("return ") or line in functions:
        if line.startswith("return "):
            line = line[7:]
            prepl = f"{functions.index(line)}->Z\n"
            prepr = ""
        else:
            prepl = f"Z*{len(_LABELS) * len(_LABELS)}+{len(functions) * len(_LABELS) + functions.index(line)}->Z\n"
            prepr = f"Lbl {_LABELS[len(functions)]}\n"
            functions.append(prepr)
        label = _LABELS[functions.index(line)]
        return f"{prepl}Goto {label}\n{prepr}", 0
    elif line.startswith("stop()"):
        return "", 0
    elif line.startswith("if "):
        if ": " in line:
            b = line.find(":")
            a = line[3:b]
            b = line[b + 2:]
            if "return" in line:
                return f"If {compile_expression(a, functions)}\nThen {compile_line(b, functions)[0]}IfEnd\n", 1
            else:
                return f"{compile_expression(a, functions)}=>{compile_line(b, functions)[0][:-1]}\n", 0
        else:
            line = line[3:line.find(":")]
            return f"If {compile_expression(line, functions)}\nThen ", 1
    if line.startswith("elif "):
        raise ValueError(f"elif statements should be broken into if-else chain:\nline")
    if line == "else:":
        return "Else ", 0
    elif line.startswith("for "):
        a = line[4]
        line = line[15:-2].split(", ")
        if len(line) == 2:
            line.append("1")
        b = line[1]
        if b.isdecimal():
            b = int(line[1]) - 1
        else:
            b = compile_expression(line[1], functions) + "+1"
        return f"For {line[0]}->{a} To {b} Step {line[2]}\n", 4
    elif line.startswith("while "):
        if ": " in line:
            line = line[6:line.find(":")]
            return f"While {compile_expression(line, functions)}\nWhileEnd\n", 0
        else:
            line = line[6:line.find(":")]
            return f"While {compile_expression(line, functions)}\n", 5

    elif line.startswith("mod("):
        line = line[4:].replace(", ", ",")
        return f"MOD({compile_expression(line, functions)})", 0

    elif COMPILE_FOR_INTERPRETER and line.startswith("tick("):
        if line.startswith("tick()"):
            n = 1
        else:
            n = int(line[5:].split(")")[0])
        return "Tick\n" * n, 0
    elif line == "clr_text()":
        return "ClrText\n", 0
    elif line.startswith("locate("):
        line = line[7:-1].split(", ")
        extra = ""
        if len(line) > 3:
            line[2] = ", ".join(line[2:])
        return f"Locate {line[0]},{line[1]},{compile_expression(line[2], functions)}\n" + extra, 0
    elif line.startswith("show_str("):
        return line[9:-1] + "\n", 0
    elif line.startswith("set_str("):
        b = line.find(", ")
        a = line[8:b]
        b = line[b + 2:-1]
        b = compile_expression(b, functions)
        return f"{b}->Str {a}\n", 0
    elif line.startswith("get_str("):
        line = line[line.find('(') + 1:line.find(')')]
        return f"Str {line}\n", 0
    elif line.startswith("str_mid("):
        line = line[8:].replace(", ", ",")
        return f"StrMid({compile_expression(line, functions)})", 0
    elif line.startswith("disps("):
        if line.endswith(", break_up=True)"):
            line = '"' + disps(line[7:-16], break_up=True, return_str=True)
        else:
            line = line[6:-1]
        return f"ClrText\n{compile_expression(line, functions)}Disps\n", 0
    elif line.startswith("ask("):
        return line[4:line.find(',')] + "? "

    elif line.startswith("get_dim_list("):
        a = line[13:-1]
        return f"Dim List {a}\n", 0
    elif line.startswith("set_dim_list("):
        line = line[13:-1].split(", ")
        return f"{line[1]}->Dim List {line[0]}\n", 0
    elif line.startswith("get_list("):
        b = line.find(", ")
        a = line[9:b]
        b = line[b + 2:-1]
        return f"List {a}[{compile_expression(b, functions)}]\n", 0
    elif line.startswith("set_list("):
        i = line.find(", ")
        a = line[9:i]
        b = line[i + 2:-1]
        j = b.find(", ")
        c = b[j + 2:]
        b = b[:j]
        return f"{compile_expression(c, functions)}->List {a}[{compile_expression(b, functions)}]\n", 0

    elif line[1:4] == " = ":
        return f"{compile_expression(line[4:], functions)}->{line[0]}\n", 0
    elif line[1:5] == " += ":
        return compile_line(f"{line[0]} = {line[0]} + {line[5:]}", functions)
    elif line[1:5] == " -= ":
        return compile_line(f"{line[0]} = {line[0]} - {line[5:]}", functions)

    elif line == "break":
        return "Break\n", 0
    return "", 0


def python_to_casio(input_file: str) -> str:
    compiled = ""
    tabs = []
    functions = ["stop()"]

    with open(input_file, 'r') as read_file:
        file: list[str] = read_file.readlines()

    while "\n" in file:
        file.remove("\n")
    i = 0
    while i < len(file):
        line = file[i]
        tab_count = line.count("    ", 0, len(line) - len(line.lstrip()))
        line = line.lstrip()
        if ";" in line:  # replace inline semicolons with newlines
            lines = line[:-1].split(";")
            lines.reverse()
            file.pop(i)
            for new_line in lines:
                file.insert(i, "    " * tab_count + new_line.lstrip() + "\n")
        elif line.startswith("def "):  # add each def to functions
            functions.append(line.rstrip()[4:-1])
        elif line.startswith("elif "):  #  replace elif with else: if
            file.insert(i + 1, file[i].replace("elif", "if"))
            file[i] = "    " * (tab_count - 1) + "else:\n"
            j = i + 1
            t = tab_count + 1
            while t > tab_count:
                j += 1
                l = file[j]
                t = l.count("    ", 0, len(l) - len(l.lstrip()))
                l = l.lstrip()
                if l.startswith("elif ") or l.startswith("else:"):
                    t += 1
            for j in range(i, j):
                file[j] = "    " + file[j]
        i += 1

    if len(functions) >= len(_LABELS):
        raise ValueError(f"More functions defined ({len(functions)}) "
                         f"than labels available ({len(_LABELS) - 1}).")

    main_function = functions.index("main()")
    compiled += f"0->Z\nGoto {main_function}\nLbl Z\n"
    for index, label in enumerate(_LABELS[0:-1]):
        compiled += f"If MOD(Z,{len(_LABELS)})={index}\nThen Int (Z/{len(_LABELS)})->Z\nGoto {label}\nIfEnd\n"
    x = compiled[:-1].replace("\n", "\n" + " " * 19)
    if DEBUG: print(f"START OF FILE ---> {x}")

    for j, line in enumerate(file):
        line = line[:-1]

        a = line
        a = a.count("    ", 0, len(a) - len(a.lstrip()))
        if "else:" in line:
            a += 1
        b = file[j - 1]
        b = b.count("    ", 0, len(b) - len(b.lstrip()))
        for _ in range(b - a):
            if len(tabs) > 0:
                x = tabs[-1]
                if x != -1:
                    if x == 1:
                        x = "IfEnd\n"
                    elif x == 4:
                        x = "Next\n"
                    elif x == 5:
                        x = "WhileEnd\n"
                    else:
                        x = "ERROR\n"
                    compiled += x
                    if DEBUG: print(a * "    " + f"BREAK TAB ---> {x[:-1]}")
                tabs.pop(-1)

        if "  # *" in line:
            a = line
            a = a.count("    ", 0, len(a) - len(a.lstrip()))
            b = file[j + 1]
            b = b.count("    ", 0, len(b) - len(b.lstrip()))
            if b > a:
                for _ in range(b - a):
                    tabs.append(-1)
            line = line[line.find("  # *") + 5:]
            compiled += line + "\n"
            if DEBUG: print(f"{file[j][:-1]} ---> {line}")
        else:
            line = line.lstrip()
            if "  # " in line and ("\"" not in line or line.rindex("\"") < line.rindex("  # ")):
                line = line[:line.rfind("  #")]
            if line == 'if __name__ == "__main__":':
                break
            else:
                x, y = compile_line(line, functions)
                if y != 0:
                    tabs.append(y)
                compiled += x
                if x: x = x[:-1].replace("\n", "\n      " + " " * len(file[j][:-1]))
                if DEBUG: print(f"{file[j][:-1]} ---> {x}" if x else file[j][:-1])
    compiled += "Goto Z\nLbl 0"
    if DEBUG: print(f"END OF FILE ---> Goto Z\n                 Lbl 0")
    return compiled


def main():
    if len(sys.argv) == 1:
        file_name = SOURCE_FILE
        if "{}" in file_name:
            file_name = file_name.format(os.listdir(os.path.dirname(file_name))[0])
    elif len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        raise IndexError(f"Expected 0 or 1 command line arguments.\nGot {len(sys.argv) - 1}")

    output_file = file_name_python_to_casio(file_name)
    output_file_data = python_to_casio(file_name)
    if not os.path.isdir(BUILD_PATH):
        os.mkdir(BUILD_PATH)
    with open(os.path.join(BUILD_PATH, output_file) + ".txt", "w") as file:
        file.write(output_file_data)


if __name__ == "__main__":
    main()
