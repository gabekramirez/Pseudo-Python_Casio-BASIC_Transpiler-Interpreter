from pygame import *
from casio_basic import *
import os
import sys
import asyncio


RUN_FILE = "./{}"  # {} gets formatted with first file found in directory
DEBUG = False
INSTRUCTIONS_PER_FRAME = 100


_FUNCTIONS = ("ClrText", "Prog ", "Int (", "Frac (", "Abs (", "MOD(", "StrMid(", "Locate ", "Dim ", "List ")
_OPERATORS = ("^", "*", "/", "+", "-", "=", "<>", "<", ">", "<=", ">=", " And ", " Or ", "=>", "->", "?", "Disps")


async def main():
    if len(sys.argv) == 1:
        file_name = RUN_FILE
        if "{}" in file_name:
            directory = os.path.dirname(file_name)
            directory_files = [f for f in os.listdir(directory) if f.endswith(".txt")]
            file_name = file_name.format(directory_files[0])
    elif len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        raise IndexError(f"Expected 0 or 1 command line arguments.\nGot {len(sys.argv) - 1}")

    with open(file_name, "r") as file_data:
        file = "".join(file_data.readlines()).split("\n")

    def update_pygame_display(*, toggle_fullscreen: bool = False, reset: bool = False) -> surface:
        nonlocal screen, fullscreen, previous_screen_size
        if toggle_fullscreen:
            if not fullscreen:
                _pygame_previous_screen_size = display.get_window_size()
            fullscreen = not fullscreen
        if reset:
            display.quit()
            display.init()
            fullscreen = False
            _pygame_previous_screen_size = (640, 360)
        screen = display.set_mode((1920, 1080) if fullscreen else previous_screen_size,
                                  FULLSCREEN if fullscreen else RESIZABLE)
        display.set_caption("Pseudo Python")

    init()
    clock = time.Clock()
    display.set_caption("Casio BASIC")
    screen = Surface((0, 0))
    fullscreen = False
    previous_screen_size = (640, 360)
    update_pygame_display(reset=True)
    display_screen = Surface((DISPLAY_WIDTH * CHAR_W, DISPLAY_HEIGHT * CHAR_H))
    display_text: str = " " * DISPLAY_SIZE
    display_font = font.Font("casio.ttf", 64)
    keyboard_mapping = get_keyboard_mapping_dict()
    variables = {variable: 0 for variable in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    strings = {string_index: "" for string_index in range(1, 26)}
    lists = [[0] for _ in range(26)]
    getkey = 0
    answer: None | str = None
    answering = 0
    in_else = False
    for_loop_next = False

    def interpret(position: int) -> int:
        nonlocal display_text, answer, answering, in_else, for_loop_next
        code = file[position]
        tokenized: list[tuple[str, any]] = []
        token = ""
        code_index = 0
        while code_index < len(code):
            token += code[code_index]
            if token == "\"":
                token = ""
                code_index += 1
                while code[code_index] != "\"":
                    token += code[code_index]
                    code_index += 1
                tokenized.append(("String", string_casio_to_python(token)))
                token = ""
            elif token in "1234567890.":
                code_index += 1
                while code_index < len(code) and code[code_index] in "1234567890.":
                    token += code[code_index]
                    code_index += 1
                if (len(tokenized) > 0 and tokenized[-1] == ("Operator", "-") and
                   (len(tokenized) == 1 or tokenized[-2][0] != "Number")):
                    token = "-" + token
                    tokenized.pop(-1)
                if len(tokenized) > 0 and tokenized[-1][0] == "Variable String":
                    tokenized.pop(-1)
                    if len(tokenized) > 0 and tokenized[-1] == ("Operator", "->"):
                        tokenized.append(("Variable String", int(token)))
                    else:
                        tokenized.append(("String", strings[int(token)]))
                elif "." in token:
                    tokenized.append(("Number", float(token)))
                else:
                    tokenized.append(("Number", int(token)))
                token = ""
                code_index -= 1
            elif token in variables.keys() and (len(code) == code_index + 1 or
                                                (len(code) > code_index + 1 and not code[code_index + 1].isalpha())):
                if len(tokenized) > 0 and tokenized[-1] == ("Operator", "->"):
                    tokenized.append(("Variable", token))
                else:
                    if (len(tokenized) > 0 and tokenized[-1] == ("Operator", "-") and
                       (len(tokenized) == 1 or (tokenized[-2][0] != "Number" and
                       (tokenized[-2][0] != "Syntax" or tokenized[-2][1] == ",")))):
                        factor = -1
                        tokenized.pop(-1)
                    else:
                        factor = 1
                    tokenized.append(("Number", variables[token] * factor))
                token = ""
            elif token == "Str ":
                tokenized.append(("Variable String", 0))
                token = ""
            elif token in _FUNCTIONS:
                tokenized.append(("Function", token))
                token = ""
            elif token == "Getkey":
                tokenized.append(("Number", getkey))
                token = ""
            elif token == "Goto ":
                tokenized.append(("Goto", code[code_index + 1]))
                token = ""
                code_index += 1
            elif token in _OPERATORS:
                if len(tokenized) > 0 and tokenized[-1][0] == "Operator" and tokenized[-1][1] + token in _OPERATORS:
                    token = tokenized[-1][1] + token
                    tokenized.pop(-1)
                tokenized.append(("Operator", token))
                token = ""
            elif token in ("If ", "Then ", "Else ", "IfEnd", "While ", "WhileEnd",
                           "For ", " To ", " Step ", "Next", "Break"):
                if token != "Then ":
                    tokenized.append(("Control", token))
                token = ""
            elif token in (",", "(", ")", "[", "]"):
                tokenized.append(("Syntax", token))
                token = ""
            code_index += 1
        if DEBUG: print(f"{line + 1}|{code} {tokenized}")

        last_tokenized = None
        while len(tokenized) > 0:
            if DEBUG: print(tokenized)
            if tokenized == last_tokenized:
                raise RecursionError
            last_tokenized = tokenized.copy()

            code_index = 0
            while code_index < len(tokenized):
                if code_index < 2 or tokenized[code_index - 1] != ("Operator", "->"):
                    if tokenized[code_index] == ("Function", "Dim "):
                        a = tokenized[code_index + 2][1] - 1
                        tokenized[code_index] = ("Number", len(lists[a]))
                        tokenized.pop(code_index + 1)
                        tokenized.pop(code_index + 1)
                    elif (tokenized[code_index] == ("Function", "List ") and code_index + 4 < len(tokenized) and
                          tokenized[code_index + 4] == ("Syntax", "]") and
                          tokenized[code_index - 1] != ("Function", "Dim ")):
                        a = tokenized[code_index + 1][1] - 1
                        b = tokenized[code_index + 3][1] - 1
                        tokenized[code_index] = ("Number", lists[a][b])
                        tokenized.pop(code_index + 1)
                        tokenized.pop(code_index + 1)
                        tokenized.pop(code_index + 1)
                        tokenized.pop(code_index + 1)
                code_index += 1

            if tokenized[0][0] == "Control":
                token = tokenized[0][1]
                if token == "If " and len(tokenized) == 2:
                    if tokenized[1][1]:
                        return position + 1
                    else:
                        depth = 0
                        while depth >= 0:
                            position += 1
                            code = file[position]
                            if depth == 0 and code.startswith("Else "):
                                in_else = True
                                break
                            elif code.startswith("If ") or code.startswith("Then If ") or code.startswith("Else If "):
                                depth += 1
                            elif code.startswith("IfEnd"):
                                depth -= 1
                        return position
                elif token == "Else ":
                    if in_else:
                        tokenized.pop(0)
                        in_else = False
                    else:
                        depth = 0
                        while depth >= 0:
                            position += 1
                            code = file[position]
                            if code.startswith("If ") or code.startswith("Then If ") or code.startswith("Else If "):
                                depth += 1
                            elif code.startswith("IfEnd"):
                                depth -= 1
                        return position
                elif token == "IfEnd":
                    in_else = False
                    return position + 1
                elif token == "While " and len(tokenized) == 2:
                    if not tokenized[1][1]:
                        depth = 0
                        while depth >= 0:
                            position += 1
                            code = file[position]
                            if (code.startswith("While ") or
                                code.startswith("Then While ") or
                                code.startswith("Else While ")):
                                depth += 1
                            elif code.startswith("WhileEnd"):
                                depth -= 1
                    return position + 1
                elif token == "WhileEnd":
                    depth = 0
                    while depth <= 0:
                        position -= 1
                        code = file[position]
                        if (code.startswith("While ") or
                            code.startswith("Then While ") or
                            code.startswith("Else While ")):
                            depth += 1
                        elif code.startswith("WhileEnd"):
                            depth -= 1
                    return position
                elif token == "For " and (len(tokenized) == 6 or
                                          len(tokenized) == 8 and ("Control", " Step ") in tokenized):
                    if for_loop_next:
                        for_loop_next = False
                        a = tokenized[3][1]
                        if len(tokenized) == 8:
                            b = tokenized[7][1]
                        else:
                            b = 1
                        variables[a] += b
                        value = tokenized[5][1]
                        if variables[a] > value:
                            depth = 0
                            while depth >= 0:
                                position += 1
                                code = file[position]
                                if (code.startswith("For ") or
                                    code.startswith("Then For ") or
                                    code.startswith("Else For ")):
                                    depth += 1
                                elif code.startswith("Next"):
                                    depth -= 1
                        return position + 1
                    else:
                        a = tokenized[3][1]
                        value = tokenized[1][1]
                        variables[a] = value
                        tokenized.pop(1)
                        tokenized.pop(1)
                        tokenized.pop(1)
                        return position + 1
                elif token == "Next":
                    depth = 0
                    while depth <= 0:
                        position -= 1
                        code = file[position]
                        if code.startswith("For ") or code.startswith("Then For ") or code.startswith("Else For "):
                            depth += 1
                        elif code.startswith("Next"):
                            depth -= 1
                    for_loop_next = True
                    if code.startswith("Else For "): in_else = True
                    return position
                elif token == "Break":
                    for_loop_next = False
                    depth = 0
                    while depth >= 0:
                        position += 1
                        code = file[position]
                        if (code.startswith("While ") or
                            code.startswith("Then While ") or
                            code.startswith("Else While ") or
                            code.startswith("For ") or
                            code.startswith("Then For ") or
                            code.startswith("Else For ")):
                            depth += 1
                        elif code.startswith("WhileEnd") or code.startswith("Next"):
                            depth -= 1
                    return position + 1
            elif tokenized[0][0] == "Goto":
                a = "Lbl " + tokenized[0][1]
                return file.index(a)
            elif len(tokenized) == 1 and tokenized[0][0] == "String":
                display_text = tokenized[0][1]
                display_text += " " * (DISPLAY_SIZE - len(display_text))
                tokenized.clear()
                break

            off_limits = set()
            redo = True
            while redo:
                redo = False
                for operator in _OPERATORS:
                    if operator != "-" and operator != "/":
                        for code_index, token in enumerate(tokenized):
                            code_index: int
                            if token == ("Syntax", "(") and tokenized[code_index + 2] == ("Syntax", ")"):
                                tokenized.pop(code_index + 2)
                                tokenized.pop(code_index)
                            elif token[0] == "Operator" and (token[1] == operator or
                                 (operator == "+" and token[1] == "-") or (operator == "*" and token[1] == "/")):
                                if (token[1] in
                                    ("^", "*", "/", "+", "-", "=", "<>", "<", ">", "<=", ">=", " And ", " Or ") and
                                    not (code_index >= 2 and tokenized[code_index - 2] == ("Function", "List "))):
                                    a = tokenized[code_index - 1][1]
                                    b = tokenized[code_index + 1][1]
                                    if (code_index - 1 not in off_limits and
                                        code_index + 1 not in off_limits and
                                        tokenized[code_index - 1][0] == "Number" and
                                        tokenized[code_index + 1][0] == "Number"):
                                        if token[1] == "^":
                                            a **= b
                                        elif token[1] == "*":
                                            a *= b
                                        elif token[1] == "/":
                                            a /= b
                                        elif token[1] == "+":
                                            a += b
                                        elif token[1] == "-":
                                            a -= b
                                        elif token[1] == "=":
                                            a = (a == b)
                                        elif token[1] == "<>":
                                            a = (a != b)
                                        elif token[1] == "<":
                                            a = (a < b)
                                        elif token[1] == ">":
                                            a = (a > b)
                                        elif token[1] == "<=":
                                            a = (a <= b)
                                        elif token[1] == ">=":
                                            a = (a >= b)
                                        elif token[1] == " And ":
                                            a = (a and b)
                                        elif token[1] == " Or ":
                                            a = (a or b)
                                        tokenized[code_index - 1] = ("Number", a)
                                        tokenized.pop(code_index)
                                        tokenized.pop(code_index)
                                        redo = True
                                        break
                                    elif (code_index - 1 not in off_limits and
                                          code_index + 1 not in off_limits and
                                          tokenized[code_index - 1][0] == "String" and
                                          tokenized[code_index + 1][0] == "String" and token[1] == "+"):
                                        tokenized[code_index - 1] = ("String", a + b)
                                        tokenized.pop(code_index)
                                        tokenized.pop(code_index)
                                        redo = True
                                        break
                                    else:
                                        off_limits.add(code_index - 1)
                                        off_limits.add(code_index + 1)
                                elif token[1] == "=>":
                                    if code_index == 1:
                                        if tokenized[0][1]:
                                            tokenized.pop(0)
                                            tokenized.pop(0)
                                        else:
                                            tokenized.clear()
                                        redo = True
                                        break
                                elif token[1] == "->":
                                    if len(tokenized) == 3:
                                        a, b = tokenized[2]
                                        value = tokenized[0][1]
                                        if a == "Variable":
                                            variables[b] = value
                                        elif a == "Variable String":
                                            strings[b] = value
                                        return position + 1
                                    elif len(tokenized) == 5 and tokenized[2][1] == "Dim ":
                                        a = tokenized[4][1] - 1
                                        value = tokenized[0][1]
                                        lists[a] = [0] * value
                                        return position + 1
                                    elif len(tokenized) == 7 and tokenized[2][1] == "List ":
                                        a = tokenized[3][1] - 1
                                        b = tokenized[5][1] - 1
                                        value = tokenized[0][1]
                                        lists[a][b] = value
                                        return position + 1
                                elif token[1] == "?":
                                    display_text = tokenized[0][1]
                                    display_text += " " * (DISPLAY_SIZE - len(display_text))  # CHANGE THIS PLEASE
                                    if answer is None:
                                        answer = ""
                                        answering = 1
                                        return position
                                    else:
                                        tokenized[code_index - 1] = ("Number", int(answer))
                                        answer = None
                                        tokenized.pop(code_index)
                                        redo = True
                                        break
                                elif token[1] == "Disps":
                                    if len(tokenized) == 2:
                                        display_text = tokenized[0][1]
                                        display_text += " " * (DISPLAY_SIZE - len(display_text) - 8) + "- Disp -"
                                        if answer is None:
                                            answering = 2
                                            return position
                                        else:
                                            answer = None
                                            return position + 1
                    if redo:
                        break

            if len(tokenized) > 0:
                if ("Operator", "=>") in tokenized:
                    code_index = tokenized.index(("Operator", "=>"))
                else:
                    code_index = len(tokenized) - 1
                while code_index >= 0 and tokenized[code_index][0] != "Function":
                    code_index -= 1
                token = tokenized[code_index][1]
                if code_index == 0 and token == "ClrText":
                    display_text = " " * DISPLAY_SIZE
                    tokenized.clear()
                elif token in ("Int (", "Frac (", "Abs (") and tokenized[code_index + 2] == ("Syntax", ")"):
                    value = float(tokenized[code_index + 1][1])
                    if token == "Int (":
                        value = int(value)
                    elif token == "Frac (":
                        value = frac(value)
                    elif token == "Abs (":
                        value = abs(value)
                    tokenized[code_index] = ("Number", value)
                    tokenized.pop(code_index + 1)
                    tokenized.pop(code_index + 1)
                elif (token == "MOD(" and
                      tokenized[code_index + 2] == ("Syntax", ",") and
                      tokenized[code_index + 4] == ("Syntax", ")")):
                    a = tokenized[code_index + 1][1]
                    b = tokenized[code_index + 3][1]
                    tokenized[code_index] = ("Number", mod(a, b))
                    tokenized.pop(code_index + 1)
                    tokenized.pop(code_index + 1)
                    tokenized.pop(code_index + 1)
                    tokenized.pop(code_index + 1)
                elif (token == "StrMid(" and tokenized[code_index + 2] == ("Syntax", ",") and
                      tokenized[code_index + 4] == ("Syntax", ",") and
                      tokenized[code_index + 6] == ("Syntax", ")")):
                    value = tokenized[code_index + 1][1]
                    a = tokenized[code_index + 3][1]
                    b = tokenized[code_index + 5][1]
                    tokenized[code_index] = ("String", str_mid(value, a, b))
                    tokenized.pop(code_index + 1)
                    tokenized.pop(code_index + 1)
                    tokenized.pop(code_index + 1)
                    tokenized.pop(code_index + 1)
                    tokenized.pop(code_index + 1)
                    tokenized.pop(code_index + 1)
                elif token == "Locate " and len(tokenized) == 6:
                    a = tokenized[code_index + 1][1] - 1
                    b = tokenized[code_index + 3][1] - 1
                    value = tokenized[code_index + 5][1]
                    a = b * DISPLAY_WIDTH + a
                    b = a + len(value)
                    display_text = display_text[:a] + value + display_text[b:]
                    return position + 1

        return position + 1

    while True:
        keys_pressed = []
        answer_cursor = 21
        answer_tick = 0
        tick_time = 0

        line = 0
        running = True
        while running:
            if not display.get_active():
                running = False
            else:
                for e in event.get():
                    if e.type == QUIT:
                        running = False
                        break
                    elif e.type == KEYDOWN:
                        e_key = e.key
                        e_unicode = e.unicode
                        if e_key == K_F10:
                            update_pygame_display(reset=True)
                        elif e_key == K_F11:
                            update_pygame_display(toggle_fullscreen=True)
                        elif e_key is not None:
                            if e_key in keyboard_mapping:
                                if keyboard_mapping[e_key] not in keys_pressed:
                                    keys_pressed.append(keyboard_mapping[e_key])
                                if e_key == K_RETURN and not (answering == 1 and answer == ""):
                                    if answering == 2:
                                        answer = ""
                                    answering = 0
                                    answer_cursor = 21
                                    answer_tick = 0
                                elif (answering == 1 and
                                      e_unicode in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '\b')):
                                    answer_tick = 0
                                    if e_unicode == "\b":
                                        if len(answer) > 0:
                                            answer = answer[:-1]
                                            display_text = (display_text[:answer_cursor - 1] + "  " +
                                                            display_text[answer_cursor + 1:])
                                            answer_cursor -= 1
                                    else:
                                        answer += e.unicode
                                        display_text = (display_text[:answer_cursor] + e_unicode +
                                                        display_text[answer_cursor + 1:])
                                        answer_cursor += 1
                    elif e.type == KEYUP:
                        if e.key in keyboard_mapping and keyboard_mapping[e.key] in keys_pressed:
                            keys_pressed.remove(keyboard_mapping[e.key])
            if len(keys_pressed) > 0:
                getkey = keys_pressed[0]
            else:
                getkey = 0
            if running:
                for _ in range(INSTRUCTIONS_PER_FRAME):
                    if answering == 0 and tick_time <= 0:
                        if line >= len(file):
                            tick_time = float("Inf")
                        elif file[line] == "Tick":
                            tick_time = 0.15
                            line += 1
                        else:
                            line = interpret(line)

                delta = clock.get_time() * 0.001
                if tick_time > 0: tick_time -= delta
                if answering == 1:
                    answer_tick += delta
                    c = "|" if answer_tick % 2 < 1 else " "
                    display_text = display_text[:answer_cursor] + c + display_text[answer_cursor + 1:]

                display_screen.fill((0, 0, 0))
                for i in range(DISPLAY_SIZE):
                    rendered_line = display_font.render(display_text[i], False, (255, 255, 255))
                    display_screen.blit(rendered_line, (CHAR_W * (i % DISPLAY_WIDTH), CHAR_H * (i // DISPLAY_WIDTH)))

                aspect_screen = screen.get_width() / screen.get_height()
                aspect_display = display_screen.get_width() / display_screen.get_height()
                if aspect_screen > aspect_display:
                    h = screen.get_height()
                    w = h * aspect_display
                else:
                    w = screen.get_width()
                    h = w / aspect_display
                x = (screen.get_width() - w) * 0.5
                y = (screen.get_height() - h) * 0.5

                screen.fill("silver")
                screen.blit(transform.scale(display_screen, (w, h)), (x, y))
                display.flip()
                clock.tick(60)
                await asyncio.sleep(0)

        quit()


if __name__ == "__main__":
    asyncio.run(main())
