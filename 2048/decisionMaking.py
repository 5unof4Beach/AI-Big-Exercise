import numpy
import math

weightedGrids = {4:[
                10000 , 7000, 4000, 2000,
                 7000, 3000, 1000, 1000,
                 4000, 1000, 1000, 1000,
                 2000, 1000, 1000, 1000
            ],

            8:[
                10000 , 7000, 5000, 4000, 4000, 2000, 2000, 2000,
                 7000, 5000, 3000, 2000, 2000, 2000, 2000, 2000,
                 5000, 3000, 2000, 2000,2000, 2000, 2000, 2000,
                 4000, 2000, 2000, 2000,2000, 2000, 2000, 2000,
                 4000, 2000, 2000, 2000,2000, 2000, 2000, 2000,
                 2000, 2000, 2000, 2000,2000, 2000, 2000, 2000,
                 2000, 2000, 2000, 2000,2000, 2000, 2000, 2000,
                 2000, 2000, 2000, 2000,2000, 2000, 2000, 2000
            ]

            # ,   
            # 8:[
            #     65000 , 6400, 6300, 6200, 6100, 6000, 5900, 5800,
            #      5000 , 5100, 5200, 5300, 5400, 5500, 5600, 5700,
            #      4900, 4800, 4700, 4600,4500, 4400, 4300, 4200,
            #      3400, 3500, 3600, 3700,3800, 3900, 4000, 4100,
            #      3300, 3200, 3100, 3000,2900, 2800, 2700, 2600,
            #      1800, 1900, 2000, 2100,2200, 2300, 2400, 2500,
            #      1700, 1600, 1500, 1400,1300, 1200, 1100, 1000,
            #      200, 300, 400, 500,600, 700, 800, 900
            # ]   
            }

def move(flattenedGrid, key):
    # temp = grid
    size = int(math.sqrt(len(flattenedGrid)))
    grid = numpy.zeros((size, size), dtype=int)

    for i in range(size):
        grid[i][:] = flattenedGrid[i*size : size*(i + 1)]

    for i in range(size):
        flipped = False
        if key in 'lr':  # nếu nhập vào là l hoặc r thì lấy hàng
            row = grid[i, :]
        else:
            row = grid[:, i]  # u hoăc d thì lấy cột

        if key in 'rd':  # nếu là r hoặc d thì lật ngược list để có thể tận dụng hàm get num
            flipped = True
            row = row[::-1]

        notZeros = checkAndSum(row)  
        newRow = numpy.zeros_like(row)  # tạo một hàng mới chỉ chứa số 0 có kích cỡ giống hàng cũ
        newRow[:len(notZeros)] = notZeros  # gắn các giá trị != 0 vào mảng mới

        if flipped:
            newRow = newRow[::-1]

        if key in 'lr':
            grid[i, :] = newRow
        else:
            grid[:, i] = newRow

    return grid.flatten()

def checkAndSum(row):
    notZeros = row[row != 0]
    res = []
    skip = False
    for i in range(len(notZeros)):
        if skip:
            skip = False
            continue
        if i != len(notZeros) - 1 and notZeros[i] == notZeros[i + 1]:  # nếu 2 số liền nhau mà giống nhau thì cộng lại và cho vào mảng mới
            sum = notZeros[i] * 2
            res.append(sum)
            skip = True
        else:
            res.append(notZeros[i])
    return res

def movable(grid, direction):
    if all(grid.flatten() == move(grid, direction)):
        return False
    else:
        return True


# Cong rhem diem voi moi o trong
def emptyValueScore(grid):
    return len(list(*numpy.where(grid == 0)))

#Cong them diem cho gia tri lon nhat
def maxValueInGrid(grid):
    maxVal = -1
    maxVal = max(grid)
    return maxVal

# Cong them diem neu hieu cac o canh nhau nho
def smallDifferentScore(grid):
    smoothness = 0
    size = int(math.sqrt(len(grid)))

    #Theo Hang
    for i in range(size):
        current = 0
        while current < size and grid[size*i + current] == 0:
            current += 1
        if current >= size:
            continue

        next = current + 1
        while next < size:
            while next < size and grid[i*size + next] == 0:
                next += 1
            if next >= size:
                break

            currentValue = grid[i*size + current]
            nextValue = grid[i*size + next]
            smoothness -= abs(currentValue - nextValue)

            current = next
            next += 1

    #Theo Cot
    for i in range(size):
        current = 0
        while current < size and grid[current*size + i] == 0:
            current += 1
        if current >= size:
            continue

        next = current + 1
        while next < size:
            while next < size and grid[size*next + i]:
                next += 1
            if next >= size:
                break

            currentValue = grid[current*size + i]
            nextValue = grid[next*size + i]
            smoothness -= abs(currentValue - nextValue)

            current = next
            next += 1
    return smoothness*10

# Cong Them Diem Neu cac hang hay cot co cac so tang hoac giam dan
def growingRowScore(grid):
    growingRowScores = [1, 1, 1, 1]

    # left/right direction
    for i in range(4):
        current = 0
        next = current + 1
        while next < 4:
            while next < 4 and grid[i*4 + next] == 0:
                next += 1

            if next >= 4:
                next -= 1
            currentValue = grid[i*4 + current]
            nextValue = grid[i*4 + next]

            if currentValue > nextValue:
                growingRowScores[0] += nextValue - currentValue
            elif nextValue > currentValue:
                growingRowScores[1] += currentValue - nextValue

            current = next
            next += 1

    #up/down direction
        for i in range(4):
            current = 0
            next = current + 4
            while next < 4:
                while next < 4 and grid[i + 4*next] == 0:
                    next += 1

                if next >= 4:
                    next -= 1
                currentValue = grid[i + 4*current]
                nextValue = grid[i + 4*next]

                if currentValue > nextValue:
                    growingRowScores[2] += nextValue - currentValue
                elif nextValue > currentValue:
                    growingRowScores[3] += currentValue - nextValue
            current = next
            next += 1

    return max(growingRowScores[0], growingRowScores[1]) + max(growingRowScores[2], growingRowScores[3])

# Neu gia tri lon nhat cua grid nam o 1 trong 4 goc thi cong them diem
def maxValueAtCorner(grid):
    size = int(math.sqrt(len(grid)))
    TL = 0
    TR = size - 1
    BR = size**2 - 1
    BL = BR - size - 1
    maxVal = maxValueInGrid(grid)
    maxValPos = list(*numpy.where(grid == maxVal))
    if TL in maxValPos or TR in maxValPos or BL in maxValPos or BR in maxValPos:
        return 5000
    else:
        if grid[TL] == 2 or grid[TL] == 4 or grid[TL] == 8 or grid[TL] == 16 or grid[size] == 2 or grid[size] == 4 or grid[TL + 1] == 2 or grid[TL + 1] == 4:
            return -7000
        return -5000
        

#Tinh diem theo trong so moi o
def weightedGridScore(grid):

    size = int(math.sqrt(len(grid)))
    weightedGrid = weightedGrids[size]
    score = 0

    for i in range(size**2):
        score += grid[i] * weightedGrid[i]

    return score


# Tinh tong diem de chon nuoc di
def calculateScore(grid):

    emptyValScore = emptyValueScore(grid) * 10000
    maxValScore = maxValueInGrid(grid) * 10000
    smallDiffScore = smallDifferentScore(grid) * 50
    simiScore = -growingRowScore(grid) * 90
    positionOfMaxValueScore = maxValueAtCorner(grid) * 90
    weightedScore = weightedGridScore(grid)

    return weightedScore + smallDiffScore + emptyValScore + maxValScore + simiScore + positionOfMaxValueScore






