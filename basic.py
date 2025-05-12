import sys
import time
from resource import *
import psutil

delta = 30
ALPHA = {
    ('A', 'A'): 0,   ('A', 'C'): 110, ('A', 'G'): 48,  ('A', 'T'): 94,
    ('C', 'A'): 110, ('C', 'C'): 0,   ('C', 'G'): 118, ('C', 'T'): 48,
    ('G', 'A'): 48,  ('G', 'C'): 118, ('G', 'G'): 0,   ('G', 'T'): 110,
    ('T', 'A'): 94,  ('T', 'C'): 48,  ('T', 'G'): 110, ('T', 'T'): 0
}


def process_memory():
    """Return current RSS memory (KB)."""
    # Get the current process
    process = psutil.Process()
    # Get the memory info
    mem_info = process.memory_info()
    # Return the RSS memory in KB
    memory_consumed = int(mem_info.rss / 1024)
    return memory_consumed

def time_wrapper(func, *args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    elapsed = (time.time() - start) * 1000.0
    return result, elapsed
# =============================================================================
# Module stubs -- we'll implement these one by one
# =============================================================================

def generate_string(base, indices):
    s = base
    # print("Base string:", base, "Indices:", indices, "s string:", s)
    for i in indices:
        # print("i:", i)
        pos = i
        # print(f"s[:pos]:", s[:pos], "s[pos:]:", s[pos:])
        s = s[:pos] + s + s[pos:]
        # print("s:", s)
        # print("****************")
    return s


def basic_alignment(s1, s2):
    m, n = len(s1), len(s2)
    # Initialize the dp matrix
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        dp[i][0] = i * delta
    for j in range(1, n + 1):
        dp[0][j] = j * delta
    # Fill the dp matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cosst_sub = ALPHA[(s1[i - 1], s2[j - 1])]
            dp[i][j] = min(
                dp[i - 1][j] + delta,  # Deletion
                dp[i][j - 1] + delta,  # Insertion
                dp[i - 1][j - 1] + cosst_sub  # Substitution
            )
    # Backtrack to find the alignment
    a1, a2 = [], []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + ALPHA[(s1[i - 1], s2[j - 1])]:
            a1.append(s1[i - 1]); a2.append(s2[j - 1]); i -= 1; j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + delta:
            a1.append(s1[i - 1]); a2.append('-'); i -= 1
        else:
            a1.append('-'); a2.append(s2[j - 1]); j -= 1
    a1.reverse(); a2.reverse()
    return dp[m][n], ''.join(a1), ''.join(a2)



def main():
    """Entry point: parse args, read input, run alignment, output results."""
    if len(sys.argv) != 3:
        print("Usage: python3 basic.py <input_file> <output_file>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # 1) Read and parse the input file
    with open(input_path) as f:
        base1 = f.readline().strip()
        print("Base string 1:", base1)
        j = int(f.readline().strip()) 
        idk1 = [int(f.readline().strip()) for _ in range(j)]
        print("Indices 1:", idk1)
        base2 = f.readline().strip()
        print("Base string 2:", base2)
        k = int(f.readline().strip())
        idk2 = [int(f.readline().strip()) for _ in range(k)]
        print("Indices 2:", idk2)
    

    # 2) Generate the full strings s1 and s2
    s1 = generate_string(base1, idk1)
    print("Generated string 1:", s1)
    s2 = generate_string(base2, idk2)
    print("Generated string 2:", s2)


    # 3) Profile memory before and after alignment
    memory_before = process_memory()
    print("Memory before alignment:", memory_before, "KB")



    # 4) Time the alignment step
    (cost, a1, a2), elapsed = time_wrapper(basic_alignment, s1, s2)
    after_memory = process_memory()
    used_memory = after_memory - memory_before
    print("Memory after alignment:", after_memory, "KB")



    # 5) Write the output file
    with open(output_path, 'w') as f:
        f.write(f"{cost}\n")
        f.write(f"{a1}\n")
        f.write(f"{a2}\n")
        f.write(f"{elapsed:.6f}\n")
        f.write(f"{used_memory}\n")


if __name__ == '__main__':
    main()
