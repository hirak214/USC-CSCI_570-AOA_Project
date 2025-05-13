import sys
import time
import psutil

delta = 30
ALPHA = {
    ('A', 'A'): 0,   ('A', 'C'): 110, ('A', 'G'): 48,  ('A', 'T'): 94,
    ('C', 'A'): 110, ('C', 'C'): 0,   ('C', 'G'): 118, ('C', 'T'): 48,
    ('G', 'A'): 48,  ('G', 'C'): 118, ('G', 'G'): 0,   ('G', 'T'): 110,
    ('T', 'A'): 94,  ('T', 'C'): 48,  ('T', 'G'): 110, ('T', 'T'): 0
}

def generate_string(base, indices):
    s = base
    for idx in indices:
        s = s[:idx+1] + s + s[idx+1:]
    return s

def compute_forward_dp(x_part, y_part):
    m = len(x_part)
    n = len(y_part)
    prev_row = [delta * j for j in range(n+1)]
    for i in range(1, m+1):
        curr_row = [0] * (n+1)
        curr_row[0] = prev_row[0] + delta
        for j in range(1, n+1):
            match = prev_row[j-1] + ALPHA[(x_part[i-1], y_part[j-1])]
            delete = prev_row[j] + delta
            insert = curr_row[j-1] + delta
            curr_row[j] = min(match, delete, insert)
        prev_row = curr_row
    return prev_row

def align_single(x, y):
    if len(x) == 1:
        a = x[0]
        n = len(y)
        prev_row = [j * delta for j in range(n+1)]
        curr_row = [prev_row[0] + delta]
        for j in range(1, n+1):
            curr_j = min(
                prev_row[j-1] + ALPHA[(a, y[j-1])],
                prev_row[j] + delta,
                curr_row[j-1] + delta
            )
            curr_row.append(curr_j)
        curr_row = curr_row[:n+1]
        cost = curr_row[-1]
        a1, a2 = [], []
        i, j = 1, n
        current_row = curr_row
        while i > 0 or j > 0:
            if i > 0 and j > 0 and current_row[j] == prev_row[j-1] + ALPHA[(a, y[j-1])]:
                a1.append(a)
                a2.append(y[j-1])
                i -= 1
                j -= 1
            elif i > 0 and current_row[j] == prev_row[j] + delta:
                a1.append(a)
                a2.append('_')
                i -= 1
            else:
                a1.append('_')
                a2.append(y[j-1])
                j -= 1
            if i == 0:
                while j > 0:
                    a1.append('_')
                    a2.append(y[j-1])
                    j -= 1
            if j == 0 and i > 0:
                while i > 0:
                    a1.append(a)
                    a2.append('_')
                    i -= 1
        a1.reverse()
        a2.reverse()
        return (cost, ''.join(a1), ''.join(a2))
    else:
        cost, a2, a1 = align_single(y, x)
        return (cost, a1, a2)

def memory_efficient_alignment(x, y):
    if len(x) == 0:
        return (delta * len(y), '_' * len(y), y)
    if len(y) == 0:
        return (delta * len(x), x, '_' * len(x))
    if len(x) == 1 or len(y) == 1:
        return align_single(x, y)
    x_mid = len(x) // 2
    forward = compute_forward_dp(x[:x_mid], y)
    x_rev = x[x_mid:][::-1]
    y_rev = y[::-1]
    backward = compute_forward_dp(x_rev, y_rev)
    min_cost = float('inf')
    split_k = 0
    n = len(y)
    for k in range(n + 1):
        current_cost = forward[k] + backward[n - k]
        if current_cost < min_cost:
            min_cost = current_cost
            split_k = k
    (cost1, a1_left, a2_left) = memory_efficient_alignment(x[:x_mid], y[:split_k])
    (cost2, a1_right, a2_right) = memory_efficient_alignment(x[x_mid:], y[split_k:])
    return (cost1 + cost2, a1_left + a1_right, a2_left + a2_right)

def process_memory():
    return psutil.Process().memory_info().rss / 1024

def time_wrapper(func, *args):
    start = time.time()
    result = func(*args)
    return result, (time.time() - start) * 1000

def main():

    input_path, output_path = sys.argv[1], sys.argv[2]

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

    s1 = generate_string(base1, idx1)
    s2 = generate_string(base2, idx2)

    before_mem = process_memory()
    (cost, a1, a2), elapsed = time_wrapper(memory_efficient_alignment, s1, s2)
    after_mem = process_memory()

    with open(output_path, 'w') as out:
        out.write(f"{cost}\n{a1}\n{a2}\n{elapsed}\n{after_mem - before_mem}\n")

if __name__ == '__main__':
    main()