import turtle
import math


def start():
    # -------- handle 2-dimension Map -------

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

    def createMap(len):
        map = []
        for i in range(len):
            temp = []
            for j in range(len):
                temp.append(0)
            map.append(temp)
        return map

    def printMap(map):
        for i in range(len(map)):
            for j in range(len(map[i])):
                print(map[i][j], end=' ')
            print()
        return map

    def checkWin(map, prevChoice):
        def isInRange(map, x, y):
            if 0 <= x and x < len(map) and 0 <= y and y < len(map[0]):
                return True
            return False

        def isWin(array, winLen, checkNumber):
            count = 0
            for i in range(len(array)):
                if array[i] == checkNumber:
                    count = count + 1
                    if count == winLen:
                        return True
                else:
                    count = 0
            return False

        if len(map) == 3:
            winLen = 3
        elif len(map) == 5:
            winLen = 4

        if map[prevChoice['x']][prevChoice['y']] == 1:
            checkNumber = 1
            winString = "machineWinValue"
        elif map[prevChoice['x']][prevChoice['y']] == 2:
            checkNumber = 2
            winString = "playerWinValue"

        x = prevChoice['x']
        y = prevChoice['y']
        horizontalArray = []
        for i in range(-(winLen - 1), winLen, 1):
            if isInRange(map, x, y+i):
                horizontalArray.append(map[x][y+i])
        if len(horizontalArray) >= winLen and isWin(horizontalArray, winLen, checkNumber):
            return result[winString]

        verticalArray = []
        for i in range(-(winLen - 1), winLen, 1):
            if isInRange(map, x+i, y):
                verticalArray.append(map[x+i][y])
        if len(verticalArray) >= winLen and isWin(verticalArray, winLen, checkNumber):
            return result[winString]

        rightDownArray = []
        for i in range(-(winLen - 1), winLen, 1):
            if isInRange(map, x+i, y+i):
                rightDownArray.append(map[x+i][y+i])
        if len(rightDownArray) >= winLen and isWin(rightDownArray, winLen, checkNumber):
            return result[winString]

        leftDownlArray = []
        for i in range(-(winLen - 1), winLen, 1):
            if isInRange(map, x+i, y-i):
                leftDownlArray.append(map[x+i][y-i])
        if len(leftDownlArray) >= winLen and isWin(leftDownlArray, winLen, checkNumber):
            return result[winString]

        # check if game is not finished
        for i in range(len(map)):
            for j in range(len(map[0])):
                if map[i][j] == 0:
                    return result["notFinished"]
        # return draw result
        return result["drawValue"]

    def findMin(map, prevChoice):  # player's turn
        gameResult = checkWin(map, prevChoice)
        if gameResult != result["notFinished"]:
            return [gameResult]

        minValue = 2
        point = {}
        for i in range(len(map)):
            for j in range(len(map[0])):
                if map[i][j] == 0:
                    setValueMap(map, i, j, 2)
                    temp = findMax(map, {'x': i, 'y': j})[0]
                    if temp < minValue:
                        minValue = temp
                        point['x'] = i
                        point['y'] = j
                    setValueMap(map, i, j, 0)
        return [minValue, point]

    def findMax(map, prevChoice):  # machine's turn
        gameResult = checkWin(map, prevChoice)
        if gameResult != result["notFinished"]:
            return [gameResult]

        maxValue = -3
        point = {}
        for i in range(len(map)):
            for j in range(len(map)):
                if map[i][j] == 0:
                    setValueMap(map, i, j, 1)
                    temp = findMin(map, {'x': i, 'y': j})[0]
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
        quinxi.speed(100)
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
        goTotPoint(quinxi, len, x, y)
        quinxi.color(circleColor)
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
                if (-len/2+i) * squareWidth < x and x < (-len/2+i+1)*squareWidth:
                    yIndex = i
                    break
            if yIndex == len:
                print('Invalid click action!')
                turtle.exitonclick()

            for i in range(len):
                if (-len/2+i) * squareWidth < y and y < (-len/2+i+1)*squareWidth:
                    xIndex = len - i - 1
                    break
            if xIndex == len:
                print('Invalid click action!')
                turtle.exitonclick()

            userPoint = {
                'x': xIndex,
                'y': yIndex
            }
            handlMachineTurn(userPoint)

        def handlMachineTurn(userChoice):
            tickMap(quinxi, len, userChoice['x'], userChoice['y'])
            setValueMap(map, userChoice['x'], userChoice['y'], 2)
            printMap(map)
            gameResult = checkWin(map, userChoice)
            if gameResult != result["notFinished"]:
                printMap(map)
                match gameResult:
                    case -1:
                        print('You win!')
                        turtle.exitonclick()
                        return

                    case 0:
                        print('draw!')
                        turtle.exitonclick()
                        return

                    case 1:
                        print('you lose!')
                        turtle.exitonclick()
                        return

            temp = findMax(map, userChoice)
            machineChoice = temp[1]
            setValueMap(map, machineChoice['x'], machineChoice['y'], 1)
            circleMap(quinxi, len, machineChoice['x'], machineChoice['y'])
            gameResult = checkWin(map, machineChoice)

            if gameResult != result["notFinished"]:
                printMap(map)
                turtle.exitonclick()
                match gameResult:
                    case -1:
                        print('You win!')
                        turtle.exitonclick()
                        return
                    case 0:
                        print('draw!')
                        turtle.exitonclick()
                        return
                    case 1:
                        print('you lose!')
                        turtle.exitonclick()
                        return

        quinxi.getscreen().onclick(moveTurtleToCursor)

    def play(len):
        map = createMap(len)
        quinxi = createQuinxi()
        drawMap(quinxi, len)
        recieveUserPoint(map, quinxi, len)
        turtle.mainloop()

    def init():
        userChoice = 0
        while userChoice != 3:
            print('1) Map 3x3.')
            print('2) Map 5x5.')
            print('3) Quit game')
            userChoice = int(input('Enter your choice: '))
            match userChoice:
                case 1:
                    play(3)
                case 2:
                    play(5)
                case 3:
                    print('Good bye!')

    init()


if __name__ == "__main__":
    start()
