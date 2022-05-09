import math
from decisionMaking import *

directions = ['u', 'd', 'l', 'r']

def createMiniMaxTree(depth, currentGrid):

    global nodeScores
    global childList
    global nodeNumber

    # Diem so cac node
    nodeScores = [0 for x in range(50000)]
    # So node con cua cac node cha
    childList = [[0 for x in range(0)] for y in range(50000)]
    # so thu tu cac node
    nodeNumber = 1

    alphaBeta(1, currentGrid, depth, -math.inf, math.inf)

def alphaBeta(node, grid, depth, alpha, beta):
    global nodeScores
    global childList
    global nodeNumber

    # Dieu kien dung de quy
    if depth == 0:
        nodeScores[node] = calculateScore(grid)
        return nodeScores[node]

    # maximize: luot choi cua nguoi choi(BOT) voi 4 nuoc di tren duoi trai
    if depth%2 == 0:

        for i in range(4):
            nodeNumber += 1
            childList[node].append(nodeNumber)
            if movable(grid, directions[i]) == True:
                alpha = max(alpha, alphaBeta(nodeNumber, move(grid,directions[i]), depth - 1, alpha, beta))

            if alpha >= beta:
                break #huy node 

        nodeScores[node] = alpha
        return alpha

    # minimize: luot choi cua may tinh: may chi cos nhiem vu dawt 2 so 2 hoac 4 vao cac o trong
    else:
        zeros = list(*numpy.where(grid == 0))

        gridTable = [[0 for x in range(16)] for y in range(0) ]
        gridTableScores = []

        for i in zeros:
            grid[i] = 2
            gridTable.append(grid)
            grid[i] = 0

        for i in zeros:
            grid[i] = 4
            gridTable.append(grid)
            grid[i] = 0

        for i in gridTable:
            nodeNumber += 1
            childList[node].append(nodeNumber)
            beta = min(beta, alphaBeta(nodeNumber, i, depth-1, alpha, beta))

            if alpha >= beta:
                break

        nodeScores[node] = beta
        return beta

def getMoves():
    bestValue = nodeScores[1] # node to tien

    for i in childList[1]:
        if nodeScores[i] == bestValue:
            return directions[childList[1].index(i)]