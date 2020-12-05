#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
program = []
try:
  with open(sys.argv[1]) as my_file:
    for line in my_file:
      comment_split = line.split('#')
      maybe_binary_number = comment_split[0]
      try:
        x = int(maybe_binary_number, 2)
        program.append(x)
      except:
        continue

except FileNotFoundError:
  print("file not found")


cpu.load(program)
cpu.run()