import numpy as np

def generate_lorenz_data(sigma=10, rho=28, beta=8/3, steps=10000, dt=0.01):
    x, y, z = 0.1, 0.0, 0.0  # Initial conditions
    xs, ys, zs = [x], [y], [z]
    for _ in range(steps):
        dx = sigma * (y - x) * dt
        dy = (x * (rho - z) - y) * dt
        dz = (x * y - beta * z) * dt
        x, y, z = x + dx, y + dy, z + dz
        xs.append(x)
        ys.append(y)
        zs.append(z)
    return xs, ys, zs

def generate_rossler_data(a=0.2, b=0.2, c=5.7, steps=10000, dt=0.01):
    x, y, z = 0.1, 0.0, 0.0  # Initial conditions
    xs, ys, zs = [x], [y], [z]
    for _ in range(steps):
        dx = -y - z
        dy = x + a * y
        dz = b + z * (x - c)
        x, y, z = x + dx * dt, y + dy * dt, z + dz * dt
        xs.append(x)
        ys.append(y)
        zs.append(z)
    return xs, ys, zs

def generate_henon_data(a=1.4, b=0.3, steps=10000):
    x, y = 0.1, 0.0  # Initial conditions
    xs, ys = [x], [y]
    for _ in range(steps):
        x, y = 1 - a * x**2 + y, b * x
        if abs(x) > 1e3 or abs(y) > 1e3:  # Limit to avoid overflow
            break
        xs.append(x)
        ys.append(y)
    return xs, ys

def generate_eclipse_vortex(a=0.7, b=1.8, c=1.2, steps=10000):
    x, y, z = 0.1, 0.1, 0.1  # Initial conditions
    xs, ys, zs = [x], [y], [z]
    for _ in range(steps):
        dx = np.sin(a * y) - z * np.cos(b * x)
        dy = z * np.sin(c * x) - y
        dz = np.cos(a * x) + np.sin(b * y)
        x, y, z = x + dx * 0.01, y + dy * 0.01, z + dz * 0.01
        xs.append(x)
        ys.append(y)
        zs.append(z)
    return xs, ys, zs
