t_dfa = []          # set of alphabet
q_dfa = []          # set of state
start_state = None
final_state = []       # set of final state
transmissions = []     # set of transmissions


def read_conf(path='DFA_Input_1.txt'):    # function for read config from txt file
    config_file = open(path, 'r')

    global t_dfa
    t_dfa = config_file.readline().split(" ")       # read alphabet from file and split elements
    t_dfa[len(t_dfa) - 1] = t_dfa[len(t_dfa) - 1][:-1]              # remove \n from end of line

    global q_dfa
    q_dfa = config_file.readline().split(" ")       # read states from file and split elements
    q_dfa[len(q_dfa) - 1] = q_dfa[len(q_dfa) - 1][:-1]          # remove \n from end of line

    global start_state
    start_state = config_file.readline()[:-1]   # read start state from file and remove \n from end of line

    global final_state
    final_state = config_file.readline().split(" ")     # read final states from file and split elements
    final_state[len(final_state) - 1] = final_state[len(final_state) - 1][:-1]  # remove \n from end of line

    global transmission
    transmission = []    # list of all transformation

    for line in config_file:
        transmission = line.split(' ')   # read states from file and split elements of each transformation
        if transmission[2][-1:] == '\n':
            transmission[2] = transmission[2][:-1]   # remove \n from end of line
        transmissions.append(transmission)


def dfa(phrase_input, init_state):   # this function check string
    current_state = init_state
    for step in range(len(phrase_input)):   # loop on char of my input string
        if phrase_input[step] in t_dfa:       # check each char in my alphabet
            for transmission_step in transmissions:   # loop on transformations
                # mach current state and char
                if transmission_step[0] == current_state and transmission_step[1] == phrase_input[step]:
                    current_state = transmission_step[2]   # change current state

                if current_state in final_state and step == len(phrase_input)-1:
                    break

    if current_state in final_state:     # check for current state is final state
        return 1
    else:
        return 0


def main():
    read_conf()

    input_string = input("Please enter your string : \n")
    input_list = [char for char in input_string]  # split string to char

    result = dfa(input_list, start_state)
    if result == 1:
        print("This input was accepted.")
    else:
        print("This input wasn't accepted!")


if __name__ == "__main__":
    main()
