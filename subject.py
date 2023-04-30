import requests
import time

'''
STEP2: fetch the details of each entry by API (subject)
API Server = https://api.bgm.tv/
API URL = /v0/subjects/{subject_id}
'''

pre = 'https://api.bgm.tv/v0/subjects/'
id_pre = 'data\\id\\'
id_suf = '.txt'
max_block = 311
block_size = lambda i: 240 if i < max_block else 233

def get_json(sid):
    url = pre + str(sid)
    try:
        r = requests.get(url, headers={'User-Agent': 'CryoVit/analyzer'})
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        ofile = open('data\\sub\\%d.json' % sid, 'w', encoding='utf-8')
        ofile.write(r.text)
        ofile.close()
        return True
    except:
        return False

def api_main():
    _ofile = open('data\\id\\removed.txt', 'a') # append mode
    for i in range(1, max_block + 1, 10):
        ifile = open(id_pre + str(i) + id_suf, 'r')
        start = time.time()
        for j in range(block_size(i)):
            sid = int(ifile.readline())
            if not get_json(sid):
                print('error on id %d' % sid)
                _ofile.write(str(sid) + '\n')
        ifile.close()
        print('block %d done, time elapsed: %.2f' % (i, time.time() - start))
    _ofile.close()

if __name__ == '__main__':
    api_main()