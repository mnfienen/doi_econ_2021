import numpy as np
import geopandas as gp
import pandas as pd
import matplotlib.pyplot as plt



def find_correlations(pred, responses, gdf):
# function to calculate Pearson's r correlation coefficient for a predictor and list of responses in the (geo)dataframe passed in
# NOTE: need to rop null values, subset to both prediction and response for each pair as some data are indeed missing
#
# returns a list of correlation coefficients in the same order as the reponses
	corrs = []
    for i in responses:
        corrs.append(np.corrcoef(gdf.dropna(subset=[pred,i])[pred].values/gdf.dropna(subset=[pred,i])[pred].max(),
                         gdf.dropna(subset=[pred,i])[i].values/gdf.dropna(subset=[pred,i])[i].max())[0,1])
   # corrs = [np.sign(i) * (i**2) for i in corrs]
    return corrs

def plot_relation(gdf, pred, resp, outfig=None):
	# plot 3 panels. colorfloods of predictor and response, and cross plot (hexbin) along with pearson's r
	# optionally save to an external figure
    fig,ax = plt.subplots(1,3, figsize=(9,4))
    # plot the predictor
    gdf.plot(column=pred, ax=ax[0], legend=True, legend_kwds={'shrink': 0.5}, rasterized=True)
    ax[0].set_title(pred)
    # plot the response
    gdf.plot(column=resp, ax=ax[1], legend=True, legend_kwds={'shrink': 0.5}, rasterized=True)
    ax[1].set_title(resp)
    for i in range(2):
        ax[i].axes.xaxis.set_visible(False)
        ax[i].axes.yaxis.set_visible(False)
    # plot the relationship
    cb = ax[2].hexbin(gdf[pred],gdf[resp],mincnt=1, rasterized=True)
    plt.colorbar(cb, ax=ax[2], shrink=0.5)
    # calculate the correlation coefficent
    r = np.corrcoef(gdf.dropna(subset=[pred,resp])[pred].values,
                         gdf.dropna(subset=[pred,resp])[resp].values)[0,1]
    # calculate the line
    linefit = np.polyfit(gdf.dropna(subset=[pred,resp])[pred].values,
                         gdf.dropna(subset=[pred,resp])[resp].values,1)
    ax[2].set_title(f"Pearson's r = {r:0.2f}")
    minpred,maxpred = gdf[pred].min(),gdf[pred].max()
    ax[2].plot([minpred,maxpred],
              [linefit[1]+linefit[0]*minpred,linefit[1]+linefit[0]*maxpred],'r')
    ax[2].set_box_aspect(1)
    ax[2].set_xlabel(pred)
    ax[2].set_ylabel(resp)
    
    plt.suptitle(f'Evaluating relationship between {pred} and {resp}', fontsize=14)
    plt.tight_layout()
    if outfig is not None:
        outfig.savefig()
        plt.close('all')