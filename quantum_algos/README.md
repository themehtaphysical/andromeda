# README for Homework 12

This file specifies how to input the values to the various algorithms and how to interpret the results.

## Input

All the programs take number of qubits as input in the input box specified at the beginning of each python notebook. This should be an integer.

### DJ Algorithm
DJ algorithm also take a string input, either 'b' for balanced or 'c' for constant.

### BV Algorithm
BV algorithm takes the binary string 'a' as input. The length of string should match n. 

### Simon's Algorithm
Simon's takes an additional input in the form of a binary string 's'. The length of string should match n.

### Grover's Algorithm
Grover's algorithm accepts the 'key', which is a binary string of length 'n' as input. 


## Output
All programs display the following outputs in the respective order:
1. The circuit diagram
2. The execution time for noiseless simulation
3. The quasi-probability of the output with a noiseless backend 'qasm_simulator'
4. The execution time for noisy simulation with 'ibmq_belem' backend
5. Noisy simulation's quasi-probability with 'ibmq_belem' backend
6. The execution time for noisy simulation with 'ibmq_manila' backend
7. Noisy simulation's quasi-probability with 'ibmq_manila' backend

Therefore, this implementation compares the simulation time for completely parameterized quantum algorithms. 

## Future

I plan to add more algorithms, and make the oracles more complex and paramterizable. And also add the use of these algorithms in some specific scenario. 
