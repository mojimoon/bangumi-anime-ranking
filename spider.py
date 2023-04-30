import requests, re, time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

'''
STEP1: fetch the entry as a list from the ranking page (spider)
'''

pre = 'https://bgm.tv/anime/browser?sort=rank&page='
pages = 9999 # not hard-coded, just a large enough number
pages_block = 10

def get_html(page, ofile):
    url = pre + str(page)
    try:
        r = requests.get(url, headers={'User-Agent': UserAgent().chrome})
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        '''
        id of each entry can be found via following selector:
        #browserItemList > li
        the id of <li> is in the format: item_%d
        '''
        soup = BeautifulSoup(r.text, 'html.parser')
        entries = 0
        for li in soup.select('#browserItemList > li'):
            id = re.search(r'item_(\d+)', li['id']).group(1)
            ofile.write(id + '\n')
            entries += 1
        return entries
    except:
        print('error on page %d' % page)
        return -1

def main():
    '''
    output into 'data\id\%d.txt'
    for each pages_block pages
    '''
    start = time.time()
    for i in range(1, pages + 1, pages_block):
        ofile = open('data\\id\\%d.txt' % i, 'w')
        entries = 0
        flag = False
        for j in range(pages_block):
            res = get_html(i + j, ofile)
            if res == -1:
                res = 0
            elif res == 0:
                flag = True
                break
            entries += res
        ofile.close()
        if entries == 0:
            break
        print('block %d done, %d entries' % (i, entries))
        if flag:
            break
    print('time elapsed: %.2f' % (time.time() - start))

if __name__ == '__main__':
    main()