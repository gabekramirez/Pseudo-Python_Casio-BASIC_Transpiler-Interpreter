from casio_basic import *


def main():
    global A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y
    clr_text()
    locate(1, 3, "   F1=New Game")
    locate(1, 4, "   F2=Load Game")
    locate(1, 5, "   F3=Help")
    locate(1, 6, "   F4=Quit")
    while get_key() != 0: pass
    I = 30
    A = 0
    B = 0
    while A == 0 or B == 1:
        I = mod(I + 1, 50)
        F = int(abs(I * 0.1 - 2))
        if F == 0: locate(1, 1, "No No Noah The Game  ")
        if F == 1: locate(1, 1, " No No Noah The Game ")
        if F == 2: locate(1, 1, "  No No Noah The Game")
        if B == 0 and get_key() != 0: B = 1
        if B == 1 and (get_key() == 79 or get_key() == 69 or get_key() == 59 or get_key() == 49): A = get_key()
        if A != 0 and get_key() != 0: B = 0
        tick()
    if A == 79 or A == 69:
        if get_dim_list(26) != 250:
            P = 3
            noah_load()
        clr_text()
        S = 0
        while S < 1 or S > 25:
            if A == 79: S = ask("NEW SAVE [1-25]", int)
            if A == 69: S = ask("LOAD SAVE [1-25]", int)
        set_str(1, str_mid("0123456789", 1 + int(10 * frac(S * 0.01)), 1))
        set_str(1, get_str(1) + str_mid("0123456789", 1 + int(10 * frac(S * 0.1)), 1))
        clr_text()
        if A == 79:
            locate(1, 1, "Are you sure that")
            locate(1, 2, "you wish to continue?")
            locate(1, 3, "Doing so will overide")
            locate(1, 4, "List" + get_str(1) + " in storage.")
            locate(1, 6, "   F1=Yes")
            locate(1, 7, "   F2=No")
            while get_key() != 0: pass
            A = 0
            while A != 79 and A != 69:
                A = get_key()
            if A == 69: return main()
            set_dim_list(S, 51)  # FILE SIZE
        if A == 69:
            while get_key() != 0: pass
            if get_dim_list(S) != 51:  # FILE SIZE
                disps("Save state missing or corrupted.")
                A = 59
        if A != 59:
            return noah_game()
    if A == 59:
        clr_text()
        disps("Having trouble getting the game to run? Contact me online at gabekramirez@gmail.com!")
        return main()
    clr_text()
    show_str("Press EXIT")
    stop()


