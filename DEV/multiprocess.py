import string, time, itertools, multiprocessing, os
from hashlib import md5
from sys import argv

num_threads = int(argv[1])

def calc_hashes():
    start_time = time.time()
    for item in itertools.product(string.printable, repeat=3):
        md5("".join(item).encode('ascii')).hexdigest()
    return time.time() - start_time

def control_test(num_threads):
    print('Starting Control Test')
    start_time = time.time()

    for _ in range(num_threads): calc_hashes()

    total_time = time.time() - start_time
    #print('Average time per task: %f' % (total_time / num_threads))
    print('Control test done after %f seconds' % total_time)

def multiprocessing_test(num_threads):
    print('Starting Multiprocessing Test')
    start_time = time.time()

    def run_hash(index):
        with open('._'+str(i), 'w') as f:
            f.write(str(calc_hashes()))
            print('.')

    processes = []
    for i in range(num_threads):
        t = multiprocessing.Process(target=run_hash, args=(i,))
        processes.append(t)
        t.start()

    for process in processes:
        process.join()

    total_time = time.time() - start_time
    #print('Time per task: %f' % (total_time / num_threads))
    print('Multiprocessing test done after %f seconds' % total_time)

    for i in range(num_threads):
        os.remove('._'+str(i))


#print(); control_test(num_threads)
print(); multiprocessing_test(num_threads)
print()