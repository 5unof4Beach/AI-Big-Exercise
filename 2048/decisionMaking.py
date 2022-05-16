import numpy
import math
#ma trận trọng số ứng vói mỗi 8x8 hoặc 4x4
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
            
            # 8:[
            #     10000 , 7000, 5000, 4000, 4000, 5000, 7000, 10000,
            #      7000, 5000, 3000, 2000, 2000, 3000, 5000, 7000,
            #      5000, 3000, 2000, 2000,2000, 2000, 3000, 5000,
            #      4000, 2000, 2000, 2000,2000, 2000, 2000, 4000,
            #      4000, 2000, 2000, 2000,2000, 2000, 2000, 4000,
            #      5000, 3000, 2000, 2000,2000, 2000, 3000, 5000,
            #      7000, 5000, 3000, 2000,2000, 3000, 5000, 7000,
            #      10000 , 7000, 5000, 4000, 4000, 5000, 7000, 10000
            # ]

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
    diff = 0
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
            diff -= abs(currentValue - nextValue)

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
            diff -= abs(currentValue - nextValue)

            current = next
            next += 1
    return diff

# Cong Them Diem Neu cac hang hay cot co cac so tang hoac giam dan
def growingRowScore(grid):
    growingRowScores = [1, 1, 1, 1]

    # theo hang
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

    # Theo cot
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
        

#Tính điểm theo trọng số mỗi ô
def weightedGridScore(grid):

    size = int(math.sqrt(len(grid)))
    weightedGrid = weightedGrids[size]
    score = 0

    for i in range(size**2):
        score += grid[i] * weightedGrid[i]

    return score


# Tinh tong diem cho node
def calculateScore(grid):

    emptyValScore = emptyValueScore(grid) * 10000
    maxValScore = maxValueInGrid(grid) * 10000
    smallDiffScore = smallDifferentScore(grid) * 2000
    simiScore = growingRowScore(grid) * 100
    positionOfMaxValueScore = maxValueAtCorner(grid) * 90
    weightedScore = weightedGridScore(grid)

    return weightedScore + smallDiffScore + emptyValScore + maxValScore + simiScore + positionOfMaxValueScore






