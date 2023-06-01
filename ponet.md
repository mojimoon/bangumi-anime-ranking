# A Simplified Ranking System Based on Partial Order Network (PONet)

## Introduction

PONet is a ranking algorithm developed by @eyecandy. The original article can be found [here](https://bgm.tv/group/topic/371075).

The core idea of PONet is to rank entries based on **how a specific user votes different entries**, instead of more classic ranking algorithms that rank entries based on *how a specific entry is voted by different users* (e.g. [Bayesian Average](https://en.wikipedia.org/wiki/Bayesian_average)). More specifically, PONet is based on the following assumptions:

> If the user group that votes **BOTH** entry A and entry B,
> **MAJORITY** of them think A is better than B,
> then we can say A is better than B.

Below is a DeepL translation for more details.

> Here, we have a principle that "to assert entry A is better than entry B, it should be true that those who rated both A and B suggest that A is better than B." That is, the judgment of the relative merits of entries is based on the judgment of the overlapping raters of the entries.
> The famous [scientific ranking](https://bgm.tv/group/topic/337638) is indeed based on this principle, but it seems that the specific ranking method is unnecessarily complex and unintuitive.
> ...
> Of course, a simple two-by-two comparison can lead to circular preferences (i.e., A is better than B, B is better than C, C is better than A, etc.), so it is necessary to convert the above "partial order" of two-by-two comparisons into a "full order" that can give a single ranking to all works with a uniform standard.

<!--

那么，怎样来解决这一矛盾呢？在此，我们有一个原则，即“判断作品甲优于作品乙的依据，应当是同时给作品甲和乙评分的群体认为作品甲优于作品乙。”亦即，依据作品间重叠评分者的判断来判断作品之间的相对优劣。著名的“科学排名”的确就是根据这一原则来的，但似乎具体的排序方法又不必要地复杂了，以至于失之直观。作为更简单易懂的科学排名的一项测试，楼主利用了@Oalvay 提供的2021年2月份记录的Bangumi 全用户动画评分数据计算出了一个排行榜。同时鸣谢@Trim21 提供的 Bangumi Archive 数据，用于将作品 ID 与作品标题进行匹配。当然，单纯的两两比较会导致循环偏好的现象（即甲优于乙，乙优于丙，丙又优于甲等）的产生，因此有必要以统一的标准将上述两两比较的“偏序”转化为可以给所有作品一个单一排名的“全序”。具体算法如下。

-->

## Algorithm

### Step 1: Pairwise Comparison

Consider all pairs of entries (A, B).

Suppose:

- `n` users have voted both A and B;
- Among them, `x` users think A is better than B, `y` users think B is better than A.

Then:

1. Check if n >= 10. If not, skip this pair. (10 is a hyperparameter. If its value is too small, the ranking will be too sensitive to the votes of a few users. If its value is too large, most pairs will be skipped.)

2. Calculate the score of A and B. Different forms of relative score of A against B is defined as:
    - **Total Score** is defined as `x - y`.
    - **Percentage Score** is defined as `(x - y) / n`.
    - **Percentage Score with Confidence** is defined as `(x - y) / sqrt(n)`.
    - **Simple Score** is defined as `sgn(x - y)`.

> Different scores can behave very differently. Suppose we have entry A and B (x = 90, y = 10, n = 100), and entry C and D (x = 9, y = 1, n = 10).
> - Total score favors entry with more votes. A will receive a higher score than C. It is likely to yield a ranking similar to the classic ones.
> - Percentage score favors entry with less disagreement. A will receive equal score as C. However, suppose we have a user thinking D is better than C. This will siginicantly reduce the score of C; and if he thinks B is better than A, this will just slightly reduce the score of A.
> - Percentage score with confidence is a compromise between the above two. It still favors entry with more votes, but it will become much less sensitive when n is large. A will still receive a higher score than C, but the difference is much smaller than that of total score.
> - Simple score is another compromise. Pretty insensitive to n, but tolerates disagreement more.

3. The relative score of B against A is defined as the negative of that of A against B.

### Step 2: Full Order

Consider all entries A.

The final score of A is defined as the sum of relative scores of A against all other entries.

Different forms of score is calculated independently, and since we have four kinds of them, we have four kinds of final score and ranking.

## Dataset and Files

The dataset used in this project is [Bangumi15M](https://www.kaggle.com/datasets/klion23/bangumi15m), which contains 8573 valid entries (including restricted ones) and 7,770,854 valid collection records (>50% of them are unrated).

Below is a tree view of the files related to PONet ranking.

```bash
├── bangumi15M
│   ├── AnonymousUserCollection.csv [*]
│   ├── Subjects.csv [*]
├── data
│   ├── ponet
│   │   ├── ponet.csv
│   │   ├── relative_votes.csv [*]
│   │   ├── subjects.csv
├── ponet.py
├── ponet.md
```

Important: `[*]` indicates that **the file is too large to be uploaded to Github**.

For the original dataset, please download via the link above.

*I will also release a .zip of the full project, including all files and data, on Baidu Netdisk. The link will be updated here when it is ready.*

- `bangumi15M` contains the original dataset. When you download it, please put it in this folder, without changing file names.
- `data/ponet` contains the files generated by this project.
    - `ponet.csv` contains the final ranking.
    - `relative_votes.csv` contains the relative votes of all pairs of entries. (Too large to be uploaded to Github.)
    - `subjects.csv` contains the details of all entries.
- `ponet.py` is the only script in this side project.
- *I will also release a .ipynb version of this project on Kaggle. The link will be updated here when it is ready.*

## Usage

### Requirements

See main [README.md](README.md#Requirements).

### Run

There are three main functions in `ponet.py`:
- `pre()` is used to preprocess the original dataset. It will generate `data/ponet/subjects.csv`. You don't need to run it again unless you have an updated dataset.
- `rela()` is used to calculate the relative votes of all pairs of entries. It will generate `data/ponet/relative_votes.csv`.
- `ponet()` is used to calculate the final ranking. It will generate `data/ponet/ponet.csv`.

## Performance

Performance issue is known to be a major problem of PONet.

The time complexity of PONet is $\mathcal{O}(N^2+M)$, where $N$ is the number of entries and $M$ is the number of votes.

### Relative Votes

This is the $O(M)$ part, also the most time-consuming process.

If a specific users votes $n$ entries, then $n(n-1)/2$ pairs will be considered. $n$ is generally small for most of the users, but some who have collected 1000+ entries will be a problem. The total number of pairs is $\sum_{i=1}^{N}n_i(n_i-1)/2$, where $n_i$ is the number of entries voted by user $i$, estimated within the range 1e7 ~ 1e8 (while M is only 7.7e6).

So how slow can it be?

> I have a laptop running i5-12500H and 16GB RAM.  
> At first the efficiency is only about 10000 records per minute, which means it will take 1000 minutes (16 hours) to finish the calculation. That was just unacceptable.  
> After consulting some friends, I found that the main reason for the low efficiency is that I used `pandas.DataFrame` to store the data. So I changed it to `numpy.ndarray`, and the efficiency increased to ~300000 records per minute. That's much better! I completed the calculation in about 25 minutes.  
> Still there is room for improvement. For example, you can try `numba`.  
> But for me, the major bottleneck is memory. The script drains about 10GB of memory, and I have to close all other programs to run it. I don't think I can do much more.

### Final Ranking

*This part is a work in progress.*

The time complexity of the final ranking is $\mathcal{O}(N^2)$, which is much smaller than that of relative votes. However, it is still too slow to be acceptable.