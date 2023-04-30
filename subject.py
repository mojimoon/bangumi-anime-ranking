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
blocks = 32
block_size = lambda i: 240 if i < blocks else 233

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

def main():
    for i in range(1, 2): # TODO: change to blocks + 1
        ifile = open(id_pre + str(i) + id_suf, 'r')
        start = time.time()
        for j in range(block_size(i)):
            id = int(ifile.readline())
            if not get_json(id):
                print('error on id %d' % id)
                time.sleep(3)
        ifile.close()
        print('block %d done, time elapsed: %.2f' % (i, time.time() - start))

if __name__ == '__main__':
    main()