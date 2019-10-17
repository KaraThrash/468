import math
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, x, y, parent=None):
        self.parent = parent
        # self.position = position
        self.x = -1
        self.y = -1
        self.g = -1
        self.h = -1
        self.f = -1

    # def __eq__(self, other):
        # return self.position == other.position

count = 0
count2 = 0
maparray = []
def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""
    global count
    global count2
    global maparray

    # Create start and end node
    start_node = Node(start[0], start[1])
    start_node.x = start[1]
    start_node.y = start[0]
    start_node.g = start_node.h = start_node.f = math.sqrt((start[0] - end[0])**2 +(start[1] - end[1])**2  )
    end_node = Node(end[0], end[1])
    end_node.g = end_node.h = end_node.f = 0
    end_node.x = end[1]
    end_node.y = end[0]
    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)
    print(open_list)
    # Loop until you find the end
    current_node = start_node
    while len(open_list) > 0:
        print("red")
        # Get the current node
        lastnode = current_node
        current_node = open_list[0]
        current_index = 0
        for el in open_list:
            if el.f < current_node.f:
                current_node = el
        open_list.remove(current_node)

        closed_list.append(current_node)

        # Found the goal
        if current_node.x == end_node.x and current_node.y == end_node.y:
            path = []
            current = current_node
            while current.x != start.x and start.y != current.y:
                path.append((current.y,current.x))
                current = current.parent
            print(path)
            return path[::-1] # Return reversed path



        if current_node.x > 0:
            if maze[current_node.y][current_node.x - 1] != 1:
                if maparray[current_node.y][current_node.x - 1] == -1 or maparray[current_node.y][current_node.x - 1].f > (current_node.f + maparray[current_node.y][current_node.x - 1].g):
                    maparray[current_node.y][current_node.x - 1].f = current_node.f + maparray[current_node.y][current_node.x - 1].g
                    maparray[current_node.y][current_node.x - 1].parent = current_node
                    open_list.append(maparray[current_node.y][current_node.x - 1])
        if current_node.x < len(maparray[0]) - 2:
            if maze[current_node.y][current_node.x + 1] != 1:
                if maparray[current_node.y][current_node.x + 1] == -1 or maparray[current_node.y][current_node.x + 1].f > (current_node.f + maparray[current_node.y][current_node.x + 1].g):
                    maparray[current_node.y][current_node.x + 1].f = current_node.f + maparray[current_node.y][current_node.x + 1].g
                    maparray[current_node.y][current_node.x + 1].parent = current_node
                    open_list.append(maparray[current_node.y][current_node.x + 1])
        if current_node.y > 0:
            if maze[current_node.y - 1][current_node.x ] != 1:
                if maparray[current_node.y - 1 ][current_node.x ] == -1 or maparray[current_node.y - 1][current_node.x ].f > (current_node.f + maparray[current_node.y - 1][current_node.x ].g):
                    maparray[current_node.y - 1][current_node.x ].f = current_node.f + maparray[current_node.y - 1][current_node.x ].g
                    maparray[current_node.y - 1][current_node.x ].parent = current_node
                    open_list.append(maparray[current_node.y - 1][current_node.x ])
        if current_node.y < len(maparray) - 2:
            if maze[current_node.y + 1][current_node.x ] != 1:
                if maparray[current_node.y + 1 ][current_node.x ] == -1 or maparray[current_node.y + 1][current_node.x ].f > (current_node.f + maparray[current_node.y + 1][current_node.x ].g):
                    maparray[current_node.y + 1][current_node.x ].f = current_node.f + maparray[current_node.y + 1][current_node.x ].g
                    maparray[current_node.y + 1][current_node.x ].parent = current_node
                    open_list.append(maparray[current_node.y + 1][current_node.x ])
        print(len(open_list))

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
        #     # Child is on the closed list
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


def mainx():        #5
    global  maparray
    # maze = [[0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0],
    #      # [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7],
    #        [0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0],
    #        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    #        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    #        [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    #        [0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0], #5
    #        [0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0],
    #        [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0],
    #        [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
    #        [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
    #        [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1],#10
    #        [0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0],
    #        [0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0],
    #        [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    #        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    #        [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
    #        [0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,0],
    #        [0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,1,1,0],
    #        [0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,1,0],
    #      # [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7],
    #        [0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,1]]

    # maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    maze = [[0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0],
         # [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7],
           [0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
           [1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
           [0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
           [0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0], #5
           [0,0,1,1,0,0,1,1,1,1,1,1,0,0,0,0,0,0],
           [0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,1,1,0],
           [0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,1,1],
           [1,1,1,1,1,1,0,0,0,0,0,1,0,0,0,1,1,1],
           [1,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,1],#10
           [1,1,1,1,1,1,1,0,0,0,0,1,0,0,0,1,1,0],
           [1,0,0,0,1,1,1,1,1,0,0,1,0,0,0,1,0,0],
           [1,0,0,0,0,0,0,1,1,1,1,1,0,0,0,1,0,0],
           [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
           [1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0],
           [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
           [0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,1,1,0],
           [0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,1,0],
         # [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7],
           [0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,1]]
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
            newnode = Node(county,countx)
            newnode.g = math.sqrt((county - end[0])**2 +(countx - end[1])**2  )
            newnode.x = countx
            newnode.y = county
            newnode.f = -1
            rowarray.append(newnode)
            countx = countx + 1

     # //shorter y because the bot has to approach from the opening
    # print(maparray)
    path = astar(maze, start, end)
    # print(path)
    return path
#
if __name__ == '__main__':
    mainx()
