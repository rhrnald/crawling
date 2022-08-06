from requests_html import HTMLSession
import time
import numpy
import random
import sys
import _thread
from os import makedirs
from os.path import join
from concurrent.futures import ThreadPoolExecutor
 

start_idx = 1

# section=5 # 국민일보
section=32 # 경향신문

__end_idx=[0]*32
__end_idx[5] = 1544261 #국민
__end_idx[32] = 3164333 #경향

end_idx=__end_idx[section]

total_num= end_idx-start_idx+1
thread_num= 32
block_size=int((total_num+thread_num-1)/thread_num)

def save_file(filepath, data):
    # open the file
    with open(filepath, 'w') as handle:
        # save the data
        handle.write(data)
 
# generate a csv file with v=10 values per line and l=5k lines

prefixs = ['div#articeBody','div#dic_area', 'div#newsEndContents']
def generate_file(idx):
    url = 'https://n.news.naver.com/mnews/article/%03d/%010d'%(section, idx)
    session = HTMLSession()

    while True:
        try:
            r = session.get(url, timeout=1)
        except:
            print(str(idx) + " get URL error " + str(cnt))
            continue

        break

    tmp = r.html.find('[property=og\:title]')
    if(not tmp) :
        return False, "", ""

    result=""

    for pf in prefixs:
        base = r.html.find(pf)
        for d in base:
            result = result+d.text+"\n"

    if(result == ""):
        print(str(idx) + " no content")

    return True, tmp[0].attrs['content'], result
 
# generate and save a file
exist_check_point=False
check_point=[0]*32
#check_point = [21995,76920,144777,157730,203986,289554,299218,374954,420416,461083,521986,565880,589494,675626,719787,753296,806799,841102,910866,965180,976524,1033180,1094031,1119377,1159397,1219222,1265294,1336030,1367352,1438864,1455030,1533856]
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
        valid, title, data = generate_file(identifier)
        # create a unique filename
        if(valid==False) :
            continue
        suc_num+=1

        filepath = join(path, str(identifier)+'.txt')
        # save data file to disk
        save_file(filepath, title+'\n'+data)

    save_file(f'res/stat.2.{section:d}/e{num:d}.txt', f'total: {try_num:d}, suc: {suc_num:d}')


# generate many data files in a directory
def main(path='res/2.'+str(section), _thread_num=thread_num):
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