import sys
import time
import psutil

# Constants
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
        idx = idx + 1
        to_insert = s
        s = s[:idx] + to_insert + s[idx:]
    return s


def space_efficient_cost(X, Y):
    """Compute the last row of the DP alignment cost table for X vs Y."""
    m, n = len(X), len(Y)
    prev = [j * delta for j in range(n + 1)]
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        curr[0] = i * delta
        for j in range(1, n + 1):
            sub_cost = ALPHA[(X[i - 1], Y[j - 1])]
            curr[j] = min(
                prev[j] + delta,
                curr[j - 1] + delta,
                prev[j - 1] + sub_cost
            )
        prev, curr = curr, prev
    return prev


def hirschberg(X, Y):
    if len(X) == 0:
        return ('_' * len(Y), Y)
    if len(Y) == 0:
        return (X, '_' * len(X))
    if len(X) == 1 or len(Y) == 1:
        _, a1, a2 = basic_alignment(X, Y)
        return a1, a2


    xlen = len(X)
    xmid = xlen // 2

    L1 = space_efficient_cost(X[:xmid], Y)
    L2 = space_efficient_cost(X[xmid:][::-1], Y[::-1])

    partition = max(range(len(Y) + 1), key=lambda j: L1[j] + L2[len(Y) - j])

    A1, B1 = hirschberg(X[:xmid], Y[:partition])
    A2, B2 = hirschberg(X[xmid:], Y[partition:])
    return (A1 + A2, B1 + B2)


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
    a1, a2 = [], []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + ALPHA[(s1[i-1], s2[j-1])]:
            a1.append(s1[i-1]); a2.append(s2[j-1]); i -= 1; j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + delta:
            a1.append(s1[i-1]); a2.append('_'); i -= 1
        else:
            a1.append('_'); a2.append(s2[j-1]); j -= 1
    a1.reverse(); a2.reverse()
    return dp[m][n], ''.join(a1), ''.join(a2)


def process_memory():
    return int(psutil.Process().memory_info().rss / 1024)

def time_wrapper(func, *args):
    start = time.time()
    result = func(*args)
    return result, (time.time() - start) * 1000

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 efficient_3.py input.txt output.txt")
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

    s1 = generate_string(base1, idx1)
    s2 = generate_string(base2, idx2)

    before_mem = process_memory()
    (a1, a2), elapsed = time_wrapper(hirschberg, s1, s2)
    after_mem = process_memory()

    cost = sum(
        delta if a1[i] == '_' or a2[i] == '_' else ALPHA[(a1[i], a2[i])]
        for i in range(len(a1))
    )

    with open(output_path, 'w') as out:
        out.write(f"{cost}\n{a1}\n{a2}\n{elapsed:.6f}\n{after_mem - before_mem}\n")

if __name__ == '__main__':
    main()
