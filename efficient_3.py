import os
import sys
import psutil
import time


DELTA = 30
ALPHA = {'AA': 0, 'AC': 110, 'AG': 48, 'AT': 94, 'CA': 110, 'CC': 0, 'CG': 118, 'CT': 48, 'GA': 48, 'GC': 118,
         'GG': 0, 'GT': 110, 'TA': 94, 'TC': 48, 'TG': 110, 'TT': 0}


def sequence_alignment(seq1, seq2, DELTA, ALPHA):
    # Initialize the DP matrix and fill in the first row and column with gap penalties
    dp = [[0] * (len(seq2) + 1) for _ in range(len(seq1) + 1)]
    for i in range(1, len(seq1) + 1):
        dp[i][0] = dp[i - 1][0] + DELTA
    for j in range(1, len(seq2) + 1):
        dp[0][j] = dp[0][j - 1] + DELTA
    # Recurrence relation
    for i in range(1, len(seq1) + 1):
        for j in range(1, len(seq2) + 1):
            match = dp[i - 1][j - 1] + ALPHA[seq1[i - 1] + seq2[j - 1]]
            delete = dp[i - 1][j] + DELTA
            insert = dp[i][j - 1] + DELTA
            dp[i][j] = min(match, delete, insert)

    # Backtracking
    aligned_seq1 = ''
    aligned_seq2 = ''
    i = len(seq1)
    j = len(seq2)
    while i > 0 or j > 0:
        if i > 0 and dp[i][j] == dp[i - 1][j] + DELTA:
            aligned_seq1 = seq1[i - 1] + aligned_seq1
            aligned_seq2 = '-' + aligned_seq2
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + DELTA:
            aligned_seq1 = '-' + aligned_seq1
            aligned_seq2 = seq2[j - 1] + aligned_seq2
            j -= 1
        else:
            aligned_seq1 = seq1[i - 1] + aligned_seq1
            aligned_seq2 = seq2[j - 1] + aligned_seq2
            i -= 1
            j -= 1

    return aligned_seq1, aligned_seq2, dp[len(seq1)][len(seq2)]

def space_efficient_alignment( A, B, flag, DELTA, ALPHA):
    dp = []
    for i in range(2):
        dp.append([0] * (len(B) + 1))
    for i in range(len(B) + 1):
        dp[0][i] = DELTA * i

    if flag:
        for i in range(1, len(A) + 1):
            dp[1][0] = i * DELTA
            for j in range(1, len(B) + 1):
                dp[1][j] = min(dp[0][j - 1] +ALPHA[A[len(A) - i] + B[len(B) - j]],
                                dp[0][j] + DELTA,
                                dp[1][j - 1] + DELTA)
            for j in range(len(B) + 1):
                dp[0][j] = dp[1][j]
    else:
        for i in range(1, len(A) + 1):
            dp[1][0] = i * DELTA
            for j in range(1, len(B) + 1):
                dp[1][j] = min(dp[0][j - 1] +ALPHA[A[i - 1] + B[j - 1]],
                                dp[0][j] + DELTA,
                                dp[1][j - 1] + DELTA)
            for j in range(len(B)+1):
                dp[0][j] = dp[1][j]
    return dp[1]


def Divide_Conquer(seq1, seq2, DELTA , ALPHA):
    m = len(seq1)
    n = len(seq2)
    if m < 2 or n < 2:
        return sequence_alignment(seq1, seq2,DELTA, ALPHA)
    else:
        part_1 = space_efficient_alignment(seq1[:m // 2], seq2, 0,DELTA, ALPHA)
        part_2 = space_efficient_alignment(seq1[m // 2:], seq2, 1,DELTA, ALPHA)
        arr = [part_1[j] + part_2[n - j] for j in range(n + 1)]
        q = arr.index(min(arr))
        left = Divide_Conquer(seq1[:len(seq1) // 2], seq2[:q], DELTA, ALPHA)
        right = Divide_Conquer(seq1[len(seq1) // 2:], seq2[q:], DELTA, ALPHA)
        res = [left[r] + right[r] for r in range(3)]
    return res[0], res[1], res[2]



def insert_into_indices(base_string, indices):
    result = base_string
    for i in indices:
        result = result[:i+1] + result + result[i+1:]
    return result


def transform_string(s0, t0, list1, list2):
    s_result = insert_into_indices(s0, list1)
    t_result = insert_into_indices(t0, list2)
    return s_result, t_result


def get_string(file_path):
    with open(file_path, 'r') as file:
        s0 = next(file).strip()
        s_indices , t_indices = [], []
        current_list = s_indices
        for line in file:
            line = line.strip()
            if line.isdigit():
                current_list.append(int(line))
            else:
                if current_list is s_indices:
                    t0 = line
                    current_list = t_indices
                else:
                    break

    return s0, t0, s_indices, t_indices

def time_wrapper(seq1, seq2, DELTA, ALPHA):
    start_time = time.time()
    aligned_seq1, aligned_seq2, alignment_cost = Divide_Conquer(seq1, seq2, DELTA, ALPHA)
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000
    return aligned_seq1, aligned_seq2, alignment_cost, time_taken

def get_aligned_sequeance(input_file, output_file):
    s0, t0, list1, list2 = get_string(input_file)
    seq1, seq2 = transform_string(s0, t0, list1, list2)
    aligned_seq1, aligned_seq2, alignment_cost,time_taken = time_wrapper(seq1, seq2, DELTA, ALPHA)
    '''File writing'''
    memory_used = psutil.Process(os.getpid()).memory_info().rss / 1024
    with open(output_file, 'w') as f:
        f.write(f"{alignment_cost}\n{aligned_seq1}\n{aligned_seq2}\n{time_taken}\n{memory_used}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 script.py <input_file> <output_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    get_aligned_sequeance(input_file, output_file)



