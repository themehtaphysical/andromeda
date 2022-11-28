# README QASM simulator

This file specifies how to use and benchmark the QASM simulator and how to interpret the results.

## Input

Run command 
> python3.x qasm_simulator.py

Upon execution, the simulator prompts the user to input the following values:
1. path for the qasm files (leave empty and press return if they are in the same directory as the one you are executing the python file in)
2. enter whether you want to generate the log and report files for the run or not (y/n) (leave empty for 'yes')
3. if the previous answer was 'yes', enter the path where you want to generate the log files. (leave empty for the present working directory) ($OUTPUT_PATH)
4. enter whether or not you want to print the quantum state after each gate execution in the terminal. (leave empty for 'yes')

## Output

The logs are generate in the $OUTPUT_PATH/logs which contain step wise execution of all the gates in the qasm files. The name of the log for a file {qasm_file_name}.qasm will be 
>log_{qasm_file_name}.txt

The cumulative report is generated and can be found at 
>$OUTPUT_PATH/report/report.txt 

The report contains a table of the benchmarking program, the final output state and the execution time for that program. It also calculates the total execution time for running all the programs. 
The same output that is stored in the report file is displayed on the terminal at the end of execution. 


## Interpreting the output

The initial state of the qasm simulator is given by:
> |0000000000000000>

for the case of the benchmark suite. The notation for qubit, that is followed across this simulator is:
> **|q0 q1 q2 .. .. .. qn >**

The output state is also represented as linear combination of the kets of 2^n hilbert space, with complex amplitudes. 
So for example, an output state given as:
> (0.737) |1100000000000000> + (0.737j)|0000001000000000>

this means that the final output state is a linear combination of two state given by the kets represented above, each state having its own complex amplitude. 


