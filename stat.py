import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm, pearsonr, mode

'''
STEP3: perform statistical analysis (stat)

Format of CSV file:
sid,title,s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,rank,vote,avg,std,user
sid, s1, s2, ..., s10, rank, vote, user - integer
title - string
avg, std - float

CSV start with a header line, end with a newline character
All other entries are valid

Task:
    * plot the distribution of avg, std and vote
    * plot the relationship between avg and rank, std and vote, vote and user
    * plot the distribution of s1, s2, ..., s10 over all entries,
        i.e. the distribution of 1, 2, ..., 10 in all users' votes
'''

ifile = "data\\sub.csv"
pre = "data\\stat\\"
_P3S = norm.cdf(3) * 100 # 99.865
_P2S = norm.cdf(2) * 100 # 97.725
_P1S = norm.cdf(1) * 100 # 84.135
_N1S = norm.cdf(-1) * 100 # 15.865
_N2S = norm.cdf(-2) * 100 # 2.275
_N3S = norm.cdf(-3) * 100 # 0.135

def x_stat(s, name, fname, n, ofile):
    '''
    params:
    s - series to be analyzed
    name - name of the series
    fname - plt file name (including extension)
    n - number of entries
    ofile - output CSV file object
    '''
    mean, std, hi, uq, med, lq, lo, p2s, n2s, p3s, n3s = \
        np.mean(s), np.std(s), np.max(s), np.percentile(s, 75), \
        np.median(s), np.percentile(s, 25), np.min(s), \
        np.percentile(s, _P2S), np.percentile(s, _N2S), \
        np.percentile(s, _P3S), np.percentile(s, _N3S)
    ofile.write("Average of %s,%.4f,\n" % (name, mean))
    ofile.write("Standard Deviation of %s,%.4f,\n" % (name, std))
    ofile.write("95%%CI,%.4f,%.4f\n" % (mean - 2 * std, mean + 2 * std))
    ofile.write("Extremes,%.4f,%.4f\n" % (lo, hi))
    ofile.write("±3 Sigma,%.4f,%.4f\n" % (p3s, n3s))
    ofile.write("1%%-99%%,%.4f,%.4f\n" % (np.percentile(s, 1), np.percentile(s, 99)))
    ofile.write("±2 Sigma,%.4f,%.4f\n" % (p2s, n2s))
    ofile.write("5%%-95%%,%.4f,%.4f\n" % (np.percentile(s, 5), np.percentile(s, 95)))
    ofile.write("10%%-90%%,%.4f,%.4f\n" % (np.percentile(s, 10), np.percentile(s, 90)))
    ofile.write("15%%-85%%,%.4f,%.4f\n" % (np.percentile(s, 15), np.percentile(s, 85)))
    ofile.write("20%%-80%%,%.4f,%.4f\n" % (np.percentile(s, 20), np.percentile(s, 80)))
    ofile.write("25%%-75%%,%.4f,%.4f\n" % (lq, uq))
    ofile.write("30%%-70%%,%.4f,%.4f\n" % (np.percentile(s, 30), np.percentile(s, 70)))
    ofile.write("40%%-60%%,%.4f,%.4f\n" % (np.percentile(s, 40), np.percentile(s, 60)))
    ofile.write("Median,%.4f,\n" % med)
    plt.hist(s, bins=250, density=True, alpha=.75, color='g')
    x = np.linspace(lo, hi, 1000)
    plt.plot(x, norm.pdf(x, mean, std), color='r', linewidth=.5)
    plt.axvline(p3s, color='b', linestyle='dashdot', linewidth=.5)
    plt.axvline(p2s, color='b', linestyle='dotted', linewidth=1)
    plt.axvline(uq, color='b', linestyle='dashed', linewidth=1)
    plt.axvline(med, color='r', linestyle='dashed', linewidth=1)
    plt.axvline(lq, color='m', linestyle='dashed', linewidth=1)
    plt.axvline(n2s, color='m', linestyle='dotted', linewidth=1)
    plt.axvline(n3s, color='m', linestyle='dashdot', linewidth=.5)
    x_diff = (hi - lo) / 500 # absolute dx: 1/500 of the plot width
    mid_y = plt.ylim()[1] / 2 # absolute y: middle of the plot height
    plt.text(p3s + x_diff, mid_y, f"{p3s:.3f}", rotation=90, va='center', color='b')
    plt.text(p2s + x_diff, mid_y, f"{p2s:.3f}", rotation=90, va='center', color='b')
    plt.text(uq + x_diff, mid_y, f"{uq:.3f}", rotation=90, va='center', color='b')
    plt.text(med + x_diff, mid_y, f"{med:.3f}", rotation=90, va='center', color='r')
    plt.text(lq + x_diff, mid_y, f"{lq:.3f}", rotation=90, va='center', color='m')
    plt.text(n2s + x_diff, mid_y, f"{n2s:.3f}", rotation=90, va='center', color='m')
    plt.text(n3s + x_diff, mid_y, f"{n3s:.3f}", rotation=90, va='center', color='m')
    plt.legend(["Normal Dist", "+3 Sigma", "+2 Sigma", "Upper Quartile", "Median", "Lower Quartile", "-2 Sigma", "-3 Sigma"])
    plt.title("Distribution of %s" % name)
    plt.xlabel(name)
    plt.ylabel("Density")
    plt.savefig(pre + fname)
    plt.clf()
    ofile.write("\n")

