import pygame as _pygame
import os as _os
import math
from threading import Thread as _Thread
from typing import Callable


"""
This is my own custom Python library I wrote to emulate Casio BASIC so that I can write my own programs for my CASIO
fx-CG50 calculator in Python and then convert them to Casio BASIC. Although this calculator already supports programming
in Python, it is very limited compared to what you can do with Casio BASIC on it.

I don't fully have all the functions I planned on making for this implemented yet, as you can see there are
no functions for handling the calculator's matrices, other display methods, and a lot of string modules missing.
"""


_pygame.init()


DISPLAY_WIDTH = 21
DISPLAY_HEIGHT = 7
DISPLAY_SIZE = DISPLAY_WIDTH * DISPLAY_HEIGHT
CHAR_W, CHAR_H = 52, 72


_display_text: str = " " * DISPLAY_SIZE
_keyboard_mapping = {_pygame.K_F1: 79, _pygame.K_F2: 69, _pygame.K_F3: 59, _pygame.K_F4: 49, _pygame.K_F5: 39, _pygame.K_F6: 29,
                     _pygame.K_LSHIFT: 78, _pygame.K_LEFT: 38, _pygame.K_UP: 28,
                     _pygame.K_LALT: 77, _pygame.K_DOWN: 37, _pygame.K_RIGHT: 27,
                     _pygame.K_COMMA: 35,
                     _pygame.K_7: 74, _pygame.K_8: 64, _pygame.K_9: 54, _pygame.K_BACKSPACE: 44,
                     _pygame.K_4: 73, _pygame.K_5: 63, _pygame.K_6: 53, _pygame.K_ASTERISK: 43, _pygame.K_QUESTION: 33,
                     _pygame.K_1: 72, _pygame.K_2: 62, _pygame.K_3: 52, _pygame.K_PLUS: 42, _pygame.K_MINUS: 32,
                     _pygame.K_0: 71, _pygame.K_PERIOD: 61,
                     _pygame.K_KP_7: 74, _pygame.K_KP_8: 64, _pygame.K_KP_9: 54,
                     _pygame.K_KP_4: 73, _pygame.K_KP_5: 63, _pygame.K_KP_6: 53,
                     _pygame.K_KP_1: 72, _pygame.K_KP_2: 62, _pygame.K_KP_3: 52,
                     _pygame.K_KP_0: 71,

                     _pygame.K_a: 76, _pygame.K_b: 66, _pygame.K_c: 56, _pygame.K_d: 46, _pygame.K_e: 36, _pygame.K_f: 26,
                     _pygame.K_g: 75, _pygame.K_h: 65, _pygame.K_i: 55, _pygame.K_j: 45, _pygame.K_k: 35, _pygame.K_l: 25,
                     _pygame.K_m: 74, _pygame.K_n: 64, _pygame.K_o: 54,
                     _pygame.K_p: 73, _pygame.K_q: 63, _pygame.K_r: 53, _pygame.K_s: 43, _pygame.K_t: 33,
                     _pygame.K_u: 72, _pygame.K_v: 62, _pygame.K_w: 52, _pygame.K_x: 42, _pygame.K_y: 32,
                     _pygame.K_z: 71, _pygame.K_SPACE: 61, _pygame.K_QUOTE: 51,

                     _pygame.K_INSERT: 44,
                     _pygame.K_LEFTBRACKET: 42, _pygame.K_RIGHTBRACKET: 32,
                     _pygame.K_RETURN: 31, _pygame.K_KP_ENTER: 31}
_get_key = 0
_answering: bool = False
_answer: str = ""
_answer_cursor: int = 0
_running = True


def get_keyboard_mapping_dict():
    return _keyboard_mapping


A = B = C = D = E = F = G = H = I = J = K = L = M = N = O = P = Q = R = S = T = U = V = W = X = Y = 0
# integer variables need to be global!
# global A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y


