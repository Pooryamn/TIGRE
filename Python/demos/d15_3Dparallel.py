#%% DEMO 15: 3D parallel tomgoraphy
#
#
# This demo shows how to run 3D paralel geometry
#
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# This file is part of the TIGRE Toolbox
#
# Copyright (c) 2015, University of Bath and
#                     CERN-European Organization for Nuclear Research
#                     All rights reserved.
#
# License:            Open Source under BSD.
#                     See the full license at
#                     https://github.com/CERN/TIGRE/blob/master/LICENSE
#
# Contact:            tigre.toolbox@gmail.com
# Codes:              https://github.com/CERN/TIGRE/
# Coded by:           Ander Biguri
# --------------------------------------------------------------------------
#%%Initialize
import tigre
import numpy as np
from tigre.utilities import sample_loader
from tigre.utilities import CTnoise
import tigre.algorithms as algs

#%% Geometry
# While you can defien you rown geometry, the easiest way is:

# just give as nVoxel the same number as your projection size.
geo = tigre.geometry(
    mode="parallel", nVoxel=np.array([512, 512, 512])
)  # Parallel beam geometry does not require anything other than the image size.


#%% Load data and generate projections
# define angles
angles = np.linspace(0, 2 * np.pi, 100)
# Load thorax phantom data
head = sample_loader.load_head_phantom(geo.nVoxel)
# generate projections
projections = tigre.Ax(head, geo, angles)
# add noise
noise_projections = CTnoise.add(projections, Poisson=1e5, Gaussian=np.array([0, 10]))

# recon
imgFBP = algs.fbp(projections, geo, angles)
imgOSSART = algs.ossart(projections, geo, angles, 40)

# plot
tigre.plotImg(np.concatenate([head, imgFBP, imgOSSART], axis=1), dim="z", step=3)