def x_nodist(s, name, fname, n, ofile):
    '''
    basically same as x_stat()
    the distribution decays faster than exponential but slower than gumbel (e^e^x)
    try to fit the distribution with a half-normal distribution
    params:
    s - series to be analyzed
    name - name of the series
    fname - plt file name (including extension)
    n - number of entries
    ofile - output CSV file object
    '''
    mean, std, hi, uq, med, lq, lo, p2s, n2s, p3s, n3s = \
        np.mean(s), np.std(s), np.max(s), np.percentile(s, 75), \
        np.median(s), np.percentile(s, 25), np.min(s), \
        np.percentile(s, _P2S), np.percentile(s, _N2S), \
        np.percentile(s, _P3S), np.percentile(s, _N3S)
    ofile.write("Average of %s,%.4f,\n" % (name, mean))
    ofile.write("Standard Deviation of %s,%.4f,\n" % (name, std))
    ofile.write("Extremes,%.0f,%.0f\n" % (lo, hi))
    ofile.write("±3 Sigma,%.0f,%.0f\n" % (p3s, n3s))
    ofile.write("1%%-99%%,%.0f,%.0f\n" % (np.percentile(s, 1), np.percentile(s, 99)))
    ofile.write("±2 Sigma,%.0f,%.0f\n" % (p2s, n2s))
    ofile.write("5%%-95%%,%.0f,%.0f\n" % (np.percentile(s, 5), np.percentile(s, 95)))
    ofile.write("10%%-90%%,%.0f,%.0f\n" % (np.percentile(s, 10), np.percentile(s, 90)))
    ofile.write("15%%-85%%,%.0f,%.0f\n" % (np.percentile(s, 15), np.percentile(s, 85)))
    ofile.write("20%%-80%%,%.0f,%.0f\n" % (np.percentile(s, 20), np.percentile(s, 80)))
    ofile.write("25%%-75%%,%.0f,%.0f\n" % (lq, uq))
    ofile.write("30%%-70%%,%.0f,%.0f\n" % (np.percentile(s, 30), np.percentile(s, 70)))
    ofile.write("40%%-60%%,%.0f,%.0f\n" % (np.percentile(s, 40), np.percentile(s, 60)))
    ofile.write("Median,%.0f,\n" % med)
    plt.hist(s, bins=500, density=True, alpha=.75, color='g')
    plt.yscale('log') # x-log(y)
    # x = np.linspace(lq, med, 100)
    # plt.plot(x, halfnorm.pdf(x, loc=lo, scale=med-lo), color='r', linewidth=1)
    plt.axvline(p3s, color='b', linestyle='dashdot', linewidth=.5)
    plt.axvline(p2s, color='b', linestyle='dotted', linewidth=1)
    plt.axvline(uq, color='b', linestyle='dashed', linewidth=1)
    plt.axvline(med, color='r', linestyle='dashed', linewidth=1)
    plt.axvline(lq, color='m', linestyle='dashed', linewidth=1)
    x_diff = (hi - lo) / 500 
    mid_y = plt.ylim()[1] / pow(2000, 1/2) # roughly center of the log scale
    plt.text(p3s + x_diff, mid_y, f"{p3s:.0f}", rotation=90, va='center', color='b')
    plt.text(p2s + x_diff, mid_y, f"{p2s:.0f}", rotation=90, va='center', color='b')
    plt.text(uq + x_diff, mid_y, f"{uq:.0f}", rotation=90, va='center', color='b')
    plt.text(med + x_diff, mid_y, f"{med:.0f}", rotation=90, va='center', color='r')
    plt.legend(["+3 Sigma", "+2 Sigma", "Upper Quartile", "Median", "Lower Quartile"])
    plt.title("Distribution of %s" % name)
    plt.xlabel(name)
    plt.ylabel("Density")
    plt.savefig(pre + fname)
    plt.clf()
    ofile.write("\n")

