import math
from decisionMaking import *

directions = ['u', 'd', 'l', 'r']

def start(depth, currentGrid):

    global nodeScores
    global children
    global nodeNumber

    # Diem so cac node
    nodeScores = [0 for x in range(10000)]
    # So node con cua cac node cha
    children = [[] for y in range(10000)]
    # so thu tu cac node
    nodeNumber = 1

    alphaBeta(1, currentGrid, depth, -math.inf, math.inf)

def alphaBeta(node, grid, depth, alpha, beta):
    global nodeScores
    global children
    global nodeNumber

    # Dieu kien dung de quy
    if depth == 0:
        nodeScores[node] = calculateScore(grid)
        return nodeScores[node]

    # maximize: luot choi cua nguoi choi(BOT) voi 4 nuoc di tren duoi trai
    if depth%2 == 0:

        for i in range(4):
            nodeNumber += 1
            children[node].append(nodeNumber)
            if movable(grid, directions[i]) == True:
                alpha = max(alpha, alphaBeta(nodeNumber, move(grid,directions[i]), depth - 1, alpha, beta))

            if alpha >= beta:
                break #huy node 

        nodeScores[node] = alpha
        return alpha

    # minimize: luot choi cua may tinh: may chi co nhiem vu dat 2 so 2 hoac 4 vao cac o trong
    else:
        zeros = list(*numpy.where(grid == 0))

        gridList = [[] for y in range(0)]

        for i in zeros:
            grid[i] = 2
            gridList.append(grid)
            grid[i] = 0

        for i in zeros:
            grid[i] = 4
            gridList.append(grid)
            grid[i] = 0

        for i in gridList:
            nodeNumber += 1
            children[node].append(nodeNumber)
            beta = min(beta, alphaBeta(nodeNumber, i, depth-1, alpha, beta))

            if alpha >= beta:
                break

        nodeScores[node] = beta
        return beta

def go():
    bestValue = nodeScores[1] # node to tien

    for i in children[1]:
        if nodeScores[i] == bestValue:
            return directions[children[1].index(i)]