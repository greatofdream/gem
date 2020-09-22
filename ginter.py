import pandas as pd, argparse
import matplotlib.pyplot as plt
import numpy as np
psr = argparse.ArgumentParser()
psr.add_argument('-1', dest="ch1", help="input ch1 xlsx file")
#psr.add_argument('-2', dest="ch2", help="input ch2 xlsx file")
#psr.add_argument('-m', dest="math", help="input math xlsx file")
#psr.add_argument('-o', dest="output", help="output txt file")
args = psr.parse_args()
args.ch2 = args.ch1 + '_Ch2.csv'
prefix = args.ch1.split('/')[-1]
tmpch1 = args.ch1
args.math = args.ch1 + '_Math1.csv'
args.output = args.ch1 + '_Voltage.png'
args.ch1 = args.ch1 + '_Ch1.csv'
# , skiprows=range(6)
#ch1 = pd.read_csv(args.ch1, usecols=[3,4], index_col=None, names=['time','voltage'], na_values=['NA'])
ch2 = pd.read_csv(args.ch2, usecols=[3,4], index_col=None, names=['time','voltage'], na_values=['NA'])
math = pd.read_csv(args.math, usecols=[3,4], index_col=None, names=['time','voltage'], na_values=['NA'])
chLength = ch2.shape[0]
noisemean = ch2['voltage'][:1500].mean()
noisestd = ch2['voltage'][:1500].std()
ch2['volNoNoise'] = ch2['voltage']-noisemean
print('noise mean:{};noise std:{}'.format(noisemean, noisestd))
ch2['sumvol']=ch2['volNoNoise'].cumsum()

fig, ax = plt.subplots()
#ax.plot(ch1['time'], ch1['sumvol'], label='ch1')
ax.plot(ch2['time'], ch2['voltage'], label='ch2')
ax.plot(math['time'], math['voltage'], label='math')
ax.set_title('{} voltage'.format(prefix))
ax.legend()
fig.savefig(args.output)
plt.close()

fig, ax = plt.subplots()
# time interval 1e-10,f interval 1e10/5000
ax.plot(np.arange(chLength)/500, np.abs(np.fft.fft(ch2['sumvol'])), label='ch2 fft')
ax.set_xlabel('f/GHz')
ax2 = ax.twiny()
color = 'tab:red'
ax2.set_xlabel('f/GHz', color=color)
ax2.plot(np.arange(500)/500, np.abs(np.fft.fft(ch2['sumvol'])[0:500]), label='ch1 fft 0-1GHz', color=color)
ax2.tick_params(axis='x', labelcolor=color)
ax2.legend(loc=9)
ax.set_title('{} fft frequency'.format(prefix))
ax.legend()
fig.savefig(tmpch1+'_fft.png')
plt.close()
#print(ch)