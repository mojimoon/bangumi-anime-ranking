import requests
from fake_useragent import UserAgent
import re
from bs4 import BeautifulSoup

'''
STEP1: fetch the entry as a list from the ranking page (spider)
STEP2: fetch wanted info from each entry, save them into csv (api)
STEP3: analyze the ranking data
'''

pre = 'https://bgm.tv/anime/browser?sort=rank&page='
pages = 320
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
        return 0

def main():
    '''
    output into 'data\id\%d.txt'
    for each pages_block pages
    '''
    for i in range(1, pages + 1, pages_block):
        ofile = open('data\\id\\%d.txt' % i, 'w')
        entries = 0
        for j in range(pages_block):
            entries += get_html(i + j, ofile)
        ofile.close()
        print('block %d done, %d entries' % (i, entries))

if __name__ == '__main__':
    main()