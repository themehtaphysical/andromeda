'''
Import the required libraries
'''

import numpy as np
from glob import glob
import os
import time
from datetime import datetime




'''
The required methods are defined here
'''


#extract the gate and the qubit on which the gate is being applied from the qasm file string
def func_extract_gate_n(line: str):
    _str = line.rstrip().replace(' ','')
    _q_index = _str.find('q[')
    _c_index = _str.find('c[')

    #check if the gate is cx or not (to extract multiple qubits)
    if (_str[0:2] == 'cx'):
        return ['cx', [(int(_str[4]) if _str[5]==']' else int(_str[4:6])), (int(_str[-3]) if _str[-4]=='[' else int(_str[-4:-2]))]]
    else:
        return [_str[0:_q_index + _c_index + 1],(int(_str[-3]) if _str[-4]=='[' else int(_str[-4:-2]))]



#flip a bit in the qubit representation
def func_flip_bit(string: str, index: int):
    return string[0:index] + str(np.abs(int(string[index])-1)) + string[index+1:len(string)]



#extract the state and the amplitude lists from a zipped list of both
def func_extract_state_amp(q_state):
    _state, _amp = zip(*q_state)
    _state = list(_state)
    _amp = list(_amp)
    return _state,_amp



#generate a zipped list (qstate) containing both amplitude and state lists
def func_generate_qstate(_state, _amp):
    #zip the lists again
    _q_state_updated = list(zip(_state,_amp))

    #sort the zipped list based on the quantum state
    _q_state_updated_sort = sorted(_q_state_updated, key = lambda x: x[0])
    return _q_state_updated_sort



#find the duplicates in the state list and merge them together by adding their corresponding amplitudes.
def func_merge_qstates(q_state):

    _state_merged = []
    _amp_merged = []

    #iterate over the q states and check if it already exists in merged list
    for _q_state_val in q_state:
        if not _state_merged:
            _state_merged.append(_q_state_val[0])
            _amp_merged.append(_q_state_val[1])
        elif(_q_state_val[0] == _state_merged[-1]):
            _amp_merged[-1] = _amp_merged[-1] + _q_state_val[1]
        else:
            _state_merged.append(_q_state_val[0])
            _amp_merged.append(_q_state_val[1])

    #generate the q state from state and amp lists
    _q_state_final = func_generate_qstate(_state_merged, _amp_merged)

    #return the sorted q state list
    return _q_state_final



#function to represent the stored qstate zipped list in a human readable format
def func_represent_state(q_state):
    #extract the quantum states and their amplitudes in separate lists
    _state, _amp = func_extract_state_amp(q_state)
    _amp = np.around(_amp, 5)
    _output_string = ''
    for _state_val, _amp_value in zip(_state,_amp):
        if(np.abs(_amp_value) !=0):
            if np.abs(np.imag(_amp_value)) == 0:
                _amp_value = '+ (' + str(np.real(_amp_value)) + ')' if np.real(_amp_value) != 1 else ''
            elif np.abs(np.real(_amp_value)) == 0:
                _amp_value = '+ (' + str(np.imag(_amp_value)*1j) + ')'
            else:
                _amp_value = '+ ' + str(_amp_value)
            _output_string = (_output_string + _amp_value + ' |' + str(_state_val)+'>  ')[1::]
        else:
            pass
    return _output_string



'''
The gates are defined below. They operate on zipped lists of quantum states and amplitudes
'''

#X gate
def gate_x(q_state, index):

    #extract the quantum states and their amplitudes in separate lists
    _state, _amp = func_extract_state_amp(q_state)

    #apply the gate logic
    for i in range(len(_state)):
        _state[i] = func_flip_bit(_state[i],index)

    #generate the q state from state and amp lists
    _q_state_final = func_generate_qstate(_state, _amp)

    #return the sorted q state list
    return _q_state_final



