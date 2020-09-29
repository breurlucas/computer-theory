# import libraries

# -----------------------------------------------------------------------------
#
# Lucas Breur
# 29-09-2020
# Senac Computer Theory - Turing Machine Simulator
#
# -----------------------------------------------------------------------------

# FILE READING

file = open("tm-example.txt", "r")  # Open file in read-only mode
file_list = file.readlines()  # Store lines as strings in an array
file_list = [line.strip('\n') for line in file_list]  # Remove newline characters
file_list = [line.replace(' ', '') for line in file_list]  # Remove spaces


# VARIABLE CONSTRUCTION

qa = file_list[1]  # Acceptance state
q0 = 1  # Initial state
q = q0  # Current state initialization
head_position = 1  # Head position initialization

# Reading variables
start_transitions = 3  # First transition item
nr_transitions = int(file_list[2])  # Number of transitions
start_words = start_transitions + nr_transitions + 1  # First word item
nr_words = int(file_list[start_transitions + nr_transitions])  # Number of words

# Create Transition Matrix
# Crop the file in order to consider only the transition rules
ts_matrix = file_list[start_transitions:(nr_transitions + start_transitions)]
# ts_matrix = [list(line) for line in ts_matrix]  # Convert strings to arrays of characters
# print(ts_matrix)

# Create list of words for the simulation
words = file_list[start_words:(nr_words + start_words)]
words = [list(word) for word in words]  # Convert strings to arrays of characters
[word.insert(0, '-') for word in words]  # Insert '-' at the start
[word.insert(len(word), '-') for word in words]  # Insert '-' at the end
# print(words)


# SIMULATOR FUNCTIONS

def write(index, new, tp):  # Function that writes on the tape
    tp[index] = new
    return tp


def move_head(direction, pos):  # Function that moves the head
    if direction == 'D':
        pos += 1
    else:
        pos -= 1
    return pos


def update_status(new, curr):  # Function that updates the status
    curr = new
    return curr


def array_to_string(arr):  # Convert array to string
    temp = ""
    for char in arr:
        temp += char
    return temp


# EXECUTION
# Loop the simulation through all the words

itr = 1  # Iteration counter
for word in words:

    tape = word[:]  # Copy word onto tape (Prevents passing it by reference)

    # While not in the accepting state
    while q != qa:

        # Create substring of current state (q) + current symbol (head position on tape)
        input_state_symbol = str(q) + str(tape[head_position])
        # print(input_state_symbol)

        # Match the input substring to the list of available instructions, if none is found, reject
        ts_match = [ts.find(input_state_symbol, 0, 2) for ts in ts_matrix]

        try:
            ts_index = ts_match.index(0)
        except ValueError:
            break

        # Save transition found
        transition = ts_matrix[ts_index]
        # print(transition)

        # Write on tape
        tape = write(head_position, transition[2], tape)

        # Move head
        head_position = move_head(transition[3], head_position)

        # Update status
        q = update_status(transition[4], q)

    # Check in the acceptance state was reached
    if q == qa:
        print(f"{itr}: {(array_to_string(word[1:len(word)-1]))} OK")
    else:
        print(f"{itr}: {(array_to_string(word[1:len(word)-1]))} not OK")

    # Reset variables
    q = 1
    head_position = 1

    # Increment counter
    itr += 1
