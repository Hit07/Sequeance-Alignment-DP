import sys
import psutil
import time

DELTA = 30
ALPHA = {'AA': 0, 'AC': 110, 'AG': 48, 'AT': 94, 'CA': 110, 'CC': 0, 'CG': 118, 'CT': 48,
         'GA': 48, 'GC': 118, 'GG': 0, 'GT': 110, 'TA': 94, 'TC': 48, 'TG': 110, 'TT': 0}


def sequence_alignment(seq1, seq2):
    # Initializing the OPT matrix and filling the first row and first column with gap penalties
    OPT = []
    for i in range(len(seq1) + 1):
        row = []
        for j in range(len(seq2) + 1):
            row.append(0)
        OPT.append(row)
    for i in range(1, len(seq1) + 1):
        OPT[i][0] = i * DELTA
    for j in range(1, len(seq2) + 1):
        OPT[0][j] = j * DELTA
    # Recurrence relation for sequence alignment
    for i in range(1, len(seq1) + 1):
        for j in range(1, len(seq2) + 1):
            OPT[i][j] = min(OPT[i - 1][j - 1] + ALPHA[seq1[i - 1] + seq2[j - 1]], OPT[i][j - 1] + DELTA,
                            OPT[i - 1][j] + DELTA)

    # finding the sequence using OPT matrix
    i = len(seq1)
    j = len(seq2)
    seq1_aligned = ''
    seq2_aligned = ''
    while i > 0 or j > 0:
        if i > 0 and OPT[i][j] == OPT[i - 1][j] + DELTA:
            seq1_aligned = seq1[i - 1] + seq1_aligned
            seq2_aligned = '_' + seq2_aligned
            i -= 1
        elif j > 0 and OPT[i][j] == OPT[i][j - 1] + DELTA:
            seq1_aligned = '_' + seq1_aligned
            seq2_aligned = seq2[j - 1] + seq2_aligned
            j -= 1
        else:
            seq1_aligned = seq1[i - 1] + seq1_aligned
            seq2_aligned = seq2[j - 1] + seq2_aligned
            i -= 1
            j -= 1

    return seq1_aligned, seq2_aligned, OPT[len(seq1)][len(seq2)]


def space_efficient_alignment(A, B, flag):
    x = len(A)
    y = len(B)
    OPT = []
    for i in range(2):
        OPT.append([0] * (y + 1))
    for i in range(y + 1):
        OPT[0][i] = i * DELTA

    if flag:
        for i in range(1, x + 1):
            OPT[1][0] = i * DELTA
            for j in range(1, y + 1):
                OPT[1][j] = min(OPT[0][j - 1] + ALPHA[A[x - i] + B[y - j]], OPT[0][j] + DELTA, OPT[1][j - 1] + DELTA)
            for j in range(y + 1):
                OPT[0][j] = OPT[1][j]
    else:
        for i in range(1, x + 1):
            OPT[1][0] = i * DELTA
            for j in range(1, y + 1):
                OPT[1][j] = min(OPT[0][j - 1] + ALPHA[A[i - 1] + B[j - 1]], OPT[0][j] + DELTA, OPT[1][j - 1] + DELTA)
            for j in range(y + 1):
                OPT[0][j] = OPT[1][j]
    return OPT[1]


def Divide_Conquer(seq1, seq2):
    if len(seq1) < 2 or len(seq2) < 2:
        return sequence_alignment(seq1, seq2)
    else:
        part_1 = space_efficient_alignment(seq1[:len(seq1) // 2], seq2, 0)
        part_2 = space_efficient_alignment(seq1[len(seq1) // 2:], seq2, 1)
        min_val = float('inf')
        split = 0
        for j in range(len(seq2) + 1):
            val = part_1[j] + part_2[len(seq2) - j]
            if val < min_val:
                min_val = val
                split = j
        left = Divide_Conquer(seq1[:len(seq1) // 2], seq2[:split])
        right = Divide_Conquer(seq1[len(seq1) // 2:], seq2[split:])
        res = []
        for i in range(3):
            res.append(left[i] + right[i])
    return res[0], res[1], res[2]


def insert_into_indices(base_string, indices):
    result = base_string
    for i in indices:
        result = result[:i + 1] + result + result[i + 1:]
    return result


def transform_string(s0, t0, list1, list2):
    s_result = insert_into_indices(s0, list1)
    t_result = insert_into_indices(t0, list2)
    return s_result, t_result


def get_string(file_path):
    with open(file_path, 'r') as file:
        s0 = next(file).strip()
        t0 = None
        s_indices = []
        t_indices = []
        is_reading_t = False
        for line in file:
            line = line.strip()
            if not line:
                continue
            elif line.isdigit():
                if is_reading_t:
                    t_indices.append(int(line))
                else:
                    s_indices.append(int(line))
            else:
                t0 = line
                is_reading_t = True

    return s0, t0, s_indices, t_indices


def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed


def time_wrapper(seq1, seq2):
    start_time = time.time()
    aligned_seq1, aligned_seq2, alignment_cost = Divide_Conquer(seq1, seq2)
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000
    return aligned_seq1, aligned_seq2, alignment_cost, time_taken


def get_aligned_sequeance(input_file, output_file):

    s0, t0, list1, list2 = get_string(input_file)
    seq1, seq2 = transform_string(s0, t0, list1, list2)
    aligned_seq1, aligned_seq2, alignment_cost, time_taken = time_wrapper(seq1, seq2)
    '''File writing'''
    with open(output_file, 'w') as f:
        f.write(f"{alignment_cost}\n{aligned_seq1}\n{aligned_seq2}\n{time_taken}\n{process_memory()}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    get_aligned_sequeance(input_file, output_file)
