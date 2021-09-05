
from netCDF4 import Dataset
import numpy as np
import sys
import os
from common.io.mkdirOutputdir import mkdirOutputdir

def readGain(ncfile):

    # Check
    if not os.path.isfile(ncfile):
        sys.exit('File not found ' +ncfile + ". Exiting.")
    print('Reading ' + ncfile)

    # Load dataset
    dset = Dataset(ncfile)

    # Extract data from NetCDF file
    gain = np.array(dset.variables['gain'][:])
    dset.close()
    print('Size of matrix ' + str(gain.shape))

    return gain

def writeGain(outputdir, name, gain):

    # Check output directory
    mkdirOutputdir(outputdir)

    # TOA filename
    savetostr = os.path.join(outputdir, name + '.nc')

    # open a netCDF file to write
    ncout = Dataset(savetostr, 'w', format='NETCDF4')

    # define axis size
    ncout.createDimension('act_columns', len(gain))

    # create variable array
    gainvar = ncout.createVariable('gain', 'float32',
                                            ('act_columns',))
    gainvar.units = 'mW/sr/m2/DN'
    gainvar.description = "Absolute radiometric gain. Digital number to radiance conversion factor."

    # Assign data
    gainvar[:] = gain[:]

    # close files
    ncout.close()

    print("Finished writing: " + savetostr)


