import pandas as pd
import numpy as np
import math

'''
STEP 4: attempt to rank the entries in different algorithms (rank)
read the data from data/sub.csv
the columns are: sid,title,s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,rank,vote,avg,std,user

first, read statistics from data/stat/stat.csv
'''
stat_fin = open('data/stat/stat.csv', 'r')
stat = stat_fin.readlines()
stat_fin.close()
ENT = int(stat[0].split(',')[1]) # 6565
VOT = int(stat[1].split(',')[1]) # 7573022
AVG_AVG = float(stat[3].split(',')[1]) # 6.663702
AVG_STD = float(stat[4].split(',')[1]) # 0.860932
AVG_MED = float(stat[17].split(',')[1]) # 6.707071
VOT_MED = int(stat[48].split(',')[1]) # 395
AVG_ALL = float(stat[56].split(',')[1]) # 7.185439
STD_ALL = float(stat[57].split(',')[1]) # 1.509041
MED_ALL = int(stat[58].split(',')[1]) # 7
VOT_MIN = 51 # minimum number of votes to be considered
VOTS = [int(stat[69 - i].split(',')[1]) / VOT for i in range(10)]
# 0.006270 0.004244 0.008782 0.023513 0.063677 0.172864 0.288221 0.271895 0.103328 0.057206


entries = []

df = pd.read_csv('data/sub.csv', header=0).drop(['user'], axis=1)

ofile = open('data/rank/log.txt', 'w')

def bayesian():
    '''
    bayesian average = (i_votes * i_avg + vote * avg) / (i_votes + vote)
    where i_vote and i_avg are imaginary votes and average
    usually i_vote = minimal votes threshold, i_avg = average of all entries
    '''
    global df
    # calculate the bayesian average
    # the imaginary votes number = VOT_MIN, value = AVG_AVG
    df.loc[:,'bayes'] = (VOT_MIN * AVG_AVG + df['vote'] * df['avg']) / (VOT_MIN + df['vote'])
    # sort by bayesian average and give bayes_rank
    df = df.sort_values(by=['bayes'], ascending=False)
    df.loc[:,'b_rank'] = np.arange(1,ENT+1)
    # calculate the distance between bayes_rank and rank
    # definition: sum(abs(b_rank - rank)) / (ENT * (ENT - 1) / 2)
    ofile.write(f'Bayesian Average Rank Distance: {sum(abs(df["b_rank"] - df["rank"])) / (ENT * (ENT - 1) / 2):.8f}\n')

def steamdb():
    '''
    steamdb average = r - (r - 0.5) * 2 ^ (-log10(v + 1))
    where r = average rating (converted to 0-1 scale), v = number of votes
    '''
    global df
    # recalculate the weighted average
    # (0/9 * s1 + 1/9 * s2 + 2/9 * s3 + ... + 9/9 * s10) / (s1 + s2 + ... + s10)
    df.loc[:, 'avg_1'] = \
        sum([df['s'+str(i)] * (i-1) for i in range(1,11)]) / sum([df['s'+str(i)] for i in range(1,11)]) / 9
    df.loc[:, 'steamdb'] = df['avg_1'] - (df['avg_1'] - 0.5) * 2 ** (-np.log10(df['vote'] + 1))
    df = df.sort_values(by=['steamdb'], ascending=False)
    df.loc[:, 's_rank'] = np.arange(1,ENT+1)
    ofile.write(f'SteamDB Average Rank Distance: {sum(abs(df["s_rank"] - df["rank"])) / (ENT * (ENT - 1) / 2):.8f}\n')

def wilson():
    '''
    wilson's interval lower bound = (p + z^2/(2n) - z * sqrt((p*(1-p)+z^2/(4n))/n)) / (1 + z^2/n)
    where p = average rating (converted to 0-1 scale), n = number of votes, z = 1.96 (95% confidence)
    '''
    global df
    df.loc[:, 'wilson'] = (df['avg_1'] + 1.96**2/(2*df['vote']) - 1.96 * np.sqrt((df['avg_1']*(1-df['avg_1'])+1.96**2/(4*df['vote']))/df['vote'])) / (1 + 1.96**2/df['vote'])
    df = df.sort_values(by=['wilson'], ascending=False)
    df.loc[:, 'w_rank'] = np.arange(1,ENT+1)
    ofile.write(f'Wilson\'s Interval Lower Bound Rank Distance: {sum(abs(df["w_rank"] - df["rank"])) / (ENT * (ENT - 1) / 2):.8f}\n')


def output():
    _df = df.sort_values(by=['rank']).drop(['s1','s2','s3','s4','s5','s6','s7','s8','s9','s10'], axis=1)
    # output only keep 4 decimal places
    _df.to_csv('data/rank/rank.csv', index=False, float_format='%.4f')


def main():
    bayesian()
    steamdb()
    wilson()
    output()

if __name__ == '__main__':
    main()