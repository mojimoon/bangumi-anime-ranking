# A Simplified Ranking System Based on Partial Order Network (PONet)

## Introduction

PONet is a ranking algorithm developed by @eyecandy. The original article can be found [here](https://bgm.tv/group/topic/371075).

The core idea of PONet is to rank entries based on **how a specific user votes different entries**, instead of more classic ranking algorithms that rank entries based on *how a specific entry is voted by different users* (e.g. [Bayesian Average](https://en.wikipedia.org/wiki/Bayesian_average)). More specifically, PONet is based on the following assumptions:

> If the user group that votes **BOTH** entry A and entry B,
> **MAJORITY** of them think A is better than B,
> then we can say A is better than B.

Excerpt from original article for more details:

> Here, we have a principle that "to assert entry A is better than entry B, it should be true that those who rated both A and B suggest that A is better than B." That is, the judgment of the relative merits of entries is based on the judgment of the overlapping raters of the entries.
>
> The famous [scientific ranking](https://bgm.tv/group/topic/337638) is indeed based on this principle, but it seems that the specific ranking method is unnecessarily complex and unintuitive.
>
> ...
>
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
    - **Simple Score** is defined as `sgn(x - y)`.

> Different scores can behave very differently. Suppose we have entry A and B (x = 90, y = 10, n = 100), and entry C and D (x = 9, y = 1, n = 10).
> - Total score favors entry with more votes. A will receive a higher score than C. It is likely to yield a ranking similar to the classic ones.
> - Percentage score favors entry with less disagreement. A will receive equal score as C. However, suppose we have a user thinking D is better than C. This will siginicantly reduce the score of C; and if he thinks B is better than A, this will just slightly reduce the score of A.
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
├── ponet (this folder)
│   ├── bangumi15M
│   │   ├── AnonymousUserCollection.csv [*]
│   │   ├── Subjects.csv [*]
│   ├── data
│   │   ├── text_result
│   │   │   ├── percentage_bot30.txt
│   │   │   ├── percentage_top100.txt
│   │   │   ├── simple_bot30.txt
│   │   │   ├── simple_top100.txt
│   │   │   ├── total_bot30.txt
│   │   │   ├── total_top100.txt
│   │   ├── ponet_gb.csv
│   │   ├── ponet.csv
│   │   ├── relative_votes.csv [*]
│   │   ├── subjects.csv
│   │   ├── unmerged.csv
│   ├── ponet.py
│   ├── README.md (this file)
```

Important: `[*]` indicates that **the file is too large to be uploaded to Github**.

For the original dataset, please download via the link above.

*I will also release a .zip of the full project, including all files and data, on Baidu Netdisk. The link will be updated here when it is ready.*

- `bangumi15M` contains the original dataset. When you download it, please put it in this folder, without changing file names.
    - `AnonymousUserCollection.csv` contains the anime collection records of all users, with user ID anonymized. (Too large to be uploaded to Github.)
    - `Subjects.csv` contains the details of all entries (in all categories including anime). (Too large to be uploaded to Github.)
- `data` contains the files generated by this project.
    - `text_result` contains part of the final ranking in text format, for posting on Bangumi.
    - `ponet.csv` contains the final ranking, a merge of `subjects.csv` and `unmerged.csv`.
    - `ponet_gb.csv` is the GB-2312 version of `ponet.csv`.
    - `relative_votes.csv` contains the relative votes of all pairs of entries. (Too large to be uploaded to Github.)
    - `subjects.csv` contains the details of all entries.
    - `unmerged.csv` contains the calculated scores of all entries.
- `ponet.py` is the only script in this side project.
- *I will also release a .ipynb version of this project on Kaggle. The link will be updated here when it is ready.*

## Usage

### Requirements

See main [README.md](../README.md#requirements).

### Run

There are three major parts in `ponet.py`:
- `pre()` is used to preprocess the original dataset. It will generate `data/ponet/subjects.csv`. You don't need to run it again unless you have an updated dataset.
- `rela()` is used to calculate the relative votes of all pairs of entries. It will generate `data/ponet/relative_votes.csv`.
- `ponet()` and `final()` are used to calculate the final ranking. They will generate `data/ponet/ponet.csv`.

Modify `main()` to run different functions.

## Performance

Performance issue is known to be a major problem of PONet.

The time complexity of PONet is $\mathcal{O}(N^2+M)$, where $N$ is the number of entries and $M$ is the number of votes.

However, simply by using `numpy.ndarray` instead of `pandas.DataFrame`, the efficiency can be improved by 2 orders of magnitude.

| Process | Relative Votes | Final Ranking |
| --- | --- | --- |
| Time Complexity | $\mathcal{O}(M)$ | $\mathcal{O}(N^2)$ |
| Estimated Time with `DataFrame` | 16 hours | 10 hours |
| Estimated Time with `ndarray` | 25 minutes | 2 minutes |

Note: The running time is based on my personal computer (i5-12500H, 16GB RAM), and the bottleneck is memory usage.

### Relative Votes

Suppose a user has voted $n$ entries. A total of $\frac{n(n-1)}{2}$ pairs of entries will be recorded. Thus the total time complexity is $\mathcal{O}\left(\sum_{i=1}^N\frac{n_i(n_i-1)}{2}\right)$, where $n_i$ is the number of entries voted by user $i$.

For most users, $n_i$ is small. However, there are some users who have voted a large number of entries. There are some hundreds of users who have voted more than 1000 entries (although unrated entries are ignored in this project). The time complexity of these users is $\mathcal{O}(n_i^2)$, which has the same OoM as the total time complexity and thus consumes most of the time.

The number of actual operations, or the pairs recorded, is estimated to be ~8e7. In comparison, the total number of votes is ~8e6, and the total number of entries is ~8e3.

It can be further optimized by switching to `numba`, though I am not familiar with it. Also, the majority of the time is spent on the users who have voted a large number of entries, while even that thousands are not large compared to total number of records. Thus, it is possible to split the dataset into several parts and run them in parallel.

### Final Ranking

The time complexity of final ranking is $\mathcal{O}(N^2)$, which is actually smaller (~2.4e7 rows in `relative_votes.csv`), because some of the entry pairs are skipped.

It can be further optimized with numpy `mask` and `bincount`, but since the speed is already acceptable, I didn't do it.

## Results

The result has been published [on Bangumi](https://bgm.tv/group/topic/382497).

You can also read [data/text_result/](data/text_result/) for the full ranking.

Result table `data/ponet.csv` is sorted by `id` in ascending order.
