'''
reference: https://bgm.tv/group/topic/371075
a simplified ranking system based on partial order network
一种基于偏序网络的简化排名系统

input[0]: .\bangumi15M\AnonymousUserCollection.csv
    columns: [user_id,subject_id,rating,type,updated_at,subject_type]
        user_id: [string] user UUID
        subject_id: [int] subject ID, same as input[1].id
        rating: [int] 0-10, 0 means no rating
        type: [string, enum] "wish", "doing", "collect", "on_hold", "dropped" - wish votes are ignored

input[1]: .\bangumi15M\Subjects.csv
    columns: [(index),id,name_cn,name,date,type,score,rating,on_hold,dropped,wish,collect,doing,platform,tags,total_episodes,eps,volumes,locked,nsfw]
        id: [int] subject ID
        name_cn: [string] Chinese name, use name if not exist
        name: [string] Original name
        type: [int, enum] 2: anime - we only consider anime here
        rating: [json] {
            "rank": [int] rank in this category
            "total": [int] total scored votes
        }
        locked: [bool] if locked - locked entries are ignored

output: .\data\ponet.csv
    columns: [id,name,rank,total,total_score,prob_score,simp_score,conf_score]
        id: [int] subject ID
        name: [string] name (Chinese > Original)
        rank: [int] original rank
        total: [int] total scored votes
        total_score, prob_score, simp_score, conf_score: [float] PO-net scores, see below

pseudo code:
    for each subject:
        init total_score, prob_score, simp_score, conf_score to 0
    for each subject A:
        for each subject B (B.id > A.id):
            if number of users rated both A and B >= N:
                let X = number of users rated A > B
                let Y = number of users rated A < B
                transfer (X-Y) from B.total_score to A.total_score
                transfer (X-Y)/N from B.prob_score to A.prob_score
                transfer sgn(X-Y) from B.simp_score to A.simp_score
                transfer (X-Y)/sqrt(N) from B.conf_score to A.conf_score
            else:
                do nothing
    sort according to original rank ascending
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json, csv, time

INPUT_0 = ".\\bangumi15M\\AnonymousUserCollection.csv"
INPUT_1 = ".\\bangumi15M\\Subjects.csv"
TMP_1 = ".\\data\\subjects.csv"
TMP_2 = ".\\data\\relative_votes.csv"
TMP_3 = ".\\data\\unmerged.csv"
OUTPUT = ".\\data\\ponet.csv"

THRESHOLD = 10 # minimum number of users rated both A and B
VOT_MIN = 50 # minimum number of votes to be considered

timer = time.time()

def pre():
    '''
    read data from INPUT_1, preprocess and save to TMP_1
    '''
    df1 = pd.read_csv(INPUT_1, index_col=0)[["id", "name_cn", "name", "type", "rating", "locked"]].reset_index(drop=True)
    df1 = df1[df1["type"] == 2]
    df1 = df1[df1["locked"] == False]
    df1 = df1.fillna({"name_cn": df1["name"]})
    df1["rating"] = df1["rating"].apply(lambda x: x.replace("'", '"'))
    df1["rating"] = df1["rating"].apply(lambda x: json.loads(x))
    df1["rank"] = df1["rating"].apply(lambda x: x["rank"])
    df1["total"] = df1["rating"].apply(lambda x: x["total"])
    df1 = df1[df1["total"] > VOT_MIN]
    df1 = df1.drop(columns=["name", "type", "rating", "locked"])
    df1.to_csv(TMP_1, index=False)
    return len(df1)

'''
input[2]: .\data\subjects.csv (TMP_1)
    replacing INPUT_1
    columns: [id,name_cn,rank,total]
    only valid anime entries with more than VOT_MIN votes
