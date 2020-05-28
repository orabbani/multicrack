from sys import exit
from tqdm import tqdm
import hashlib, argparse, time, string, os, math
import itertools, multiprocessing, textwrap

parser = argparse.ArgumentParser(
    description=textwrap.dedent('''\
        A simple brute-force decryption tool.
        '''),
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent('''\
        Available algorithms:
            %s        
        ''') % ', '.join(hashlib.algorithms_available)
)
parser.add_argument('hashfile', metavar='HASHFILE',
    type=str,
    help='A file with the hashes to be cracked, seperated by newlines.'
)
parser.add_argument('algorithm', metavar='ALGORITHM',
    type=str,
    help='The hashing algorithm to use.'
)
parser.add_argument('-m', '--min-chars', metavar='MIN',
    type=int, default=1,
    help='Minimum number of characters in generated strings.'
)
parser.add_argument('-M', '--max-chars', metavar='MAX',
    type=int, default = 8,
    help='Maximum number of characters in generated strings.'
)
args = parser.parse_args()
#print(str(args)+'\n')

# This just takes hashfile path and attempts to read the given file.
# It was not included in the main brute function as it wouldn't necessarily be required
#   whenever brute is called. For example, a single hash may be passed as a list of length 1.
def get_hash_list(hash_file):
    try:
        # Open hash file and put contents into list
        with open(hash_file) as f:
            hash_list = f.read().split('\n')
        
        # Remove carriage returns and empty lines
        for h in hash_list:
            h.replace('\r', '')
        while('' in hash_list): hash_list.remove('')

        return hash_list
    except FileNotFoundError:
        print('No such file or directory "%s"' % hash_file)
        exit()

# Prforms all the major script functions. It takes a list of hashes, generates strings
#   within the min and max string length parameters, and spawns processes to perform hashing
#   functions and compares those hashes to the given hash list.
def brute(hash_list, min_chars, max_chars, algorithm, out_file):

    # Establishes ascii characters to use when generating strings. Everything but whitespace.
    string_chars = string.ascii_letters + string.digits + string.punctuation

    # This is how many strings are generated before the list is passed to a new process
    string_list_length = 10000000

    # Takes a pregenerated list of strings, performs the given hashing algorithm, compares to
    #   the given hash file, prints found hashes and outputs to path in out_file
    def hash_string_list(string_list, hash_list, algorithm, out_file):
        for s in string_list:
            h = getattr(hashlib, algorithm)(s.encode('ascii')).hexdigest()
            if h in hash_list:
                # Formats output string
                cracked_hash = '%s::%s' % (h, s)
                print(cracked_hash)
                # This has potential for collision if multiple processes attempt to access the
                #   file simultaneously.
                try:
                    with open(out_file) as f:
                        data = f.read()
                except:
                    data = ''
                with open(out_file, 'w') as f:
                    f.write('%s\n%s' % (data, cracked_hash))

    processes = []
    # Iterates over range of string lengths to generate
    for i in range(min_chars, max_chars+1):
        print('Processing strings of length ' + str(i))

        # This is the number of permutations that will be generated for a given string length. 
        # It is used in cases where the number of permutations would be less than string_list_length.
        permutations = math.pow(len(string_chars), i)

        # This is the list that will be passed to hash_string_list
        string_list = [''] * string_list_length
        index = 0
        # tqdm provides the progress bar
        # itertools generates the strings to be hashed
        for item in tqdm(itertools.product(string_chars, repeat=i), total=int(permutations)):
            string_list[index] = ''.join(item) # itertools returns lists
            index += 1
            # Checks if the current list is >= the set max length or number of permutations
            if index >= string_list_length or index >= permutations:
                index = 0
                
                t = multiprocessing.Process( # Spawn hash_string_list process
                    target=hash_string_list,
                    kwargs={
                        'string_list':string_list,
                        'hash_list':hash_list,
                        'algorithm':algorithm,
                        'out_file':out_file
                    }
                )
                processes.append(t)
                t.start()
    for process in processes: process.join() # Wait for all processes to finish before exiting

# Main loop, just takes arguments, opens hashfile, and performs brute force
if __name__ == '__main__':
    start_time = time.time()
    if args.hashfile:
        if args.algorithm:
            out_file = args.hashfile + '.crack'
            hash_list = get_hash_list(args.hashfile)
            brute(
                hash_list, args.min_chars, args.max_chars, 
                args.algorithm, out_file
            )
        else:
            print('No algorithm specified')
            exit()
    else:
        print('No hash file given')
        exit()