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
        to_insert = s
        s = s[:idx] + to_insert + s[idx:]
    return s


def basic_alignment(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1):
        dp[i][0] = i * delta
    for j in range(n+1):
        dp[0][j] = j * delta
    for i in range(1, m+1):
        for j in range(1, n+1):
            dp[i][j] = min(
                dp[i-1][j] + delta,
                dp[i][j-1] + delta,
                dp[i-1][j-1] + ALPHA[(s1[i-1], s2[j-1])]
            )
    # Backtrack
    a1, a2 = [], []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + ALPHA[(s1[i-1], s2[j-1])]:
            a1.append(s1[i-1])
            a2.append(s2[j-1])
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + delta:
            a1.append(s1[i-1])
            a2.append('-')
            i -= 1
        else:
            a1.append('-')
            a2.append(s2[j-1])
            j -= 1
    a1.reverse()
    a2.reverse()
    return dp[m][n], ''.join(a1), ''.join(a2)

def process_memory():
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

    # with open(input_path, 'r') as f:
    #     base1 = f.readline().strip()
    #     j = int(f.readline().strip())
    #     idx1 = [int(f.readline().strip()) for _ in range(j)]
    #     base2 = f.readline().strip()
    #     k = int(f.readline().strip())
    #     idx2 = [int(f.readline().strip()) for _ in range(k)]
    base1 = "ACTG"
    idx1 = [3, 6, 1, 1]
    base2 = "TACG"
    idx2 = [1, 2, 9, 2]

    s1 = generate_string(base1, idx1)
    s2 = generate_string(base2, idx2)

    before_mem = process_memory()
    (cost, a1, a2), elapsed = time_wrapper(basic_alignment, s1, s2)
    after_mem = process_memory()

    with open(output_path, 'w') as out:
        out.write(f"{cost}\n{a1}\n{a2}\n{elapsed:.6f}\n{after_mem - before_mem}\n")

if __name__ == '__main__':
    main()