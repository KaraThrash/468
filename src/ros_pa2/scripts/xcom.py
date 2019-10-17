import math
class Node():
    # """A node class for A* Pathfinding"""
    #
    # def __init__(self, x, y, parent=None):
    parent = None
    position = (-1,-1)
    x = -1
    y = -1
    g = -1
    h = -1
    f = -1
    wall = 1

    # def __eq__(self, other):
        # return self.position == other.position

count = 0
count2 = 0
maparray = []
maze = []
def astar(maze2, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    global maparray
    global maze
    # Create start and end node
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
    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node

    print(open_list)
    # Loop until you find the end
    current_node = start_node

    open_list.append(start_node)

    while current_node.position != end :
    # while len(open_list) > 0:
        # Get the current node
        lastnode = current_node


        # closed_list.append(current_node)

        # Found the goal
        # if current_node.x == end[1] and current_node.y == end[0]:
        #     print(current_node.y,current_node.x)
        #     path = []
        #     current = current_node
        #     while current.x != start[1] and start[0] != current.y:
        #         path.append((current.y,current.x))
        #         maze[current.y][current.x] = 2
        #         current = current.parent
        #     print(current.y,current.x)
        #     print(start_node.y,start_node.x)
        #     for el in maze:
        #         print(el)
        #     # print(path)
        #     return path[::-1] # Return reversed path



        if current_node.x > 0:
            if maparray[current_node.y][current_node.x - 1].wall == 0:
                print(maparray[current_node.y][current_node.x - 1])
                if maparray[current_node.y][current_node.x - 1].f == -1 or maparray[current_node.y][current_node.x - 1].f > (1 + current_node.f + maparray[current_node.y][current_node.x - 1].g):
                    maparray[current_node.y][current_node.x - 1].f = current_node.f + maparray[current_node.y][current_node.x - 1].g
                    maparray[current_node.y][current_node.x - 1].parent = current_node
                    open_list.append(maparray[current_node.y][current_node.x - 1])
        if current_node.x < len(maparray[0]) - 1:
            if maparray[current_node.y][current_node.x + 1].wall == 0:
                print(maparray[current_node.y][current_node.x + 1].wall )
                if maparray[current_node.y][current_node.x + 1].f == -1 or maparray[current_node.y][current_node.x + 1].f > (1 + current_node.f + maparray[current_node.y][current_node.x + 1].g):
                    maparray[current_node.y][current_node.x + 1].f = current_node.f + maparray[current_node.y][current_node.x + 1].g
                    maparray[current_node.y][current_node.x + 1].parent = current_node
                    open_list.append(maparray[current_node.y][current_node.x + 1])


        if current_node.y > 0:
            if maparray[current_node.y - 1][current_node.x ].wall == 0:
                print(maparray[current_node.y - 1][current_node.x ].wall)
                if maparray[current_node.y - 1 ][current_node.x ].f == -1 or maparray[current_node.y - 1][current_node.x ].f > (1 + current_node.f + maparray[current_node.y - 1][current_node.x ].g):
                    maparray[current_node.y - 1][current_node.x ].f = current_node.f + maparray[current_node.y - 1][current_node.x ].g
                    maparray[current_node.y - 1][current_node.x ].parent = current_node
                    open_list.append(maparray[current_node.y - 1][current_node.x ])

            if current_node.x > 0:
                if maparray[current_node.y - 1][current_node.x - 1].wall == 0:
                    if maparray[current_node.y ][current_node.x - 1].wall != 1 and maparray[current_node.y - 1][current_node.x ].wall != 1:
                        print(maparray[current_node.y - 1][current_node.x - 1])
                        if maparray[current_node.y - 1][current_node.x - 1].f == -1 or maparray[current_node.y - 1][current_node.x - 1].f > (2 + current_node.f + maparray[current_node.y - 1][current_node.x - 1].g):
                            maparray[current_node.y - 1][current_node.x - 1].f = current_node.f + maparray[current_node.y - 1][current_node.x - 1].g
                            maparray[current_node.y - 1][current_node.x - 1].parent = current_node
                            open_list.append(maparray[current_node.y - 1][current_node.x - 1])
            if current_node.x < len(maparray[0]) - 1:
                if maparray[current_node.y - 1][current_node.x + 1].wall == 0:
                    if maparray[current_node.y ][current_node.x + 1].wall != 1 and maparray[current_node.y - 1][current_node.x ].wall != 1:
                        print(maparray[current_node.y - 1][current_node.x + 1].wall )
                        if maparray[current_node.y - 1][current_node.x + 1].f == -1 or maparray[current_node.y - 1][current_node.x + 1].f > (2 + current_node.f + maparray[current_node.y - 1][current_node.x + 1].g):
                            maparray[current_node.y - 1][current_node.x + 1].f = current_node.f + maparray[current_node.y - 1][current_node.x + 1].g
                            maparray[current_node.y - 1][current_node.x + 1].parent = current_node
                            open_list.append(maparray[current_node.y - 1][current_node.x + 1])
        if current_node.y < len(maparray) - 1:
            if maparray[current_node.y + 1][current_node.x ].wall == 0:
                print(maparray[current_node.y + 1][current_node.x ].wall)
                if maparray[current_node.y + 1 ][current_node.x ].f == -1 or maparray[current_node.y + 1][current_node.x ].f > (1 + current_node.f + maparray[current_node.y + 1][current_node.x ].g):
                    maparray[current_node.y + 1][current_node.x ].f = current_node.f + maparray[current_node.y + 1][current_node.x ].g
                    maparray[current_node.y + 1][current_node.x ].parent = current_node
                    open_list.append(maparray[current_node.y + 1][current_node.x ])

                if current_node.x > 0:
                    if maparray[current_node.y + 1][current_node.x - 1].wall == 0:
                        if maparray[current_node.y ][current_node.x - 1].wall != 1 and maparray[current_node.y + 1][current_node.x ].wall != 1:
                            print(maparray[current_node.y + 1][current_node.x - 1])
                            if maparray[current_node.y + 1][current_node.x - 1].f == -1 or maparray[current_node.y + 1][current_node.x - 1].f > (2 + current_node.f + maparray[current_node.y + 1][current_node.x - 1].g):
                                maparray[current_node.y + 1][current_node.x - 1].f = current_node.f + maparray[current_node.y + 1][current_node.x - 1].g
                                maparray[current_node.y + 1][current_node.x - 1].parent = current_node
                                open_list.append(maparray[current_node.y + 1][current_node.x - 1])
                if current_node.x < len(maparray[0]) - 1:
                    if maparray[current_node.y + 1][current_node.x + 1].wall == 0:
                        if maparray[current_node.y ][current_node.x + 1].wall != 1 and maparray[current_node.y + 1][current_node.x ].wall != 1:
                            print(maparray[current_node.y + 1][current_node.x + 1].wall )
                            if maparray[current_node.y + 1][current_node.x + 1].f == -1 or maparray[current_node.y + 1][current_node.x + 1].f > (2 + current_node.f + maparray[current_node.y + 1][current_node.x + 1].g):
                                maparray[current_node.y + 1][current_node.x + 1].f = current_node.f + maparray[current_node.y + 1][current_node.x + 1].g
                                maparray[current_node.y + 1][current_node.x + 1].parent = current_node
                                open_list.append(maparray[current_node.y + 1][current_node.x + 1])
        # print(len(open_list))
        for el in open_list:
            print(" : ",el.y," : ",el.x)

        current_node = open_list[0]
        current_index = 0
        print(current_node.y,current_node.x)
        for el in open_list:
            if el.f < current_node.f:
                current_node = el
                print(current_node.y,current_node.x)
        open_list.remove(current_node)
    # if current_node.x == end[1] and current_node.y == end[0]:
    print(current_node.y,current_node.x)
    path = []
    current = current_node
    while current.position != start:
        path.append((current.y,current.x))
        print(len(path),"path : nodes")
        maze[current.y][current.x] = 2
        current = current.parent

    print(current.y,current.x)
    print(start_node.y,start_node.x)
    for el in maze:
        print(el)
    # print(path)
    return path[::-1] # Return reversed path
            # Make sure within range
            # if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
            #     print("-")maparray
            #     continue
            #
            # # Make sure walkable terrain
            # if maze[node_position[0]][node_position[1]] != 0:
            #
            #     continue
            #
            # # Create new node
            # new_node = Node(current_node, node_position)
            #
            # # Append
            # children.append(new_node)

        #
        # # Loop through children
        # for child in children:
        #     # print("==")
        #     count = count + 1
        #     if count > 1000:
        #         print("xx", count2)
        #         count = 0
        #         count2 = count2 + 1
        #     # Child is on the c.flosed list
        #     for closed_child in closed_list:
        #
        #         if child == closed_child:
        #             continue
        #
        #     # Create the f, g, and h values
        #     child.g = current_node.g + 10
        #     child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
        #     child.f = child.g + child.h
        #
        #     # Child is already in the open list
        #     for open_node in open_list:
        #
        #         if child == open_node and child.g > open_node.g:
        #             continue
        #
        #     # Add the child to the open list
        #     open_list.append(child)


def main():        #5
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

    # maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0.f, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    # maze = [[0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0],
    #      # [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7],
    #        [0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0],
    #        [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    #        [1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    #        [0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    #        [0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0], #5
    #        [0,0,1,1,0,0,1,1,1,1,1,1,0,0,0,0,0,0],
    #        [0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,1,1,0],
    #        [0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,1,1],
    #        [1,1,1,1,1,1,0,0,0,0,0,1,0,0,0,1,1,1],
    #        [1,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,1],#10
    #        [1,1,1,1,1,1,1,0,0,0,0,1,0,0,0,1,1,0],
    #        [1,0,0,0,1,1,1,1,1,0,0,1,0,0,0,1,0,0],
    #        [1,0,0,0,1,0,0,1,1,1,1,1,0,0,0,1,0,0],
    #        [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0],
    #        [1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0],
    #        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    #        [0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,1,1,0],
    #        [0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,1,0],
    #      # [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7],
    #        [0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,1]]
    #
    # maze = [[0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0], #5
    #        [0,0,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0,0],
    #        [0,0,0,1,1,1,0,0,0,1,0,0,0,0,1,1,0],
    #        [0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,1,1,1],
    #        [0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,1,1,1],
    #        [1,1,1,1,1,1,0,0,0,1,0,0,0,0,0,1,1,1],#10
    #        [1,0,0,0,0,1,1,0,0,1,0,0,0,0,0,1,1,0],
    #        [1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,1,0,0],
    #        [1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0],
    #        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
    #        [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0],
    #        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],,0,0,0],
    #      # [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7],
    #        [0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1],
    #        [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],0
    #        [1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    #        [0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    #        [0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0], #5
    #        [0,0,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0,0],
    #        [0,0,0,1,1,1,0,0,0,1,0,0,0,0,1,1,0],
    #        [0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,1,1,1],
    #        [0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,1,1,1],
    #        [1,1,1,1,1,1,0,0,0,1,0,0,0,0,0,1,1,1],#10
    #        [1,0,0,0,0,1,1,0,0,1,0,0,0,0,0,1,1,0],
    #        [1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,1,0,0],
    #        [1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0],
    #        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
    #        [1,0,0,0,0,0,0,0,1,0,0,0,county0,0,0,1,0,0],
    #        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    #        [0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,1,1,0],
    #        [1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,0],
    #      # [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7],
    #        [0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,1]]

# + 10x + 9y to off set the negative start
# y,x

    countx = 0
    county = -1
    start = (12, 1)
    end = (1,13)
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
    # print(maparray)
    path = astar(maze, start, end)
    print(path)
    return path
#
# if __name__ == '__main__':
#     mainx()
