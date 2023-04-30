# Bangumi Ranking Analysis

Yet another [Bangumi](https://bgm.tv/) ranking analysis project.

- Only anime is considered.
- Last Update: 2023-04-30
- Entries: 7673 (all ranked anime)
- Refer to [Bangumi API](https://bangumi.github.io/api/) for everything about API.
- Enjoys!

## Usage

### Requirements

- Python 3.6+
- `pip install -r requirements.txt`

### Run

Since crawling data can be time consuming, I have already crawled the data and put it in `data/`.

* Crawling entry ID from ranking: `python spider.py`, the output will be txts in `data/ids/`.

* Crawling entry details via API: `python subject.py`, the output will be jsons in `data/sub/` and an integrated CSV file `data/ranking.csv`.

* Analyzing data: `python analysis.py`, the output will be figures in `output/`.

