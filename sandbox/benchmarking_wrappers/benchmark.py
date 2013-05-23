import time

import sum_of_squares_ctypes
import sum_of_squares_cython


def sum_of_squares_py(N):
    sum = 0
    for i in range(1, N+1):
        sum += i*i
    return sum


funcs = [sum_of_squares_ctypes.sum_of_squares_ctypes,
         sum_of_squares_cython.sum_of_squares_cython_compile,
         sum_of_squares_cython.sum_of_squares_cython_wrap,
         sum_of_squares_py,
         ]

input = 100

f_vals = [f(100) for f in funcs]
print("Testing")
if filter(lambda v: v != f_vals[0], f_vals):
    print("  Not all function evaluations the same\n", f_vals)
else:
    print("  test pass.")

print "Benchmarking:"
for f in funcs:
    times = []
    for repeats in range(10):
        t0 = time.time()
        for i in range(1000):
            f(100)
        t1 = time.time()
        times.append(t1 - t0)
    print(" %30s: %f ms" % (f.__name__, min(times) * 1000))
