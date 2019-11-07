if col[0] > 0: # right
    if colcount + dist < 35:
        grida[rowcount][colcount + dist][0] = grida[rowcount][colcount + dist][0] + (col[0] * sortedrots2[0]) * sortedrots2[0])
        grida[rowcount][colcount + dist][1] = grida[rowcount][colcount + dist][1] + (col[0] * sortedrots2[0]) * sortedrots2[1])
        grida[rowcount][colcount + dist][2] = grida[rowcount][colcount + dist][2] + (col[0] * sortedrots2[0]) * sortedrots2[2])
        grida[rowcount][colcount + dist][3] = grida[rowcount][colcount + dist][3] + (col[0] * sortedrots2[0]) * sortedrots2[3])
    if colcount - dist > 0:
        grida[rowcount][colcount + dist][0] = grida[rowcount][colcount - dist][0] + (col[0] * sortedrots2[2]) * sortedrots2[0])
        grida[rowcount][colcount + dist][1] = grida[rowcount][colcount - dist][1] + (col[0] * sortedrots2[2]) * sortedrots2[1])
        grida[rowcount][colcount + dist][2] = grida[rowcount][colcount - dist][2] + (col[0] * sortedrots2[2]) * sortedrots2[2])
        grida[rowcount][colcount + dist][3] = grida[rowcount][colcount - dist][3] + (col[0] * sortedrots2[2]) * sortedrots2[3])
    if rowcount - dist > 0:
        grida[rowcount][colcount + dist][0] = grida[rowcount - dist][colcount ][0] + (col[0] * sortedrots2[1]) * sortedrots2[0])
        grida[rowcount][colcount + dist][1] = grida[rowcount - dist][colcount ][1] + (col[0] * sortedrots2[1]) * sortedrots2[1])
        grida[rowcount][colcount + dist][2] = grida[rowcount - dist][colcount ][2] + (col[0] * sortedrots2[1]) * sortedrots2[2])
        grida[rowcount][colcount + dist][3] = grida[rowcount - dist][colcount ][3] + (col[0] * sortedrots2[1]) * sortedrots2[3])
    if rowcount + dist < 35:
        grida[rowcount][colcount + dist][0] = grida[rowcount + dist][colcount ][0] + (col[0] * sortedrots2[3]) * sortedrots2[0])
        grida[rowcount][colcount + dist][1] = grida[rowcount + dist][colcount ][1] + (col[0] * sortedrots2[3]) * sortedrots2[1])
        grida[rowcount][colcount + dist][2] = grida[rowcount + dist][colcount ][2] + (col[0] * sortedrots2[3]) * sortedrots2[2])
        grida[rowcount][colcount + dist][3] = grida[rowcount + dist][colcount ][3] + (col[0] * sortedrots2[3]) * sortedrots2[3])

    # rot 1: the bot current facing up
if col[1] > 0: # up
    if colcount + dist < 35:
        grida[rowcount][colcount + dist][0] = grida[rowcount][colcount + dist][0] + (col[1] * sortedrots2[3]) * sortedrots2[0])
        grida[rowcount][colcount + dist][1] = grida[rowcount][colcount + dist][1] + (col[1] * sortedrots2[3]) * sortedrots2[1])
        grida[rowcount][colcount + dist][2] = grida[rowcount][colcount + dist][2] + (col[1] * sortedrots2[3]) * sortedrots2[2])
        grida[rowcount][colcount + dist][3] = grida[rowcount][colcount + dist][3] + (col[1] * sortedrots2[3]) * sortedrots2[3])
    if colcount - dist > 0:
        grida[rowcount][colcount + dist][0] = grida[rowcount][colcount - dist][0] + (col[1] * sortedrots2[0]) * sortedrots2[0])
        grida[rowcount][colcount + dist][1] = grida[rowcount][colcount - dist][1] + (col[1] * sortedrots2[0]) * sortedrots2[1])
        grida[rowcount][colcount + dist][2] = grida[rowcount][colcount - dist][2] + (col[1] * sortedrots2[0]) * sortedrots2[2])
        grida[rowcount][colcount + dist][3] = grida[rowcount][colcount - dist][3] + (col[1] * sortedrots2[0]) * sortedrots2[3])
    if rowcount - dist > 0:
        grida[rowcount][colcount + dist][0] = grida[rowcount - dist][colcount ][0] + (col[1] * sortedrots2[1]) * sortedrots2[0])
        grida[rowcount][colcount + dist][1] = grida[rowcount - dist][colcount ][1] + (col[1] * sortedrots2[1]) * sortedrots2[1])
        grida[rowcount][colcount + dist][2] = grida[rowcount - dist][colcount ][2] + (col[1] * sortedrots2[1]) * sortedrots2[2])
        grida[rowcount][colcount + dist][3] = grida[rowcount - dist][colcount ][3] + (col[1] * sortedrots2[1]) * sortedrots2[3])
    if rowcount + dist < 35:
        grida[rowcount][colcount + dist][0] = grida[rowcount + dist][colcount ][0] + (col[1] * sortedrots2[2]) * sortedrots2[0])
        grida[rowcount][colcount + dist][1] = grida[rowcount + dist][colcount ][1] + (col[1] * sortedrots2[2]) * sortedrots2[1])
        grida[rowcount][colcount + dist][2] = grida[rowcount + dist][colcount ][2] + (col[1] * sortedrots2[2]) * sortedrots2[2])
        grida[rowcount][colcount + dist][3] = grida[rowcount + dist][colcount ][3] + (col[1] * sortedrots2[2]) * sortedrots2[3])
