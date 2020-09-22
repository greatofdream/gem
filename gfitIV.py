import pandas as pd, argparse
import matplotlib.pyplot as plt
import numpy as np, h5py
psr = argparse.ArgumentParser()
psr.add_argument('-1', dest="ch1", nargs='+', help="input ch1 xlsx file")
psr.add_argument('-p', dest="prefix", help="prefix")
psr.add_argument('-d', dest="distance", help="distance", type=int)
psr.add_argument('-o', dest='opt', help="output h5 file")
args = psr.parse_args()
intVoltage = np.zeros(len(args.ch1))
realVoltage = np.zeros(len(args.ch1))
with h5py.File(args.opt, 'w') as opt:
    for i, ci in enumerate(args.ch1):
        #ch1 = pd.read_csv(args.prefix+ci+'_Ch1.csv', usecols=[3,4], index_col=None, names=['time','voltage'], na_values=['NA'])
        ch2 = pd.read_csv(args.prefix+ci+'_Ch2.csv', usecols=[3,4], index_col=None, names=['time','voltage'], na_values=['NA'])
        chLength = ch2.shape[0]
        noisemean = ch2['voltage'][:1500].mean()
        noisestd = ch2['voltage'][:1500].std()
        ch2['volNoNoise'] = ch2['voltage']-noisemean
        print('noise mean:{};noise std:{}'.format(noisemean, noisestd))
        ch2['sumvol']=ch2['volNoNoise'].cumsum()
        intVoltage[i] = np.max(ch2['sumvol'])
        realVoltage[i] = np.int(ci)*100/args.distance
        opt.create_dataset('{}'.format(ci), data=ch2, compression='gzip')
z = np.polyfit(realVoltage, intVoltage, 1)
p = np.poly1d(z)
fig, ax = plt.subplots()
# time interval 1e-10,f interval 1e10/5000
ax.scatter(realVoltage, intVoltage, label='integral voltage ~ real voltage')
ax.plot(realVoltage, p(realVoltage), label='fit k={}'.format(z[0]))
ax.set_xlabel('real voltage/Vm^-1')
ax.set_ylabel('integral voltage')
ax.set_title('integral voltage ~ real voltage')
ax.legend()
fig.savefig(args.opt.replace('.h5', '.png'))
plt.close()