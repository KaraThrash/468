import math
class Node():

    parent = None
    position = (-1,-1)
    x = -1
    y = -1
    g = -1
    h = -1
    f = -1
    wall = 1


count = 0
count2 = 0
maparray = []
maze = []
def astar(maze2, start, end):

    global maparray
    global maze

    start_node = Node()
    start_node.position = start
    start_node.x = start[1]
    start_node.y = start[0]
    start_node.f = 0
    start_node.g = 0
    start_node.h = 0#math.sqrt((start[0] - end[0])**2 +(start[1] - end[1])**2  )
    end_node = Node()
    end_node.position = end
    end_node.g = 0
    end_node.h = 0
    end_node.f = -100
    end_node.x = end[1]
    end_node.y = end[0]

    open_list = []

    current_node = start_node

    open_list.append(start_node)

    while current_node.position != end :

        lastnode = current_node


        if current_node.x > 0:
            if maparray[current_node.y][current_node.x - 1].wall == 0:
                # #print(maparray[current_node.y][current_node.x - 1])
                if maparray[current_node.y][current_node.x - 1].f == -1 or maparray[current_node.y][current_node.x - 1].f > (1 + current_node.f + maparray[current_node.y][current_node.x - 1].g):
                    maparray[current_node.y][current_node.x - 1].f = current_node.f + maparray[current_node.y][current_node.x - 1].g
                    maparray[current_node.y][current_node.x - 1].parent = current_node
                    open_list.append(maparray[current_node.y][current_node.x - 1])
        if current_node.x < len(maparray[0]) - 1:
            if maparray[current_node.y][current_node.x + 1].wall == 0:
                # #print(maparray[current_node.y][current_node.x + 1].wall )
                if maparray[current_node.y][current_node.x + 1].f == -1 or maparray[current_node.y][current_node.x + 1].f > (1 + current_node.f + maparray[current_node.y][current_node.x + 1].g):
                    maparray[current_node.y][current_node.x + 1].f = current_node.f + maparray[current_node.y][current_node.x + 1].g
                    maparray[current_node.y][current_node.x + 1].parent = current_node
                    open_list.append(maparray[current_node.y][current_node.x + 1])


        if current_node.y > 0:
            if maparray[current_node.y - 1][current_node.x ].wall == 0:
                #print(maparray[current_node.y - 1][current_node.x ].wall)
                if maparray[current_node.y - 1 ][current_node.x ].f == -1 or maparray[current_node.y - 1][current_node.x ].f > (1 + current_node.f + maparray[current_node.y - 1][current_node.x ].g):
                    maparray[current_node.y - 1][current_node.x ].f = current_node.f + maparray[current_node.y - 1][current_node.x ].g
                    maparray[current_node.y - 1][current_node.x ].parent = current_node
                    open_list.append(maparray[current_node.y - 1][current_node.x ])

            if current_node.x > 0:
                if maparray[current_node.y - 1][current_node.x - 1].wall == 0:
                    if maparray[current_node.y ][current_node.x - 1].wall != 1 and maparray[current_node.y - 1][current_node.x ].wall != 1:
                        #print(maparray[current_node.y - 1][current_node.x - 1])
                        if maparray[current_node.y - 1][current_node.x - 1].f == -1 or maparray[current_node.y - 1][current_node.x - 1].f > (2 + current_node.f + maparray[current_node.y - 1][current_node.x - 1].g):
                            maparray[current_node.y - 1][current_node.x - 1].f = current_node.f + maparray[current_node.y - 1][current_node.x - 1].g
                            maparray[current_node.y - 1][current_node.x - 1].parent = current_node
                            open_list.append(maparray[current_node.y - 1][current_node.x - 1])
            if current_node.x < len(maparray[0]) - 1:
                if maparray[current_node.y - 1][current_node.x + 1].wall == 0:
                    if maparray[current_node.y ][current_node.x + 1].wall != 1 and maparray[current_node.y - 1][current_node.x ].wall != 1:
                        #print(maparray[current_node.y - 1][current_node.x + 1].wall )
                        if maparray[current_node.y - 1][current_node.x + 1].f == -1 or maparray[current_node.y - 1][current_node.x + 1].f > (2 + current_node.f + maparray[current_node.y - 1][current_node.x + 1].g):
                            maparray[current_node.y - 1][current_node.x + 1].f = current_node.f + maparray[current_node.y - 1][current_node.x + 1].g
                            maparray[current_node.y - 1][current_node.x + 1].parent = current_node
                            open_list.append(maparray[current_node.y - 1][current_node.x + 1])
        if current_node.y < len(maparray) - 1:
            if maparray[current_node.y + 1][current_node.x ].wall == 0:
                #print(maparray[current_node.y + 1][current_node.x ].wall)
                if maparray[current_node.y + 1 ][current_node.x ].f == -1 or maparray[current_node.y + 1][current_node.x ].f > (1 + current_node.f + maparray[current_node.y + 1][current_node.x ].g):
                    maparray[current_node.y + 1][current_node.x ].f = current_node.f + maparray[current_node.y + 1][current_node.x ].g
                    maparray[current_node.y + 1][current_node.x ].parent = current_node
                    open_list.append(maparray[current_node.y + 1][current_node.x ])

                if current_node.x > 0:
                    if maparray[current_node.y + 1][current_node.x - 1].wall == 0:
                        if maparray[current_node.y ][current_node.x - 1].wall != 1 and maparray[current_node.y + 1][current_node.x ].wall != 1:
                            #print(maparray[current_node.y + 1][current_node.x - 1])
                            if maparray[current_node.y + 1][current_node.x - 1].f == -1 or maparray[current_node.y + 1][current_node.x - 1].f > (2 + current_node.f + maparray[current_node.y + 1][current_node.x - 1].g):
                                maparray[current_node.y + 1][current_node.x - 1].f = current_node.f + maparray[current_node.y + 1][current_node.x - 1].g
                                maparray[current_node.y + 1][current_node.x - 1].parent = current_node
                                open_list.append(maparray[current_node.y + 1][current_node.x - 1])
                if current_node.x < len(maparray[0]) - 1:
                    if maparray[current_node.y + 1][current_node.x + 1].wall == 0:
                        if maparray[current_node.y ][current_node.x + 1].wall != 1 and maparray[current_node.y + 1][current_node.x ].wall != 1:
                            #print(maparray[current_node.y + 1][current_node.x + 1].wall )
                            if maparray[current_node.y + 1][current_node.x + 1].f == -1 or maparray[current_node.y + 1][current_node.x + 1].f > (2 + current_node.f + maparray[current_node.y + 1][current_node.x + 1].g):
                                maparray[current_node.y + 1][current_node.x + 1].f = current_node.f + maparray[current_node.y + 1][current_node.x + 1].g
                                maparray[current_node.y + 1][current_node.x + 1].parent = current_node
                                open_list.append(maparray[current_node.y + 1][current_node.x + 1])

        if len(open_list) > 0:
            current_node = open_list[0]
            open_list.remove(current_node)
        for el in open_list:
            if el.f < current_node.f:
                current_node = el



    path = []
    current = current_node
    while current.position != start:
        path.append((current.y,current.x))
        # maze[current.y][current.x] = 2
        current = current.parent
    # for el in maze:
    #     print(el)
    pathlength = len(path) - 1
    returnpath = []
    while pathlength >= 0:
        returnpath.append(path[pathlength])
        pathlength = pathlength - 1

    return returnpath#path[::-1]


def mainx(endy,endx,starty,startx):        #5
    global maparray
    global maze
    maze = [[0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0],
         # [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7],
           [0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0], #5
           [0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0],
           [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0],
           [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
           [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
           [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1],#10
           [0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0],
           [0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,0],
           [0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,1,1,0],
           [0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,1,0],
         # [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7],
           [0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,1]]

# + 10x + 9y to off set the negative start
# y,x

    countx = 0
    county = -1
    # start = (12, 1)
    # end = (1,13)
    start = (10 - starty,startx + 9)
    end = (endy,endx)
    for row in maze:
        countx = 0
        county = county + 1
        rowarray = []
        maparray.append(rowarray)
        for col in row:
            newnode = Node()
            newnode.g = math.sqrt((county - end[0])**2 +(countx - end[1])**2  )
            newnode.x = countx
            newnode.y = county
            newnode.position = (county,countx)
            newnode.f = -1
            newnode.wall = maze[county][countx]
            rowarray.append(newnode)
            countx = countx + 1

     # //shorter y because the bot has to approach from the opening
    # #print(maparray)
    path = astar(maze, start, end)
    print(path)
    return path
#
# if __name__ == '__main__':
    # main(13,1)
