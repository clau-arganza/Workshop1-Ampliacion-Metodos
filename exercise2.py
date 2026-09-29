# EXERCISE 2 - PART B
# Newton-Raphson method with initial estimate p0 = 1.5.

# Define the function whose root we want to find: f(x) = 0.
def f(x):
    return x**3 - 2*x - 2
# Derivative of the function.
def df(x):
    return 3*x**2 - 2

def newton_raphson(p0, tolerance, max_iterations=100):
   
    p = p0

    # Limit the number of iterations to avoid an endless loop if the method doesn't converge.
    for iteration in range(1, max_iterations + 1):
        derivative = df(p)

        # The derivative is the denominator in Newton's formula.
        # Stop if it is too close to zero to avoid an unstable division.
        # This threshold is a numerical safeguard, not the root tolerance.
        if abs(derivative) < 1e-14:
            raise ValueError("The derivative is too close to zero.")

        # Apply Newton's formula to obtain the next approximation:
        p_next = p - f(p) / derivative

        # Stopping criterion: absolute difference between successive approximations <= tolerance.
        # This measures the change between estimates, not the true error, since the exact root is not known during the calculation.
        if abs(p_next - p) <= tolerance:
            # Return both the approximation and the iteration count.
            return p_next, iteration

        # Use the new approximation as the starting point for the next iteration.
        p = p_next

    # If no approximation satisfies the stopping criterion within the iteration limit, report that convergence was not achieved.
    raise RuntimeError("The method did not converge.")


print("EXERCISE 2 - PART B")

# Each calculation starts again from p0 = 1.5.
for tolerance in (1e-3, 1e-5):
    root, iterations = newton_raphson(1.5, tolerance)

    # Display the tolerance, the root estimate and the iteration count.
    # .12f displays 12 decimal places; it doesn't guarantee that all the displayed digits are accurate.
    print(f"\nTolerance: {tolerance:g}")
    print(f"Root approximation: {root:.12f}")
    print(f"Number of iterations: {iterations}")



# EXERCISE 2 - PART C
# Compare initial estimates p0 = 1.5 and p0 = 2.5.

def f(x):
    return x**3 - 2*x - 2

# Derivative of f(x).
def df(x):
    return 3*x**2 - 2


def newton_raphson(p0, tolerance, max_iterations=100):
    p = p0

    for iteration in range(1, max_iterations + 1):
        derivative = df(p)

        # Check the denominator before applying Newton's formula.
        if abs(derivative) < 1e-14:
            raise ValueError("The derivative is too close to zero.")

        # Calculate the next root estimate.
        p_next = p - f(p) / derivative

        # Use the same stopping criterion as in Part B so the iteration counts can be compared consistently.
        if abs(p_next - p) <= tolerance:
            return p_next, iteration

        # Update the current estimate and continue.
        p = p_next

    raise RuntimeError("The method did not converge.")

print()
print("EXERCISE 2 - PART C")

# The outer loop selects the tolerance.
for tolerance in (1e-3, 1e-5):
    print(f"\nTolerance: {tolerance:g}")

    # The inner loop tests both initial estimates at that tolerance.
    # This gives four calculations in total: two estimates combined with two tolerances.
    for p0 in (1.5, 2.5):
        root, iterations = newton_raphson(p0, tolerance)

        print(
            f"Initial estimate: {p0} | "
            f"Root: {root:.12f} | "
            f"Iterations: {iterations}"
        )

# Interpret the results obtained with the stopping criterion above.
# For p0 = 1.5, the fourth update already satisfies both tolerances.
# For p0 = 2.5, a fifth update is needed for the tighter tolerance.
print("\nDiscussion:")
print("Both initial estimates converge to the same root.")
print("For tolerance 1e-3, both require 4 iterations.")
print("For tolerance 1e-5, p0 = 1.5 requires 4 iterations,")
print("whereas p0 = 2.5 requires 5 iterations.")
print("Therefore, p0 = 1.5 reaches the tighter tolerance faster.")
print("Newton-Raphson converges quadratically near a simple root,")
print("but an unsuitable initial estimate may lead to divergence.")