def noah_game():
    global A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y
    while True:
        if get_list(S, 1) == 0:
            locate(1, 1, "    Name the Noah    ")
            locate(1, 2, "                     ")
            locate(1, 3, "                     ")
            locate(1, 4, "a b c d e f g h i j k")
            locate(1, 5, "l m n o p q r s t u v")
            locate(1, 6, "w x t z              ")
            locate(1, 7, "    space   done     ")
            set_str(1, "")
            A = -1
            B = 0
            C = 0
            while B != 5:
                if get_key() == 64 and B == 0:
                    set_str(1, get_str(1) + "N")
                    B = 1
                    C = 1
                if get_key() == 54 and B == 1:
                    set_str(1, get_str(1) + "o")
                    A += 1
                    B = 2
                    C = 1
                if get_key() == 76 and B == 2:
                    set_str(1, get_str(1) + "a")
                    B = 3
                    C = 1
                if get_key() == 65 and B == 3:
                    set_str(1, get_str(1) + "h")
                    B = 4
                    C = 1
                if get_key() == 61 and B == 2:
                    set_str(1, get_str(1) + " ")
                    B = 0
                    C = 1
                if get_key() == 31 and B == 4:
                    B = 5
                if C == 1:
                    if B == 1: locate(5, 5, "N")
                    if B == 2: locate(7, 5, "O")
                    if B == 3: locate(1, 4, "A")
                    if B == 4: locate(15, 4, "H")
                    if B == 0: locate(5, 7, "SPACE")
                    while get_key() != 0: pass
                    if B == 1: locate(5, 5, "n")
                    if B == 2: locate(7, 5, "o")
                    if B == 3: locate(1, 4, "a")
                    if B == 4: locate(15, 4, "h")
                    if B == 0: locate(5, 7, "space")
                    if A > 5:
                        set_str(1, str_mid(get_str(1), 2, 19))
                    C = 0
                locate(1, 2, get_str(1))
            set_list(S, 1, 3)  # starting mode
            set_list(S, 2, A)  # Noah's name length
            set_list(S, 3, 19)  # player entity
            set_list(S, 4, 9)
            set_list(S, 5, 0)
            set_list(S, 6, 21)
            set_list(S, 7, 28)  # wall entity
            set_list(S, 8, 9)
            set_list(S, 9, 200)
            set_list(S, 10, 0)
            set_list(S, 11, 16)  # door entities
            set_list(S, 12, 5)
            set_list(S, 13, 201)
            set_list(S, 14, 0)
            set_list(S, 15, 16)
            set_list(S, 16, 23)
            set_list(S, 17, 202)
            set_list(S, 18, 0)
            set_list(S, 19, 17)
            set_list(S, 20, 23)
            set_list(S, 21, 202)
            set_list(S, 22, 0)
            set_list(S, 23, 38)
            set_list(S, 24, 9)
            set_list(S, 25, 203)
            set_list(S, 26, 0)
            set_list(S, 27, 17)  # old man entity
            set_list(S, 28, 19)
            set_list(S, 29, 1)
            set_list(S, 30, 0)
            set_list(S, 43, 0)  # inventory
            set_list(S, 44, -1)  # story progression
            set_list(S, 45, 0)  # raft 1
            set_list(S, 46, 0)
            set_list(S, 47, 0)
            set_list(S, 48, 0)  # raft 2
            set_list(S, 49, 0)
            set_list(S, 50, 0)
            set_list(S, 50, 3)
            set_list(S, 51, 11)  # number of entities that need to be displayed (times 4 plus 3)

        if get_list(S, 1) == 1:
            F = 0
            W = -1
            X = get_list(S, 3)
            Y = get_list(S, 4)
            P = 2
            noah_load()

            # movement logic
            if get_list(S, 44) == -1:
                locate(1, 1, "Move with arrow keys!")
                set_list(S, 44, 0)
            while get_list(S, 1) == 1:
                if F != 2: M = 0
                F = 0
                while M != 27 and M != 28 and M != 37 and M != 38 and M != 79 and M != 69 and M != 59 and F == 0:
                    M = get_key()
                    if M == 52 or M == 53 or M == 54 or M == 62 or M == 64 or M == 72 or M == 73 or M == 74: F = 1
                U = X
                V = Y
                if M == 79 or M == 69 or M == 59:
                    set_list(S, 1, 2)
                    return noah_game()
                if M == 27 and X < 245: X += 1
                if M == 28 and Y > 4: Y -= 1
                if M == 37 and Y < 32: Y += 1
                if M == 38 and X > 11: X -= 1
                if U != X or V != Y or get_list(S, 45) != 0:
                    A = X - 11 + (Y - 4) * 235
                    B = int(A / 32) + 1
                    A = int(frac(A * 0.03125) * 32)

                    # raft logic
                    if frac(int(get_list(26, B) * (0.5 ** A)) * 0.5) == 0.5:
                        N = 1
                    else:
                        N = 0
                    L = 0
                    C = 0
                    if get_list(S, 45) != 0:
                        if X > 42:
                            if Y == 29:
                                set_list(S, 45, 27)  # raft 1
                                set_list(S, 46, 29)
                                set_list(S, 47, 0)
                                set_list(S, 48, 127)  # raft 2
                                set_list(S, 49, 32)
                                set_list(S, 50, 1)
                            elif Y == 28:
                                set_list(S, 45, 35)  # raft 1
                                set_list(S, 46, 25)
                                set_list(S, 47, 3)
                                set_list(S, 48, 34)  # raft 2
                                set_list(S, 49, 23)
                                set_list(S, 50, 5)
                        for I in range(45, 50, 3):
                            A = get_list(S, I)
                            B = get_list(S, I + 1)
                            Q = get_list(S, I + 2)
                            if A - 1 <= U and U <= A + 1 and V == B:
                                H = 1
                            else:
                                H = 0
                            if Q == 0:
                                if A >= 31:
                                    set_list(S, I, 27)
                                else:
                                    set_list(S, I, A + 1)
                                D = 1
                            elif Q == 1:
                                if A >= 33:
                                    set_list(S, I, 33)
                                    set_list(S, I + 2, 2)
                                    D = 0
                                else:
                                    set_list(S, I, A + 1)
                                    D = 1
                            elif Q == 2:
                                if A <= 29:
                                    set_list(S, I, 29)
                                    set_list(S, I + 2, 1)
                                    D = 0
                                else:
                                    set_list(S, I, A - 1)
                                    D = -1
                            elif Q == 3:
                                if A >= 53:
                                    set_list(S, I, 53)
                                    set_list(S, I + 2, 4)
                                    D = 0
                                else:
                                    set_list(S, I, A + 1)
                                    D = 1
                            elif Q == 4:
                                if A <= 35:
                                    set_list(S, I, 35)
                                    set_list(S, I + 2, 3)
                                    D = 0
                                else:
                                    set_list(S, I, A - 1)
                                    D = -1
                            elif Q == 5:
                                if A >= 54:
                                    set_list(S, I, 54)
                                    set_list(S, I + 1, 21)
                                    set_list(S, I + 2, 6)
                                    D = 0
                                else:
                                    set_list(S, I, A + 1)
                                    D = 1
                            elif Q == 6:
                                if A <= 34:
                                    set_list(S, I, 34)
                                    set_list(S, I + 1, 23)
                                    set_list(S, I + 2, 5)
                                    D = 0
                                else:
                                    set_list(S, I, A - 1)
                                    D = -1
                            A = get_list(S, I)
                            B = get_list(S, I + 1)
                            if A - 1 - D <= X and X <= A + 1 - D and Y == B:
                                X += D
                                L = 1
                            elif N == 1 and H == 1 and get_list(S, 44) != 7:
                                if Q == 0:
                                    X = 12
                                    Y = 28
                                elif Q == 1 or Q == 2:
                                    X = 31
                                    Y = 31
                                elif Q == 3 or Q == 4:
                                    X = 44
                                    Y = 26
                                elif Q == 5 or Q == 6:
                                    X = 39
                                    Y = 24
                                C = 1

                    if get_list(S, 44) != 7:
                        if N == 1 and L == 0 and C == 0:
                            X = U
                            Y = V
                        else:
                            # interaction logic
                            for I in range(7, 42, 4):
                                if X == get_list(S, I) and Y == get_list(S, I + 1):
                                    X = U
                                    Y = V
                                    A = get_list(S, I + 2)
                                    if A == 1:  # old man
                                        set_list(S, 1, 3)
                                        if Y > 26:
                                            set_list(S, 44, 4)
                                    elif A == 201:  # doors
                                        X = 16
                                        Y = 23
                                        F = 2
                                    elif A == 202:
                                        X = 16
                                        Y = 5
                                        F = 2
                                    elif A == 203:
                                        set_list(S, 44, 3)
                                        set_list(S, 1, 3)
                                    elif A == 205:
                                        set_list(S, 44, 6)
                                        set_list(S, 1, 3)
                                    elif A == 300:
                                        set_list(S, 44, 5)
                                        set_list(S, 1, 3)
                                    break
                    set_list(S, 3, X)
                    set_list(S, 4, Y)
                P = 2
                noah_load()
                tick()
        if get_list(S, 1) == 2:
            A = 0
            B = 0
            C = -1
            N = -1
            while get_list(S, 1) == 2:
                if A == 0:
                    B = int(frac(B * 0.334) * 3)
                    locate(1, 1, "     ___LEAVE___     ")
                    if B != 0: locate(1, 2, "    RETURN TO GAME   ")
                    locate(1, 3, "      MAIN MENU      ")
                    locate(1, 4, "      EXIT GAME      ")
                    locate(1, 5, "                     ")
                    locate(1, 6, "Use ENTER, ARROW KEYS")
                    locate(1, 7, "or F1F2F3 to navigate")
                    if B == 0: locate(1, 2, "   > RETURN TO GAME  ")
                    if B == 1: locate(1, 3, "     > MAIN MENU     ")
                    if B == 2: locate(1, 4, "     > EXIT GAME     ")
                    if M == 31:
                        if B == 0:
                            set_list(S, 1, 1)
                            return noah_game()
                        if B == 1: return main()
                        if B == 2:
                            clr_text()
                            show_str("Press EXIT")
                            stop()
                elif A == 1:
                    if M == 31 and C > -1:
                        if C == 0: disps("    ___PEB-BLE___    A tiny rough stone   forged from millenniaof igneous and sedime-ntary processes and so on")
                        if get_list(S, 44) == 0: set_list(S, 44, 1)
                        while get_key() != 0: pass
                    R = 1
                    while R == 1:
                        locate(1, 1, "     ___STUFF___     ")
                        locate(1, 2, "                     ")
                        locate(1, 3, "                     ")
                        locate(1, 4, "                     ")
                        locate(1, 5, "                     ")
                        locate(1, 6, "                     ")
                        locate(1, 7, "                     ")
                        Y = 1
                        J = get_list(S, 43)
                        C = -1
                        for I in range(0, 2):
                            K = frac(J * 0.5) * 2
                            if K == 1:
                                X = 4
                                Y += 1
                                if B == (Y - 2): X = 5
                                if B == (Y - 2): C = I
                                if I == C: locate(3, Y, ">")
                                if I == 0: locate(X, Y, "PEBBLE")
                            J = int(J * 0.5)
                        R = 0
                        if Y == 2 and B != 0:
                            B = 0
                            R = 1
                        if Y >= 3:
                            if B < 0: R = 1
                            if B < 0: B = Y - 2
                            if B > (Y - 2): R = 1
                            if B > (Y - 2): B = 0
                elif A == 2:
                    locate(1, 1, "     ___STATS___     ")
                    J = get_list(S, 2)
                    if J == 0: locate(1, 2, "    NAME:    NOAH    ")
                    if J == 1: locate(1, 2, "    NAME: NO NOAH    ")
                    if J == 2: locate(1, 2, "   NAME: NO NO NOAH  ")
                    if J == 3: locate(1, 2, " NAME: NO NO NO NOAH ")
                    if J == 4: locate(1, 2, "NAME: NO NO NO NO NOAH")
                    if J >= 5: locate(1, 2, "NAME: NO NO NO NO NO N")
                    locate(1, 3, "    SANITY:    20    ")
                    locate(1, 4, "    POWER:      1    ")
                    locate(1, 5, "    RIZZ:       0    ")
                    locate(1, 6, "                     ")
                    locate(1, 7, "                     ")
                M = 0
                if N != -1: N = 0
                while M != 27 and M != 28 and M != 37 and M != 38 and M != 31 and M != 79 and M != 69 and M != 59:
                    M = get_key()
                    if M == 0:
                        if N == -1: N = 0
                        M = N
                    elif M == 79 or M == 69 or M == 59:
                        if N == 0 and ((M == 79 and A == 0) or (M == 69 and A == 1) or (M == 59 and A == 2)):
                            while get_key() != 0: pass
                            set_list(S, 1, 1)
                            return noah_game()
                    else:
                        N = M
                        M = 0
                if M == 79 or M == 69 or M == 59:
                    N = -1
                    if M == 79: A = 0
                    if M == 69: A = 1
                    if M == 59: A = 2
                else:
                    if M == 28: B -= 1
                    if M == 37: B += 1
                    if M == 27: A += 1
                    if M == 38: A -= 1
                    if A == -1: A = 2
                    if A == 3: A = 0
        if get_list(S, 1) == 3:
            if get_list(S, 44) == -1:
                locate(1, 1, r"      /\  (  )       ")
                locate(1, 2, r"     /  \            ")
                locate(1, 3, r"  (   )  \_  (   )   ")
                locate(1, 4, r"   _/      \         ")
                locate(1, 5, r"  /         \        ")
                locate(1, 6, r"---------------------")
                locate(1, 7, r"MOUNT BESTEST 10/4/20")
                while get_key() != 0: pass
                while get_key() == 0: pass
                while get_key() != 0: pass
                disps("It is said that atop this mountain, one brave enough to complete this journey might find the ultimate gaming PC setup.", break_up=True)
                disps("Here we find the protagonist of this tale,", break_up=True)
                clr_text()
                locate(2, 4, "N") or tick()
                locate(3, 4, "O") or tick()
                locate(4, 4, "A") or tick()
                locate(5, 4, "H") or tick()
                locate(7, 4, "K") or tick()
                locate(8, 4, "Y") or tick()
                locate(9, 4, "L") or tick()
                locate(10, 4, "E") or tick()
                locate(12, 4, "A") or tick()
                locate(13, 4, "N") or tick()
                locate(14, 4, "D") or tick()
                locate(15, 4, "E") or tick()
                locate(16, 4, "R") or tick()
                locate(17, 4, "S") or tick()
                locate(18, 4, "O") or tick()
                locate(19, 4, "N") or tick()
                locate(1, 4, "> NOAH KYLE ANDERSON") or tick()
                while get_key() == 0: pass
                while get_key() != 0: pass
                locate(1, 1, r"                /    ")
                locate(1, 2, r"\           o   |    ")
                locate(1, 3, r" --\       /N\  /    ")
                locate(1, 4, r"    \      / \ /     ")
                locate(1, 5, r"   /----    ----\    ")
                locate(1, 6, r"---------------------")
                locate(1, 7, "MOUNT BESTEST 10/4/20")
                while get_key() == 0: pass
                while get_key() != 0: pass
                locate(12, 1, "o") or tick()
                locate(11, 2, "/N\\") or tick()
                locate(11, 3, "/ \\ ") or tick()
                locate(12, 4, "   ") or tick()
                locate(12, 1, " ") or tick()
                locate(11, 2, "o  ") or tick()
                locate(10, 3, "/N\\ ") or tick()
                locate(10, 4, "/ \\") or tick()
                locate(11, 2, " ") or tick()
                locate(10, 3, " o ") or tick()
                locate(10, 4, "/N\\") or tick()
                locate(10, 5, "/ \\") or tick()
                locate(11, 3, " ") or tick()
                locate(10, 4, " o ") or tick()
                locate(10, 5, "/N\\") or tick()
                locate(11, 4, " ") or tick()
                locate(10, 5, " o ") or tick()
                locate(11, 5, " ") or tick()
                locate(1, 7, "     No no Noah!     ")
                while get_key() == 0: pass
                while get_key() != 0: pass
                disps("It would appear that Noah fell into Mount Bestest. How clumsy!", break_up=True)
            elif get_list(S, 44) == 0:
                if get_list(S, 43) == 0:
                    disps("OLD MAN: Hello, fallen child,", break_up=True)
                    disps("OLD MAN: It's dangerous to go alone! Take this.", break_up=True)
                    disps("*Obtained pebble*")
                    set_list(S, 43, 1)
                    disps("OLD MAN: Sorry, some lad in a green tunic already took the sword.", break_up=True)
                    disps("OLD MAN: This is all that I have left, but I'm sure that you'll make good use of it!", break_up=True)
                disps("OLD MAN: Press F1 and navigate to your stuff to admire the pebble!", break_up=True)
            elif get_list(S, 44) < 3:
                if get_list(S, 44) == 1:
                    disps("OLD MAN: Very well done!", break_up=True)
                    set_list(S, 51, 7)  # DELETE ENTITY
                    set_list(S, 7, 0)
                    set_list(S, 8, 0)
                    set_list(S, 9, 0)
                    set_list(S, 10, 0)

                    set_list(S, 44, 2)
                disps("OLD MAN: Now hurry back home.", break_up=True)
                disps("OLD MAN: I'm sure you'll find that the PC you seek is in another castle.", break_up=True)
            elif get_list(S, 44) == 3:
                disps("ENTERING SEWER...")
                set_list(S, 51, 27)
                set_list(S, 3, 12)  # Noah
                set_list(S, 4, 28)
                set_list(S, 7, 12)  # loot
                set_list(S, 8, 32)
                set_list(S, 9, 300)
                set_list(S, 10, 1)
                set_list(S, 11, 19)  # wall entities
                set_list(S, 12, 27)
                set_list(S, 13, 204)
                set_list(S, 14, 0)
                set_list(S, 15, 19)
                set_list(S, 16, 28)
                set_list(S, 17, 204)
                set_list(S, 18, 0)
                set_list(S, 19, 19)
                set_list(S, 20, 29)
                set_list(S, 21, 204)
                set_list(S, 22, 0)
                set_list(S, 23, 27)
                set_list(S, 24, 32)
                set_list(S, 25, 204)
                set_list(S, 26, 0)
                set_list(S, 27, 16)  # old man entity
                set_list(S, 28, 28)
                set_list(S, 29, 1)
                set_list(S, 30, 0)
                set_list(S, 31, 44)  # end
                set_list(S, 32, 18)
                set_list(S, 33, 205)
                set_list(S, 34, 0)
                set_list(S, 45, 27)  # raft 1
                set_list(S, 46, 29)
                set_list(S, 47, 0)
                set_list(S, 48, 127)  # raft 2
                set_list(S, 49, 32)
                set_list(S, 50, 1)
            elif get_list(S, 44) == 4:
                disps("OLD MAN: You can use the number keys on the numpad to fight.", break_up=True)
                disps("OLD MAN: Use this information to punch down that wall!", break_up=True)
            elif get_list(S, 44) == 5:
                disps("*Obtained absolutely nothing*")
                set_list(S, 7, get_list(S, E - 4))  # DELETE ENTITY
                set_list(S, 8, get_list(S, E - 3))
                set_list(S, 9, get_list(S, E - 2))
                set_list(S, 10, get_list(S, E - 1))
                set_list(S, E - 4, 0)
                set_list(S, E - 3, 0)
                set_list(S, E - 2, 0)
                set_list(S, E - 1, 0)
                set_list(S, 51, E - 4)
            elif get_list(S, 44) == 6:
                disps("End of DEMO.")
                set_str(1, "_______CREDITS_______DEVELOPER:                 Gabriel RamirezMUSIC ARTIST:             Zachery Stockton____________STARRING_        Noah Anderson       as main player              Old Man           as old manThanks for playing!  ")
                clr_text()
                for I in range(-146, 189, 21):
                    for J in range(1, 8):
                        K = I + J * 21
                        if K < 1 or K > 231:
                            locate(1, J, "                     ")
                        else:
                            locate(1, J, str_mid(get_str(1), K, 21))
                    for J in range(1, 2001):
                        pass
                    tick(10)
                disps("Thanks for playing!")
                set_list(S, 44, 7)
            set_list(S, 1, 1)


