from requests_html import HTMLSession
import time
import numpy
import random
import sys
import _thread
from os import makedirs
from os.path import join
from concurrent.futures import ThreadPoolExecutor
 
# save data to a file

N=6619634
M=10
bs=int((N-1)/M)+1
section=9 #0~9
start_idx=bs*section+1 # 6619634
total_num=bs
thread_num=128
block_size=int((total_num+thread_num-1)/thread_num)

def save_file(filepath, data):
    # open the file
    with open(filepath, 'w') as handle:
        # save the data
        handle.write(data)
 
# generate a csv file with v=10 values per line and l=5k lines

def generate_file(idx):
    
    url = 'https://terms.naver.com/entry.naver?docId=' + str(idx)

    session = HTMLSession()
    r = session.get(url)
    tmp = r.html.find('[property=og\:title]')
    if(not tmp) :
        return False, "", ""

    base = r.html.find('p.txt')
    

    result=""
    for d in base:
        result = result+d.text+"\n"
    return True, tmp[0].attrs['content'], result
 
# generate and save a file
def generate_and_save(path, num):
    try_num=0
    suc_num=0
    for identifier in range(start_idx+block_size*num, start_idx+block_size*(num+1)):
        # generate data
        try_num+=1
        valid, title, data = generate_file(identifier)
        # create a unique filename
        if(valid==False) :
            continue
        suc_num+=1

        filepath = join(path, str(identifier)+'.txt')
        # save data file to disk
        save_file(filepath, title+'\n'+data)

    save_file(f'res/stat/{num:d}.txt', f'total: {try_num:d}, suc: {suc_num:d}')


# generate many data files in a directory
def main(path='res/1.'+str(section), _thread_num=thread_num):
    # create a local directory to save files
    makedirs(path, exist_ok=True)
    # create the thread pool
    ss=time.time()
    
    with ThreadPoolExecutor(_thread_num) as exe:
        # submit tasks to generate files
        _ = [exe.submit(generate_and_save, path, i) for i in range(_thread_num)]
    
    ee = time.time()

    print("Total time:", ee-ss)
 
# entry point
if __name__ == '__main__':
    main()