#control X gate
def gate_cx(q_state, index):

    #extract the quantum states and their amplitudes in separate lists
    _state, _amp = func_extract_state_amp(q_state)

    #apply the gate logic
    for i in range(len(_state)):
        if(_state[i][index[0]] == '1'):
            _state[i] = func_flip_bit(_state[i],index[1])

    #generate the q state from state and amp lists
    _q_state_final = func_generate_qstate(_state, _amp)

    #return the sorted q state list
    return _q_state_final



#hadamard gate
def gate_h(q_state, index):

    #extract the quantum states and their amplitudes in separate lists
    _state, _amp = func_extract_state_amp(q_state)

    #apply the gate logic
    for i in range(len(_state)):
        _state.append(func_flip_bit(_state[i],index))
        if(_state[i][index] == '0'):
            _amp[i] = (1/np.sqrt(2))*_amp[i]
            _amp.append(_amp[i])
        else:
            _amp[i] = (-1/np.sqrt(2))*_amp[i]
            _amp.append(-1*_amp[i])
        

    #generate the q state from state and amp lists
    _q_state_unmerged = func_generate_qstate(_state, _amp)

    #merge the duplicate elements
    _q_state_final = func_merge_qstates(_q_state_unmerged)
    
    #return the sorted q state list
    return _q_state_final



#t gate
def gate_t(q_state, index):
    #extract the quantum states and their amplitudes in separate lists
    _state, _amp = func_extract_state_amp(q_state)

    #apply the gate logic
    t = np.exp(1j*np.pi/4)
    for i in range(len(_state)):
        if(_state[i][index] == '0'):
            pass
        else:
            _amp[i] = (t*_amp[i])
        

    #generate the q state from state and amp lists
    _q_state_final = func_generate_qstate(_state, _amp)

    #return the sorted q state list
    return _q_state_final



#tdg gate
def gate_tdg(q_state, index):
    #extract the quantum states and their amplitudes in separate lists
    _state, _amp = func_extract_state_amp(q_state)

    #apply the gate logic
    tdg = np.exp(-1j*np.pi/4)
    for i in range(len(_state)):
        if(_state[i][index] == '0'):
            pass
        else:
            _amp[i] = (tdg*_amp[i])
        

    #generate the q state from state and amp lists
    _q_state_final = func_generate_qstate(_state, _amp)

    #return the sorted q state list
    return _q_state_final



'''
The main method is defined here
'''

