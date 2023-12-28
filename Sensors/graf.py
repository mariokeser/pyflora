import matplotlib.pyplot as plt
import numpy as np
xpoints = np.array([1, 8, 4])
ypoints = np.array([3, 10])
"""
num_bins =  500
plt.hist(
    xpoints,
    #ypoints,
    num_bins,
    density=1,
    color="green"

)
plt.xlabel("x-axis")
plt.ylabel("y-axis")
plt.show()
"""
"""
plt.plot(xpoints, ypoints, color = "red", marker = "o")
plt.title("seminar")
plt.xlabel("x label")
plt.ylabel("y label")
plt.grid(True)
plt.show()
"""
labels = "Frogs", "Hogs", "Dogs", "Logs"
sizes = [15, 30, 45, 10]
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=["olivedrab", "rosybrown", "gray", "saddlebrown"])
plt.show()