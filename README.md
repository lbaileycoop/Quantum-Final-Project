## Bloch Sphere Quantum Simulator

A Python based interactive simulator for visualizing single qubit quantum states and gates on the Bloch sphere.

It supports standard quantum gates, rotation gates, measurement, and custom unitary matrices.

Features

Quantum States
- Built in basis states: 0, 1, plus, minus, plus i, minus i
- Custom user defined single qubit states

Quantum Gates

Standard Gates
- X, Y, Z Pauli gates
- H Hadamard gate
- S and T phase gates
- I identity gate

Rotation Gates
- RX(theta)
- RY(theta)
- RZ(theta)

Example input:
rx(pi/2)
ry(pi/3)
rz(pi)

Custom Unitary Gates
You can input any 2x2 matrix as a quantum gate.

Example:
[[1, 0],
 [0, -1]]

All custom gates are checked to ensure they are unitary.

Visualization
- 3D Bloch sphere visualization
- State vector trajectory
- Real time state arrow
- Step by step animation

Measurement
- Z basis measurement simulation
- Probabilistic collapse of the state

How to Run

python your_file_name.py

How to Use

1. Choose initial state

Custom state:
[1, 0]
[0.6, 0.8]
[1+1j, 0]

Named state:
0, 1, +, -, +i, -i

2. Apply gates

Standard gates:
X
Y
Z
H
S
T

Rotation gates:
rx(pi/2)
ry(pi/3)
rz(pi)

Custom gate:
You also enter custom gate by doing [2x2] Matrix `x_gate = [[1,0],[0,1]]` or even sqrt_x gate
Then enter matrix:
[[0, 1],
 [1, 0]]

3. Quit (q)

Core Concepts

- State normalization
- Unitary matrix validation (U dagger U equals I)
- Bloch sphere representation using Pauli expectation values
- Quantum state evolution using matrix multiplication

Mathematical Background

- Pauli matrices
- Rotation operators RX, RY, RZ
- Unitary evolution: psi prime equals U psi

Limitations

- Single qubit only
- No entanglement
- Custom gates must be 2x2 unitary matrices
- No noise simulation

Future Improvements

- Multi qubit support
- Quantum circuit syntax
- Gate chaining
- Noise models
- Export animations