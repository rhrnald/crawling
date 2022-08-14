from requests_html import HTMLSession
from urllib.request import urlopen
import time
import numpy
import random
import sys
import _thread
from os import makedirs
from os.path import join
from concurrent.futures import ThreadPoolExecutor
 

start_idx = 1

section = 21 # 문화일보 
# section = 20 #동아일보
# section=5 # 국민일보
# section=32 # 경향신문
# section = 81 # 서울신문

__end_idx={0:0}
__end_idx[5]=1544261 #국민
__end_idx[20]=3445333 #동아일보
__end_idx[21]=2526385 #문화일보
__end_idx[32]=3164333 #경향
__end_idx[81]=3294291 #서울신문

end_idx=__end_idx[section]

total_num= end_idx-start_idx+1
thread_num=32

block_size=int((total_num+thread_num-1)/thread_num)

RAW=True

def save_file(filepath, data):
    # open the file
    with open(filepath, 'w') as handle:
        # save the data
        handle.write(data)
 
# generate a csv file with v=10 values per line and l=5k lines

prefixs = ['div#articeBody','div#dic_area', 'div#newsEndContents']
def generate_file(idx):
    url = 'https://n.news.naver.com/mnews/article/%03d/%010d'%(section, idx)
    with urlopen(url) as r:
        return True, r.read().decode("utf-8")
 
# generate and save a file
exist_check_point=False
check_point = [48259,88269,144777,189017,241295,289554,337813,386072,434331,482590,530849,579108,613866,675626,723885,772144,820403,868662,916921,965180,987610,1048442,1109957,1158216,1174995,1254734,1302993,1351252,1399511,1447770,1496029,1544288]
def generate_and_save(path, num):
    try_num=0
    suc_num=0

    s=0
    if exist_check_point:
        s = check_point[num]
    else:
        s = start_idx+block_size*num

    for identifier in range(s, start_idx+block_size*(num+1)):
        if identifier%100 == 0:
            save_file(f'res/stat.2.{section:d}/p{num:d}_proc.txt', f'total: {try_num:d}, suc: {suc_num:d}, i: {identifier:d}')

        # generate data
        try_num+=1
        valid, data = generate_file(identifier)
        # create a unique filename
        if(valid==False) :
            continue
        suc_num+=1

        filepath = join(path, str(identifier)+'.txt')
        # save data file to disk
        
        save_file(filepath, data)
        #save_file(filepath, title+'\n'+data)

    save_file(f'res/stat.2.{section:d}/e{num:d}.txt', f'total: {try_num:d}, suc: {suc_num:d}')


# generate many data files in a directory
#root_path ='/data/hyejin/chaewon/'
root_path ='/data/roseanne/chaewon/'
save_path = root_path+'raw_2.'+str(section)

def main(path=save_path, _thread_num=thread_num):
    # create a local directory to save files
    makedirs(path, exist_ok=True)
    makedirs(f'res/stat.2.{section:d}', exist_ok=True)

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