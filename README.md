# USC - CSCI570 - Spring25 Project
## Sequence Alignment Using Dynamic Programming

This project implements sequence alignment algorithms for DNA/protein sequences using dynamic programming. It includes both a **basic O(mn) space** implementation and a **memory-efficient O(m+n) space** implementation using Hirschberg's algorithm.

## Overview

Sequence alignment is a fundamental problem in bioinformatics used to identify regions of similarity between biological sequences (DNA, RNA, or proteins). This project implements:

1. **Basic Sequence Alignment** - Standard Needleman-Wunsch algorithm with full DP table
2. **Memory-Efficient Alignment** - Hirschberg's divide-and-conquer algorithm with reduced space complexity

Both implementations:
- Use a gap penalty of 30
- Use a mismatch penalty matrix (ALPHA) for DNA bases (A, C, G, T)
- Generate strings from base strings and index positions
- Measure time complexity and memory usage

## Algorithm Details

### String Generation
Input files contain:
- A base string (e.g., "ACTG")
- Indices where the string should be doubled (inserted after position)
- This generates exponentially growing test strings

### Alignment Scoring
- **Gap Penalty**: 30
- **Mismatch Penalties**: Defined in ALPHA matrix
  - Match (e.g., A-A): 0
  - Mismatches: varying costs (48-118)

### Output Format
Each output file contains:
1. Alignment cost (total penalty)
2. First aligned sequence (with gaps as '_')
3. Second aligned sequence (with gaps as '_')
4. Time taken (milliseconds)
5. Memory used (KB)

## Installation

### Python Version
Install required libraries:

```bash
pip install psutil
```

### C++ Version
Compile the C++ implementation:

```bash
g++ basic.cpp -o basic -std=c++17
```

## Usage

### Python - Basic Implementation
```bash
python3 basic_3.py <input_file> <output_file>
```

Example:
```bash
python3 basic_3.py SampleTestCases/input1.txt output.txt
```

### Python - Memory-Efficient Implementation
```bash
python3 efficient_3.py <input_file> <output_file>
```

Example:
```bash
python3 efficient_3.py SampleTestCases/input1.txt output.txt
```

### C++ - Basic Implementation
```bash
./basic <input_file> <output_file>
```

Example:
```bash
./basic datapoints/in1.txt datapoints/out1.txt
```

### Batch Processing (C++)
Run all test cases using the shell script:

```bash
bash basic.sh
```

This will process all input files in the `datapoints/` directory.

## Test Cases

The project includes two sets of test cases:

1. **SampleTestCases/** - 5 sample test cases with expected outputs
   - `input1.txt` through `input5.txt`
   - `output1.txt` through `output5.txt` (expected results)

2. **datapoints/** - 15 test cases for performance benchmarking
   - `in1.txt` through `in15.txt`
   - Progressive increase in string length for complexity analysis

## Input File Format

```
<base_string_1>
<index_1>
<index_2>
...
<base_string_2>
<index_1>
<index_2>
...
```

Example (`input1.txt`):
```
ACTG
3
6
1
1
TACG
1
2
9
2
```

## Project Structure

```
.
├── basic_3.py              # Python basic O(mn) implementation
├── efficient_3.py          # Python memory-efficient O(m+n) space implementation
├── basic.cpp               # C++ basic implementation
├── basic.sh                # Shell script to run all C++ test cases
├── SampleTestCases/        # Sample test cases with expected outputs
├── datapoints/             # Performance benchmarking test cases
└── README.md               # This file
```

## Performance Analysis

The implementations allow comparison between:
- **Time Complexity**: Both are O(mn)
- **Space Complexity**: 
  - Basic: O(mn) - stores full DP table
  - Efficient: O(m+n) - uses Hirschberg's algorithm (O(n) for DP rows + O(m) recursion depth)

Use the different test cases to analyze how time and memory scale with input size.

## Authors

- [@Hirak Desai](https://www.github.com/hirak214) - Masters in Computer Science (AI)
- [@Jaanaki Dave](https://github.com/JaanakiDave11) - Masters in Computer Science (AI)
- [@Suyash Roy](https://github.com/SuyashRoy) - Masters in Computer Science

