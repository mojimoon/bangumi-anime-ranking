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
_P3S = norm.cdf(3) * 100 # 99.865
_P2S = norm.cdf(2) * 100 # 97.725
_P1S = norm.cdf(1) * 100 # 84.135
_N1S = norm.cdf(-1) * 100 # 15.865
_N2S = norm.cdf(-2) * 100 # 2.275
_N3S = norm.cdf(-3) * 100 # 0.135

def analyze(s, name, fname, n, ofile):
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
    ofile.write("Average of %s,%.4f\n" % (name, mean))
    ofile.write("Standard Deviation of %s,%.4f\n" % (name, std))
    ofile.write("95%%CI,%.4f,%.4f\n" % (mean - 2 * std, mean + 2 * std))
    ofile.write("Extremes,%.4f,%.4f\n" % (lo, hi))
    ofile.write("±3 Sigma,%.4f,%.4f\n" % (p3s, n3s))
    ofile.write("1%%-99%%,%.4f,%.4f\n" % (np.percentile(s, 1), np.percentile(s, 99)))
    ofile.write("±2 Sigma,%.4f,%.4f\n" % (p2s, n2s))
    ofile.write("5%%-95%%,%.4f,%.4f\n" % (np.percentile(s, 5), np.percentile(s, 95)))
    ofile.write("10%%-90%%,%.4f,%.4f\n" % (np.percentile(s, 10), np.percentile(s, 90)))
    ofile.write("15%%-85%%,%.4f,%.4f\n" % (np.percentile(s, 15), np.percentile(s, 85)))
    ofile.write("20%%-80%%,%.4f,%.4f\n" % (np.percentile(s, 20), np.percentile(s, 80)))
    ofile.write("Quartiles,%.4f,%.4f\n" % (lq, uq))
    ofile.write("30%%-70%%,%.4f,%.4f\n" % (np.percentile(s, 30), np.percentile(s, 70)))
    ofile.write("40%%-60%%,%.4f,%.4f\n" % (np.percentile(s, 40), np.percentile(s, 60)))
    ofile.write("Median,%.4f\n" % med)
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

def analyze_exp(s, name, fname, n, ofile):
    '''
    basically same as analyze(), but exponential distribution-like
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
    ofile.write("Average of %s,%.4f\n" % (name, mean))
    ofile.write("Standard Deviation of %s,%.4f\n" % (name, std))
    ofile.write("Extremes,%.0f,%.0f\n" % (lo, hi))
    ofile.write("±3 Sigma,%.0f,%.0f\n" % (p3s, n3s))
    ofile.write("1%%-99%%,%.0f,%.0f\n" % (np.percentile(s, 1), np.percentile(s, 99)))
    ofile.write("±2 Sigma,%.0f,%.0f\n" % (p2s, n2s))
    ofile.write("5%%-95%%,%.0f,%.0f\n" % (np.percentile(s, 5), np.percentile(s, 95)))
    ofile.write("10%%-90%%,%.0f,%.0f\n" % (np.percentile(s, 10), np.percentile(s, 90)))
    ofile.write("15%%-85%%,%.0f,%.0f\n" % (np.percentile(s, 15), np.percentile(s, 85)))
    ofile.write("20%%-80%%,%.0f,%.0f\n" % (np.percentile(s, 20), np.percentile(s, 80)))
    ofile.write("Quartiles,%.0f,%.0f\n" % (lq, uq))
    ofile.write("30%%-70%%,%.0f,%.0f\n" % (np.percentile(s, 30), np.percentile(s, 70)))
    ofile.write("40%%-60%%,%.0f,%.0f\n" % (np.percentile(s, 40), np.percentile(s, 60)))
    ofile.write("Median,%.0f\n" % med)
    plt.hist(s, bins=500, density=True, alpha=.75, color='g')
    plt.yscale('log') # x-log(y)
    plt.axvline(p3s, color='b', linestyle='dashdot', linewidth=.5)
    plt.axvline(p2s, color='b', linestyle='dotted', linewidth=1)
    plt.axvline(uq, color='b', linestyle='dashed', linewidth=1)
    plt.axvline(med, color='r', linestyle='dashed', linewidth=1)
    plt.axvline(lq, color='m', linestyle='dashed', linewidth=1)
    x_diff = (hi - lo) / 500 
    mid_y = plt.ylim()[1] / 100
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


def main():
    df = pd.read_csv(ifile)
    df = df.dropna()
    n = len(df)
    ofile = open(pre + "stat.csv", "w")
    ofile.write("Entries,%d\n" % n)
    ofile.write("Total Votes,%d\n\n" % df['vote'].sum())

    # avg => data/stat/avg.png; negative skew (avg < med)
    avg = df['avg'].values.tolist()
    analyze(avg, "Average", "avg.png", n, ofile)
    # std => data/stat/std.png; positive skew (avg > med)
    std = df['std'].values.tolist()
    analyze(std, "Standard Deviation", "std.png", n, ofile)
    # vote => data/stat/vote.png; exponential distribution
    vote = df['vote'].values.tolist()
    analyze_exp(vote, "Votes", "vote.png", n, ofile)
    ofile.close()

if __name__ == '__main__':
    main()