# When this library is imported it will run a Pygame window on a secondary thread that displays all the games graphics and detects button presses.
def run(main: Callable[[], None]):
    global _running, _get_key, _display_text, _answer, _answering, _answer_cursor

    load()
    _Thread(target=main, daemon=True).start()

    def update_pygame_display(*, toggle_fullscreen: bool = False, reset: bool = False) -> _pygame.surface:
        nonlocal screen, fullscreen, previous_screen_size
        if toggle_fullscreen:
            if not fullscreen:
                _pygame_previous_screen_size = _pygame.display.get_window_size()
            fullscreen = not fullscreen
        if reset:
            _pygame.display.quit()
            _pygame.display.init()
            fullscreen = False
            _pygame_previous_screen_size = (640, 360)
        screen = _pygame.display.set_mode((1920, 1080) if fullscreen else previous_screen_size,
                                          _pygame.FULLSCREEN if fullscreen else _pygame.RESIZABLE)
        _pygame.display.set_caption("Pseudo Python")

    def type_key(character: str):
        nonlocal keys_held, last_key, answer_tick
        global _display_text, _answer, _answering, _answer_cursor
        if character == '\r':
            last_key = ''
            _answering = False
        elif character == '\b':
            if len(_answer) > 0:
                _answer = _answer[:-1]
                _display_text = _display_text[:_answer_cursor] + ' ' + _display_text[_answer_cursor + 1:]
                _answer_cursor -= 1
        else:
            _answer += character
            _display_text = _display_text[:_answer_cursor] + character + _display_text[_answer_cursor + 1:]
            _answer_cursor += 1
        answer_tick = 0

    screen = _pygame.Surface((0, 0))
    fullscreen = False
    previous_screen_size = (640, 360)
    update_pygame_display(reset=True)
    display_screen = _pygame.Surface((DISPLAY_WIDTH * CHAR_W, DISPLAY_HEIGHT * CHAR_H))
    display_font = _pygame.font.Font("../casio.ttf", 64)
    keys_pressed = []
    clock = _pygame.time.Clock()
    _running = True

    answer_tick = 0
    keys_held = 0
    keys_held_for = 0
    last_key = ''
    while _running:
        delta = clock.get_time() * 0.001
        if _answering:
            answer_tick += delta
            c = "|" if answer_tick % 2 < 1 else " "
            _display_text = _display_text[:_answer_cursor] + c + _display_text[_answer_cursor + 1:]
        for event in _pygame.event.get():
            if event.type == _pygame.QUIT:
                _running = False
            elif event.type == _pygame.KEYDOWN:
                if event.key == _pygame.K_F10:
                    update_pygame_display(reset=True)
                elif event.key == _pygame.K_F11:
                    update_pygame_display(toggle_fullscreen=True)
                elif event.key in _keyboard_mapping:
                    keys_pressed.append(_keyboard_mapping[event.key])
                    if _answering and event.unicode not in ('', '\t', '^['):
                        keys_held += 1
                        last_key = event.unicode
                        type_key(event.unicode)
            elif event.type == _pygame.KEYUP:
                if event.key in _keyboard_mapping:
                    keys_pressed.remove(_keyboard_mapping[event.key])
                    if _answering and event.unicode not in ('', '\t', '^['):
                        keys_held -= 1
        if keys_held == 0:
            keys_held_for = 0
        elif last_key != '':
            keys_held_for += delta
            if keys_held_for > 0.5 and keys_held_for % 0.2 > 0.1:
                type_key(last_key)
        _get_key = 0 if len(keys_pressed) == 0 else keys_pressed[0]

        display_screen.fill((0, 0, 0))
        for i in range(DISPLAY_SIZE):
            rendered_line = display_font.render(_display_text[i], False, (255, 255, 255))
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
        screen.blit(_pygame.transform.scale(display_screen, (w, h)), (x, y))
        _pygame.display.flip()

        clock.tick(60)
    _pygame.quit()


def string_python_to_casio(text: str):
    text = text.replace("/", "//").replace("*", "**")
    text = text.replace("÷", "/").replace("×", "*")
    return text


def string_casio_to_python(text: str):
    text = text.replace("/", "÷").replace("*", "×")
    text = text.replace("÷÷", "/").replace("\\\\", "\\").replace("××", "*")
    return text


def file_name_python_to_casio(text: str) -> str:
    return _os.path.basename(text)[:-3].upper().replace("_", "")[:8]


def tick(times: int = 1):
    _pygame.time.wait(150 * times)


def stop():
    while True:
        tick()


def save():
    global _lists
    data = [','.join([str(i) for i in list_]) + '\n' for list_ in _lists]
    data[-1] = data[-1][:-1]
    with open("lists.csv", "w") as file:
        file.writelines(data)


def load():
    global _lists
    if _os.path.isfile("lists.csv"):
        with open("lists.csv", "r") as file:
            data = file.readlines()
        _lists.clear()
        for line in data:
            line = line.strip()
            if line == "":
                _lists.append([])
            else:
                _lists.append([int(i) for i in line.split(',')])


# Casio BASIC equivalent: Getkey
def get_key() -> int:
    return _get_key


# Casio BASIC equivalent: ClrText
def clr_text():
    global _display_text
    _display_text = ' ' * DISPLAY_SIZE