'''

# XXX: YOU NEED TO RUN THIS FIRST
# n = pre()
n = 8573 # entries in INPUT_1

df2 = pd.read_csv(TMP_1)
ids = df2["id"].tolist()

# ["user_id", "subject_id", "rating"]
UID = 0
SID = 1
RAT = 2

def rela():
    '''
    read data from INPUT_0, preprocess and save to TMP_2
    '''
    df0 = pd.read_csv(INPUT_0)[["user_id", "subject_id", "rating"]].reset_index(drop=True)
    df0 = df0.sort_values(by=["user_id", "subject_id"]).reset_index(drop=True)
    df0 = df0[df0["subject_id"].isin(ids)]
    df0 = df0[df0["rating"] > 0]
    len0 = len(df0) # 7770854

    last = time.time()
    print("time elapsed: %.2f" % (last - timer))

    pv = {} # relative positive votes
    nv = {} # relative negative votes
    tv = {} # total votes
    arr = df0.to_numpy()
    cur_begin = 0
    cur_end = 1
    # use double pointer to get this current user's records in rows [cur_begin, cur_end-1]
    while cur_end < len0:
        if arr[cur_end, UID] == arr[cur_begin, UID]:
            cur_end += 1
        else:
            for i in range(cur_begin, cur_end - 1):
                ri = arr[i, RAT]
                if ri == 0:
                    continue
                si = arr[i, SID]
                for j in range(i + 1, cur_end):
                    # it is guaranteed that si < sj
                    rj = arr[j, RAT]
                    if rj == 0:
                        continue
                    sj = arr[j, SID]
                    if ri > rj:
                        pv[(si, sj)] = pv.get((si, sj), 0) + 1
                    elif ri < rj:
                        nv[(si, sj)] = nv.get((si, sj), 0) + 1
                    tv[(si, sj)] = tv.get((si, sj), 0) + 1
            cur_begin = cur_end
            cur_end += 1
            # print cur_begin every minute
            if time.time() - last > 59:
                print("%d %.0f" % (cur_begin, time.time() - timer))
                last = time.time()

    print("time elapsed: %.2f" % (time.time() - timer))

    with open(TMP_2, "w") as f:
        for (si, sj), v in tv.items():
            f.write("%d,%d,%d,%d\n" % (si, sj, v, pv.get((si, sj), 0) - nv.get((si, sj), 0)))

def ponet():
    global df2
    data = np.loadtxt(TMP_2, delimiter=",", dtype=int)
    mask = np.where(data[:, 2] >= THRESHOLD)[0]
    data = data[mask]
    # cols: [si, sj, N, X]
    # print(data.shape) # (19151383, 4)
    si = np.unique(data[:, 0])
    sj = np.unique(data[:, 1])
    _ids = np.union1d(si, sj)
    # print(_ids.shape) # (7696,)
    # print(len(ids)) # 8573 (also n = 8573)
    scores = np.zeros((n, 5))
    # cols: [id, total_score, prob_score, simp_score, conf_score]
    scores[:, 0] = ids
    '''
    scores[si, 1] = sum(data[l, 3] for l in range(data.shape[0]) if data[l, 0] == scores[si, 0])
    also use a map to memory which row each sid is in (since there are only 8573 rows)
    '''
    sid2row = {}
    for l in range(data.shape[0]):
        if l % 1000000 == 0:
            print("%d %.2f" % (l, time.time() - timer))
        _si = data[l, 0]
        if _si not in sid2row:
            sid2row[_si] = np.where(scores[:, 0] == _si)[0][0]
        _sj = data[l, 1]
        if _sj not in sid2row:
            sid2row[_sj] = np.where(scores[:, 0] == _sj)[0][0]
        scores[sid2row[_si], 1] += data[l, 3] # total_score: X
        scores[sid2row[_sj], 1] -= data[l, 3]
        scores[sid2row[_si], 2] += data[l, 3] / data[l, 2] # prob_score: X / N
        scores[sid2row[_sj], 2] -= data[l, 3] / data[l, 2]
        scores[sid2row[_si], 3] += np.sign(data[l, 3]) # simp_score: sgn(X)
        scores[sid2row[_sj], 3] -= np.sign(data[l, 3])
        scores[sid2row[_si], 4] += data[l, 3] / np.sqrt(data[l, 2]) # conf_score: X / sqrt(N)
        scores[sid2row[_sj], 4] -= data[l, 3] / np.sqrt(data[l, 2])
    
    np.savetxt(TMP_3, scores, delimiter=",", fmt="%.0f,%.0f,%.4f,%.0f,%.4f")

    print("time elapsed: %.2f" % (time.time() - timer))

def final():
    # finally, merge df2 and scores
    df3 = pd.read_csv(TMP_3, header=None, names=["id", "total_score", "prob_score", "simp_score", "conf_score"])
    df3 = df3.drop_duplicates(subset=["id"])
    # drop if total_score is 0
    df3 = df3[df3["total_score"] != 0]
    df3 = df3.sort_values(by=["id"]).reset_index(drop=True)
    df4 = pd.merge(df2.drop_duplicates(subset=["id"]), df3, on="id")
    df4.to_csv(OUTPUT, index=False)

def extra():
    # plot the distribution of users' votes count
    df0 = pd.read_csv(INPUT_0)[["user_id", "subject_id", "rating"]].reset_index(drop=True)
    df0 = df0.sort_values(by=["user_id", "subject_id"]).reset_index(drop=True)
    df0 = df0[df0["rating"] > 0]
    counts = df0["user_id"].value_counts()
    plt.hist(counts, bins=500, range=(0, 3000))
    plt.xlabel("Number of entries rated")
    plt.ylabel("Users")
    plt.yscale("log")
    plt.savefig(".\\data\\user_votes.png")
    plt.clf()

    # plot the distribution of subjects' new scores
    df3 = pd.read_csv(TMP_3, header=None, names=["id", "total_score", "prob_score", "simp_score", "conf_score"])
    # scores are only "transfered" from other subjects so the mean must be 0
    # still normalize them to std = 1
    df3["total_score"] /= df3["total_score"].std()
    df3["prob_score"] /= df3["prob_score"].std()
    df3["simp_score"] /= df3["simp_score"].std()

    plt.hist(df3["total_score"], bins=100, color="red", alpha=0.5, label="total_score", range=(-5, 5))
    plt.hist(df3["prob_score"], bins=100, color="green", alpha=0.5, label="prob_score", range=(-5, 5))
    plt.hist(df3["simp_score"], bins=100, color="blue", alpha=0.5, label="simp_score", range=(-5, 5))

    plt.xlabel("Normalized score")
    plt.ylabel("Subjects")
    plt.legend()
    plt.savefig(".\\data\\score_dist.png")
    plt.clf()


def main():
    pre()
    rela()
    ponet()
    final()

if __name__ == "__main__":
    main()