if col[2] > 0: # left
    if colcount + dist < 35:
        grida[rowcount][colcount + dist][0] = grida[rowcount][colcount + dist][0] + (col[2] * sortedrots2[2]) * sortedrots2[0])
        grida[rowcount][colcount + dist][1] = grida[rowcount][colcount + dist][1] + (col[2] * sortedrots2[2]) * sortedrots2[1])
        grida[rowcount][colcount + dist][2] = grida[rowcount][colcount + dist][2] + (col[2] * sortedrots2[2]) * sortedrots2[2])
        grida[rowcount][colcount + dist][3] = grida[rowcount][colcount + dist][3] + (col[2] * sortedrots2[2]) * sortedrots2[3])
    if colcount - dist > 0:
        grida[rowcount][colcount + dist][0] = grida[rowcount][colcount - dist][0] + (col[2] * sortedrots2[0]) * sortedrots2[0])
        grida[rowcount][colcount + dist][1] = grida[rowcount][colcount - dist][1] + (col[2] * sortedrots2[0]) * sortedrots2[1])
        grida[rowcount][colcount + dist][2] = grida[rowcount][colcount - dist][2] + (col[2] * sortedrots2[0]) * sortedrots2[2])
        grida[rowcount][colcount + dist][3] = grida[rowcount][colcount - dist][3] + (col[2] * sortedrots2[0]) * sortedrots2[3])
    if rowcount - dist > 0:
        grida[rowcount][colcount + dist][0] = grida[rowcount - dist][colcount ][0] + (col[2] * sortedrots2[3]) * sortedrots2[0])
        grida[rowcount][colcount + dist][1] = grida[rowcount - dist][colcount ][1] + (col[2] * sortedrots2[3]) * sortedrots2[1])
        grida[rowcount][colcount + dist][2] = grida[rowcount - dist][colcount ][2] + (col[2] * sortedrots2[3]) * sortedrots2[2])
        grida[rowcount][colcount + dist][3] = grida[rowcount - dist][colcount ][3] + (col[2] * sortedrots2[3]) * sortedrots2[3])
    if rowcount + dist < 35:
        grida[rowcount][colcount + dist][0] = grida[rowcount + dist][colcount ][0] + (col[2] * sortedrots2[1]) * sortedrots2[0])
        grida[rowcount][colcount + dist][1] = grida[rowcount + dist][colcount ][1] + (col[2] * sortedrots2[1]) * sortedrots2[1])
        grida[rowcount][colcount + dist][2] = grida[rowcount + dist][colcount ][2] + (col[2] * sortedrots2[1]) * sortedrots2[2])
        grida[rowcount][colcount + dist][3] = grida[rowcount + dist][colcount ][3] + (col[2] * sortedrots2[1]) * sortedrots2[3])
if col[3] > 0: # down
    if colcount + dist < 35:
        grida[rowcount][colcount + dist][0] = grida[rowcount][colcount + dist][0] + (col[3] * sortedrots2[1]) * sortedrots2[0])
        grida[rowcount][colcount + dist][1] = grida[rowcount][colcount + dist][1] + (col[3] * sortedrots2[1]) * sortedrots2[1])
        grida[rowcount][colcount + dist][2] = grida[rowcount][colcount + dist][2] + (col[3] * sortedrots2[1]) * sortedrots2[2])
        grida[rowcount][colcount + dist][3] = grida[rowcount][colcount + dist][3] + (col[3] * sortedrots2[1]) * sortedrots2[3])
    if colcount - dist > 0:
        grida[rowcount][colcount + dist][0] = grida[rowcount][colcount - dist][0] + (col[3] * sortedrots2[3]) * sortedrots2[0])
        grida[rowcount][colcount + dist][1] = grida[rowcount][colcount - dist][1] + (col[3] * sortedrots2[3]) * sortedrots2[1])
        grida[rowcount][colcount + dist][2] = grida[rowcount][colcount - dist][2] + (col[3] * sortedrots2[3]) * sortedrots2[2])
        grida[rowcount][colcount + dist][3] = grida[rowcount][colcount - dist][3] + (col[3] * sortedrots2[3]) * sortedrots2[3])
    if rowcount - dist > 0:
        grida[rowcount][colcount + dist][0] = grida[rowcount - dist][colcount ][0] + (col[3] * sortedrots2[2]) * sortedrots2[0])
        grida[rowcount][colcount + dist][1] = grida[rowcount - dist][colcount ][1] + (col[3] * sortedrots2[2]) * sortedrots2[1])
        grida[rowcount][colcount + dist][2] = grida[rowcount - dist][colcount ][2] + (col[3] * sortedrots2[2]) * sortedrots2[2])
        grida[rowcount][colcount + dist][3] = grida[rowcount - dist][colcount ][3] + (col[3] * sortedrots2[2]) * sortedrots2[3])
    if rowcount + dist < 35:
        grida[rowcount][colcount + dist][0] = grida[rowcount + dist][colcount ][0] + (col[3] * sortedrots2[0]) * sortedrots2[0])
        grida[rowcount][colcount + dist][1] = grida[rowcount + dist][colcount ][1] + (col[3] * sortedrots2[0]) * sortedrots2[1])
        grida[rowcount][colcount + dist][2] = grida[rowcount + dist][colcount ][2] + (col[3] * sortedrots2[0]) * sortedrots2[2])
        grida[rowcount][colcount + dist][3] = grida[rowcount + dist][colcount ][3] + (col[3] * sortedrots2[0]) * sortedrots2[3])
