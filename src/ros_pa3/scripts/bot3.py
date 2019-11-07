

# grid = np.zeros((35,35,36))
count = 0
grid = []
grida = []

# NOTE: for movement multiople translation by 5, result in numbert of squares distance
while count < 35:
    grid2 = []
    grid.append(grid2)
    gridb = []
    grida.append(gridb)
    count = count + 1
    count2 = 0
    while count2 < 35:
        grid3 = [0,0,0,0] # the 4 possible rotations that could be in the square
        gridc = [0,0,0,0]
        grid2.append(grid3)
        gridb.append(gridc)
        count2 = count2 + 1

# NOTE: step through the distribution and place a chip in that grid space


# >>> mu, sigma = 0, 0.1 # mean and standard deviation
# >>> s = np.random.normal(mu, sigma, 1000)
# print(numpy.random.normal(.1, .1, 10))

# tag_positions[0] = Grid_centre_class(125,525,0)
# tag_positions[1] = Grid_centre_class(125,325,0)
# tag_positions[2] = Grid_centre_class(125,125,0)
# tag_positions[3] = Grid_centre_class(425,125,0)
# tag_positions[4] = Grid_centre_class(425,325,0)
# tag_positions[5] = Grid_centre_class(425,525,0)

# as squares
tag_positions[0] = Grid_centre_class(6.25,26.25,0)
tag_positions[1] = Grid_centre_class(6.25,16.25,0)
tag_positions[2] = Grid_centre_class(6.25,6.25,0)
tag_positions[3] = Grid_centre_class(21.25,6.25,0)
tag_positions[4] = Grid_centre_class(21.25,16.25,0)
tag_positions[5] = Grid_centre_class(21.25,26.25,0)

    # print(numpy.degrees(euler))
quaternion = (data.x,data.y,data.z,data.w)
euler = transform.euler_from_quaternion(quaternion)
gausrots = np.random.normal(numpy.degrees(euler), 45, 10) #rot1
sortedrots = [0,0,0,0]
for normalrot in gausrots:
    if normalrot < 45 or normalrot > 305:
        sortedrots[0] = sortedrots[0] + 1
    elif normalrot < 135:
        sortedrots[1] = sortedrots[1] + 1
    elif normalrot < 225:
        sortedrots[2] = sortedrots[2] + 1
    else:
        sortedrots[3] = sortedrots[3] + 1


quaternion2 = (data.x,data.y,data.z,data.w)
euler2 = transform.euler_from_quaternion(quaternion2)
gausrots2 = np.random.normal(numpy.degrees(euler2), 45, 10) #rot2
sortedrots2 = [0,0,0,0]
for normalrot2 in gausrots2:
    if normalrot2 < 45 or normalrot2 > 305:
        sortedrots2[0] = sortedrots2[0] + 1
    elif normalrot < 135:
        sortedrots2[1] = sortedrots2[1] + 1
    elif normalrot < 225:
        sortedrots2[2] = sortedrots2[2] + 1
    else:
        sortedrots2[3] = sortedrots2[3] + 1

travelnormal = np.random.normal((msg.translation * 5), 0.5, 10) # translation
rowcount = -1
colcount = -1

# go through each square and if there is probabikity that the bot is there
# Then set the values on the OTHER grid, resulting in the sum of all possible ecurrent states
while rowcount < 35:
    rowcount = rowcount + 1
    colcount = -1
    while colcount < 35:
        colcount = colcount + 1
        col = grid[rowcount][colcount]

        for distnotrounded in travelnormal:
            dist = 0
            dist = int(ceil(distnotrounded))
            # NOTE: iterate through each possible rotation and current rotation in square to check if moving the distance is on the map
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


        if rowcount + dist < 35 and rowcount + dist > 0
        for rot in col:
            if rot > 0:
                for dist in travelnormal:
                    if rowcount + dist < 35 and rowcount + dist > 0
