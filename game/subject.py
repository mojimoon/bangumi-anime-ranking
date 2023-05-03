import requests, time, json, csv
from fake_useragent import UserAgent

'''
STEP2: fetch the details of each entry by API (subject)
API Server = https://api.bgm.tv/
API URL = /v0/subjects/{subject_id}
'''

pre = 'https://api.bgm.tv/v0/subjects/'
id_pre = 'data\\id\\'
id_suf = '.txt'
max_block = 10002 # not hard-coded, just a large enough number

def get_json(sid):
    url = pre + str(sid)
    try:
        # r = requests.get(url, headers={'User-Agent': 'CryoVit/bangumi-anime-ranking'})
        r = requests.get(url, headers={'User-Agent': UserAgent().chrome})
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        ofile = open('data\\sub\\%d.json' % sid, 'w', encoding='utf-8')
        ofile.write(r.text)
        ofile.close()
        return True
    except:
        return False

def api_main():
    # HACK: change open mode to 'w' for a fresh start; 'a' for block resuming
    res_ofile = open('data\\id\\restricted.txt', 'a')
    for i in range(1, max_block, 10):
        try:
            ifile = open(id_pre + str(i) + id_suf, 'r')
        except:
            print('block %d not found' % i)
            return
        else:
            start = time.time()
            for _sid in ifile:
                sid = int(_sid)
                if not get_json(sid):
                    print('missing id ' + _sid, end='')
                    res_ofile.write(_sid)
            ifile.close()
            print('block %d done, time elapsed: %.2f' % (i, time.time() - start))
    res_ofile.close()

restricted = []

def available():
    res_ifile = open('data\\id\\restricted.txt', 'r')
    for line in res_ifile:
        if line != '\n':
            restricted.append(int(line))
    res_ifile.close()

    res_index = 0
    res_len = len(restricted)
    '''
    since all data come in original rank order,
    double pointer is used to avoid unnecessary search
    '''
    for i in range(1, max_block, 10):
        try:
            ifile = open(id_pre + str(i) + id_suf, 'r')
        except:
            # print('block %d not found' % i)
            return
        else:
            for _sid in ifile:
                sid = int(_sid)
                if res_index < res_len and sid == restricted[res_index]:
                    res_index += 1
                else:
                    yield sid
        ifile.close()

def ava_main():
    ofile = open('data\\id\\available.txt', 'w')
    for sid in available():
        ofile.write(str(sid) + '\n')
    ofile.close()

def csv_main():
    ifile = open('data\\id\\available.txt', 'r')
    ofile = open('data\\sub.csv', 'w', newline='')
    '''
    extract the following fields:
        * "id": sid
        * "name_cn" (if empty, use "name" instead): title
        * "rating": {"count": {"1": s[0], ..., "10": s[9]}}
        * "collection": {"collect": collect, "doing": doing, "on_hold": on_hold, "dropped": dropped}

    write the following fields into CSV:
        * sid
        * title
        * s[0] ... s[9]
        * rank (NOT JSON rank)
        * total votes = sum(s[0] ... s[9])
        * average score (NOT JSON score)
        * standard deviation
        * user count = collect + doing + on_hold + dropped
    '''
    writer = csv.writer(ofile)
    writer.writerow(['sid', 'title', 's1', 's2', 's3', 's4', 's5', 's6', 's7',
        's8', 's9', 's10', 'rank', 'vote', 'avg', 'std', 'user'])
    rank = 0
    for line in ifile:
        sid = int(line)
        jfile = open('data\\sub\\%d.json' % sid, 'r', encoding='utf-8')
        j = json.load(jfile)
        jfile.close()

        sid = j['id']
        title = j['name_cn'] if j['name_cn'] else j['name']
        s = [0] * 10
        for i in range(10):
            s[i] = j['rating']['count'][str(i + 1)]
        rank += 1 # rank within the available entries, not original rank
        vote = sum(s)
        avg = sum([(i + 1) * s[i] for i in range(10)]) / vote
        std = (sum([(i + 1 - avg) ** 2 * s[i] for i in range(10)]) / vote) ** 0.5
        user = j['collection']['collect'] + j['collection']['doing'] + \
            j['collection']['on_hold'] + j['collection']['dropped']
        
        writer.writerow([sid, title] + s + [rank, vote, avg, std, user])
    ifile.close()
    ofile.close()

def main():
    api_main()
    ava_main()
    csv_main()

if __name__ == '__main__':
    main()