def x_discr(s, x1, name, fname, n, ofile):
    '''
    params:
    s - series to be analyzed (y values)
    x1 - additional series for comparison (x values)
    name - name of the series
    fname - plt file name (including extension)
    n - number of entries
    ofile - output CSV file object
    '''
    mean = sum((i + 1) * s[i] for i in range(0, 10)) / n
    std = np.sqrt(sum((i + 1 - mean) ** 2 * s[i] for i in range(0, 10)) / n)
    pre_sum = 0
    max_idx = 0
    mid_idx = 0
    for i in range(0, 10):
        pre_sum += s[i]
        if pre_sum > n // 2:
            mid_idx = i
            pre_sum = -999999999
        if s[i] > s[max_idx]:
            max_idx = i
    mid_idx += 1
    max_idx += 1
    ofile.write("Average of %s,%.4f,\n" % (name, mean))
    ofile.write("Standard Deviation of %s,%.4f,\n" % (name, std))
    ofile.write("Median of %s,%d,\n" % (name, mid_idx))
    ofile.write("Mode of %s,%d,\n" % (name, max_idx))
    for i in range(10, 0, -1):
        ofile.write("Vote %d,%d,%.2f%%\n" % (i, s[i - 1], s[i - 1] / n * 100))
    # convert to probability density
    plt.bar(range(1, 11), s / n, width=.8, color='g', alpha=.75)
    plt.hist(x1, bins=250, density=True, alpha=.25, color='b')
    plt.axvline(mean, color='b', linestyle='dashed', linewidth=1)
    x1_mean = np.mean(x1)
    plt.axvline(x1_mean, color='m', linestyle='dashed', linewidth=1)
    x_diff = (10 - 1) / 250 # hi = 10, lo = 1
    mid_y = plt.ylim()[1] / 1.9
    plt.text(mean + x_diff, mid_y, f"{mean:.4f}", rotation=90, va='center', color='b')
    plt.text(x1_mean + x_diff, mid_y, f"{x1_mean:.4f}", rotation=90, va='center', color='m')
    lnsp = np.linspace(1, 10, 100)
    plt.plot(lnsp, norm.pdf(lnsp, loc=mean, scale=std), color='r', linewidth=1)
    plt.title("Distribution of All Votes and Entry Average")
    plt.xlabel("Score")
    plt.ylabel("Density")
    plt.xticks(range(1, 11))
    plt.legend(["Average of Votes", "Average of Average", "Votes Normal Dist", "All User Votes", "Entry Average"])
    plt.savefig(pre + fname)
    plt.clf()
    ofile.write("\n")

