import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 

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
addTime.view()

rule1 = ctrl.Rule(additions["tiny"]  |
    (additions["small"] & 
        (congestion["tiny"] | congestion["small"]  | congestion["medium"])),addTime["tiny"])

rule2 = ctrl.Rule(additions["small"] & (congestion["large"] | congestion["huge"]), addTime["small"])
rule4 = ctrl.Rule(additions["medium"] & (congestion["tiny"] | congestion["small"] | congestion["medium"]), addTime["small"])
rule3 = ctrl.Rule(additions["medium"] & (congestion["large"] | congestion["huge"]), addTime["medium"])
rule6 = ctrl.Rule(additions["large"] & (congestion["tiny"] | congestion["small"] | congestion["medium"]), addTime["medium"])
rule5 = ctrl.Rule(additions["large"] & (congestion["large"] | congestion["huge"]), addTime["large"])
rule8 = ctrl.Rule(additions["huge"] & (congestion["tiny"] | congestion["small"] | congestion["medium"]), addTime["large"])
rule7 = ctrl.Rule(additions["huge"] & (congestion["large"] | congestion["huge"] ), addTime["huge"])

rules = [rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8]

addTimeControl = ctrl.ControlSystem(rules)
addTimeController = ctrl.ControlSystemSimulation(addTimeControl)

upsampled1 = np.linspace(0, 10, 50)
upsampled2 = np.linspace(0, 4, 50)
x, y, = np.meshgrid(upsampled1, upsampled2)
z = np.zeros_like(x)

for i in range(50):
    for j in range(50):
        addTimeController.input['congestion'] = x[i, j]
        addTimeController.input['additions'] = y[i, j]
        addTimeController.compute()
        z[i, j] = addTimeController.output['addTime']

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

cset = ax.contourf(x, y, z, zdir='z', offset=-0.2, cmap='viridis', alpha=0.5)
cset = ax.contourf(x, y, z, zdir='x', offset=11, cmap='viridis', alpha=0.5)
cset = ax.contourf(x, y, z, zdir='y', offset=4.5, cmap='viridis', alpha=0.5)

surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis',linewidth=0.4, antialiased=True)

ax.set_xlabel('Congestion')
ax.set_ylabel('Additions')
ax.set_zlabel('addTime')

ax.view_init(30, 200)

plt.show()
