# Exercise 4: Integration and graphical representations
# Requires numpy and matplotlib.

# Import the mathematical functions needed for the reference integral.
from math import sqrt, pi, erf

# NumPy is used for arrays and calculations at several points.
import numpy as np

# Matplotlib is used to draw the function and both approximations.
import matplotlib.pyplot as plt


# Run this section when the script is executed directly.
if __name__ == "__main__":
    # Define the integration limits and the number of subintervals.
    a, b = 0.0, 2.0
    n = 4

    # All subintervals have the same width: h = 0.5.
    h = (b - a) / n

    # Four subintervals require five integration nodes.
    # linspace gives equally spaced points, including both endpoints.
    x = np.linspace(a, b, n + 1)

    # Evaluate f(x) = exp(-x^2) at each integration node.
    y = np.exp(-x**2)

    # Composite Trapezoidal Rule.
    # The first and last values have weight 1/2.
    # y[1:-1] contains all the interior values.
    trapezoidal = h * (
        y[0] / 2 + np.sum(y[1:-1]) + y[-1] / 2
    )

    # Composite Simpson's 1/3 Rule requires an even number of subintervals.
    # The weights for n = 4 are 1, 4, 2, 4, 1.
    # y[1:-1:2] selects the odd-indexed interior values: y[1], y[3].
    # y[2:-1:2] selects the even-indexed interior value: y[2].
    simpson = h / 3 * (
        y[0]
        + 4 * np.sum(y[1:-1:2])
        + 2 * np.sum(y[2:-1:2])
        + y[-1]
    )

    # The integral can be expressed using the error function, erf.
    # This provides a reference value for checking the approximations.
    reference = sqrt(pi) / 2 * erf(2)

    # The trapezoidal error bound uses max|f''(x)| = 2 on [0, 2].
    # Formula: (b - a) * h^2 * max|f''(x)| / 12.
    trapezoidal_bound = (b - a) * h**2 * 2 / 12

    # The Simpson error bound uses max|f''''(x)| = 12 on [0, 2].
    # Formula: (b - a) * h^4 * max|f''''(x)| / 180.
    # These bounds are upper limits, not the actual errors.
    simpson_bound = (b - a) * h**4 * 12 / 180

    # Display the approximations, error bounds and reference value.
    # .12f displays each result with 12 decimal places.
    print(f"Trapezoidal approximation: {trapezoidal:.12f}")
    print(f"Trapezoidal error bound: {trapezoidal_bound:.12f}")
    print(f"Simpson approximation: {simpson:.12f}")
    print(f"Simpson error bound: {simpson_bound:.12f}")
    print(f"Reference integral: {reference:.12f}")

    # Calculate the absolute true errors by comparing each
    # approximation with the reference integral.
    print(
        "Trapezoidal absolute true error: "
        f"{abs(reference - trapezoidal):.12f}"
    )
    print(
        "Simpson absolute true error: "
        f"{abs(reference - simpson):.12f}"
    )

    # Create two plots side by side.
    # Sharing the vertical scale makes the methods easier to compare.
    fig, axes = plt.subplots(
        1, 2, figsize=(12, 5), sharey=True
    )

    # Use more points to draw a smooth curve.
    # These points are only for plotting; the integration still uses n = 4.
    dense_x = np.linspace(a, b, 600)

    # Alternate the shading colors to distinguish adjacent regions.
    colors = ["#91c7eb", "#b7dfd2"]

    # Draw the original function and integration nodes on both plots.
    for ax in axes:
        ax.plot(
            dense_x,
            np.exp(-dense_x**2),
            color="#172c48",
            linewidth=2,
            label="f(x) = exp(-x²)",
            zorder=4
        )

        # Mark the five nodes used in the numerical integration.
        # zorder keeps the points visible above the shaded regions.
        ax.scatter(
            x, y,
            color="#172c48",
            label="Integration nodes",
            zorder=5
        )

        # Draw vertical dotted lines from the x-axis to each node.
        ax.vlines(
            x, 0, y,
            colors="gray",
            linestyles=":",
            linewidth=1
        )

        # Set the axis limits, node positions and a light grid.
        ax.set_xlabel("x")
        ax.set_xlim(a, b)
        ax.set_ylim(0, 1.1)
        ax.set_xticks(x)
        ax.grid(alpha=0.15)

    # Construct one straight line over each of the four subintervals.
    for i in range(n):
        xx = np.linspace(x[i], x[i + 1], 50)

        # Equation of the line joining two consecutive nodes:
        # y = y_i + slope * (x - x_i).
        # The slope is (y[i + 1] - y[i]) / h.
        yy = y[i] + (y[i + 1] - y[i]) * (xx - x[i]) / h

        # Shade the area between the line and the x-axis.
        # i % 2 alternates between the two colors.
        axes[0].fill_between(
            xx, 0, yy,
            color=colors[i % 2],
            alpha=0.65
        )

        # Draw the upper edge of each trapezoid.
        # Add the label only once to avoid repeated legend entries.
        axes[0].plot(
            xx, yy,
            color="#c16622",
            linewidth=1.8,
            label="Linear segments" if i == 0 else None
        )

    # Simpson's rule uses one parabola for each pair of subintervals.
    # The first passes through nodes 0, 1, 2; the second through 2, 3, 4.
    for i in (0, 2):
        xx = np.linspace(x[i], x[i + 2], 150)

        # Start with zero and add the three Lagrange polynomial terms.
        yy = np.zeros_like(xx)

        # Each j selects one of the three interpolation nodes.
        for j in range(i, i + 3):
            term = np.ones_like(xx) * y[j]

            # Construct y[j] * L_j(x), where L_j is 1 at node j
            # and 0 at the other two nodes.
            for k in range(i, i + 3):
                if j != k:
                    term *= (xx - x[k]) / (x[j] - x[k])

            # Add this contribution to the quadratic interpolant.
            yy += term

        # Shade the area under each parabola.
        # i // 2 selects color 0 for the first and color 1 for the second.
        axes[1].fill_between(
            xx, 0, yy,
            color=colors[i // 2],
            alpha=0.65
        )

        # Draw the parabolas used by Simpson's rule.
        axes[1].plot(
            xx, yy,
            color="#c16622",
            linewidth=1.8,
            label="Quadratic interpolants" if i == 0 else None
        )

    # Include the method, number of subintervals and result in each title.
    # \n places the numerical result on a new line.
    axes[0].set_title(
        f"Composite Trapezoidal Rule: n = 4\n"
        f"T = {trapezoidal:.9f}"
    )
    axes[1].set_title(
        f"Composite Simpson's 1/3 Rule: n = 4\n"
        f"S = {simpson:.9f}"
    )
    axes[0].set_ylabel("y")

    # Display the labels identifying the curves and integration nodes.
    for ax in axes:
        ax.legend(fontsize=8)

    # Adjust the spacing to prevent titles and labels from overlapping.
    fig.tight_layout()

    # Save the figure before displaying it.
    fig.savefig("exercise_4_plots.png", dpi=200)
    plt.show()