# This is the development copy of the main program.
# It should only be copied to the ../multicrack/ folder if STABLE AND FUNCTIONAL

from sys import exit
from tqdm import tqdm
import hashlib
import argparse
import time
import string
import itertools
import multiprocessing
import os

# Multiprocess
#   Each process takes

# Modes and Required Arguments
#   Dictionary attack [-D]
#       hash|hashfile word|dictionary 
#   Brute-force attack [-B]
#       hash|hashfile minchars maxchars
#   Rainbow attack [-R]
#       hash|hashfile rainbowtable
#   Generate rainbow table from dictionary [-Gd]
#       dictionary outfile
#   Generate rainbow table iteratively [-Gi]
#       minchars maxchars outfile
# Optional Arguments
#       outfile verbose quiet, threads

parser = argparse.ArgumentParser(
    description='\
        Simple encryption multitool written in python'
)

args = parser.parse_args()

# Argument Rules
#   - Verbose only applies to terminal output, not outfile
#   - Having outfile defaults quiet in Generate modes

# Program Flow
#   main checks mode
#   main calls func to verify parameters, based on mode
#   main calls mode-specific funcs
#
# Dictionary Attack
#
#
# Brute-force Attack
#
#
# Rainbow Attack
#
#
# Generate Rainbow
#

