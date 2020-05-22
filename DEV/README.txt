Contained here is partial code that is to be integrated into the final program.

NOTES
-------------------------------
- Development is with Python3 on Linux.
- Python2 has an issue where it doesn't find all the hashes. This will not be investigated
    as Python2 is deprecated anyway.
- Windows has an issue with spawning new processes with multiprocess.Process(). This *will*
    be investigated as cross-platform usage is desirable. 

USAGE
-------------------------------
Install requirements:
'pip3 install -r requirements'

Using multibrute.py:
Help:           python3 multibrute.py --help
Basic usage:    python3 multibrute.py HASHFILE ALGORITHM <options>
Example:        python3 ./multibrute.py ./Resources/hash.txt md5