import psutil
import time


def sequence_alignment(seq1, seq2, gap_penalty, alpha):
    # Initialize the DP matrix
    dp = [[0] * (len(seq2) + 1) for _ in range(len(seq1) + 1)]

    # Initialize the first row and column with gap penalties
    for i in range(1, len(seq1) + 1):
        dp[i][0] = dp[i - 1][0] + gap_penalty
    for j in range(1, len(seq2) + 1):
        dp[0][j] = dp[0][j - 1] + gap_penalty

    # Fill in the DP matrix
    for i in range(1, len(seq1) + 1):
        for j in range(1, len(seq2) + 1):
            match = dp[i - 1][j - 1] + alpha[seq1[i - 1] + seq2[j - 1]]
            delete = dp[i - 1][j] + gap_penalty
            insert = dp[i][j - 1] + gap_penalty
            dp[i][j] = min(match, delete, insert)

    # Backtrack to find the alignment
    aligned_seq1, aligned_seq2 = '', ''
    i, j = len(seq1), len(seq2)
    while i > 0 or j > 0:
        if i > 0 and dp[i][j] == dp[i - 1][j] + gap_penalty:
            aligned_seq1 = seq1[i - 1] + aligned_seq1
            aligned_seq2 = '-' + aligned_seq2
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + gap_penalty:
            aligned_seq1 = '-' + aligned_seq1
            aligned_seq2 = seq2[j - 1] + aligned_seq2
            j -= 1
        else:
            aligned_seq1 = seq1[i - 1] + aligned_seq1
            aligned_seq2 = seq2[j - 1] + aligned_seq2
            i -= 1
            j -= 1

    return aligned_seq1, aligned_seq2, dp[len(seq1)][len(seq2)]


def insert_string_at_indices(base_string, indices):
    result = base_string
    for idx in indices:
        result = result[:idx+1] + result + result[idx+1:]
    return result


def process_strings(s0, t0, list1, list2):
    s_result = insert_string_at_indices(s0, list1)
    t_result = insert_string_at_indices(t0, list2)
    return s_result, t_result

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
# s0, t0, list1, list2 = read_strings_and_indices('SampleTestCases/input1.txt')
# s0, t0, list1, list2 = read_strings_and_indices('SampleTestCases/input2.txt')
# s0, t0, list1, list2 = read_strings_and_indices('SampleTestCases/input3.txt')
# s0, t0, list1, list2 = read_strings_and_indices('SampleTestCases/input4.txt')
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
    aligned_seq1, aligned_seq2, alignment_cost = sequence_alignment(seq1, seq2, gap_penalty, alpha)
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000  # in milliseconds
    return time_taken

# Perform alignment and measure memory and time
aligned_seq1, aligned_seq2, alignment_cost = sequence_alignment(seq1, seq2, gap_penalty, alpha)
print("Alignment Cost:", alignment_cost)
print("Aligned Sequence 1:", aligned_seq1)
print("Aligned Sequence 2:", aligned_seq2)

memory_used = process_memory()
execution_time = time_wrapper()

print("Execution Time:", execution_time, "milliseconds")
print("Memory Used:", memory_used, "KB")





