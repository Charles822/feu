#!/usr/bin/env python3

# Exercise 5. Trouver le plus grand carré/ Find the biggest square


import sys
import random


# Check if the correct number of arguments is given
if len(sys.argv) != 4:
    print("params needed: x y density")
    sys.exit()

# Assign arguments to variables after converting them to integers
x = int(sys.argv[1])
y = int(sys.argv[2])
density = int(sys.argv[3])

print(f"{y}.xo")
for i in range(y):
    for j in range(x):
        # Print 'x' or '.' based on the density condition
        print('x' if random.randint(0, y) * 2 < density else '.', end='')
    print()  # Newline after each row


