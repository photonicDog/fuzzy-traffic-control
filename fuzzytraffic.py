import random
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
from graphics import *
import time

def fuzzyExtendTime(currentQueue,currentArrivals):
    queue = ctrl.Antecedent(np.arange(0,21,1), "queue")
    queue["tiny"] = fuzz.trimf(queue.universe, [0,0,5])
    queue["small"] = fuzz.trimf(queue.universe, [0,5,10])
    queue["medium"] = fuzz.trimf(queue.universe, [5,10,15])
    queue["large"] = fuzz.trimf(queue.universe, [10,15,20])
    queue["huge"] = fuzz.trimf(queue.universe, [15,20,20])

    arrivals = ctrl.Antecedent(np.arange(0,9,1), "arrivals")
    arrivals["tiny"] = fuzz.trimf(arrivals.universe, [0,0,2])
    arrivals["small"] = fuzz.trimf(arrivals.universe, [0,2,4])
    arrivals["medium"] = fuzz.trimf(arrivals.universe, [2,4,6])
    arrivals["large"] = fuzz.trimf(arrivals.universe, [4,6,8])
    arrivals["huge"] = fuzz.trimf(arrivals.universe, [6,8,8])

    extensions = ctrl.Consequent(np.arange(0,5,1), "extensions")
    extensions["tiny"] = fuzz.trimf(extensions.universe, [0,0,1])
    extensions["small"] = fuzz.trimf(extensions.universe, [0,1,2])
    extensions["medium"] = fuzz.trimf(extensions.universe, [1,2,3])
    extensions["large"] = fuzz.trimf(extensions.universe, [2,3,4])
    extensions["huge"] = fuzz.trimf(extensions.universe, [3,4,4])

    rule1 = ctrl.Rule(arrivals["tiny"]  | (arrivals["small"] & (queue["tiny"] | queue["small"] | queue["medium"])), extensions["tiny"])
    rule2 = ctrl.Rule(arrivals["small"] & (queue["large"] | queue["huge"]), extensions["small"])
    rule3 = ctrl.Rule(arrivals["medium"] & (queue["tiny"] | queue["small"] | queue["medium"]), extensions["small"])
    rule4 = ctrl.Rule(arrivals["medium"] & (queue["large"] | queue["huge"]), extensions["medium"])
    rule5 = ctrl.Rule(arrivals["large"] & (queue["tiny"] | queue["small"] | queue["medium"]), extensions["medium"])
    rule6 = ctrl.Rule(arrivals["large"] & (queue["large"] | queue["huge"]), extensions["large"])
    rule7 = ctrl.Rule(arrivals["huge"] & (queue["tiny"] | queue["small"] | queue["medium"]), extensions["large"])
    rule8 = ctrl.Rule(arrivals["huge"] & (queue["large"] | queue["huge"]), extensions["huge"])

    rules = [rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8]

    extensionsControl = ctrl.ControlSystem(rules)
    timeExtension = ctrl.ControlSystemSimulation(extensionsControl)

    timeExtension.input["queue"] = currentQueue
    timeExtension.input["arrivals"] = currentArrivals

    timeExtension.compute()
    return round(timeExtension.output["extensions"])

def main(iterlimit):
    roadLeft = 0
    roadRight = 0
    roadTop = 0
    roadBot = 0
    cross = 3
    roadTime = 2

    roadVert = True
    vertColor = "green"
    horiColor = "red"

    win = GraphWin("Traffic",500,500)
    win.setBackground("grey")

    for i in range(iterlimit):
        congestion = int(1+random.random()*3)
        addLeft = random.randint(0,congestion)
        addRight = random.randint(0,congestion)
        addTop = random.randint(0,congestion)
        addBot = random.randint(0,congestion)

        if roadVert == True:
            roadTop = max(0,roadTop - cross)
            roadBot = max(0,roadBot - cross)
            queue = roadTop + roadBot
            arrive = addTop + addBot
        else:
            roadLeft = max(0,roadLeft - cross)
            roadRight = max(0,roadRight - cross)
            queue = roadLeft + roadRight
            arrive = addLeft + addRight

        roadTime += fuzzyExtendTime(queue,arrive) - 1

        roadLeft += addLeft
        roadRight += addRight
        roadTop += addTop
        roadBot += addBot

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

        if roadTime == 0 or queue == 0:
            roadVert = not roadVert
            roadTime = 2
            vertColor, horiColor = horiColor, vertColor

        time.sleep(1)

main(30)

"""
queue/arrivals goes from Tiny - Small - Medium - Large - Huge (0-5-10-15-20)
time increase (0-2-4-6-8)
3 cars cross per iteration
roadVert is if the vertical road is open
rules:
    AQ> T S M L H
    T   T T T T T
    S   T T T S S
    M   S S S M M
    L   M M M L L
    H   L L L H H
"""
