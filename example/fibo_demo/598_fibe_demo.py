'''
This is a demo for generating nth Fibonacci number.

Read README.md present in this folder before proceeding

'''
import sys

sys.setrecursionlimit(1 << 30)

def fibo(num):
    if num == 1 or num == 0:
        return num
    return fibo(num - 1) + fibo(num - 2)


store_file = "cs598_fibo_demo_internal_file.txt"

with open(store_file, 'w') as __w_file:
    for i in range(len(sys.argv) - 1):
        __w_file.write(sys.argv[i + 1] + "\n")

with open(store_file, 'r') as __r_file:
    for __line in __r_file:
        print(fibo(int(__line)))
