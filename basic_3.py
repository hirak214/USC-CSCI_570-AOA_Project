import sys, time
import psutil

GAP_COST = 30
ALPHA = {
    ('A', 'A'): 0,   ('A', 'C'): 110, ('A', 'G'): 48,  ('A', 'T'): 94,
    ('C', 'A'): 110, ('C', 'C'): 0,   ('C', 'G'): 118, ('C', 'T'): 48,
    ('G', 'A'): 48,  ('G', 'C'): 118, ('G', 'G'): 0,   ('G', 'T'): 110,
    ('T', 'A'): 94,  ('T', 'C'): 48,  ('T', 'G'): 110, ('T', 'T'): 0
}

def generate_str(base_str, indices):
    result_s = base_str
    for idx in indices:
        idx = idx + 1
        to_insert = result_s
        result_s = result_s[:idx] + to_insert + result_s[idx:]
    return result_s


def basic_alignment(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1):
        dp[i][0] = i * GAP_COST
    for j in range(n+1):
        dp[0][j] = j * GAP_COST
    for i in range(1, m+1):
        for j in range(1, n+1):
            dp[i][j] = min(
                dp[i-1][j] + GAP_COST,
                dp[i][j-1] + GAP_COST,
                dp[i-1][j-1] + ALPHA[(s1[i-1], s2[j-1])]
            )
    # Backtrack
    aligned1, aligned2 = [], []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + ALPHA[(s1[i-1], s2[j-1])]:
            aligned1.append(s1[i-1])
            aligned2.append(s2[j-1])
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + GAP_COST:
            aligned1.append(s1[i-1])
            aligned2.append('_')
            i -= 1
        else:
            aligned1.append('_')
            aligned2.append(s2[j-1])
            j -= 1
    aligned1.reverse()
    aligned2.reverse()
    return dp[m][n], ''.join(aligned1), ''.join(aligned2)

def get_memory_usuage():
    return psutil.Process().memory_info().rss // 1024

def time_wrapper(func, *args):
    start = time.time()
    result = func(*args)
    return result, (time.time() - start) * 1000

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 basic_3.py input.txt output.txt")
        sys.exit(1)
    input_path, output_path = sys.argv[1], sys.argv[2]

    with open(input_path, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        base1 = lines[0]
        idx1 = []
        j = 1
        while lines[j].isdigit():
            idx1.append(int(lines[j]))
            j += 1

        base2 = lines[j]
        idx2 = []
        k = j + 1
        while k < len(lines) and lines[k].isdigit():
            idx2.append(int(lines[k]))
            k += 1
        idx1 = [int(x) for x in idx1]
        idx2 = [int(x) for x in idx2]


    s1 = generate_str(base1, idx1)
    s2 = generate_str(base2, idx2)

    before_memory = get_memory_usuage()
    (cost, a1, a2), runtime = time_wrapper(basic_alignment, s1, s2)
    after_memory = get_memory_usuage()

    with open(output_path, 'w') as out:
        out.write(f"{cost}\n{a1}\n{a2}\n{runtime:.6f}\n{after_memory - before_memory}\n")

if __name__ == '__main__':
    main()