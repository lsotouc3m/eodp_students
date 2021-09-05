from config.ismConfig import ismConfig
from ism.src.mtf import mtf
from common.plot.plotMat2D import plotMat2D
from common.plot.plotF import plotF

myMtf = mtf([])
myIsmConfig = ismConfig()
directory = '/home/luss/EODP/eodp/ism/test/ut01/output'

# 2D
# ----------------------------------------------------------------
fr = myMtf.freq_2d(myIsmConfig.pix_size, myIsmConfig.npoints)
mtf_jitter = myMtf.mtf_jitter(myIsmConfig.sigma_jitter,fr)
# print(fr)
# print(mtf_jitter)

# Plot
title_str = "2D frequencies"
xlabel_str = 'ACT'
ylabel_str = 'ALT'
saveas_str = 'fr'
plotMat2D(fr, title_str, xlabel_str, ylabel_str, directory, saveas_str)

title_str = "Jitter MTF"
xlabel_str = 'ACT'
ylabel_str = 'ALT'
saveas_str = 'mtf_jitter'
plotMat2D(mtf_jitter, title_str, xlabel_str, ylabel_str, directory, saveas_str)


# 1D
# ----------------------------------------------------------------
u = myMtf.spatial_freq(myIsmConfig.pix_size, myIsmConfig.npoints)
mtf_jitter_1d = myMtf.mtf_jitter(myIsmConfig.sigma_jitter,u)
# print(u)
# print(mtf_jitter)
title_str = "1D spatial frequencies"
xlabel_str = '-'
ylabel_str = '-'
saveas_str = 'u'
plotF(u, [], title_str, xlabel_str, ylabel_str, directory, saveas_str)


title_str = "1D jitter MTF"
xlabel_str = 'Spatial frequencies [m-1]'
ylabel_str = 'MTF [-]'
saveas_str = 'mtf_jitter_1d'
plotF(u, mtf_jitter_1d, title_str, xlabel_str, ylabel_str, directory, saveas_str)
