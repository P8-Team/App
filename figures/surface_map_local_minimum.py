from src.location.multi_lateration_non_linear_least_square_sum import Anchor, non_linear_squared_sum_weighted, \
    get_least_squared_error
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm


def make_surface_plot(fig, anchors: list[Anchor]):
    axs = fig.add_subplot(1, 2, 2, projection='3d')
    X = np.arange(-7, 8, 0.1)
    Y = np.arange(-7, 8, 0.1)
    X, Y = np.meshgrid(X, Y)

    Z = np.zeros(X.shape)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = non_linear_squared_sum_weighted(np.array([X[i, j], Y[i, j]]), anchors)

    # invert z-axis


    axs.plot_surface(X, Y, Z, rstride=5, cstride=5, cmap=cm.hsv,
                     linewidth=50, antialiased=True, alpha=0.5, zorder=1)
    axs.set_xlabel("x (m)")
    axs.set_ylabel("y (m)")
    axs.set_zlabel("Residual")
    # add estimated location as a vertical line
    position = get_least_squared_error(anchors).x.tolist()
    residual = non_linear_squared_sum_weighted(np.array(position), anchors)
    # set a point
    axs.scatter(position[0], position[1], residual, s=100, marker='o', color='k')
    # axs.plot([position[0], position[0]], [position[1], position[1]], [0, 50], "k", alpha=1, linewidth=2.5,
    #          zorder=2)


def make_circle_plot(fig, anchors):
    position = get_least_squared_error(anchors).x.tolist()

    axs = fig.add_subplot(1, 2, 1)
    axs.set_xlim(-7, 10)
    axs.set_ylim(-7, 10)
    axs.scatter(position[0], position[1], s=100, marker='o', color='k')
    for anchor in anchors:
        axs.scatter(anchor.location[0], anchor.location[1], s=100, marker='o', color='y')
        axs.add_artist(
            plt.Circle(
                (anchor.location[0], anchor.location[1]),
                anchor.distance,
                color='r',
                fill=False,
                linestyle='--'
            )
        )

    axs.legend(["Estimated position", "Anchor node", "Anchor range circle"], loc='upper right')
    axs.grid(True)
    axs.set_xlabel("x (m)")
    axs.set_ylabel("y (m)")


if __name__ == '__main__':
    anchors = [
        Anchor(np.array([0, 0.433], dtype=np.float64), 6, 0),
        Anchor(np.array([-0.433, -0.5], dtype=np.float64), 5.5, 0),
        Anchor(np.array([0.433, -0.5], dtype=np.float64), 5, 0),
    ]

    fig = plt.figure(figsize=plt.figaspect(.5))
    fig.suptitle('Surface map of residual function')

    make_surface_plot(fig, anchors)
    make_circle_plot(fig, anchors)

    # plt.show()
    plt.savefig("render/surface_map.pdf")