# Casio BASIC equivalent: Locate [x],[y],"[text]"
def locate(x: int, y: int, text: str):
    global _display_text
    x -= 1
    y -= 1
    if 0 <= x and x + len(text) <= DISPLAY_WIDTH and 0 <= y < DISPLAY_HEIGHT:
        p = y * DISPLAY_WIDTH + x
        _display_text = _display_text[:p] + text + _display_text[(p + len(text)):]
    else:
        raise ValueError(x, y, text)


def frac(x: float | int):
    return x % 1


def mod(x: float | int, y: float | int):
    return x % y


"""
str (string) modules
"""


__strs: list[str | None] = [None] * 20


# Casio BASIC equivalent: "[text]"
def show_str(text: str):
    global _display_text
    lines = []
    for i in range(0, len(text), DISPLAY_WIDTH):
        lines.append(text[i:i + DISPLAY_WIDTH])
    _display_text = text + " " * (DISPLAY_SIZE - len(text))


# Casio BASIC equivalent: "[text]"Disps
def disps(text: str, *, break_up: bool = False, return_str: bool = False):
    global _display_text
    if break_up:
        i = 0
        j = ""
        while True:
            if i + 21 < len(text):
                if text[i + 20] == " ":
                    j += text[i:i + 21]
                elif text[i + 21] == " ":
                    j += text[i:i + 21]
                    i += 1
                elif text[i + 19] == " ":
                    j += text[i:i + 20] + " "
                    i -= 1
                else:
                    j += text[i:i + 20] + "-"
                    i -= 1
            else:
                j += text[i:]
                break
            i += 21
        text = j
        if return_str: return text
    show_str(text)
    _display_text = _display_text[:-21] + "             - Disp -"
    while _get_key == 31: pass
    while _get_key != 31: pass


# Casio BASIC equivalent: "[text]"?
def ask(text: str, value_type: type):
    global _answering, _answer, _answer_cursor
    show_str(text)
    _answer_cursor = (len(text) // DISPLAY_WIDTH + 1) * DISPLAY_WIDTH
    _answering = True
    _answer = ""
    while _answering:
        while _answering:
            pass
        try:
            return value_type(_answer)
        except ValueError:
            _answering = True


# Casio BASIC equivalent: "[value]"->Str [str_id]
def set_str(str_id: int, value: str):
    global __strs
    if len(value) > 255:
        raise ValueError(f"len(\"{value}\") = {len(value)} exceeds 255")
    __strs[str_id - 1] = value


# Casio BASIC equivalent: Str [str_id]
def get_str(str_id: int) -> str:
    global __strs
    str_id = __strs[str_id - 1]
    return str_id


# Casio BASIC equivalent: StrMid("[value]",start,length)
def str_mid(value: str, start: int, length: int) -> str:
    start -= 1
    value = value[start:start + length]
    return value


#  StrInv("STRING") // Inverts the sequence of a string
#  StrJoin("STRING1", "STRING 2") // Same as adding them using "+"
#  StrLeft("STRING", n) // Copies a string up the nth character from the left
#  StrMid("STRING", n, m) // m is optional; Extracts the nth to mth characters of a string
#  StrRight("STRING", n) // Copies a string up the nth character from the right
#  StrLen("STRING") // Returns the length of a string
#  StrLwr("STRING") // Converts a string to lower case
#  StrUpr("STRING") // Converts a string to upper case


"""
list modules
"""


_lists: list[list[float]] = [[] for _ in range(26)]
# load()


# Casio BASIC equivalent: List [list_id][[index]]
def get_list(list_id: int, index: int) -> int | float:
    return _lists[list_id - 1][index - 1]


# Casio BASIC equivalent: [value]->List [list_id][[index]]
def set_list(list_id: int, index: int, value: float):
    _lists[list_id - 1][index - 1] = value
    save()


# Casio BASIC equivalent: List [list_id_2]->List [list_id_1]
def copy_list(list_id_1: int, list_id_2: int):
    list_id_1 = _lists[list_id_1 - 1]
    list_id_1.clear()
    for value in _lists[list_id_2 - 1]:
        list_id_1.append(value)
    save()


# Casio BASIC equivalent: [dim]->Dim List [list_id]
def set_dim_list(list_id: int, dim: int):
    list_id = _lists[list_id - 1]
    list_id.clear()
    for _ in range(dim):
        list_id.append(0)
    save()


# Casio BASIC equivalent: Dim List [list_id]
def get_dim_list(list_id: int) -> int:
    return len(_lists[list_id - 1])


# Fill([value],List [list_id])
def fill_list(list_id: int, value: float):
    list_id = _lists[list_id - 1]
    for i in range(len(list_id)):
        list_id[i] = value
    save()


"""
mat (matrix) modules
TO BE IMPLEMENTED
"""


__mats: list = []
