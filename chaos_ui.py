import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.colors import Normalize
import numpy as np
from lorenz import (
    generate_lorenz_data,
    generate_rossler_data,
    generate_henon_data,
    generate_eclipse_vortex,
)

# Streamlit setup
st.set_page_config(page_title="Chaos Art Generator", layout="wide")

# Title
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>🌌 Chaos Art Generator</h1>",
    unsafe_allow_html=True,
)

# Sidebar for attractor selection
st.sidebar.header("✨ Choose a Chaos System")
chaos_system = st.sidebar.selectbox(
    "Select an Attractor",
    ["Lorenz Attractor", "Rössler Attractor", "Henon Map", "Eclipse Vortex Attractor"],
)

# Attractor equations and parameter explanations
attractor_info = {
    "Lorenz Attractor": {
        "formula": r"""
        $$\frac{dx}{dt} = \sigma (y - x)$$
        $$\frac{dy}{dt} = x (\rho - z) - y$$
        $$\frac{dz}{dt} = x y - \beta z$$
        """,
        "params": {
            "sigma": "Controls the rate of change in the x-direction.",
            "rho": "Controls the size and shape of the attractor.",
            "beta": "Adjusts the decay rate in the z-direction.",
        },
    },
    "Rössler Attractor": {
        "formula": r"""
        $$\frac{dx}{dt} = -y - z$$
        $$\frac{dy}{dt} = x + a y$$
        $$\frac{dz}{dt} = b + z (x - c)$$
        """,
        "params": {
            "a": "Controls the damping effect in the y-direction.",
            "b": "Adds a constant offset to the z-direction.",
            "c": "Adjusts the coupling between x and z.",
        },
    },
    "Henon Map": {
        "formula": r"""
        $$x_{n+1} = 1 - a x_n^2 + y_n$$
        $$y_{n+1} = b x_n$$
        """,
        "params": {
            "a": "Determines the shape of the fractal-like structure.",
            "b": "Controls the strength of the coupling between x and y.",
        },
    },
    "Eclipse Vortex Attractor": {
        "formula": r"""
        $$x_{n+1} = \sin(a y) - z \cos(b x)$$
        $$y_{n+1} = z \sin(c x) - y$$
        $$z_{n+1} = \cos(a x) + \sin(b y)$$
        """,
        "params": {
            "a": "Adjusts the frequency of oscillations in x.",
            "b": "Controls the rotation effect in the system.",
            "c": "Modulates the wave patterns.",
        },
    },
}

# Display formula and parameter explanations
with st.container():
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"<h3 style='color: #4CAF50;'>{chaos_system} Equations</h3>", unsafe_allow_html=True)
        st.markdown(attractor_info[chaos_system]["formula"], unsafe_allow_html=True)

    with col2:
        st.markdown("<h3 style='color: #4CAF50;'>Parameter Explanations</h3>", unsafe_allow_html=True)
        for param, desc in attractor_info[chaos_system]["params"].items():
            st.markdown(f"**{param}:** {desc}")

# Sidebar controls
st.sidebar.header("🎛️ Adjust Parameters")
steps = st.sidebar.slider("Steps", 1000, 50000, 10000, step=1000)

# Generate data based on selection
if chaos_system == "Lorenz Attractor":
    sigma = st.sidebar.slider("Sigma (σ)", 0.1, 50.0, 10.0, step=0.1)
    rho = st.sidebar.slider("Rho (ρ)", 0.1, 50.0, 28.0, step=0.1)
    beta = st.sidebar.slider("Beta (β)", 0.1, 10.0, 2.67, step=0.01)
    xs, ys, zs = generate_lorenz_data(sigma, rho, beta, steps, 0.01)
elif chaos_system == "Rössler Attractor":
    a = st.sidebar.slider("a", 0.1, 1.0, 0.2)
    b = st.sidebar.slider("b", 0.1, 1.0, 0.2)
    c = st.sidebar.slider("c", 0.1, 10.0, 5.7)
    xs, ys, zs = generate_rossler_data(a, b, c, steps, 0.01)
elif chaos_system == "Henon Map":
    a = st.sidebar.slider("a", 1.0, 2.0, 1.4)
    b = st.sidebar.slider("b", 0.1, 0.5, 0.3)
    xs, ys = generate_henon_data(a, b, steps)
    zs = None
elif chaos_system == "Eclipse Vortex Attractor":
    a = st.sidebar.slider("a (Eclipse)", 0.1, 2.0, 0.7)
    b = st.sidebar.slider("b (Eclipse)", 0.1, 2.0, 1.8)
    c = st.sidebar.slider("c (Eclipse)", 0.1, 2.0, 1.2)
    xs, ys, zs = generate_eclipse_vortex(a, b, c, steps)

# Plot
fig = plt.figure(figsize=(8, 6))
if zs is not None:
    points = np.array([xs, ys, zs]).T.reshape(-1, 1, 3)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    norm = Normalize(vmin=0, vmax=len(xs))
    lc = Line3DCollection(segments, cmap="viridis", norm=norm)
    lc.set_array(np.linspace(0, 1, len(xs)))
    lc.set_linewidth(0.8)

    ax = fig.add_subplot(111, projection="3d")
    ax.add_collection3d(lc)
    ax.set_xlim([min(xs), max(xs)])
    ax.set_ylim([min(ys), max(ys)])
    ax.set_zlim([min(zs), max(zs)])
    ax.set_title(chaos_system, fontsize=14)
else:
    points = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    norm = Normalize(vmin=0, vmax=len(xs))
    lc = LineCollection(segments, cmap="plasma", norm=norm)
    lc.set_array(np.linspace(0, 1, len(xs)))
    lc.set_linewidth(0.8)

    ax = fig.add_subplot(111)
    ax.add_collection(lc)
    ax.set_xlim([min(xs), max(xs)])
    ax.set_ylim([min(ys), max(ys)])
    ax.set_title(chaos_system, fontsize=14)

# Display plot
st.pyplot(fig)
