import numpy as np
from matplotlib import pyplot as plt

from src.location.multi_lateration_non_linear_least_square_sum import Anchor

anchors = [
    Anchor(location=np.array([-0.5,-0.433]), distance=4.5, variance=1),
    Anchor(location=np.array([0.5,-0.433]), distance=3.82, variance=1),
    Anchor(location=np.array([0,0.433]), distance=3.56, variance=1),
]

position = np.array([2.82,2.6])


fig, axs = plt.subplots(1, 2, figsize=(14, 7), sharey=True)


axs[0].set_xlim(-6, 6)
axs[0].set_ylim(-6, 6)
axs[0].scatter(position[0], position[1], s=100, marker='o', color='g')
for anchor in anchors:
    axs[0].scatter(anchor.location[0], anchor.location[1], s=100, marker='o', color='y')
    axs[0].add_artist(
        plt.Circle(
            (anchor.location[0], anchor.location[1]),
            anchor.distance,
            color='r',
            fill=False,
            linestyle='--'
        )
    )


anchors = [
    Anchor(location=np.array([-0.5,-0.433]), distance=4.75, variance=1),
    Anchor(location=np.array([0.5,-0.433]), distance=3.63, variance=1),
    Anchor(location=np.array([0,0.433]), distance=3.68, variance=1),
]

position = np.array([2.82,2.6])


axs[1].set_xlim(-6, 6)
axs[1].set_ylim(-6, 6)
axs[1].scatter(position[0], position[1], s=100, marker='o', color='g')
for anchor in anchors:
    axs[1].scatter(anchor.location[0], anchor.location[1], s=100, marker='o', color='y')
    axs[1].add_artist(
        plt.Circle(
            (anchor.location[0], anchor.location[1]),
            anchor.distance,
            color='r',
            fill=False,
            linestyle='--'
        )
    )


# add legend
axs[0].legend(["Estimated position", "Anchor node", "Anchor range circle"], loc='upper right')
axs[1].legend(["Estimated position", "Anchor node", "Anchor range circle"], loc='upper right')

# add title
axs[0].set_title("True-range multi-lateration")
axs[1].set_title("Pseudo-range multi-lateration")

# add grid
axs[0].grid(True)
axs[1].grid(True)

# axis labels
axs[0].set_xlabel("x (m)")
axs[0].set_ylabel("y (m)")
axs[1].set_xlabel("x (m)")
axs[1].set_ylabel("y (m)")

# save as svg
plt.savefig("render/pseudo_multilateration.pdf")