def noah_load():
    global A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y
    if P == 1:
        W = mod(Y - 4, 13) + I + 1
        if W < 11:
            if W < 6:
                if W == 2: set_str(1, get_str(2))
                if W == 3: set_str(1, get_str(3))
                if W == 4: set_str(1, get_str(4))
                if W == 5: set_str(1, get_str(5))
            else:
                if W == 6: set_str(1, get_str(6))
                if W == 7: set_str(1, get_str(7))
                if W == 8: set_str(1, get_str(8))
                if W == 9: set_str(1, get_str(9))
                if W == 10: set_str(1, get_str(10))
        else:
            if W < 16:
                if W == 11: set_str(1, get_str(11))
                if W == 12: set_str(1, get_str(12))
                if W == 13: set_str(1, get_str(13))
                if W == 14: set_str(1, get_str(14))
                if W == 15: set_str(1, get_str(15))
            else:
                if W == 16: set_str(1, get_str(16))
                if W == 17: set_str(1, get_str(17))
                if W == 18: set_str(1, get_str(18))
                if W == 19: set_str(1, get_str(19))
                if W == 20: set_str(1, get_str(20))
        locate(1, I, str_mid(get_str(1), X - 10, 21))
    elif P == 2:
        if W != mod(Y - 4, 13):
            if Y < 17:
                set_str(2, r"##################  ############################               AD                   AE                   AF                   AG                   AH                   AI                   AJ                   AK                   AL                   AM ")
                set_str(3, r"##################  ############################                                                                                                                                                                                                               ")
                set_str(4, r"################################################                                                                                                                                                                                                               ")
                set_str(5, r"##################  ############################                                                                                                                                                                                                               ")
                set_str(6, r"##############[ ]/  ############################                                                                                                                                                                                                               ")
                set_str(7, r"#############/      ############################                                                                                                                                                                                                               ")
                set_str(8, r"############/       ############################                                                                                                                                                                                                               ")
                set_str(9, r"###########/        \###########################               BD                   BE                   BF                   BG                   BH                   BI                   BJ                   BK                   BL                   BM ")
                set_str(10, r"         #                           *##########                                                                                                                                                                                                               ")
                set_str(11, r"###########\             #######################                                                                                                                                                                                                               ")
                set_str(12, r"############             #######################                                                                                                                                                                                                               ")
                set_str(13, r"############             #######################                                                                                                                                                                                                               ")
                set_str(14, r"#################################################################                                                                                                                                                                                              ")
                set_str(15, r"#################################################################                                                                                                                                                                                              ")
                set_str(16, r"#################################################################                   CE                   CF                   CG                   CH                   CI                   CJ                   CK                   CL                   CM ")
                set_str(17, r"##########            ##########/~~~~~~~~~~~~~~~~~~~~~\##########                                                                                                                                                                                              ")
                set_str(18, r"##########            ##########~~~~~~~~~/---\~~~~~~~~~##########                                                                                                                                                                                              ")
                set_str(19, r"##########            ##########~~~~~~~~~| * |~~~~~~~~~##########                                                                                                                                                                                              ")
                set_str(20, r"##########  ^   O  ^  ##########~~~~~~~~~|   |~~~~~~~~~##########                                                                                                                                                                                              ")
            elif Y < 30:
                set_str(2, r"#################################################################                                                                                                                                                                                              ")
                set_str(3, r"#################################################################                   CE                   CF                   CG                   CH                   CI                   CJ                   CK                   CL                   CM ")
                set_str(4, r"##########            ##########/~~~~~~~~~~~~~~~~~~~~~\##########                                                                                                                                                                                              ")
                set_str(5, r"##########            ##########~~~~~~~~~/---\~~~~~~~~~##########                                                                                                                                                                                              ")
                set_str(6, r"##########            ##########~~~~~~~~~| * |~~~~~~~~~##########                                                                                                                                                                                              ")
                set_str(7, r"##########  ^   O  ^  ##########~~~~~~~~~|   |~~~~~~~~~##########                                                                                                                                                                                              ")
                set_str(8, r"##########            ##########~~~~~~~~~\---/~~~~~~~~~##########                                                                                                                                                                                              ")
                set_str(9, r"##########            ##########~~~~~~~~~~~~~~~~~~~~~~~##########                                                                                                                                                                                              ")
                set_str(10, r"##########            ##########~~~~~~~~~~~~~~~~ ~~~~~~##########                   DE                   DF                   DG                   DH                   DI                   DJ                   DK                   DL                   DM ")
                set_str(11, r"##############[  ]##############~~~~~~~~~~~~~~~~~~~~~~~##########                                                                                                                                                                                              ")
                set_str(12, r"################################~~~~~  ~~~~~~~~~~~~~~~~##########                                                                                                                                                                                              ")
                set_str(13, r"################################\~~~~~~~~~~~~~~~~~~~~~/##########                                                                                                                                                                                              ")
                set_str(14, r"##########################################   ####################                                                                                                                                                                                              ")
                set_str(15, r"##########/             ~~~~~~~\##########   ####################                                                                                                                                                                                              ")
                set_str(16, r"########## *   O         ~~ ~~~~##########   ####################                                                                                                                                                                                              ")
                set_str(17, r"##########\               ~~~~~~##########   ####################                   EE                   EF                   EG                   EH                   EI                   EJ                   EK                   EL                   EM ")
                set_str(18, r"###########################~~~ ~#########/   ####################                                                                                                                                                                                              ")
                set_str(19, r"###########################~~~ ~~            ####################                                                                                                                                                                                              ")
                set_str(20, r"##########                 ~~~~~~~          /####################                                                                                                                                                                                              ")
            else:
                set_str(2, r"##########/             ~~~~~~~\##########   ####################                                                                                                                                                                                              ")
                set_str(3, r"########## *   O         ~~ ~~~~##########   ####################                                                                                                                                                                                              ")
                set_str(4, r"##########\               ~~~~~~##########   ####################                   EE                   EF                   EG                   EH                   EI                   EJ                   EK                   EL                   EM ")
                set_str(5, r"###########################~~~ ~#########/   ####################                                                                                                                                                                                              ")
                set_str(6, r"###########################~~~ ~~            ####################                                                                                                                                                                                              ")
                set_str(7, r"##########                 ~~~~~~~          /####################                                                                                                                                                                                              ")
                set_str(8, r"#################################################################                                                                                                                                                                                              ")
                set_str(9, r"#################################################################                                                                                                                                                                                              ")
                set_str(10, r"#################################################################                                                                                                                                                                                              ")

        if F == 1:
            U = 6 - int(M * 0.1)
            V = 3 - int(frac(M * 0.1) * 10)
            if U == V: T = -1
            if V == 0: T = 0
            if U == -V: T = 1
            if U == 0: T = 2
            U += 11
            V += 4

        P = 1
        for I in range(1, 8):
            noah_load()

        if get_list(S, 45) != 0:  # display rafts
            for J in range(45, 50, 3):
                A = get_list(S, J) - X + 10
                B = get_list(S, J + 1) - Y + 4
                if B > 0 and B < 8:
                    if A > 0 and A < 22:
                        locate(A, B, "(")
                    A += 1
                    if A > 0 and A < 22:
                        locate(A, B, " ")
                    A += 1
                    if A > 0 and A < 22:
                        locate(A, B, ")")

        E = get_list(S, 51)
        for J in range(3, E, 4):
            A = get_list(S, J) - X + 11
            B = get_list(S, J + 1) - Y + 4
            C = get_list(S, J + 2)
            D = get_list(S, J + 3)
            if A > 0 and A < 22 and B > 0 and B < 8:
                if F == 1 and A == U and B == V:
                    T = 3
                    if C == 204:
                        set_list(S, J, get_list(S, E - 4))  # DELETE ENTITY
                        set_list(S, J + 1, get_list(S, E - 3))
                        set_list(S, J + 2, get_list(S, E - 2))
                        set_list(S, J + 3, get_list(S, E - 1))
                        set_list(S, E - 4, 0)
                        set_list(S, E - 3, 0)
                        set_list(S, E - 2, 0)
                        set_list(S, E - 1, 0)
                        set_list(S, 51, E - 4)
                if C == 0: locate(A, B, "N")  # Noah
                if C == 200: locate(A, B, "#")  # Wall
                if C == 204: locate(A, B, "!")  # Breakable Wall
                if C == 300: locate(A, B, "*")  # Interact-able

        if F == 1:
            if T == -1: locate(U, V, "\\")
            if T == 0: locate(U, V, "-")
            if T == 1: locate(U, V, "//")
            if T == 2: locate(U, V, "|")
            if T == 3: locate(U, V, "*")
        W = mod(Y - 4, 13)
    elif P == 3:
        set_dim_list(26, 250)
        set_list(26, 1, 536870143)
        set_list(26, 2, 0)
        set_list(26, 3, 0)
        set_list(26, 4, 0)
        set_list(26, 5, 0)
        set_list(26, 6, 0)
        set_list(26, 7, 0)
        set_list(26, 8, 4293326848)
        set_list(26, 9, 255)
        set_list(26, 10, 0)
        set_list(26, 11, 0)
        set_list(26, 12, 0)
        set_list(26, 13, 0)
        set_list(26, 14, 0)
        set_list(26, 15, 62914560)
        set_list(26, 16, 524287)
        set_list(26, 17, 0)
        set_list(26, 18, 0)
        set_list(26, 19, 0)
        set_list(26, 20, 0)
        set_list(26, 21, 0)
        set_list(26, 22, 0)
        set_list(26, 23, 1073739790)
        set_list(26, 24, 0)
        set_list(26, 25, 0)
        set_list(26, 26, 0)
        set_list(26, 27, 0)
        set_list(26, 28, 0)
        set_list(26, 29, 0)
        set_list(26, 30, 4290785280)
        set_list(26, 31, 511)
        set_list(26, 32, 0)
        set_list(26, 33, 0)
        set_list(26, 34, 0)
        set_list(26, 35, 0)
        set_list(26, 36, 0)
        set_list(26, 37, 0)
        set_list(26, 38, 524288)
        set_list(26, 39, 0)
        set_list(26, 40, 0)
        set_list(26, 41, 0)
        set_list(26, 42, 0)
        set_list(26, 43, 0)
        set_list(26, 44, 0)
        set_list(26, 45, 2147352588)
        set_list(26, 46, 0)
        set_list(26, 47, 0)
        set_list(26, 48, 0)
        set_list(26, 49, 0)
        set_list(26, 50, 0)
        set_list(26, 51, 0)
        set_list(26, 52, 4026556416)
        set_list(26, 53, 1023)
        set_list(26, 54, 0)
        set_list(26, 55, 0)
        set_list(26, 56, 0)
        set_list(26, 57, 0)
        set_list(26, 58, 0)
        set_list(26, 59, 50331648)
        set_list(26, 60, 2097024)
        set_list(26, 61, 0)
        set_list(26, 62, 0)
        set_list(26, 63, 0)
        set_list(26, 64, 0)
        set_list(26, 65, 0)
        set_list(26, 66, 0)
        set_list(26, 67, 4294967288)
        set_list(26, 68, 0)
        set_list(26, 69, 0)
        set_list(26, 70, 0)
        set_list(26, 71, 0)
        set_list(26, 72, 0)
        set_list(26, 73, 0)
        set_list(26, 74, 4294950912)
        set_list(26, 75, 2047)
        set_list(26, 76, 0)
        set_list(26, 77, 0)
        set_list(26, 78, 0)
        set_list(26, 79, 0)
        set_list(26, 80, 0)
        set_list(26, 81, 4261412864)
        set_list(26, 82, 4294967295)
        set_list(26, 83, 65535)
        set_list(26, 84, 0)
        set_list(26, 85, 0)
        set_list(26, 86, 0)
        set_list(26, 87, 0)
        set_list(26, 88, 0)
        set_list(26, 89, 4294901760)
        set_list(26, 90, 134217727)
        set_list(26, 91, 0)
        set_list(26, 92, 0)
        set_list(26, 93, 0)
        set_list(26, 94, 0)
        set_list(26, 95, 0)
        set_list(26, 96, 4160749568)
        set_list(26, 97, 4294459391)
        set_list(26, 98, 63)
        set_list(26, 99, 0)
        set_list(26, 100, 0)
        set_list(26, 101, 0)
        set_list(26, 102, 0)
        set_list(26, 103, 0)
        set_list(26, 104, 3254779840)
        set_list(26, 105, 131071)
        set_list(26, 106, 0)
        set_list(26, 107, 0)
        set_list(26, 108, 0)
        set_list(26, 109, 0)
        set_list(26, 110, 0)
        set_list(26, 111, 4294852736)
        set_list(26, 112, 268434959)
        set_list(26, 113, 0)
        set_list(26, 114, 0)
        set_list(26, 115, 0)
        set_list(26, 116, 0)
        set_list(26, 117, 0)
        set_list(26, 118, 4026531840)
        set_list(26, 119, 4293951487)
        set_list(26, 120, 127)
        set_list(26, 121, 0)
        set_list(26, 122, 0)
        set_list(26, 123, 0)
        set_list(26, 124, 0)
        set_list(26, 125, 0)
        set_list(26, 126, 4294967168)
        set_list(26, 127, 262143)
        set_list(26, 128, 0)
        set_list(26, 129, 0)
        set_list(26, 130, 0)
        set_list(26, 131, 0)
        set_list(26, 132, 0)
        set_list(26, 133, 4294705152)
        set_list(26, 134, 536866815)
        set_list(26, 135, 0)
        set_list(26, 136, 0)
        set_list(26, 137, 0)
        set_list(26, 138, 0)
        set_list(26, 139, 0)
        set_list(26, 140, 4282253312)
        set_list(26, 141, 4294967295)
        set_list(26, 142, 255)
        set_list(26, 143, 0)
        set_list(26, 144, 0)
        set_list(26, 145, 0)
        set_list(26, 146, 0)
        set_list(26, 147, 4026531840)
        set_list(26, 148, 4269801471)
        set_list(26, 149, 524287)
        set_list(26, 150, 0)
        set_list(26, 151, 0)
        set_list(26, 152, 0)
        set_list(26, 153, 0)
        set_list(26, 154, 0)
        set_list(26, 155, 4294967168)
        set_list(26, 156, 1073741823)
        set_list(26, 157, 0)
        set_list(26, 158, 0)
        set_list(26, 159, 0)
        set_list(26, 160, 0)
        set_list(26, 161, 0)
        set_list(26, 162, 4294705152)
        set_list(26, 163, 4293132287)
        set_list(26, 164, 511)
        set_list(26, 165, 0)
        set_list(26, 166, 0)
        set_list(26, 167, 0)
        set_list(26, 168, 0)
        set_list(26, 169, 536870912)
        set_list(26, 170, 536606720)
        set_list(26, 171, 1048575)
        set_list(26, 172, 0)
        set_list(26, 173, 0)
        set_list(26, 174, 0)
        set_list(26, 175, 0)
        set_list(26, 176, 0)
        set_list(26, 177, 4253024256)
        set_list(26, 178, 2147481855)
        set_list(26, 179, 0)
        set_list(26, 180, 0)
        set_list(26, 181, 0)
        set_list(26, 182, 0)
        set_list(26, 183, 0)
        set_list(26, 184, 524288)
        set_list(26, 185, 4291297272)
        set_list(26, 186, 1023)
        set_list(26, 187, 0)
        set_list(26, 188, 0)
        set_list(26, 189, 0)
        set_list(26, 190, 0)
        set_list(26, 191, 3221225472)
        set_list(26, 192, 1073479679)
        set_list(26, 193, 2097150)
        set_list(26, 194, 0)
        set_list(26, 195, 0)
        set_list(26, 196, 0)
        set_list(26, 197, 0)
        set_list(26, 198, 0)
        set_list(26, 199, 3758095872)
        set_list(26, 200, 4294963200)
        set_list(26, 201, 0)
        set_list(26, 202, 0)
        set_list(26, 203, 0)
        set_list(26, 204, 0)
        set_list(26, 205, 0)
        set_list(26, 206, 0)
        set_list(26, 207, 4290777056)
        set_list(26, 208, 2047)
        set_list(26, 209, 0)
        set_list(26, 210, 0)
        set_list(26, 211, 0)
        set_list(26, 212, 0)
        set_list(26, 213, 0)
        set_list(26, 214, 0)
        set_list(26, 215, 0)
        set_list(26, 216, 0)
        set_list(26, 217, 0)
        set_list(26, 218, 0)
        set_list(26, 219, 0)
        set_list(26, 220, 0)
        set_list(26, 221, 0)
        set_list(26, 222, 0)
        set_list(26, 223, 0)
        set_list(26, 224, 0)
        set_list(26, 225, 0)
        set_list(26, 226, 0)
        set_list(26, 227, 0)
        set_list(26, 228, 0)
        set_list(26, 229, 0)
        set_list(26, 230, 0)
        set_list(26, 231, 0)
        set_list(26, 232, 0)
        set_list(26, 233, 0)
        set_list(26, 234, 0)
        set_list(26, 235, 0)
        set_list(26, 236, 0)
        set_list(26, 237, 0)
        set_list(26, 238, 0)
        set_list(26, 239, 0)
        set_list(26, 240, 0)
        set_list(26, 241, 0)
        set_list(26, 242, 0)
        set_list(26, 243, 0)
        set_list(26, 244, 0)
        set_list(26, 245, 0)
        set_list(26, 246, 0)
        set_list(26, 247, 0)
        set_list(26, 248, 0)
        set_list(26, 249, 0)
        set_list(26, 250, 0)


if __name__ == "__main__":
    run(main)
