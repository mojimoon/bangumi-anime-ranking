import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

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

def analyze(s, name, fname, n, ofile):
    '''
    s - series to be analyzed
    name - name of the series
    fname - plt file name (including extension)
    n - number of entries
    ofile - output CSV file object
    '''
    mean, std, hi, uq, med, lq, lo, p2s, n2s = \
        np.mean(s), np.std(s), np.max(s), np.percentile(s, 75), \
        np.median(s), np.percentile(s, 25), np.min(s), \
        np.percentile(s, 97.5), np.percentile(s, 2.5)
    ofile.write("Average of %s,%.4f\n" % (name, mean))
    ofile.write("Standard Deviation of %s,%.4f\n" % (name, std))
    ofile.write("Maximum of %s,%.4f\n" % (name, hi))
    ofile.write("+2sigma of %s,%.4f\n" % (name, p2s))
    ofile.write("Upper Quartile of %s,%.4f\n" % (name, uq))
    ofile.write("Median of %s,%.4f\n" % (name, med))
    ofile.write("Lower Quartile of %s,%.4f\n" % (name, lq))
    ofile.write("-2sigma of %s,%.4f\n" % (name, n2s))
    ofile.write("Minimum of %s,%.4f\n" % (name, lo))
    plt.hist(s, bins=250, density=True, alpha=.75)
    x = np.linspace(lo, hi, 1000)
    plt.plot(x, norm.pdf(x, mean, std), color='r', linewidth=.5)
    plt.axvline(p2s, color='b', linestyle='dotted', linewidth=1)
    plt.axvline(uq, color='b', linestyle='dashed', linewidth=1)
    plt.axvline(med, color='r', linestyle='dashed', linewidth=1)
    plt.axvline(lq, color='m', linestyle='dashed', linewidth=1)
    plt.axvline(n2s, color='m', linestyle='dotted', linewidth=1)
    x_diff = (hi - lo) / 500
    mid_y = plt.ylim()[1] / 2
    plt.text(p2s + x_diff, mid_y, f"{p2s:.4f}", rotation=90, va='center', color='b')
    plt.text(uq + x_diff, mid_y, f"{uq:.4f}", rotation=90, va='center', color='b')
    plt.text(med + x_diff, mid_y, f"{med:.4f}", rotation=90, va='center', color='r')
    plt.text(lq + x_diff, mid_y, f"{lq:.4f}", rotation=90, va='center', color='m')
    plt.text(n2s + x_diff, mid_y, f"{n2s:.4f}", rotation=90, va='center', color='m')
    plt.legend(["Normal Dist", "+2 Sigma", "Upper Quartile", "Median", "Lower Quartile", "-2 Sigma"])
    plt.title("Distribution of %s" % name)
    plt.xlabel(name)
    plt.ylabel("Density")
    plt.savefig(pre + fname)
    plt.clf()
    ofile.write("\n")

def analyze_exp(s, name, fname, n, ofile):
    pass

def main():
    df = pd.read_csv(ifile)
    df = df.dropna()
    n = len(df)
    ofile = open(pre + "stat.csv", "w")
    ofile.write("Entries,%d\n\n" % n)

    # avg => data/stat/avg.png; negative skew (avg < med)
    avg = df['avg'].values.tolist()
    analyze(avg, "Average", "avg.png", n, ofile)
    # std => data/stat/std.png; positive skew (avg > med)
    std = df['std'].values.tolist()
    analyze(std, "Standard Deviation", "std.png", n, ofile)
    # vote => data/stat/vote.png; exponential distribution
    # vote = df['vote'].values.tolist()
    # analyze_exp(vote, "Votes", "vote.png", n, ofile)
    ofile.close()

if __name__ == '__main__':
    main()