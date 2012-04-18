#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      heistermann
#
# Created:     28.10.2011
# Copyright:   (c) heistermann 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import wradlib.adjust as adjust

if __name__ == '__main__':

    import numpy as np
    import pylab as pl

    #---------------------------------------------------------------------------
    # Creating synthetic data
    # --------------------------------------------------------------------------
    # number of points of raw per axis (total number of points of raw will be num_raw**2)
    num_raw = 100
    num_obs = 50
    # making raw coordinates
    raw_coords = np.meshgrid(np.linspace(0,100,num_raw), np.linspace(0,100,num_raw))
    raw_coords = np.vstack((raw_coords[0].ravel(), raw_coords[1].ravel())).transpose()
    # making raw data
    raw = np.abs(np.sin(0.1*raw_coords).sum(axis=1))
    # indices for creating obs from raw
    obs_ix = np.random.uniform(low=0, high=num_raw**2, size=num_obs).astype('i4')
    # creating obs_coordinates
    obs_coords = raw_coords[obs_ix]
    # creating obs data by perturbing raw
    obs = raw[obs_ix]+np.random.uniform(low=-1., high=1, size=len(obs_ix))
    obs = np.abs(obs)

    #---------------------------------------------------------------------------
    # Gage adjustment
    #---------------------------------------------------------------------------
    adjuster = adjust.AdjustAdd(obs_coords, raw_coords, stat='median', p_idw=2.)
    result = adjuster(obs, raw)

    #---------------------------------------------------------------------------
    # Plotting
    #---------------------------------------------------------------------------
    # maximum value for normalisation
    maxval = np.max(np.concatenate((raw, obs, result)).ravel())
    # open figure
    fig = pl.figure()
    # adding subplot for unadjusted
    ax = fig.add_subplot(221, aspect='equal')
    raw_plot = ax.scatter(raw_coords[:,0], raw_coords[:,1], c=raw, vmin=0, vmax=maxval, edgecolor='none')
    ax.scatter(obs_coords[:,0], obs_coords[:,1], c=obs.ravel(), marker='s', s=50, vmin=0, vmax=maxval)
    pl.colorbar(raw_plot)
    pl.title('Raw field and observations')
    # adding subplot for adjusted
    ax = fig.add_subplot(222, aspect='equal')
    raw_plot = ax.scatter(raw_coords[:,0], raw_coords[:,1], c=result, vmin=0, vmax=maxval, edgecolor='none')
    ax.scatter(obs_coords[:,0], obs_coords[:,1], c=obs.ravel(), marker='s', s=50, vmin=0, vmax=maxval)
    pl.colorbar(raw_plot)
    pl.title('Adjusted field and observations')
    # scatter plot raw vs. obs
    ax = fig.add_subplot(223, aspect='equal')
    ax.scatter(obs, raw[obs_ix])
    ax.plot([0,maxval],[0,maxval],'-', color='grey')
    pl.title('Scatter plot raw vs. obs')
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    # scatter adjusted vs. raw (for control purposes)
    ax = fig.add_subplot(224, aspect='equal')
    ax.scatter(obs, result[obs_ix])
    ax.plot([0,maxval],[0,maxval],'-', color='grey')
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    pl.title('Scatter plot adjusted vs. obs')

    pl.show()
    pl.close()

