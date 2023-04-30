# Bangumi Anime Ranking

Yet another [Bangumi](https://bgm.tv/) anime ranking analysis project.

- Last Update: 2023-04-30
- Entries: 6565 (= 7673 all ranked animes - 1108 restricted entries)
- As there are too many files, you cannot preview all of them on Github. Clone this repo and view the files locally.
- Enjoys!

## Usage

### Requirements

Python 3.6+ is required. You can install the dependencies by running the following command.
```bash
pip install -r requirements.txt
```

### Run

Since crawling data can be time consuming, I have already crawled the data and put it in `data/`.

To crawl data by yourself, you can run the following commands, or simply run `run.bat` (Windows only).

| Task | Script | Output | Function |
| ---- | ------- | ------ | ---- |
| Get ranking list | `spider.py` | `data/id/` | |
| Get entry details | `subject.py` | `data/sub/` | `api_main()` |
| Pick up available entries | `subject.py` | `data/id/available.txt` | `ava_main()` |
| Generate CSV containing all entries | `subject.py` | `data/sub.csv` | `csv_main()` |
| Perform General Statistics | `stat.py` | `data/stat/` | |

### Notes

- **All data are stored in UTF-8 encoding**. Your spreadsheet software may not recognize it. You should open the CSV file with encoding `UTF-8` or `UTF-8 with BOM`.
- **Please configure `subject.py` Line 31 before running**. If you need a fresh start, change to `w`; but if you want to resume after some blocks, change to `a`.
- Estimated time to get entry list: around 2 minutes.
- Estimated time to get entry details: 40-60 minutes.
- Refer to [Bangumi API](https://bangumi.github.io/api/) for everything about API.
- Although fake user-agent works, it is recommended to [configure your own UA](https://github.com/bangumi/api/blob/master/docs-raw/user%20agent.md).
- The data are crawled and processed in blocks. By default, 10 pages (240 entries) per block. At 2023-04-30, there are 320 pages in total, which are split into 32 blocks, numbered with their starting page number (1, 11, 21, ..., 311). It is very likely that pages and blocks will increase over time, but there should be no issue if you keep the default block setting.
- Restricted entries can be found in `data/id/restricted.txt`. They appear in the ranking list but cannot be accessed by API. They are excluded from the CSV file.
- The `rank` field in the CSV file is the rank within available entries. The original rank is not included since it cannot provide any statistical information.
- Because of the restricted entries, it is common to see many entries missing with logs in the console. You can safely ignore them. However, if there are too many missing entries, you may want to check if your UA is correct.
