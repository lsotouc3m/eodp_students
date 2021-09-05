import matplotlib.pyplot as plt
from common.io.readIsrf import readIsrf

# Inputs
# ------------------------------------------------------------------------------------------
bands = ['VNIR-0','VNIR-1','VNIR-2','VNIR-3']
isrffile = '/home/luss/EODP/eodp/auxiliary/isrf/ISRF_'
directory = '/home/luss/EODP/eodp/ism/test/ut01/output'

# Plot
# ------------------------------------------------------------------------------------------

fig = plt.figure(figsize=(20,10))

for b in bands:
    isrf, wv = readIsrf(isrffile, b)
    plt.plot(wv, isrf, label=b)

plt.title('ISRF', fontsize=20)
plt.xlabel('Wavelegnths [um]', fontsize=16)
plt.ylabel('ISRF', fontsize=16)
plt.grid()
plt.legend()
saveas_str = 'isrf_lstm'
savestr = directory + "/" + saveas_str
plt.savefig(savestr)
plt.close(fig)
print("Saved image " + savestr)
