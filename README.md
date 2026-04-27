# Bloch Sphere Quantum Simulator

## Summary of Results

A Python based interactive simulator for visualizing single qubit quantum states and gates on the Bloch sphere.

It supports standard quantum gates, rotation gates, measurement, and custom unitary matrices.

**Features**
1. Quantum States
   - Built in basis states: 0, 1, plus, minus, plus i, minus i
   - Custom user defined single qubit states

**Quantum Gates**
1. Standard Gates
   - X, Y, Z Pauli gates
   - H Hadamard gate
   - S and T phase gates
   - I identity gate
2. Rotation Gates
   - RX(theta)
   - RY(theta)
   - RZ(theta)
3. Example input:
   - rx(pi/2)
   - ry(pi/3)
   - rz(pi)
4. Custom Unitary Gates
   - You can input any 2x2 matrix as a quantum gate. 
   - Example: [[1, 0], [0, -1]]

All custom gates are checked to ensure they are unitary.

**Visualization**
- 3D Bloch sphere visualization
- State vector trajectory
- Real time state arrow
- Step by step animation

**Measurement**
- Z basis measurement simulation
- Probabilistic collapse of the state

**How to Run**
- python your_file_name.py

**How to Use**

1. **Choose initial state**
 - Custom state:
   - [1, 0]
   - [0.6, 0.8]
   - [1+1j, 0]
- Named state:
  - 0, 1, +, -, +i, -i

2. **Apply gates**
- Standard gates:
  - X
  - Y 
  - Z
  - H
  - S
  - T
- Rotation gates:
  - rx(pi/2)
  - ry(pi/3)
  - rz(pi)
- Custom gate:
- You also enter custom gate by doing [2x2] Matrix `x_gate = [[1,0],[0,1]]` or even sqrt_x gate 
- Then enter matrix:
  - [[0, 1], [1, 0]]
3. **Quit (q)**

**Core Concepts**
- State normalization
- Unitary matrix validation (U dagger U equals I)
- Bloch sphere representation using Pauli expectation values
- Quantum state evolution using matrix multiplication

**Mathematical Background**
- Pauli matrices
- Rotation operators RX, RY, RZ
- Unitary evolution: psi prime equals U psi

**Limitations**
- Single qubit only
- No entanglement
- Custom gates must be 2x2 unitary matrices
- No noise simulation

**Future Improvements**
- Multi qubit support
- Quantum circuit syntax
- Gate chaining
- Noise models
- Export animations

## Suggested Grade Based on Rubric
- Based on the specifications of the rubric, we believe that this project deserves a 100%/A+.
- We sucessfully completed an "implementation of a tool such as a simulator" as the rubric indicates. 
- In response to the feedback suggestion from our proposal regarding the ZYZ decomposition \(R_Z(\theta_1), R_Y(\theta_2), R_Z(\theta_3)\), we implemented full ZYZ decomposition for arbitrary \(2 \times 2\) unitary matrices. Any valid single-qubit unitary can now be expressed as a sequence of three rotations \(R_Z\), \(R_Y\), and \(R_Z\), allowing direct interpretation in terms of standard quantum gates.

However we are not confident with our attempt to compute the ZYZ-decompostions, So we created seperat file that has the ZYZ decompostions, it print on the termnal:
![Alt text](working_example.png)

- Overall, we belive we hit all the goals of this proejct, including the feedback that was suggested. This readme is our project write-up.  

## Contributions
- Both Lucas and Diwas contributed to the design and approach of the project equally. We met in person multiple times to work together in order to incorporate all required deliverables. We implemented the initial apprach together. We also editted and finalized our intial code to include eveything we wanted 
