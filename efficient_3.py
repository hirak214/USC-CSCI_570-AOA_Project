import sys, time
import psutil

GAP_COST = 30
mismatched_cost = {
    ('A', 'A'): 0,   ('A', 'C'): 110, ('A', 'G'): 48,  ('A', 'T'): 94,
    ('C', 'A'): 110, ('C', 'C'): 0,   ('C', 'G'): 118, ('C', 'T'): 48,
    ('G', 'A'): 48,  ('G', 'C'): 118, ('G', 'G'): 0,   ('G', 'T'): 110,
    ('T', 'A'): 94,  ('T', 'C'): 48,  ('T', 'G'): 110, ('T', 'T'): 0
}

def generate_str(base_str, indices):
    result_s= base_str
    for idx in indices:
        result_s= result_s[:idx+1] + result_s+ result_s[idx+1:]
    return result_s

def get_forward_dp(x_part, y_part):
    m = len(x_part)
    n = len(y_part)
    prev_row = [GAP_COST * j for j in range(n+1)]
    for i in range(1, m+1):
        current_row = [0] * (n+1)
        current_row[0] = prev_row[0] + GAP_COST
        for j in range(1, n+1):
            match = prev_row[j-1] + mismatched_cost[(x_part[i-1], y_part[j-1])]
            delete = prev_row[j] + GAP_COST
            insert = current_row[j-1] + GAP_COST
            current_row[j] = min(match, delete, insert)
        prev_row = current_row
    return prev_row

def align_single(x, y):
    if len(x) == 1:
        a = x[0]
        n = len(y)
        prev_row = [j * GAP_COST for j in range(n+1)]
        curr_row = [prev_row[0] + GAP_COST]
        for j in range(1, n+1):
            curr_j = min(
                prev_row[j-1] + mismatched_cost[(a, y[j-1])],
                prev_row[j] + GAP_COST,
                curr_row[j-1] + GAP_COST
            )
            curr_row.append(curr_j)
        curr_row = curr_row[:n+1]
        cost = curr_row[-1]
        aligned1, aligned2 = [], []
        i, j = 1, n
        current_row = curr_row
        while i > 0 or j > 0:
            if i > 0 and j > 0 and current_row[j] == prev_row[j-1] + mismatched_cost[(a, y[j-1])]:
                aligned1.append(a)
                aligned2.append(y[j-1])
                i -= 1
                j -= 1
            elif i > 0 and current_row[j] == prev_row[j] + GAP_COST:
                aligned1.append(a)
                aligned2.append('_')
                i -= 1
            else:
                aligned1.append('_')
                aligned2.append(y[j-1])
                j -= 1
            if i == 0:
                while j > 0:
                    aligned1.append('_')
                    aligned2.append(y[j-1])
                    j -= 1
            if j == 0 and i > 0:
                while i > 0:
                    aligned1.append(a)
                    aligned2.append('_')
                    i -= 1
        aligned1.reverse()
        aligned2.reverse()
        return (cost, ''.join(aligned1), ''.join(aligned2))
    else:
        cost, aligned2, aligned1 = align_single(y, x)
        return (cost, aligned1, aligned2)

def memory_efficient_alignment(x, y):
    if len(x) == 0:
        return (GAP_COST * len(y), '_' * len(y), y)
    if len(y) == 0:
        return (GAP_COST * len(x), x, '_' * len(x))
    if len(x) == 1 or len(y) == 1:
        return align_single(x, y)
    mid = len(x) // 2
    forward = get_forward_dp(x[:mid], y)
    x_rev = x[mid:][::-1]
    y_rev = y[::-1]
    backward = get_forward_dp(x_rev, y_rev)
    min_cost = float('inf')
    split_k = 0
    n = len(y)
    for k in range(n + 1):
        total_curr_cost = forward[k] + backward[n - k]
        if total_curr_cost < min_cost:
            min_cost = total_curr_cost
            split_k = k
    (cost1, a1_left, a2_left) = memory_efficient_alignment(x[:mid], y[:split_k])
    (cost2, a1_right, a2_right) = memory_efficient_alignment(x[mid:], y[split_k:])
    return (cost1 + cost2, a1_left + a1_right, a2_left + a2_right)

def get_memory_usuage():
    return int(psutil.Process().memory_info().rss / 1024)

def time_wrapper(func, *args):
    start = time.time()
    result = func(*args)
    return result, (time.time() - start) * 1000

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 basic_3.py input.txt output.txt")
        sys.exit(1)
    input_path= sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        base1 = lines[0]
        idx1 = []
        j = 1
        while j < len(lines) and lines[j].isdigit():
            idx1.append(int(lines[j]))
            j += 1

        base2 = lines[j]
        idx2 = []
        k = j + 1
        while k < len(lines) and lines[k].isdigit():
            idx2.append(int(lines[k]))
            k += 1

    s1 = generate_str(base1, idx1)
    s2 = generate_str(base2, idx2)

    before_memory = get_memory_usuage()
    (cost, a1, a2), runtime = time_wrapper(memory_efficient_alignment, s1, s2)
    after_memory = get_memory_usuage()

    with open(output_path, 'w') as out:
        out.write(f"{cost}\n{a1}\n{a2}\n{runtime:.6f}\n{after_memory - before_memory}\n")

if __name__ == '__main__':
    main()