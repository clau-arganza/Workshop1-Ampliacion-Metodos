def bisection(f, a, b, tolerance, max_iterations=1000):

    "Stop when the midpoint's absolute error bound (b - a) / 2 is less than or equal to the tolerance "

    if tolerance <= 0 or a >= b:
        raise ValueError("Invalid interval or tolerance.")

    fa = f(a)
    fb = f(b)

    if fa == 0:
        return a, 0
    if fb == 0:
        return b, 0

    if fa * fb > 0:
        raise ValueError("The endpoints must have opposite signs.")

    for iteration in range(1, max_iterations + 1):
        p = (a + b) / 2
        fp = f(p)

        if fp == 0 or (b - a) / 2 <= tolerance:
            return p, iteration

        # Retain the half-interval containing a sign change.
        if fa * fp < 0:
            b = p
        else:
            a = p
            fa = fp

    raise RuntimeError("The tolerance was not reached.")


if __name__ == "__main__":
    def f(x):
        return x**3 + x - 3

    for tolerance in (1e-3, 1e-5):
        root, iterations = bisection(f, 1.0, 1.5, tolerance)

        print(
            f"Tolerance = {tolerance:g}, "
            f"root = {root:.12f}, "
            f"iterations = {iterations}"
        )