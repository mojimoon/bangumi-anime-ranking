# Bangumi Ranking Analysis

Yet another [Bangumi](https://bgm.tv/) ranking analysis project.

- Only anime is considered.
- Last Update: 2023-04-30
- Entries: ~7673 (all ranked anime, expect the removed ones)
- Refer to [Bangumi API](https://bangumi.github.io/api/) for everything about API.
- As there are too many files, you cannot preview all of them on Github. You can clone this repo and view the files locally.
- Enjoys!

## Usage

### Requirements

- Python 3.6+
- `pip install -r requirements.txt`

### Run

Since crawling data can be time consuming, I have already crawled the data and put it in `data/`.

* Crawling entry ID from ranking: `python spider.py`, the output will be txts in `data/ids/`. The removed entries will be in `data/ids/removed.txt`.

* Crawling entry details via API: `python subject.py`, the output will be jsons in `data/sub/` and an integrated CSV file `data/ranking.csv`.

* Analyzing data: `python analysis.py`, the output will be figures in `output/`.

I prefer crawling data in blocks. By default, 10 pages (240 entries) per block, and there are 32 blocks (320 pages). However, when you read this, it is very likely that the number of pages has increased. You should change related variables in all three scripts.
