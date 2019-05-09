import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
from graphics import *
import time

congestion = ctrl.Antecedent(np.arange(0,12.5,2.5), "congestion")
congestion["tiny"] = fuzz.trimf(congestion.universe, [0,0,2.5])
congestion["small"] = fuzz.trimf(congestion.universe, [0,2.5,5])
congestion["medium"] = fuzz.trimf(congestion.universe, [2.5,5,7.5])
congestion["large"] = fuzz.trimf(congestion.universe, [5,7.5,10])
congestion["huge"] = fuzz.trimf(congestion.universe, [7.5,10,10])

additions = ctrl.Antecedent(np.arange(0,5,1), "additions")
additions["tiny"] = fuzz.trimf(additions.universe, [0,0,1])
additions["small"] = fuzz.trimf(additions.universe, [0,1,2])
additions["medium"] = fuzz.trimf(additions.universe, [1,2,3])
additions["large"] = fuzz.trimf(additions.universe, [2,3,4])
additions["huge"] = fuzz.trimf(additions.universe, [3,4,4])

addTime = ctrl.Consequent(np.arange(0,2.5,0.5), "addTime")
addTime["tiny"] = fuzz.trimf(addTime.universe, [0,0,0.5])
addTime["small"] = fuzz.trimf(addTime.universe, [0,0.5,1])
addTime["medium"] = fuzz.trimf(addTime.universe, [0.5,1,1.5])
addTime["large"] = fuzz.trimf(addTime.universe, [1,1.5,2])
addTime["huge"] = fuzz.trimf(addTime.universe, [1.5,2,2])

rule1 = ctrl.Rule(additions["tiny"]  | (additions["small"] & (congestion["tiny"] | congestion["small"]  | congestion["medium"])), addTime["tiny"])
rule2 = ctrl.Rule(additions["small"] & (congestion["large"] | congestion["huge"]), addTime["small"])
rule3 = ctrl.Rule(additions["medium"] & (congestion["large"] | congestion["huge"]), addTime["medium"])
rule4 = ctrl.Rule(additions["medium"] & (congestion["tiny"] | congestion["small"] | congestion["medium"]), addTime["small"])
rule5 = ctrl.Rule(additions["large"] & (congestion["large"] | congestion["huge"]), addTime["large"])
rule6 = ctrl.Rule(additions["large"] & (congestion["tiny"] | congestion["small"] | congestion["medium"]), addTime["medium"])
rule7 = ctrl.Rule(additions["huge"] & (congestion["large"] | congestion["huge"] ), addTime["huge"])
rule8 = ctrl.Rule(additions["huge"] & (congestion["tiny"] | congestion["small"] | congestion["medium"]), addTime["large"])

rules = [rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8]

addTimeControl = ctrl.ControlSystem(rules)
addTimeController = ctrl.ControlSystemSimulation(addTimeControl)

def fuzzyExtendTime(currentCongestion,currentAdditions):

    addTimeController.input["congestion"] = currentCongestion
    addTimeController.input["additions"] = currentAdditions

    addTimeController.compute()
    return round(addTimeController.output["addTime"])

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

    safety = 15
    cross = 2
    roadVertTime = 1
    roadHoriTime = 1

    pattern = [0, 1, 0, 1, 1, 0, 0, 1, 2, 2, 1, 0, 1, 3, 2, 1, 2, 1, 0, 1]
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

        congestionHori = roadLeft + roadRight
        arriveHori = addLeft + addRight
        roadHoriTime += fuzzyExtendTime(congestionHori,arriveHori)

        congestionVert = roadTop + roadBot
        arriveVert = addTop + addBot
        roadVertTime += fuzzyExtendTime(congestionVert,arriveVert)

        if roadVert == True:
            roadTop = max(0,roadTop - cross)
            roadBot = max(0,roadBot - cross)
            traversedTop = min(roadTop - cross,3)
            if traversedTop <= 0:
                traversedTop += cross + traversedTop
                lostCount += cross - roadTop
            traversedBot = min(roadBot - cross,3)
            if traversedBot <= 0:
                traversedBot += cross + traversedBot
                lostCount += cross - roadBot
            roadVertTime -= 1
            #congestion
            if roadLeft > 10 or roadRight > 10:
                roadLeft = min(roadLeft,10)
                roadRight = min(roadRight,10)
                congestionTotal += 1


        else:
            roadLeft = max(0,roadLeft - cross)
            roadRight = max(0,roadRight - cross)
            traversedLeft = min(roadLeft - cross,3)
            if traversedLeft <= 0:
                traversedLeft += cross + traversedLeft
                lostCount += cross - roadLeft
            traversedRight = min(roadRight - cross,3)
            if traversedRight <= 0:
                traversedRight += cross + traversedRight
                lostCount += cross - roadRight
            roadHoriTime -= 1
            # congestion
            if roadTop > 10 or roadBot > 10:
                roadTop = min(roadTop,10)
                roadBot = min(roadBot,10)
                congestionTotal += 1

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

        if roadHoriTime <= 0 or roadVertTime <= 0 or safety == 0 or congestionHori == 0 or congestionVert == 0:
            if congestionVert == 0:
                roadVertTime = 1
            elif congestionHori == 0:
                roadHoriTime = 1 
            roadVert = not roadVert
            roadVertTime = max(roadVertTime,1)
            roadHoriTime = max(roadHoriTime,1)
            vertColor, horiColor = horiColor, vertColor
            safety = 14
            switchCount += 1
        else:
            safety -= 1

        #time.sleep(1)

    print("-FUZZY STATS-\n\n")
    print("Number of switches: "+str(switchCount))
    print("Congestion total: "+str(congestionTotal))
    print("Lost time: "+str(lostCount))
    f = open("fuz_log.txt","a+")
    f.write("run "+str(sum(pattern))+": switch,"+str(switchCount)+" cong,"+str(congestionTotal)+" lost,"+str(lostCount)+" seq,"+str(pattern)+"\n")
    f.close()

main(500)
