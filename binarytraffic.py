from graphics import *
import time
import numpy as np

def main(iterlimit):
    roadLeft = 0
    roadRight = 0
    roadTop = 0
    roadBot = 0

    traversedTop = 0
    traversedBot = 0
    traversedLeft = 0
    traversedRight = 0
    switchCount = 0
    congestionTotal = 0
    lostCount = 0

    pattern = [0, 1, 0, 1, 1, 0, 0, 1, 2, 2, 1, 0, 1, 3, 2, 1, 2, 1, 0, 1]
    cross = 2
    roadTime = 2

    roadVert = True
    vertColor = "green"
    horiColor = "red"

    win = GraphWin("Traffic",500,500)
    win.setBackground("grey")
    road1 = Rectangle(Point(200,0),Point(300,500))
    road1.setFill("black")
    road1.draw(win)
    road2 = Rectangle(Point(0,200),Point(500,300))
    road2.setFill("black")
    road2.draw(win)
    valueTop = Text(Point(250,100),str(roadTop))
    valueTop.setFill(vertColor)
    valueTop.draw(win)
    valueBot = Text(Point(250,400),str(roadBot))
    valueBot.setFill(vertColor)
    valueBot.draw(win)
    valueLeft = Text(Point(100,250),str(roadLeft))
    valueLeft.setFill(horiColor)
    valueLeft.draw(win)
    valueRight = Text(Point(400,250),str(roadRight))
    valueRight.setFill(horiColor)
    valueRight.draw(win)

    for i in range(iterlimit):
        addLeft = pattern[i%20]
        addRight = pattern[(i+5)%20]
        addTop = pattern[(i+10)%20]
        addBot = pattern[(i+15)%20]

        if roadVert == True:
            roadTop = max(0,roadTop - cross)
            roadBot = max(0,roadBot - cross)
            queue = roadTop + roadBot
            arrive = addTop + addBot
            traversedTop = min(roadTop - cross,3)
            if traversedTop <= 0:
                traversedTop += cross + traversedTop
                lostCount += cross - roadTop
            traversedBot = min(roadBot - cross,3)
            if traversedBot <= 0:
                traversedBot += cross + traversedBot
                lostCount += cross - roadBot
            #congestion
            if roadLeft > 10 or roadRight > 10:
                roadLeft = min(roadLeft,10)
                roadRight = min(roadRight,10)
                congestionTotal += 1
        else:
            roadLeft = max(0,roadLeft - cross)
            roadRight = max(0,roadRight - cross)
            queue = roadLeft + roadRight
            arrive = addLeft + addRight
            traversedLeft = min(roadLeft - cross,3)
            if traversedLeft <= 0:
                traversedLeft += cross + traversedLeft
                lostCount += cross - roadLeft
            traversedRight = min(roadRight - cross,3)
            if traversedRight <= 0:
                traversedRight += cross + traversedRight
                lostCount += cross - roadRight
            # congestion
            if roadTop > 10 or roadBot > 10:
                roadTop = min(roadTop,10)
                roadBot = min(roadBot,10)
                congestionTotal += 1

        roadTime -= 1
        roadLeft += addLeft
        roadRight += addRight
        roadTop += addTop
        roadBot += addBot

        valueLeft.setText(str(roadLeft))
        valueLeft.setFill(horiColor)
        valueRight.setText(str(roadRight))
        valueRight.setFill(horiColor)
        valueTop.setText(str(roadTop))
        valueTop.setFill(vertColor)
        valueBot.setText(str(roadBot))
        valueBot.setFill(vertColor)

        if roadTime == 0:
            roadVert = not roadVert
            roadTime = 2
            vertColor, horiColor = horiColor, vertColor
            switchCount += 1

        #time.sleep(1)

    print("-BINARY STATS-\n\n")
    print("Number of switches: "+str(switchCount))
    print("Congestion total: "+str(congestionTotal))
    print("Lost time: "+str(lostCount))
    f = open("bin_log.txt","a+")
    f.write("run "+str(sum(pattern))+": switch,"+str(switchCount)+" cong,"+str(congestionTotal)+" lost,"+str(lostCount)+" seq,"+str(pattern)+"\n")
    f.close()

main(500)