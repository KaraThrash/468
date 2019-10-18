# import math
# class MapSquare():
#
#     parent = None
#     position = (-1,-1)
#     x = -1
#     y = -1
#     g = -1
#     h = -1
#     f = -1
#     wall = 1
#
#
# def astar(endy,endx,starty,startx):
#
#     map2d = [[0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0],
#          # [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7],
#            [0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0], #5
#            [0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0],
#            [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0],
#            [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
#            [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
#            [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1],#10
#            [0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0],
#            [0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,0],
#            [0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,1,1,0],
#            [0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,1,0],
#          # [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7],
#            [0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,1]]
#
#     # + 10x + 9y to off set the negative start
#     # y,x
#
#     countx = 0
#     county = -1
#     # start = (12, 1)
#     # end = (1,13)
#     start = (10 - starty,startx + 9)
#     end = (10 - math.floor(endy),9 + math.floor(endx))
#     for row in map2d:
#         countx = 0
#         county = county + 1
#         rowarray = []
#         maparray.append(rowarray)
#         for col in row:
#             newsquare = MapSquare()
#             newsquare.g = math.sqrt((county - end[0])**2 +(countx - end[1])**2  )
#             newsquare.x = countx
#             newsquare.y = county
#             newsquare.position = (county,countx)
#             newsquare.f = -1
#             newsquare.wall = map2d[county][countx]
#             rowarray.append(newsquare)
#             countx = countx + 1
#     startsquare = MapSquare()
#     startsquare.position = start
#     startsquare.x = start[1]
#     startsquare.y = start[0]
#     startsquare.f = 0
#     startsquare.g = 0
#     startsquare.h = 0#math.sqrt((start[0] - end[0])**2 +(start[1] - end[1])**2  )
#     endsquare = MapSquare()
#     endsquare.position = end
#     endsquare.g = 0
#     endsquare.h = 0
#     endsquare.f = -100
#     endsquare.x = end[1]
#     endsquare.y = end[0]
#
#     opensquares = []
#
#     currentsquare = startsquare
#
#     opensquares.append(startsquare)
#
#     while currentsquare.position != end :
#
#         lastsquare = currentsquare
#
#
#         if currentsquare.x > 0:
#             if maparray[currentsquare.y][currentsquare.x - 1].wall == 0:
#                 # #print(maparray[currentsquare.y][currentsquare.x - 1])
#                 if maparray[currentsquare.y][currentsquare.x - 1].f == -1 or maparray[currentsquare.y][currentsquare.x - 1].f > (1 + currentsquare.f + maparray[currentsquare.y][currentsquare.x - 1].g):
#                     maparray[currentsquare.y][currentsquare.x - 1].f = currentsquare.f + maparray[currentsquare.y][currentsquare.x - 1].g
#                     maparray[currentsquare.y][currentsquare.x - 1].parent = currentsquare
#                     opensquares.append(maparray[currentsquare.y][currentsquare.x - 1])
#         if currentsquare.x < len(maparray[0]) - 1:
#             if maparray[currentsquare.y][currentsquare.x + 1].wall == 0:
#                 # #print(maparray[currentsquare.y][currentsquare.x + 1].wall )
#                 if maparray[currentsquare.y][currentsquare.x + 1].f == -1 or maparray[currentsquare.y][currentsquare.x + 1].f > (1 + currentsquare.f + maparray[currentsquare.y][currentsquare.x + 1].g):
#                     maparray[currentsquare.y][currentsquare.x + 1].f = currentsquare.f + maparray[currentsquare.y][currentsquare.x + 1].g
#                     maparray[currentsquare.y][currentsquare.x + 1].parent = currentsquare
#                     opensquares.append(maparray[currentsquare.y][currentsquare.x + 1])
#
#
#         if currentsquare.y > 0:
#             if maparray[currentsquare.y - 1][currentsquare.x ].wall == 0:
#                 #print(maparray[currentsquare.y - 1][currentsquare.x ].wall)
#                 if maparray[currentsquare.y - 1 ][currentsquare.x ].f == -1 or maparray[currentsquare.y - 1][currentsquare.x ].f > (1 + currentsquare.f + maparray[currentsquare.y - 1][currentsquare.x ].g):
#                     maparray[currentsquare.y - 1][currentsquare.x ].f = currentsquare.f + maparray[currentsquare.y - 1][currentsquare.x ].g
#                     maparray[currentsquare.y - 1][currentsquare.x ].parent = currentsquare
#                     opensquares.append(maparray[currentsquare.y - 1][currentsquare.x ])
#
#             if currentsquare.x > 0:
#                 if maparray[currentsquare.y - 1][currentsquare.x - 1].wall == 0:
#                     if maparray[currentsquare.y ][currentsquare.x - 1].wall != 1 and maparray[currentsquare.y - 1][currentsquare.x ].wall != 1:
#                         #print(maparray[currentsquare.y - 1][currentsquare.x - 1])
#                         if maparray[currentsquare.y - 1][currentsquare.x - 1].f == -1 or maparray[currentsquare.y - 1][currentsquare.x - 1].f > (2 + currentsquare.f + maparray[currentsquare.y - 1][currentsquare.x - 1].g):
#                             maparray[currentsquare.y - 1][currentsquare.x - 1].f = currentsquare.f + maparray[currentsquare.y - 1][currentsquare.x - 1].g
#                             maparray[currentsquare.y - 1][currentsquare.x - 1].parent = currentsquare
#                             opensquares.append(maparray[currentsquare.y - 1][currentsquare.x - 1])
#             if currentsquare.x < len(maparray[0]) - 1:
#                 if maparray[currentsquare.y - 1][currentsquare.x + 1].wall == 0:
#                     if maparray[currentsquare.y ][currentsquare.x + 1].wall != 1 and maparray[currentsquare.y - 1][currentsquare.x ].wall != 1:
#                         #print(maparray[currentsquare.y - 1][currentsquare.x + 1].wall )
#                         if maparray[currentsquare.y - 1][currentsquare.x + 1].f == -1 or maparray[currentsquare.y - 1][currentsquare.x + 1].f > (2 + currentsquare.f + maparray[currentsquare.y - 1][currentsquare.x + 1].g):
#                             maparray[currentsquare.y - 1][currentsquare.x + 1].f = currentsquare.f + maparray[currentsquare.y - 1][currentsquare.x + 1].g
#                             maparray[currentsquare.y - 1][currentsquare.x + 1].parent = currentsquare
#                             opensquares.append(maparray[currentsquare.y - 1][currentsquare.x + 1])
#         if currentsquare.y < len(maparray) - 1:
#             if maparray[currentsquare.y + 1][currentsquare.x ].wall == 0:
#                 #print(maparray[currentsquare.y + 1][currentsquare.x ].wall)
#                 if maparray[currentsquare.y + 1 ][currentsquare.x ].f == -1 or maparray[currentsquare.y + 1][currentsquare.x ].f > (1 + currentsquare.f + maparray[currentsquare.y + 1][currentsquare.x ].g):
#                     maparray[currentsquare.y + 1][currentsquare.x ].f = currentsquare.f + maparray[currentsquare.y + 1][currentsquare.x ].g
#                     maparray[currentsquare.y + 1][currentsquare.x ].parent = currentsquare
#                     opensquares.append(maparray[currentsquare.y + 1][currentsquare.x ])
#
#                 if currentsquare.x > 0:
#                     if maparray[currentsquare.y + 1][currentsquare.x - 1].wall == 0:
#                         if maparray[currentsquare.y ][currentsquare.x - 1].wall != 1 and maparray[currentsquare.y + 1][currentsquare.x ].wall != 1:
#                             #print(maparray[currentsquare.y + 1][currentsquare.x - 1])
#                             if maparray[currentsquare.y + 1][currentsquare.x - 1].f == -1 or maparray[currentsquare.y + 1][currentsquare.x - 1].f > (2 + currentsquare.f + maparray[currentsquare.y + 1][currentsquare.x - 1].g):
#                                 maparray[currentsquare.y + 1][currentsquare.x - 1].f = currentsquare.f + maparray[currentsquare.y + 1][currentsquare.x - 1].g
#                                 maparray[currentsquare.y + 1][currentsquare.x - 1].parent = currentsquare
#                                 opensquares.append(maparray[currentsquare.y + 1][currentsquare.x - 1])
#                 if currentsquare.x < len(maparray[0]) - 1:
#                     if maparray[currentsquare.y + 1][currentsquare.x + 1].wall == 0:
#                         if maparray[currentsquare.y ][currentsquare.x + 1].wall != 1 and maparray[currentsquare.y + 1][currentsquare.x ].wall != 1:
#                             #print(maparray[currentsquare.y + 1][currentsquare.x + 1].wall )
#                             if maparray[currentsquare.y + 1][currentsquare.x + 1].f == -1 or maparray[currentsquare.y + 1][currentsquare.x + 1].f > (2 + currentsquare.f + maparray[currentsquare.y + 1][currentsquare.x + 1].g):
#                                 maparray[currentsquare.y + 1][currentsquare.x + 1].f = currentsquare.f + maparray[currentsquare.y + 1][currentsquare.x + 1].g
#                                 maparray[currentsquare.y + 1][currentsquare.x + 1].parent = currentsquare
#                                 opensquares.append(maparray[currentsquare.y + 1][currentsquare.x + 1])
#
#         if len(opensquares) > 0:
#             currentsquare = opensquares[0]
#             opensquares.remove(currentsquare)
#         for el in opensquares:
#             if el.f < currentsquare.f:
#                 currentsquare = el
#
#
#
#     togoal = []
#     current = currentsquare
#     while current.position != start:
#         togoal.append((current.y,current.x))
#         # map2d[current.y][current.x] = 2
#         current = current.parent
#     # for el in map2d:
#     #     print(el)
#     pathlength = len(togoal) - 1
#     returnpath = []
#     while pathlength >= 0:
#         returnpath.append(togoal[pathlength])
#         pathlength = pathlength - 1
#
#     return returnpath
#
#
# def mainx(endy,endx,starty,startx):        #5
#     global maparray
#     global maze
#     maze = [[0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0],
#          # [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7],
#            [0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0], #5
#            [0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0],
#            [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0],
#            [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
#            [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
#            [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1],#10
#            [0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0],
#            [0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
#            [0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,0],
#            [0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,1,1,0],
#            [0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,1,0],
#          # [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7],
#            [0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,1]]
#
# # + 10x + 9y to off set the negative start
# # y,x
#
#     countx = 0
#     county = -1
#     # start = (12, 1)
#     # end = (1,13)
#     start = (10 - starty,startx + 9)
#     end = (10 - math.floor(endy),9 + math.floor(endx))
#     for row in maze:
#         countx = 0
#         county = county + 1
#         rowarray = []
#         maparray.append(rowarray)
#         for col in row:
#             newsquare = MapSquare()
#             newsquare.g = math.sqrt((county - end[0])**2 +(countx - end[1])**2  )
#             newsquare.x = countx
#             newsquare.y = county
#             newsquare.position = (county,countx)
#             newsquare.f = -1
#             newsquare.wall = maze[county][countx]
#             rowarray.append(newsquare)
#             countx = countx + 1
#
#      # //shorter y because the bot has to approach from the opening
#     # #print(maparray)
#     togoal = astar(maze, start, end)
#     print(togoal)
#     return togoal
# #
# # if __name__ == '__main__':
#     # main(13,1)
