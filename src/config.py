#################################
# seed file configuration       #
#################################

# original length of the strings to be written in seed
string_len = 10

# seed workflow, composed of a list of item [#writers, #readers, #threads],
# each item refers to a concurrent block in seed file
seed_flow = [
    [1, 1, 2],
    [1, 1, 2]
]


#################################
# fuzzing configuration         #
#################################

# range of replacing string length
string_len_new_l = 10000
string_len_new_h = 20000

# range of mutating thread number
thread_num_new_l = 1
thread_num_new_h = 10

# operations to be performed at a single fuzzing stage
# [#replaces, #threading, #swap, #writer, #checker]
fuzz_ops = [0, 1, 0, 0, 0]

# number of iterations
# A iteration refers to the process of generating a new version of file that has a higher
# inconsistency rate than the previous version
num_itr = 10


#################################
# checking configuration        #
#################################

# number of times to run while calculating the inconsistency rate of a file
# the inconsistency rate will be calculated by taking the average of these executions
check_itr = 50
