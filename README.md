# DNA Sequence Alignment 

This repository contains implementations of two different algorithms for solving the DNA sequence alignment problem: a basic version using Dynamic Programming (DP) and an optimized version using DP combined with a Divide-and-Conquer strategy for improved efficiency.

## Project Description

This project involves implementing and comparing two solutions to the DNA sequence alignment problem. The basic solution uses a classic DP approach, while the memory-efficient solution enhances DP with a Divide-and-Conquer method to handle larger sequences more effectively.

## Problem Overview

Given two strings, \(X\) and \(Y\), where:
- \(X = x_1, x_2, \ldots, x_m\)
- \(Y = y_1, y_2, \ldots, y_n\)

We aim to find the optimal alignment between \(X\) and \(Y\) by minimizing the alignment cost, which includes gap penalties and mismatch costs. The alignment process involves matching symbols from the two strings, allowing for gaps to achieve the best possible similarity score.

### Gap Penalty and Mismatch Costs
- **Gap Penalty (δ)**: 30
- **Mismatch Costs (α)**:

|   | A   | C   | G   | T   |
|---|-----|-----|-----|-----|
| A | 0   | 110 | 48  | 94  |
| C | 110 | 0   | 118 | 48  |
| G | 48  | 118 | 0   | 110 |
| T | 94  | 48  | 110 | 0   |

## Input String Generation

Input strings are generated using a base string and a series of insertion steps, which iteratively double the length of the string. The process is as follows:
1. Start with a base string \(s_0\).
2. For each step, insert the current string into itself at a specified index, producing a new string.
3. Repeat for the given number of steps to generate the final string.

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/Hit07/Sequence-Alignment-DP.git
cd Sequence-Alignment-DP        
```
## Ensure you have the required dependencies installed:

```bash
pip install -r requirements.txt
```
## Execute the basic algorithm:

```bash
python basic.py input.txt output.txt
```

## Execute the memory-efficient algorithm:

```bash
python efficient.py input.txt output.txt
```

## Input and Output
Input: A text file containing the base strings and the steps for string generation.
Output: A text file containing the alignment cost, aligned strings, execution time, and memory usage.


## Results
The results include:

- Alignment Cost: The minimum cost of aligning the two strings.
- Aligned Strings: The two input strings with gaps inserted to show the optimal alignment.
- Execution Time: Time taken to compute the alignment.
- Memory Usage: Memory used during the computation.
- Additionally, plots are provided to compare CPU time and memory usage versus problem size for both algorithms.
