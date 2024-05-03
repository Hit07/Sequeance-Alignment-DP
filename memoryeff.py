import psutil
import time

# The sequence_alignment function calculates the alignment score between two sequences using dynamic programming.
def sequence_alignment(seq1, seq2, gap_penalty, alpha):
    # Initialize the DP matrix
    dp = [[0] * (len(seq2) + 1) for _ in range(2)]

    # Initialize the first row with gap penalties
    for j in range(1, len(seq2) + 1):
        dp[0][j] = dp[0][j - 1] + gap_penalty

    # Fill in the DP matrix
    for i in range(1, len(seq1) + 1):
        dp[i % 2][0] = dp[(i - 1) % 2][0] + gap_penalty
        for j in range(1, len(seq2) + 1):
            match = dp[(i - 1) % 2][j - 1] + alpha[seq1[i - 1] + seq2[j - 1]]
            delete = dp[(i - 1) % 2][j] + gap_penalty
            insert = dp[i % 2][j - 1] + gap_penalty
            dp[i % 2][j] = min(match, delete, insert)

    return dp[len(seq1) % 2][-1]  # Return only the alignment score


# The divide_and_conquer_alignment function is a memory-efficient version of the sequence_alignment function that uses a divide-and-conquer approach to reduce memory consumption.

def divide_and_conquer_alignment(seq1, seq2, alpha, gap_penalty, low_i=0, high_i=None, low_j=0, high_j=None):
    if high_i is None:
        high_i = len(seq1)
    if high_j is None:
        high_j = len(seq2)

    if high_i - low_i == 0:
        return [0] * (high_j - low_j + 1)

    if high_i - low_i == 1:
        return sequence_alignment(seq1[low_i:high_i], seq2[low_j:high_j], gap_penalty, alpha)

    mid_i = (low_i + high_i) // 2

    score_l = sequence_alignment(seq1[low_i:mid_i], seq2, gap_penalty, alpha)
    score_r = sequence_alignment(seq1[mid_i:high_i], seq2[::-1], gap_penalty, alpha)[::-1]

    max_score = float('-inf')
    for j in range(len(score_l)):
        score = score_l[j] + score_r[j]
        if score > max_score:
            max_score = score
            q = j

    score_up = divide_and_conquer_alignment(seq1[low_i:mid_i], seq2[:q], alpha, gap_penalty, 0, mid_i - low_i, 0, q)
    score_down = divide_and_conquer_alignment(seq1[mid_i:high_i], seq2[q:], alpha, gap_penalty, 0, high_i - mid_i, q, high_j - low_j)

    return score_up + score_down


# The insert_string_at_indices function inserts characters into a base string at specified indices.

def insert_string_at_indices(base_string, indices):
    result = base_string
    for idx in indices:
        result = result[:idx + 1] + result + result[idx + 1:]
    return result


# The process_strings function reads the input strings and indices from a file, processes the strings, and returns the modified strings.
def process_strings(s0, t0, list1, list2):
    s_result = insert_string_at_indices(s0, list1)
    t_result = insert_string_at_indices(t0, list2)
    return s_result, t_result


# The read_strings_and_indices function reads the input strings and indices from a file and returns the strings and indices as variables.
def read_strings_and_indices(file_path):
    with open(file_path, 'r') as file:
        # Read the first string (s0)
        s0 = next(file).strip()

        # Initialize variables for indices
        s_indices = []
        t_indices = []

        current_list = s_indices  # Start with s_indices
        for line in file:
            line = line.strip()
            if line.isdigit():  # Check if the line contains digits only
                current_list.append(int(line))
            else:
                if current_list is s_indices:
                    t0 = line  # Assign the second string (t0)
                    current_list = t_indices  # Switch to t_indices
                else:
                    break

    return s0, t0, s_indices, t_indices


# Read strings and indices from the input file
s0, t0, list1, list2 = read_strings_and_indices('SampleTestCases/input5.txt')

# Process the strings and print the results
seq1, seq2 = process_strings(s0, t0, list1, list2)
print("seq1:", seq1)
print("seq2:", seq2)

gap_penalty = 30
alpha = {'AA': 0, 'AC': 110, 'AG': 48, 'AT': 94, 'CA': 110, 'CC': 0, 'CG': 118,'CT': 48, 'GA': 48, 'GC': 118, 'GG': 0, 'GT':110, 'TA': 94, 'TC': 48, 'TG': 110, 'TT': 0}


# Calculate memory consumption
def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)  # in KB
    return memory_consumed


# Calculate time taken
def time_wrapper():
    start_time = time.time()
    alignment_cost = sequence_alignment(seq1, seq2, gap_penalty, alpha)
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000  # in milliseconds
    return time_taken

# Perform alignment and measure memory and time
alignment_cost = sequence_alignment(seq1, seq2, gap_penalty, alpha)
print("Alignment Cost:", alignment_cost)

memory_used = process_memory()
execution_time = time_wrapper()

print("Execution Time:", execution_time, "milliseconds")
print("Memory Used:", memory_used, "KB")