def xy_corr(x, y, xname, yname, fname, n, ofile):
    '''
    params:
    x, y - series to be analyzed
    xname, yname - name of the series (for labeling)
    fname - plt file name (including extension)
    n - number of entries
    ofile - output CSV file object
    '''
    r, p = pearsonr(x, y)
    ofile.write("Correlation between %s and %s,%.4f,\n" % (xname, yname, r))
    plt.scatter(x, y, s=1, alpha=.5, color='g')
    plt.title("Correlation between %s and %s" % (xname, yname))
    plt.xlabel(xname)
    plt.ylabel(yname)
    m, b = np.polyfit(x, y, 1) # draw the linear regression line
    ofile.write("%s = a * %s + b,%.6f,%.6f\n" % (yname, xname, m, b))
    plt.plot(x, m*np.float64(x) + b, color='b', linewidth=.5)
    plt.legend(["Data", "Linear Regression"])
    plt.savefig(pre + fname)
    plt.clf()
    ofile.write("\n")

def xy(x, y, xname, yname, fname, n, ofile, xs='linear', ys='linear'):
    '''
    basically the same as xy_corr(), but no linear regression line
    params:
    x, y - series to be analyzed
    xname, yname - name of the series (for labeling)
    fname - plt file name (including extension)
    n - number of entries
    ofile - output CSV file object
    '''
    plt.scatter(x, y, s=1, alpha=.5, color='g')
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.xscale(xs)
    plt.yscale(ys)
    plt.title("Relation between %s and %s" % (xname, yname))
    plt.savefig(pre + fname)
    plt.clf()

def main():
    df = pd.read_csv(ifile)
    df = df.dropna()
    n = len(df)
    sum_votes = df['vote'].sum()
    ofile = open(pre + "stat.csv", "w")
    ofile.write("Entries,%d,\n" % n)
    ofile.write("Total Votes,%d,\n\n" % sum_votes)

    # avg => data/stat/avg.png; negative skew (avg < med)
    avg = df['avg'].values.tolist()
    x_stat(avg, "Average", "avg.png", n, ofile)
    # std => data/stat/std.png; positive skew (avg > med)
    std = df['std'].values.tolist()
    x_stat(std, "Standard Deviation", "std.png", n, ofile)
    # vote => data/stat/vote.png
    vote = df['vote'].values.tolist()
    x_nodist(vote, "Votes", "vote.png", n, ofile)
    # rank(x) vs avg(y) => data/stat/rank_avg.png; negative correlation
    rank = df['rank'].values.tolist() # in the same order as avg
    xy_corr(rank, avg, "Rank", "Average", "rank_avg.png", n, ofile)
    # user(x) vs vote(y) => data/stat/user_vote.png; positive correlation
    user = df['user'].values.tolist()
    xy_corr(user, vote, "User", "Votes", "user_vote.png", n, ofile)
    # vote(x) vs std(y) => data/stat/vote_std.png; R~0.62
    xy(vote, std, "Votes", "Standard Deviation", "vote_std.png", n, ofile, xs='log')
    # rank(x) vs std(y) => data/stat/rank_std.png
    xy(rank, std, "Rank", "Standard Deviation", "rank_std.png", n, ofile)
    # rank(x) vs vote(y) => data/stat/rank_vote.png; not worth analyzing
    # xy(rank, vote, "Rank", "Votes", "rank_vote.png", n, ofile)
    # avg(x) vs std(y) => data/stat/avg_std.png
    xy(avg, std, "Average", "Standard Deviation", "avg_std.png", n, ofile)
    # vote(x) vs avg(y) => data/stat/vote_avg.png; R~0.35, no strong correlation
    xy(vote, avg, "Votes", "Average", "vote_avg.png", n, ofile, xs='log')
    # s1, ..., s10
    ss = [sum(df['s%d' % i].values.tolist()) for i in range(1, 11)]
    x_discr(ss, avg, "All User Votes", "vote_breakdown.png", sum_votes, ofile)
    ofile.close()

if __name__ == '__main__':
    main()