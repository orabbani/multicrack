from tqdm import tqdm
import itertools
import passlib.hash
import string
import math

#h = '$P$BjRvZQ.VQcGZlDeiKToCQd.cPw5XCe0' # 'michael'
h = '$P$5f85L.50r/yErtFqDJx4WL9ZLQcOKw0' # 'win'

def brute(h):
    string_chars = string.ascii_letters + string.digits + string.punctuation

    rounds = (string.digits + string.ascii_uppercase).find(h[3]) + 2
    salt = h[4:12]

    cracked = None
    length = 0
    while not cracked:
        length += 1
        permutations = math.pow(len(string_chars), length)
        t = tqdm(itertools.product(string_chars, repeat=length), total=permutations)
        for item in t:
            s = ''.join(item)
            # This shows the current string being generated at signifcant expense to speed
            #t.set_description(s)
            #t.refresh() 
            if passlib.hash.phpass.hash(s, salt=salt, rounds=rounds) == h:
                cracked = s
                break
    print(cracked)

if __name__ == '__main__':
    brute(h)