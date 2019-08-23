#!/usr/bin/python3

import base64

POWERS = [2**x for x in range(50)]
POWERS[0] = 0

def exportGame(board):
    binData = "1"
    for row in board:
        for col in row:
            binData += ("1"*POWERS.index(col))+"0"
    # return base64.b64encode(hex(int(binData,2))[2:].encode()).decode() # With b64
    return hex(int(binData,2))[2:] # Without b64

def importGame(code):
    # binData = bin(int(base64.b64decode(code.encode()).decode(), 16))[3:] # With b64
    binData = bin(int(code, 16))[3:] # Without b64
    numbers = []
    while binData.find("0") >= 0:
        part = binData[:binData.find("0")]
        binData = binData[binData.find("0")+1:]
        # print(part, binData)
        numbers.append(2**len(part))
    numbers = [0 if x == 1 else x for x in numbers]
    board = [[numbers[y] for y in range(x, x+4)] for x in range(0, 16, 4)]
    return board


if __name__ == "__main__":
    import game2048
    inp = input("Recovery code: ")
    print(game2048.render_screen(importGame(inp)))
