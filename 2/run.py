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


# 문화일보 21
# 동아일보 20
# 국민일보 5
# 경향신문 32
# 서울신문 81

section = 20
__end_idx={0:0}
__end_idx[5]=1544261 #국민일보
__end_idx[20]=3445333 #동아일보
__end_idx[21]=2526385 #문화일보
__end_idx[32]=3164333 #경향
__end_idx[81]=3294291 #서울신문

start_idx=1830340
end_idx=__end_idx[section]

total_num= end_idx-start_idx+1
thread_num= 32
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
    session = HTMLSession()

    while True:
        try:
            r = session.get(url, timeout=1)
        except:
            continue

        break
    return True, r.text
    
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
check_point = [15812,123469,231021,338758,446215,538337,646004,753671,861338,969005,1076672,1184339,1292006,1399673,1507340,1615007,1722674,1830341,1946475,2055692,2168710,2272480,2380871,2487946,2589818,2697740,2814954,2913156,3030341,3137892,3245753,3353389]
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

    save_file(f'res/stat.2.{section:d}/e{num:d}.txt', f'total: {try_num:d}, suc: {suc_num:d}')


# generate many data files in a directory

save_path = '/data/hyejin/chaewon/raw_2.'+str(section)
#save_path = 'res/raw_2.'+str(section)

def main(path=save_path, _thread_num=thread_num):
    # create a local directory to save files
    makedirs(path, exist_ok=True)
    makedirs(f'res/stat.2.{section:d}', exist_ok=True)

    # create the thread pool
    ss=time.time()

    '''
    with ThreadPoolExecutor(_thread_num) as exe:
        # submit tasks to generate files
        _ = [exe.submit(generate_and_save, path, i) for i in range(_thread_num)]
    '''
    process_num=int(sys.argv[1])
    generate_and_save(path, process_num)
    
    ee = time.time()

    print("Total time:", ee-ss)
 
# entry point
if __name__ == '__main__':
    main()