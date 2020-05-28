from hashlib import md5
from sys import exit
import argparse, time, string, itertools, math
from tqdm import tqdm

parser = argparse.ArgumentParser(
    description='\
        Simple MD5 brute-force decryption tool.'
)
parser.add_argument(
    'HASHFILE',
    type=str,
    help='A file with the hashes to be cracked, seperated by newlines.'
)
parser.add_argument(
    'MINCHARS',
    type=int,
    help='Minimum number of characters to generate.'
)
parser.add_argument(
    'MAXCHARS',
    type=int,
    help='Maximum number of characters to generate.'
)
args = parser.parse_args()

# Read hashes
file = open(args.HASHFILE)
hashlist = file.read().split('\n')
file.close()
while('' in hashlist): hashlist.remove('')
for i in range(len(hashlist)):
    if '\r' in hashlist[i]:
        hashlist[i] = hashlist[i][:-1]

chars = string.ascii_letters + string.digits + string.punctuation

for i in range(args.MINCHARS, args.MAXCHARS+1):
    permutations = math.pow(len(chars), i)
    for item in tqdm(itertools.product(chars, repeat=i), total=permutations):
        word = "".join(item)
        wordhash = md5(word.encode('ascii')).hexdigest()
        if wordhash in hashlist:
            print(word + '::' + wordhash)