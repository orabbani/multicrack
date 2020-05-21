from hashlib import md5
from sys import exit
import argparse, time
#import chardet

parser = argparse.ArgumentParser(
    description='\
        Simple MD5 dictionary-attack decryption tool.'
)
parser.add_argument (
    'HASHFILE',
    type=str,
    help='A file with the hashes to be cracked, seperated by newlines.'
)
parser.add_argument(
    'DICTIONARY',
    type=str,
    help='The dictionary file to use.'
)
args = parser.parse_args()

def get_file_as_list(path):
    try:
        file = open(path)
    except:
        print('Could not open file at given path.')
        exit()
    else:
        lst = file.read().split('\n')
        file.close()
        # Remove empty lines
        while('' in lst): lst.remove('')
    # Remove carriage returns
    for i in range(len(lst)):
        if '\r' in lst[i]:
            lst[i] = lst[i][:-1]
    return lst

hashlist = get_file_as_list(args.HASHFILE)

print('Number of hashes to test: ' + str(len(hashlist)))

dictionary = get_file_as_list(args.DICTIONARY)
#encoding = chardet.detect(dictionary[0])['encoding']
#print('Dictionary encoding: ' + encoding)
print('Number of words in dictionary: ' + str(len(dictionary)) + '\n')

start_time = time.time()
print('Starting on ' + time.ctime(start_time) + '\n')

found = 0
hashed = 0
invalid = 0
for word in dictionary:
    try:
        md5hash = md5(word).hexdigest()
        hashed += 1
    except:
        print('Invalid dictionary entry: ' + word)
        invalid += 1
    else:
        if md5hash in hashlist:
            print(word+'::'+md5hash)
            found += 1

    if found == len(hashlist): 
        print('All hashes found.')
        break

end_time = time.time()
print('\nFinished on ' + time.ctime(end_time))
print('Time taken: %i seconds' % (end_time - start_time))
print('Words hashed: %i' % hashed)
print('Invalid dictionary entries: %i' % invalid)
print('Valid hashes found: %i' % found)