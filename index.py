import turtle
import math


def start():
    # machine's note number: 1
    # player's note number: 2
    result = {
        "playerWinValue": -1,
        "drawValue": 0,
        "machineWinValue": 1,
        "notFinished": -2
    }

    def setValueMap(map, x, y, value):
        map[x][y] = value

    def getUserChoice():
        x = int(input('Enter your x position: '))
        y = int(input('Enter your y position: '))
        return {
            'x': x,
            'y': y
        }

    def createMap():
        map = []
        for i in range(3):
            temp = []
            for j in range(3):
                temp.append(0)
            map.append(temp)
        return map

    def printMap(map):
        for i in range(len(map)):
            for j in range(len(map[i])):
                print(map[i][j], end=' ')
            print()
        return map

    def checkWin(map):
        def isOne(num):
            if num == 1:
                return True

        def isTwo(num):
            if num == 2:
                return True

        # check machine win
        for i in range(3):
            if isOne(map[i][0]) and isOne(map[i][1]) and isOne(map[i][2]):
                return result["machineWinValue"]
        for i in range(3):
            if isOne(map[0][i]) and isOne(map[1][i]) and isOne(map[2][i]):
                return result["machineWinValue"]
        if isOne(map[0][0]) and isOne(map[1][1]) and isOne(map[2][2]):
            return result["machineWinValue"]
        if isOne(map[0][2]) and isOne(map[1][1]) and isOne(map[2][0]):
            return result["machineWinValue"]
        # check player win
        for i in range(3):
            if isTwo(map[i][0]) and isTwo(map[i][1]) and isTwo(map[i][2]):
                return result["playerWinValue"]
        for i in range(3):
            if isTwo(map[0][i]) and isTwo(map[1][i]) and isTwo(map[2][i]):
                return result["playerWinValue"]
        if isTwo(map[0][0]) and isTwo(map[1][1]) and isTwo(map[2][2]):
            return result["playerWinValue"]
        if isTwo(map[0][2]) and isTwo(map[1][1]) and isTwo(map[2][0]):
            return result["playerWinValue"]
        # check if game is not finished
        for i in range(3):
            for j in range(3):
                if map[i][j] == 0:
                    return result["notFinished"]
        # return draw result
        return result["drawValue"]

    def findMin(map):  # player's turn
        gameResult = checkWin(map)
        if gameResult != result["notFinished"]:
            return [gameResult]

        minValue = 2
        point = {}
        for i in range(3):
            for j in range(3):
                if map[i][j] == 0:
                    setValueMap(map, i, j, 2)
                    temp = findMax(map)[0]
                    if temp < minValue:
                        minValue = temp
                        point['x'] = i
                        point['y'] = j
                    setValueMap(map, i, j, 0)
        return [minValue, point]

    def findMax(map):  # machine's turn
        gameResult = checkWin(map)
        if gameResult != result["notFinished"]:
            return [gameResult]

        maxValue = -3
        point = {}
        for i in range(3):
            for j in range(3):
                if map[i][j] == 0:
                    setValueMap(map, i, j, 1)
                    temp = findMin(map)[0]
                    if temp > maxValue:
                        maxValue = temp
                        point['x'] = i
                        point['y'] = j
                    setValueMap(map, i, j, 0)
        return [maxValue, point]

    # --------- handle visualization --------

    squareWidth = 100
    outlineColor = '#4c4c4c'
    fillColor = '#e2dada'
    tickColor = '#620097'
    circleColor = '#fdba31'

    def createQuinxi():
        quinxi = turtle.Turtle()
        quinxi.speed(10000)
        quinxi.color(outlineColor)
        quinxi.fillcolor(fillColor)
        quinxi.pensize(5)
        quinxi.shape('turtle')
        quinxi.hideturtle()
        return quinxi

    def goTotPoint(quinxi, len, x, y):
        quinxi.penup()
        quinxi.goto((-len/2 + y) * squareWidth, (len/2 - x) * squareWidth)
        quinxi.pendown()

    def drawRectangle(quinxi, x, y):
        quinxi.penup()
        quinxi.goto(x, y)
        quinxi.pendown()
        quinxi.begin_fill()
        for i in range(4):
            quinxi.forward(squareWidth)
            quinxi.right(90)
        quinxi.end_fill()

    def tickMap(quinxi, len, x, y):
        goTotPoint(quinxi, len, x, y)
        quinxi.color(tickColor)
        quinxi.setheading(-45)
        quinxi.penup()
        quinxi.forward((math.sqrt(2) / 4) * squareWidth)
        quinxi.pendown()
        quinxi.forward((math.sqrt(2) / 2) * squareWidth)
        quinxi.penup()
        quinxi.setheading(90)
        quinxi.forward(squareWidth/2)
        quinxi.pendown()
        quinxi.setheading(225)
        quinxi.forward((math.sqrt(2) / 2) * squareWidth)
        quinxi.color(outlineColor)

    def circleMap(quinxi, len, x, y):
        quinxi.color(circleColor)
        goTotPoint(quinxi, len, x, y)
        quinxi.penup()
        quinxi.setheading(-45)
        quinxi.forward((math.sqrt(2) / 2) * squareWidth)
        quinxi.setheading(-90)
        quinxi.forward(squareWidth/4)
        quinxi.setheading(0)
        quinxi.pendown()
        quinxi.circle(squareWidth/4)
        quinxi.color(outlineColor)

    def drawMap(quinxi, len):
        for i in range(len):
            for j in range(len):
                startPoint = {
                    'x': (-len/2 + j) * squareWidth,
                    'y': (len/2 - i) * squareWidth,
                }
                drawRectangle(quinxi, startPoint['x'], startPoint['y'])

    def recieveUserPoint(map, quinxi, len):
        def moveTurtleToCursor(x, y):
            quinxi.penup()
            quinxi.goto(x, y)
            quinxi.pendown()
            getIndexByCoordinateAndTickMap(x, y)

        def getIndexByCoordinateAndTickMap(x, y):
            xIndex = len
            yIndex = len
            for i in range(len):
                if (-3/2+i) * squareWidth < x and x < (-3/2+i+1)*squareWidth:
                    yIndex = i
                    break
            if yIndex == len:
                print('Invalid click action!')
                turtle.bye()

            for i in range(len):
                if (-3/2+i) * squareWidth < y and y < (-3/2+i+1)*squareWidth:
                    xIndex = len - i - 1
                    break
            if xIndex == len:
                print('Invalid click action!')
                quinxi.bye()

            userPoint = {
                'x': xIndex,
                'y': yIndex
            }
            handlMachineTurn(userPoint)

        def handlMachineTurn(userChoice):
            printMap(map)
            # userChoice = getUserChoice()
            tickMap(quinxi, len, userChoice['x'], userChoice['y'])
            setValueMap(map, userChoice['x'], userChoice['y'], 2)
            gameResult = checkWin(map)
            if gameResult != result["notFinished"]:
                printMap(map)
                quinxi.bye()
                match gameResult:
                    case -1:
                        print('You win!')

                    case 0:
                        print('draw!')

                    case 1:
                        print('you lose!')

            machineChoice = findMax(map)[1]
            setValueMap(map, machineChoice['x'], machineChoice['y'], 1)
            circleMap(quinxi, len, machineChoice['x'], machineChoice['y'])
            gameResult = checkWin(map)

            if gameResult != result["notFinished"]:
                printMap(map)
                turtle.bye()
                match gameResult:
                    case -1:
                        print('You win!')
                    case 0:
                        print('draw!')
                    case 1:
                        print('you lose!')

        quinxi.getscreen().onclick(moveTurtleToCursor)

    def play():
        len = 3
        map = createMap()
        quinxi = createQuinxi()
        drawMap(quinxi, len)
        recieveUserPoint(map, quinxi, len)
        turtle.mainloop()

    def play5x5Map():
        pass

    def init():
        userChoice = 0
        while userChoice != 3:
            print('1) Map 3x3.')
            print('2) Map 5x5.')
            print('3) Quit game')
            userChoice = int(input('Enter your choice: '))
            match userChoice:
                case 1:
                    play()
                case 2:
                    play5x5Map()
                case 3:
                    print('Good bye!')

    init()


if __name__ == "__main__":
    start()

# Ngoc Nhi Nguyen Thi
