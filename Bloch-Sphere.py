import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ----------------------------
# Basic single-qubit utilities
# ----------------------------

ket0 = np.array([[1.0 + 0j], [0.0 + 0j]])
ket1 = np.array([[0.0 + 0j], [1.0 + 0j]])

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

def h_gate():
    return (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)

def rx(theta):
    return np.cos(theta / 2) * I - 1j * np.sin(theta / 2) * X

def ry(theta):
    return np.cos(theta / 2) * I - 1j * np.sin(theta / 2) * Y

def rz(theta):
    return np.cos(theta / 2) * I - 1j * np.sin(theta / 2) * Z

def normalize(state):
    return state / np.linalg.norm(state)

def bloch_vector(state):
    """Return (x,y,z) for a normalized 2x1 statevector."""
    psi = normalize(state)
    x = np.real((psi.conj().T @ X @ psi)[0, 0])
    y = np.real((psi.conj().T @ Y @ psi)[0, 0])
    z = np.real((psi.conj().T @ Z @ psi)[0, 0])
    return np.array([x, y, z], dtype=float)

def measure_z(state, rng=None):
    """Projective measurement in the Z basis."""
    if rng is None:
        rng = np.random.default_rng()

    psi = normalize(state)
    p0 = float(np.abs(psi[0, 0]) ** 2)
    p1 = float(np.abs(psi[1, 0]) ** 2)

    outcome = 0 if rng.random() < p0 else 1
    collapsed = ket0.copy() if outcome == 0 else ket1.copy()
    return outcome, collapsed, p0, p1

# ----------------------------
# Build a demo sequence
# ----------------------------

state = ket0.copy()
states = [state.copy()]

# Example evolution
for gate in [h_gate(), rz(np.pi / 3), ry(np.pi / 4), rx(np.pi / 5)]:
    state = gate @ state
    states.append(state.copy())

# Measurement step
outcome, collapsed, p0, p1 = measure_z(state)
states.append(collapsed.copy())

vectors = [bloch_vector(s) for s in states]

# ----------------------------
# Plot Bloch sphere
# ----------------------------

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection="3d")
ax.set_box_aspect((1, 1, 1))

# Sphere surface
u = np.linspace(0, 2 * np.pi, 80)
v = np.linspace(0, np.pi, 40)
xs = np.outer(np.cos(u), np.sin(v))
ys = np.outer(np.sin(u), np.sin(v))
zs = np.outer(np.ones_like(u), np.cos(v))

ax.plot_surface(xs, ys, zs, alpha=0.12, linewidth=0)

# Axes
ax.plot([-1, 1], [0, 0], [0, 0])
ax.plot([0, 0], [-1, 1], [0, 0])
ax.plot([0, 0], [0, 0], [-1, 1])

ax.text(1.1, 0, 0, "X")
ax.text(0, 1.1, 0, "Y")
ax.text(0, 0, 1.1, "|0>")
ax.text(0, 0, -1.2, "|1>")

ax.set_xlim([-1.2, 1.2])
ax.set_ylim([-1.2, 1.2])
ax.set_zlim([-1.2, 1.2])
ax.set_title("Single-Qubit Bloch Sphere Measurement Demo")

# Dynamic artists
traj_x, traj_y, traj_z = [], [], []
traj_line, = ax.plot([], [], [], lw=2)
point = ax.scatter([], [], [], s=60)
arrow = None

info = ax.text2D(
    0.02, 0.95,
    f"Before measurement",
    transform=ax.transAxes
)

def update(frame):
    global arrow
    vec = vectors[frame]

    traj_x.append(vec[0])
    traj_y.append(vec[1])
    traj_z.append(vec[2])

    traj_line.set_data(traj_x, traj_y)
    traj_line.set_3d_properties(traj_z)

    # Remove previous arrow
    if update.arrow_artist is not None:
        update.arrow_artist.remove()

    update.arrow_artist = ax.quiver(
        0, 0, 0,
        vec[0], vec[1], vec[2],
        length=1.0,
        normalize=False
    )

    # Recreate point
    update.point_artist._offsets3d = ([vec[0]], [vec[1]], [vec[2]])

    if frame < len(vectors) - 1:
        info.set_text(
            f"Evolution step {frame}\n"
            f"P(0) = {p0:.3f}, P(1) = {p1:.3f}"
        )
    else:
        info.set_text(
            f"Measurement outcome: {outcome}\n"
            f"P(0) = {p0:.3f}, P(1) = {p1:.3f}"
        )

    return traj_line, update.point_artist, update.arrow_artist, info

update.arrow_artist = None
update.point_artist = ax.scatter([vectors[0][0]], [vectors[0][1]], [vectors[0][2]], s=60)

ani = FuncAnimation(fig, update, frames=len(vectors), interval=1200, repeat=False)

plt.show()