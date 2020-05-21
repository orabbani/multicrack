from sys import exit
from tqdm import tqdm
import hashlib, argparse, time, string, os, math
import itertools, multiprocessing, textwrap

parser = argparse.ArgumentParser(
    description='Simple brute-force decryption tool.',
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
    type=int, default = 32,
    help='Maximum number of characters in generated strings.'
)
args = parser.parse_args()
#print(str(args)+'\n')

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

def brute(hash_list, min_chars, max_chars, algorithm, out_file):

    string_chars = string.ascii_letters + string.digits + string.punctuation
    string_list_length = 3000000 

    def hash_string_list(index, string_list, hash_list, algorithm, out_file):
        for s in string_list:
            h = getattr(hashlib, algorithm)(s.encode('ascii')).hexdigest()
            if h in hash_list:
                cracked_hash = '%s::%s' % (h, s)
                print('  '+cracked_hash)
                try:
                    with open(out_file) as f:
                        data = f.read()
                except:
                    data = ''
                with open(out_file, 'w') as f:
                    f.write('%s\n%s' % (data, cracked_hash))

    processes = []
    for i in range(min_chars, max_chars+1):
        max_string_length_list = math.pow(len(string_chars), i)
        string_list = [''] * string_list_length
        iterator = 0
        #for item in itertools.product(string_chars, repeat=i):
        for item in tqdm(itertools.product(string_chars, repeat=i)):
            string_list[iterator] = ''.join(item)
            iterator += 1
            if iterator >= string_list_length or iterator >= max_string_length_list:
                iterator = 0
                t = multiprocessing.Process(
                    target=hash_string_list,
                    args=(None,),
                    kwargs={
                        'string_list':string_list,
                        'hash_list':hash_list,
                        'algorithm':algorithm,
                        'out_file':out_file
                    }
                )
                processes.append(t)
                t.start()
    for process in processes: process.join()
    
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