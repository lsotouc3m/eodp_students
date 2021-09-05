from common.io.writeToa import readToa
import numpy as np

dir1 = "/home/luss/EODP/eodp/l1c/test/ut01/output1/"
dir2 = "/home/luss/EODP/eodp/l1c/test/ut01/output2/"


toa1 = readToa(dir1, "l1c_toa_VNIR-0.nc")
toa2 = readToa(dir2, "l1c_toa_VNIR-0.nc")
print(np.max(toa1) == np.max(toa2))
print(np.min(toa1) == np.min(toa2))
np.sort
luss=0