def main():
    start_time = time.time()

    search_path = str(input("Enter the path for qasm files") or './').strip(' ')
    if not os.path.exists(search_path):
        raise NameError("Path not found")
    #search_path = '/home/amanmehta/workspace/ucla/quantum_programming_cs238/homework/qasm_simulation/'
    search_path = search_path if search_path[-1] == '/' else search_path + '/'

    is_generate_logs = str(input("Generate logs and report (y/n)") or 'y')
    

    is_generate_logs = True if (is_generate_logs.lower() == 'y' or is_generate_logs.lower() == 'yes') else False
    

    if (is_generate_logs):
        output_path = str(input("Enter the path for output logs and report") or './').strip(' ')
        output_path = output_path + 'logs/'
        if not os.path.exists(output_path):
            os.mkdir(output_path)

    is_display_print = str(input("Display terminal prints (y/n)") or 'y')
    is_display_print = True if (is_display_print.lower() == 'y' or is_display_print.lower() == 'yes') else False

    qasm_flie_list = glob(search_path+'/*.qasm')
    if not qasm_flie_list:
        raise NameError("No QASM files found!")
    final_states = {}
    #print(qasm_flie_list)
    for qasm_flie in qasm_flie_list:
        start_time_iteration = time.time()
        fp_in = open(qasm_flie, 'r')

        if (is_generate_logs):
            output_file = output_path + 'log_' + (qasm_flie.replace(search_path,'')).replace('.qasm', '.txt')
            fp_out = open(output_file, 'w')


        number_of_qubits = 0
        quantum_state = []


        for line in fp_in:
            if line[0] not in ['O','i','#']:
                q_gate, n = func_extract_gate_n(line)
                #print(q_gate,n)
                if q_gate == 'qreg':
                    number_of_qubits = n
                    #intialize the state
                    quantum_state = [(str(0).zfill(number_of_qubits),1)]
                    if is_display_print:
                        print("initialized the quantum state to " + func_represent_state(quantum_state))


                elif q_gate == 'h':
                    quantum_state =  gate_h(quantum_state,n)
                    if is_display_print:
                        print("\napplied hadamard on qubit "+str(n)+ " :\n" + func_represent_state(quantum_state))

                elif q_gate == 'x':
                    quantum_state =  gate_x(quantum_state,n)
                    if is_display_print:
                        print("\napplied x gate on qubit "+str(n)+ " :\n" + func_represent_state(quantum_state))

                elif q_gate == 't':
                    quantum_state =  gate_t(quantum_state,n)
                    if is_display_print:
                        print("\napplied t gate on qubit "+str(n)+ " :\n" + func_represent_state(quantum_state))

                elif q_gate == 'tdg':
                    quantum_state =  gate_tdg(quantum_state,n)
                    if is_display_print:
                        print("\napplied tdg gate on qubit "+str(n)+ " :\n" + func_represent_state(quantum_state))

                elif q_gate == 'cx':
                    quantum_state =  gate_cx(quantum_state,n)
                    if is_display_print:
                        print("\napplied cx gate on qubit "+str(n)+ " :\n" + func_represent_state(quantum_state))

                else:
                    pass


                if (is_generate_logs):
                    fp_out.write(line)
                    fp_out.write('\n')
                    fp_out.write(func_represent_state(quantum_state))
                    fp_out.write('\n\n')

        fp_in.close()
        if (is_generate_logs):
            fp_out.close()
        if is_display_print:
            print('\n\nThe final state is:\n')
            print(func_represent_state(quantum_state))
        total_time_iteration = time.time() - start_time_iteration
        final_states[qasm_flie.replace(search_path,'')] = [func_represent_state(quantum_state), total_time_iteration]

    final_states =  dict(sorted(final_states.items(), key = lambda x: x[1][1]))


    if (is_generate_logs):
        output_path = output_path.replace('logs', 'report') 
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        fp_out = open(output_path + 'report.txt', 'w')
        fp_out.write('Report generated at %s\n'%datetime.now())


        fp_out.write("\n\n\n____________________________________________________________________________________________________\n")
        fp_out.write("{:<40} {:<40} {:<40}".format('benchmark program', 'final output state', 'execution time (s)'))
        fp_out.write("\n____________________________________________________________________________________________________\n")


    print("\n\n\n____________________________________________________________________________________________________")
    print("{:<40} {:<40} {:<40}".format('benchmark program', 'final output state', 'execution time (s)'))
    print("____________________________________________________________________________________________________\n")
    for key, value in final_states.items():
        fs,time_taken = value
        print("{:<40} {:<40} {:<40}".format(key, fs, str(np.around(time_taken,12)).zfill(15)))
        if (is_generate_logs):
            fp_out.write("{:<40} {:<40} {:<40}".format(key, fs, str(np.around(time_taken,12)).zfill(15)))
            fp_out.write('\n')

    if (is_generate_logs):
        fp_out.write("\n\n-----total benchmark execution time is  %s seconds -----" % (time.time() - start_time))
        fp_out.close()





'''
Testing Code here
'''

test_state = ['1100','0100','1010']
test_amp = [1,1,2]
test_q_state = list(zip(test_state,test_amp))
#print(test_q_state)
#print(gate_h(test_q_state,0))
#print(sorted(gate_h(test_q_state,0), key = lambda x: x[0]))




'''
Run the main function here
'''

start_time = time.time()
main()
print("\n\n-----total benchmark execution time is  %s seconds -----" % (time.time() - start_time))


