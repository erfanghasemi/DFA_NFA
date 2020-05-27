import collections.abc

all_states_transmission = {}   # all states that transmit by alphabets for states

t_nfa = []  # set of NFA alphabet
q_nfa = []  # set of NFA state
start_state_nfa = None
final_states_nfa = []    # set of NFA final state
transmissions_nfa = []  # set of NFA transmission

q_dfa = []  # set of DFA state
start_state_dfa = []
final_states_dfa = []    # set of DFA final state
transmissions_dfa = []  # set of DFA transformations of state


def read_conf(path='NFA_Input_2.txt'):      # function for read NFA config from txt file
    config_file = open(path, 'r')

    global t_nfa
    t_nfa = config_file.readline().split(" ")       # read NFA alphabet from file and split elements
    t_nfa[len(t_nfa) - 1] = t_nfa[len(t_nfa) - 1][:-1]  # remove \n from end of line

    global q_nfa
    q_nfa = config_file.readline().split(" ")       # read NFA states from file and split elements
    q_nfa[len(q_nfa) - 1] = q_nfa[len(q_nfa) - 1][:-1]  # remove \n from end of line

    global start_state_nfa
    start_state_nfa = config_file.readline()[:-1]   # read NFA start state from file and remove \n from end of line

    global final_states_nfa
    final_states_nfa = config_file.readline().split(" ")     # read NFA final states from file and split elements
    final_states_nfa[len(final_states_nfa) - 1] = final_states_nfa[len(final_states_nfa) - 1][:-1]

    global transmissions_nfa
    transmissions_nfa = []  # list of all NFA transformation

    for line in config_file:
        transmission_nfa = line.split(' ')  # read NFA states from file and split elements of each transformation
        if transmission_nfa[1] not in t_nfa:    # change the sign of LAMBDA to string of 'LAMBDA'
            transmission_nfa[1] = 'LAMBDA'
        if transmission_nfa[2][-1:] == '\n':
            transmission_nfa[2] = transmission_nfa[2][:-1]  # remove \n from end of line
        transmissions_nfa.append(transmission_nfa)


def flatten(nested_list):   # this function use for handle some irregular nested list
    for item in nested_list:  # and aggregate all of them to one list
        if isinstance(item, collections.abc.Iterable) and not isinstance(item, (str, bytes)):
            yield from flatten(item)
        else:
            yield item


# this function find all possible destinations for specific state and alphabet


def find_destination_states(state, alphabet):
    destinations_list = []

    if alphabet == 'LAMBDA':     # this condition created for initial state
        if state not in destinations_list:
            destinations_list.append(state)

    for transmission in transmissions_nfa:  # this section created for find all destination
        if transmission[0] == state and transmission[1] == alphabet:
            if transmission[2] not in destinations_list:
                destinations_list.append(transmission[2])
            # this recursive manner for eliminate lambda label
            destinations_list.append(find_destination_states(transmission[2], 'LAMBDA'))

    distinct_destination_set = []
    for state in flatten(destinations_list):   # this section is for eliminate nested list
        if state not in distinct_destination_set:
            distinct_destination_set.append(state)

    return set(distinct_destination_set)


def calc_all_transmit():   # this section for calculate all transmission that possible
    temp_alphabet = t_nfa.copy()
    temp_alphabet.append('LAMBDA')  # add lambda to alphabet to calculate epsilon closure
    for state in q_nfa:
        for alphabet in temp_alphabet:
            # store all transmission in dict that contain one tuple as key and one set as value
            all_states_transmission[tuple([state, alphabet])] = find_destination_states(state, alphabet)


def new_state_set(current_state):   # this recursive function apply

    for alphabet in t_nfa:  # loop on DFA alphabet
        target_state_set = []   # new set of state
        for member_state in current_state:  # loop on member of multi member state
            target_state_set = set(target_state_set) | all_states_transmission[(member_state, alphabet)]
        # condition of len in if statement exist because remove dead state
        if target_state_set not in q_dfa and len(target_state_set) != 0:
            # add transmission to DFA transmissions
            transmissions_dfa.append([current_state, alphabet, target_state_set])
            q_dfa.append(target_state_set)
            new_state_set(target_state_set)
    return


def find_final_states(states_list, final_nfa):
    for state in states_list:    # fins states of DFA that include final state of NFA
        for final_state in final_nfa:
            if final_state in state and state not in final_states_dfa:
                final_states_dfa.append(state)


def create_file():    # write config of DFA to txt file
    dfa_txt_file = open("DFA_Output_2.txt", 'w')
    dfa_txt_file.write(' '.join(t_nfa))
    dfa_txt_file.write('\n')

    for state in q_dfa:
        dfa_txt_file.write(str(state))
    dfa_txt_file.write('\n')

    dfa_txt_file.write(str(start_state_dfa))
    dfa_txt_file.write('\n')

    for state in final_states_dfa:
        dfa_txt_file.write(str(state))
    dfa_txt_file.write('\n')

    for transmission in transmissions_dfa:
        dfa_txt_file.write(f"{transmission[0]} {transmission[1]} {transmission[2]}")
        dfa_txt_file.write('\n')


def main():
    read_conf()

    calc_all_transmit()

    global start_state_dfa
    start_state_dfa = all_states_transmission[(start_state_nfa, 'LAMBDA')]
    q_dfa.append(start_state_dfa)

    new_state_set(start_state_dfa)
    find_final_states(q_dfa, final_states_nfa)
    create_file()


if __name__ == "__main__":
    main()
