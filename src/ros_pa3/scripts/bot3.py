

# grid = np.zeros((35,35,36))
count = 0
grid = []
while count < 35:
    grid2 = []
    grid.append(grid2)
    count = count + 1
    count2 = 0
    while count2 < 35:
        grid3 = [0,0,0,0] # the 4 possible rotations that could be in the square
        grid2.append(grid3)
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
