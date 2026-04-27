import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import ast

# ============================================================
# Basic 1-qubit states
# ============================================================

ket0 = np.array([[1.0 + 0j], [0.0 + 0j]])
ket1 = np.array([[0.0 + 0j], [1.0 + 0j]])

ket_plus = (1 / np.sqrt(2)) * np.array([[1.0 + 0j], [1.0 + 0j]])
ket_minus = (1 / np.sqrt(2)) * np.array([[1.0 + 0j], [-1.0 + 0j]])

ket_plus_i = (1 / np.sqrt(2)) * np.array([[1.0 + 0j], [1.0j]])
ket_minus_i = (1 / np.sqrt(2)) * np.array([[1.0 + 0j], [-1.0j]])

NAMED_STATES = {
    "0": ket0,
    "1": ket1,
    "+": ket_plus,
    "-": ket_minus,
    "+i": ket_plus_i,
    "-i": ket_minus_i,
}

GATE_ALIASES = {
    "x":"X","paulix":"X",
    "y":"Y","pauliy":"Y",
    "z":"Z","pauliz":"Z",
    "h":"H","hadamard":"H",
    "s":"S","phase":"S",
    "t":"T",
    "i":"I","identity":"I",
}

# ============================================================
# Standard 1-qubit gates / unitaries
# ============================================================

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
S = np.array([[1, 0], [0, 1j]], dtype=complex)
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)

def rx(theta: float) -> np.ndarray:
    return np.cos(theta / 2) * I - 1j * np.sin(theta / 2) * X

def ry(theta: float) -> np.ndarray:
    return np.cos(theta / 2) * I - 1j * np.sin(theta / 2) * Y

def rz(theta: float) -> np.ndarray:
    return np.cos(theta / 2) * I - 1j * np.sin(theta / 2) * Z

# ============================================================
# Utility functions
# ============================================================

