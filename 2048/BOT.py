import math
from decisionMaking import *

# Cac huong di len xuong trai phai
directions = 'udlr'

def start(depth, currentGrid):

    global nodeScores
    global children
    global nodeNumber

    # Diem so cac node
    nodeScores = [0 for x in range(5000)]
    # So node con cua cac node cha
    children = [[] for y in range(5000)]
    # so thu tu cac node
    nodeNumber = 1

    minimax(1, currentGrid, depth, -math.inf, math.inf)

def minimax(node, grid, depth, alpha, beta):

    global nodeScores
    global children
    global nodeNumber

    # Dieu kien dung de quy
    if depth == 0:
        nodeScores[node] = calculateScore(grid)
        return nodeScores[node]

    # maximize: luot choi cua nguoi choi(BOT) voi 4 nuoc di tren duoi trai
    if depth%2 == 0:
        # chon 4 buoc di
        for i in directions:
            nodeNumber += 1
            children[node].append(nodeNumber)
            if movable(grid, i):
                alpha = max(alpha, minimax(nodeNumber, move(grid,i), depth - 1, alpha, beta))

            if alpha >= beta:
                break #huy node 

        nodeScores[node] = alpha
        return alpha

    # minimize: luot choi cua may tinh: may chi co nhiem vu dat 2 so 2 hoac 4 vao cac o trong
    else:
        #danh sach cac vi tri co gia tri bang 0
        zeros = list(*numpy.where(grid == 0))

        gridList = [[] for y in range(0)]

        #Dat cac so 2 vao cac o trong
        for i in zeros:
            grid[i] = 2
            gridList.append(grid)
            grid[i] = 0

        #Dat cac so 4 vao cac o trong
        for i in zeros:
            grid[i] = 4
            gridList.append(grid)
            grid[i] = 0

        for i in gridList:
            nodeNumber += 1
            children[node].append(nodeNumber)
            beta = min(beta, minimax(nodeNumber, i, depth-1, alpha, beta))

            if alpha >= beta:
                break

        nodeScores[node] = beta
        return beta

def go():
    bestValue = nodeScores[1] # node to tien

    for i in children[1]:
        if nodeScores[i] == bestValue:
            return directions[children[1].index(i)]


# ham di chuyen grid theo huong chi dinh giong move_event trong gameplay.py
def move(flattenedGrid, key):
    size = int(math.sqrt(len(flattenedGrid)))
    grid = numpy.zeros((size, size), dtype=int)

    for i in range(size):
        grid[i][:] = flattenedGrid[i*size : size*(i + 1)]

    for i in range(size):
        flipped = False
        if key in 'lr':  # n???u nh???p v??o l?? l ho???c r th?? l???y h??ng
            row = grid[i, :]
        else:
            row = grid[:, i]  # u ho??c d th?? l???y c???t

        if key in 'rd':  # n???u l?? r ho???c d th?? l???t ng?????c list ????? c?? th??? t???n d???ng h??m get num
            flipped = True
            row = row[::-1]

        notZeros = checkAndSum(row)  
        newRow = numpy.zeros_like(row)  # t???o m???t h??ng m???i ch??? ch???a s??? 0 c?? k??ch c??? gi???ng h??ng c??
        newRow[:len(notZeros)] = notZeros  # g???n c??c gi?? tr??? != 0 v??o m???ng m???i

        if flipped:
            newRow = newRow[::-1]

        if key in 'lr':
            grid[i, :] = newRow
        else:
            grid[:, i] = newRow

    return grid.flatten()

# ham xu ly cac so trong grid sau moi lan bam nut
def checkAndSum(row):
    notZeros = row[row != 0]
    res = []
    skip = False
    for i in range(len(notZeros)):
        if skip:
            skip = False
            continue
        if i != len(notZeros) - 1 and notZeros[i] == notZeros[i + 1]:  # n???u 2 s??? li???n nhau m?? gi???ng nhau th?? c???ng l???i v?? cho v??o m???ng m???i
            sum = notZeros[i] * 2
            res.append(sum)
            skip = True
        else:
            res.append(notZeros[i])
    return res

# Kiem tra sau khi an nut di chuyen thi grid co bo thay doi hay khong
def movable(grid, direction):
    if all(grid.flatten() == move(grid, direction)):
        return False
    else:
        return True