def normalize(state: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(state)
    if norm == 0:
        raise ValueError("Statevector has zero norm.")
    return state / norm

def is_unitary(U: np.ndarray, tol: float = 1e-9) -> bool:
    U = np.asarray(U, dtype=complex)
    return U.shape == (2, 2) and np.allclose(U.conj().T @ U, I, atol=tol)

def bloch_vector(state: np.ndarray) -> np.ndarray:
    """
    Convert a normalized 2x1 statevector into Bloch coordinates (x, y, z).
    """
    psi = normalize(state)
    x = np.real((psi.conj().T @ X @ psi)[0, 0])
    y = np.real((psi.conj().T @ Y @ psi)[0, 0])
    z = np.real((psi.conj().T @ Z @ psi)[0, 0])
    return np.array([x, y, z], dtype=float)

def format_state(state: np.ndarray, decimals: int = 3) -> str:
    psi = normalize(state).flatten()
    a, b = psi[0], psi[1]
    return f"{np.round(a, decimals)}|0> + {np.round(b, decimals)}|1>"

def spherical_to_state(theta: float, phi: float) -> np.ndarray:
    """
    |psi> = cos(theta/2)|0> + e^{i phi} sin(theta/2)|1>
    """
    return np.array([
        [np.cos(theta / 2)],
        [np.exp(1j * phi) * np.sin(theta / 2)]
    ], dtype=complex)

def unitary_to_axis_angle(U: np.ndarray, tol: float = 1e-9):
    """
    Given a 2x2 unitary U, return (axis, angle) such that:
    U ≈ exp(-i * theta/2 * (n·σ))

    Returns:
        axis: np.array([nx, ny, nz])
        theta: float (radians)
    """
    U = np.asarray(U, dtype=complex)

    if not is_unitary(U):
        raise ValueError("Matrix is not unitary.")

    # Step 1: remove global phase
    detU = np.linalg.det(U)
    U_su2 = U / np.sqrt(detU)  # now det ≈ 1

    # Step 2: compute angle 
    trace = np.trace(U_su2)
    cos_half_theta = np.real(trace) / 2
    cos_half_theta = np.clip(cos_half_theta, -1.0, 1.0)

    theta = 2 * np.arccos(cos_half_theta)

    # Step 3: compute axis 
    if abs(np.sin(theta / 2)) < tol:
        # No rotation (or very small) aka arbitrary axis
        return np.array([0.0, 0.0, 1.0]), 0.0

    factor = -1j / (2 * np.sin(theta / 2))
    A = factor * (U_su2 - U_su2.conj().T)

    nx = np.real(A[0, 1] + A[1, 0]) / 2
    ny = np.real((A[0, 1] - A[1, 0]) / (2j))
    nz = np.real((A[0, 0] - A[1, 1]) / 2)

    axis = np.array([nx, ny, nz], dtype=float)

    # normalize axis
    norm = np.linalg.norm(axis)
    if norm > tol:
        axis /= norm

    return axis, theta


def parse_custom_state():
    """
    Let user input a custom 1-qubit state like:
    [1, 1], [0.6, 0.8], [1+1j, 0]
    Returns a normalized 2x1 statevector.
    """
    
    raw = input("Enter custom state vector [a, b]: ")

    try:
        vec = ast.literal_eval(raw)  # safer than eval
        if len(vec) != 2:
            raise ValueError("State must have exactly 2 components.")

        state = np.array(vec, dtype=complex).reshape(2, 1)
        return normalize(state)

    except Exception as e:
        print("Invalid state input:", e)
        return None
    
def parse_custom_unitary():
    """
    Input a 2x2 unitary matrix:
    [[a,b],[c,d]]
    """
    raw = input("Enter 2x2 unitary matrix [[a,b],[c,d]]: ")

    try:
        U = np.array(ast.literal_eval(raw), dtype=complex)

        if U.shape != (2, 2):
            raise ValueError("Must be a 2x2 matrix.")

        if not is_unitary(U):
            raise ValueError("Matrix is not unitary.")

        return U

    except Exception as e:
        print("Invalid unitary:", e)
        return None

# ============================================================
# Bloch sphere visualizer class
# ============================================================

class BlochSphereSimulator:
    def __init__(self, initial_state: np.ndarray = ket0):
        self.state = normalize(initial_state.copy())
        self.history = [self.state.copy()]
        self.labels = ["init"]

        self.fig = None
        self.ax = None
        self.path_line = None
        self.vector_artist = None
        self.point_artist = None
        self.text_artist = None
        self.anim = None  # keep reference alive for FuncAnimation

    def set_state(self, state: np.ndarray, label: str = "set_state"):
        self.state = normalize(state.copy())
        self.history.append(self.state.copy())
        self.labels.append(label)

    def set_named_state(self, name: str):
        if name not in NAMED_STATES:
            raise ValueError(f"Unknown named state '{name}'. Valid: {list(NAMED_STATES.keys())}")
        self.set_state(NAMED_STATES[name], label=f"|{name}>")

   
    def apply_unitary(self, U: np.ndarray, label: str = "U"):
        U = np.asarray(U, dtype=complex)
        if not is_unitary(U):
            raise ValueError("Input matrix is not a valid 2x2 unitary.")

        axis, theta = unitary_to_axis_angle(U)

        print("\n--- Unitary Interpretation ---")
        print(f"Rotation angle: {theta:.3f} radians")
        print(f"Rotation axis: ({axis[0]:.3f}, {axis[1]:.3f}, {axis[2]:.3f})")

        # Apply as before
        self.state = normalize(U @ self.state)
        self.history.append(self.state.copy())
        self.labels.append(label)

    def apply_gate(self, gate_name: str, theta: float = None):
        gate_name = gate_name.upper()
        if gate_name == "I":
            self.apply_unitary(I, "I")
        elif gate_name == "X":
            self.apply_unitary(X, "X")
        elif gate_name == "Y":
            self.apply_unitary(Y, "Y")
        elif gate_name == "Z":
            self.apply_unitary(Z, "Z")
        elif gate_name == "H":
            self.apply_unitary(H, "H")
        elif gate_name == "S":
            self.apply_unitary(S, "S")
        elif gate_name == "T":
            self.apply_unitary(T, "T")
        elif gate_name == "RX":
            if theta is None:
                raise ValueError("RX requires theta.")
            self.apply_unitary(rx(theta), f"Rx({theta:.3f})")
        elif gate_name == "RY":
            if theta is None:
                raise ValueError("RY requires theta.")
            self.apply_unitary(ry(theta), f"Ry({theta:.3f})")
        elif gate_name == "RZ":
            if theta is None:
                raise ValueError("RZ requires theta.")
            self.apply_unitary(rz(theta), f"Rz({theta:.3f})")
        else:
            raise ValueError("Unsupported gate name.")

    def measure_z(self, rng=None):
        """
        Sample a Z-basis measurement and collapse the state.
        """
        if rng is None:
            rng = np.random.default_rng()

        psi = normalize(self.state).flatten()
        p0 = float(np.abs(psi[0]) ** 2)
        p1 = float(np.abs(psi[1]) ** 2)
        outcome = 0 if rng.random() < p0 else 1

        self.state = ket0.copy() if outcome == 0 else ket1.copy()
        self.history.append(self.state.copy())
        self.labels.append(f"measure Z -> {outcome}")

        return outcome, p0, p1

    def _setup_plot(self, title="Bloch Sphere Simulator"):
        self.fig = plt.figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.ax.set_box_aspect((1, 1, 1))

        # Sphere
        u = np.linspace(0, 2 * np.pi, 80)
        v = np.linspace(0, np.pi, 40)
        xs = np.outer(np.cos(u), np.sin(v))
        ys = np.outer(np.sin(u), np.sin(v))
        zs = np.outer(np.ones_like(u), np.cos(v))
        self.ax.plot_surface(xs, ys, zs, alpha=0.10, linewidth=0)

        # Axes
        self.ax.plot([-1, 1], [0, 0], [0, 0], linewidth=1)
        self.ax.plot([0, 0], [-1, 1], [0, 0], linewidth=1)
        self.ax.plot([0, 0], [0, 0], [-1, 1], linewidth=1)

        # Labels
        self.ax.text(1.10, 0, 0, "|+>")
        self.ax.text(-1.20, 0, 0, "|->")
        self.ax.text(0, 1.10, 0, "|+i>")
        self.ax.text(0, -1.20, 0, "|-i>")
        self.ax.text(0, 0, 1.10, "|0>")
        self.ax.text(0, 0, -1.18, "|1>")

        self.ax.set_xlim([-1.2, 1.2])
        self.ax.set_ylim([-1.2, 1.2])
        self.ax.set_zlim([-1.2, 1.2])
        self.ax.set_title(title)

        self.path_line, = self.ax.plot([], [], [], linewidth=2)
        v0 = bloch_vector(self.history[0])

        self.point_artist = self.ax.scatter([v0[0]], [v0[1]], [v0[2]], s=60)
        self.vector_artist = self.ax.quiver(
            0, 0, 0, v0[0], v0[1], v0[2],
            length=1.0, normalize=False
        )

        self.text_artist = self.ax.text2D(0.02, 0.95, "", transform=self.ax.transAxes)
        self._refresh_frame(0)

    def _refresh_frame(self, frame_idx: int):
        vecs = [bloch_vector(s) for s in self.history[:frame_idx + 1]]
        xs = [v[0] for v in vecs]
        ys = [v[1] for v in vecs]
        zs = [v[2] for v in vecs]

        self.path_line.set_data(xs, ys)
        self.path_line.set_3d_properties(zs)

        current = vecs[-1]

        # redraw quiver
        if self.vector_artist is not None:
            self.vector_artist.remove()

        self.vector_artist = self.ax.quiver(
            0, 0, 0,
            current[0], current[1], current[2],
            length=1.0,
            normalize=False
        )

        self.point_artist._offsets3d = ([current[0]], [current[1]], [current[2]])

        label = self.labels[frame_idx]
        state_str = format_state(self.history[frame_idx])
        self.text_artist.set_text(
            f"Step {frame_idx}: {label}\n"
            f"State: {state_str}\n"
            f"Bloch: ({current[0]:.3f}, {current[1]:.3f}, {current[2]:.3f})"
        )
    '''also showing this'''
    def show(self, title="Bloch Sphere Simulator"):
        self._setup_plot(title=title)
        plt.show()

    def animate(self, interval_ms: int = 1200, title="Bloch Sphere Simulator"):
        self._setup_plot(title=title)

        def update(frame):
            self._refresh_frame(frame)
            return self.path_line, self.point_artist, self.vector_artist, self.text_artist

        self.anim = FuncAnimation(
            self.fig,
            update,
            frames=len(self.history),
            interval=interval_ms,
            repeat=False
        )
        plt.draw()
        plt.pause(.001)
        # plt.show()

# ============================================================
# TEST CASES
# ============================================================

# test case for differ bases
def demo_named_states():
    sim = BlochSphereSimulator(ket0)
    sim.set_named_state("+")
    sim.set_named_state("-")
    sim.set_named_state("+i")
    sim.set_named_state("-i")
    sim.animate(title="Named States Demo")

# test cases for the Gates
def demo_gates():
    sim = BlochSphereSimulator(ket0)
    sim.apply_gate("H")
    sim.apply_gate("RZ", np.pi / 2)
    sim.apply_gate("RY", np.pi / 3)
    sim.apply_gate("X")
    sim.animate(title="Gate Demo")
    print("ALL TEST CASE PASSED!")

# custome gates
def demo_custom_unitary():
    sim = BlochSphereSimulator(ket_plus)

    # Example custom unitary:
    # U = Rz(pi/4) @ Ry(pi/3)
    U = rz(np.pi / 4) @ ry(np.pi / 3)

    sim.apply_unitary(U, label="Custom U")
    sim.animate(title="Custom Unitary Demo")

def demo_measurement():
    sim = BlochSphereSimulator(ket0)
    sim.apply_gate("H")
    sim.apply_gate("RZ", np.pi / 3)
    outcome, p0, p1 = sim.measure_z()
    print(f"Measurement outcome: {outcome}, P(0)={p0:.4f}, P(1)={p1:.4f}")
    sim.animate(title="Measurement Demo")


def intro():
    print("="*32)
    print("Welcome to Bloch Sphere Visualizations\n")
    print("Enter 'c' for custom state like: [1, 0], [0.6, 0.8], [1+1j, 0]")
    print("Enter 'r' for named basis:", ", ".join(NAMED_STATES.keys()))
    print("\nGates:", ", ".join(set(GATE_ALIASES.values())))
    print("Rotations Gates: rx(pi/2), ry(pi/3), rz(pi)")
    print("You also enter custom gate by doing [2x2] Matrix `x_gate = [[1,0],[0,1]]` or even sqrt_x gate")
    print("Type 'help' anytime to see this again.\n")


def choose_initial_state():
    while True:
        choice = input("Choose initial state (c/r): ").lower()

        if choice == "c":
            state = parse_custom_state()
            if state is not None:
                return state

        elif choice == "r":
            name = input(f"Enter basis {list(NAMED_STATES.keys())}: ")
            if name in NAMED_STATES:
                return NAMED_STATES[name]
            else:
                print("Invalid named state.")

        elif choice == "help":
            intro()

        else:
            print("Invalid choice. Enter 'c' or 'r'.")


def gate_loop(sim):
    while True:
        gate = input("Enter gate (or 'q', 'help'): ")

        if gate.lower() == "q":
            break

        if gate.lower() == "help":
            intro()
            continue

        # basic gates
        if gate.upper() in ["X", "Y", "Z", "H", "S", "T", "I"]:
            sim.apply_gate(gate.upper())

        # rotation gates like rx(pi/2)
        elif gate.lower().startswith(("rx", "ry", "rz")):
            try:
                name, angle = gate.split("(")
                angle = angle.strip(")")
                theta = eval(angle, {"pi": np.pi})  # safe enough for this use

                sim.apply_gate(name.upper(), theta)

            except Exception:
                print("Invalid rotation format. Use rx(pi/2) etc.")
                continue

        # custom gate
        elif gate.lower() == "custom":
            U = parse_custom_unitary()
            if U is not None:
                sim.apply_unitary(U, label="Custom U")

        else:
            print("Unknown gate.")
            continue

        sim.animate()



if __name__ == "__main__":
    intro()

    state = choose_initial_state()
    sim = BlochSphereSimulator(state)

    # show initial state
    sim.animate()
    gate_loop(sim)

    # ++++++++++TEST for diffre gates, states++++++++++++
    # demo_named_states()
    # sim = BlochSphereSimulator(ket0)
    # sim.set_named_state("+")
    # sim.animate()
    # demo_gates()
    # demo_custom_unitary()
    # demo_measurement()