#!/usr/bin/env python           
                                                                                                                     
############################################################################
# Copyright (C) 2016  John J. Oh
#                                                                                                                                    
# This program is free software; you can redistribute it and/or modify it                                                            
# under the terms of the GNU General Public License as published by the                                                              
# Free Software Foundation; either version 2 of the License, or (at your                                                             
# option) any later version.                                                                                                         
#                                                                                                                                    
# This program is distributed in the hope that it will be useful, but                                                                
# WITHOUT ANY WARRANTY; without even the implied warranty of                                                                         
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General                                                          
# Public License for more details.                                                                                                   
#                                                                                                                                    
# You should have received a copy of the GNU General Public License along                                                            
# with this program; if not, write to the Free Software Foundation, Inc.,                                                            
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.                                                                      
#############################################################################
"""
CAGMon-2.0: This Code provides a correlated channel list between GW channel 
and Auxiliary Channels of Gravitational Wave Detectors. This program uses time-series
data with splitted by a time-stride (default 0.1sec), generating correlation
matrices for auxiliary channels of each subsystem.
"""

__author__  = "John J. Oh <john.oh@ligo.org>"
#__version__ = git_version.id                                                                                                        
#__date__    = git_version.date   

import numpy as np
import scipy as sp
from scipy.stats import pearsonr
from scipy.stats import kendalltau
from minepy import MINE
import os
import sys
import glob
from os import makedirs
from os.path import isdir, exists
from sys import exit
from optparse import *
from pylal import seriesutils
from glue import lal
import matplotlib.pyplot as plt
from pylab import *
import matplotlib as mpl
from os import listdir
from mpl_toolkits.axes_grid1 import make_axes_locatable
matplotlib.rcParams['text.usetex']=False
matplotlib.rcParams['text.latex.unicode']=False
import ConfigParser
config=ConfigParser.ConfigParser()

parser=OptionParser(usage="CAGMon", version="2.0")
parser.add_option("-s", "--gps-start-time", action="store", type="int", default="00000", help="start gps time")
parser.add_option("-e", "--gps-end-time", action="store", type="int", default="00000", help="end gps time")
parser.add_option("-o", "--ifo", action="store", type="string", default="H", help="ifos:L, H, K")
parser.add_option("-r", "--run-data", action="store", type="string", default="ER8", help="ER8, O1, O2, K1")
parser.add_option("-f", "--sampling-rate", action="store", type="string", default="4096", help="sampling rate: 2048, 4098, 8196, etc")
parser.add_option("-c", "--channel-list", action="store", type="string", default="none", help="auxiliary channel list")
parser.add_option("-t", "--time-stride", action="store", type="float", default="0.125", help="time stride to be splitted")
(opts, files)=parser.parse_args()
stime=str(opts.gps_start_time)
etime=str(opts.gps_end_time)
obs=opts.ifo
SamRate=opts.sampling_rate
ChanList=opts.channel_list
TimeStride=opts.time_stride
RunData=opts.run_data
dur=int(etime)-int(stime)

tmpdir='tmp'
sortlist=listdir(tmpdir)
sortlist.sort()
for i in range(len(sortlist)):
    gstart=int(sortlist[i].split('.')[1])
    gdur=int(sortlist[i].split('.')[2])
    gend=int(gstart+gdur)
    if gstart <= int(stime) and gend >= int(etime):
        config.read(tmpdir+'/'+sortlist[i])
        break
    else:
        pass

ResDir=os.getenv("HOME")+'/public_html'

if isdir(ResDir):
    print "Directory exists:", ResDir
else:
    print "Creating directory", ResDir
    makedirs(ResDir)

Dir=ResDir+'/'+RunData+'.'+str(gstart)+'.'+str(gdur)+'.'+SamRate+'.'+str(TimeStride)

if isdir(Dir):
    print "Directory exists:", Dir
else:
    print "Creating directory", Dir
    makedirs(Dir)    

WorkDir=Dir+'/'+stime+'-'+etime+'.'+SamRate+'.'+str(TimeStride)

if isdir(WorkDir):
    print "Directory exists:", WorkDir
else:
    print "Creating directory", WorkDir
    makedirs(WorkDir)

#########################################           
###                                   ###                                                                                            
###  Making Cache File from Raw Data  ###
###                                   ### 
#########################################  

ChanDir=WorkDir+'/'+ChanList.split('_')[1]
if isdir(ChanDir):
    print "Directory exists:", ChanDir
else:
    print "Creating directory", ChanDir
    makedirs(ChanDir)
CacheDir=WorkDir+'/'+'Caches'

if isdir(CacheDir):
    print "Directory exists:", CacheDir
else:
    print "Creating directory", CacheDir
    makedirs(CacheDir)

if obs == 'K':
    CacheType=obs+'1'+'_C'
    CacheFile=CacheType+'_'+str(stime)+'_'+str(dur)+'.'+RunData+'.cache'
else:
    HoftCacheType=obs+'1'+'_HOFT_C00'
    AuxCacheType=obs+'1'+'_R'
    HoftCacheFile=HoftCacheType+'_'+str(stime)+'_'+str(dur)+'.'+RunData+'.cache'
    AuxCacheFile=AuxCacheType+'_'+str(stime)+'_'+str(dur)+'.'+RunData+'.cache'

if os.path.exists(CacheFile) == 'True':
    pass
else:
    if obs == 'K':
        MKCacheCMD="./mkcache.py --observatory %s --type %s --run %s --gps-start-time %s --gps-end-time %s --cache-file %s" % (obs, CacheType, RunData, stime, etime, CacheDir+'/'+CacheFile)    
        os.system(MKCacheCMD)
    else:
        MKCacheCMD1="gw_data_find --observatory %s --type %s --gps-start-time %s --gps-end-time %s --url-type file --lal-cache > %s" % (obs, HoftCacheType, stime, etime, CacheDir+'/'+HoftCacheFile)
        MKCacheCMD2="gw_data_find --observatory %s --type %s --gps-start-time %s --gps-end-time %s --url-type file --lal-cache > %s" % (obs, AuxCacheType, stime, etime, CacheDir+'/'+AuxCacheFile)
        os.system(MKCacheCMD1)
        os.system(MKCacheCMD2)

#############################################
###                                       ###
### Computing MIC, PearsonR, & KendallTau ###
###     - Extracting Data                 ###
###     - Resampling                      ### 
###     - Computing Scores                ###
###     - Writing a result file           ###
###                                       ###
#############################################
if obs=='K':
    GWChan=obs+'1:'+'LSC-MICH_CTRL_CAL_OUT_DQ'
else:
    GWChan=obs+'1:'+'GDS-CALIB_STRAIN'
GWSamRate='16384'
AuxChan=np.loadtxt(ChanList,dtype=np.str).tolist()

for i in range(len(AuxChan)):
    print 'Channel No. %s' % (i+1)
    print 'Extracting data and resampling for Aux Channel: ' + AuxChan[i][0]
    try:
        if obs=='K':
            HoftData=seriesutils.fromlalcache(CacheDir+'/'+CacheFile, GWChan, lal.LIGOTimeGPS(stime), dur)
            AuxData=seriesutils.fromlalcache(CacheDir+'/'+CacheFile,AuxChan[i][0], lal.LIGOTimeGPS(stime), dur)
        else:
            HoftData=seriesutils.fromlalcache(CacheDir+'/'+HoftCacheFile, GWChan, lal.LIGOTimeGPS(stime), dur)
            AuxData=seriesutils.fromlalcache(CacheDir+'/'+AuxCacheFile,AuxChan[i][0], lal.LIGOTimeGPS(stime), dur)
    except RuntimeError:
        print 'No such channel data in the data. Passed.'
        pass
    else:
    ###############################################################################################                                                  
    # * Resampling Data:                                                                          #                                                  
    # When the sampling rate of Aux. channel is greater than or equal to Sam. Threshold (SamRate) #                                                  
    # then the data shold be down-sampled to SamRate while when it is less than "SamRate", then   #                                                  
    # the data should be down-sampled to the sampling rate of Aux Channel.                        #                                                  
    ###############################################################################################                                                  
        if int(AuxChan[i][1]) >= int(SamRate):
            AuxResamp=seriesutils.resample(AuxData, float(SamRate), inplace=True)
            HoftResamp=seriesutils.resample(HoftData, float(SamRate), inplace=True)
            SRate=int(SamRate)
        else:
            AuxResamp=AuxData
            HoftResamp=seriesutils.resample(HoftData, float(AuxChan[i][1]), inplace=True)
            SRate=int(AuxChan[i][1])
    ### Time Split by Stride ###
        TStride=TimeStride # sec#
        Nseg=int(dur/TStride)
        Npsec=int(SRate*TStride)
        for j in range(Nseg):
    ### Computing MIC, Abs-PearsonR, and Abs-Kendall Tau Scores ###
            print 'Computing MIC ...'
#        mine=MINE(alpha=0.6, c=15, est="mic_approx")
            mine=MINE(alpha=0.6, c=15)
            mine.compute_score(AuxResamp.data.data[Npsec*j:Npsec*(j+1)], HoftResamp.data.data[Npsec*j:Npsec*(j+1)])
            MicVal=mine.mic()
            print 'MIC:', MicVal
            print 'Recording results...'
            f=open(ChanDir+'/'+'Correlation.Result.MIC'+'.'+str(stime)+'.'+str(dur)+'.'+RunData+'.'+str(TStride)+'.'+str(SamRate)+'.txt','a')
            f.write(str(MicVal))
            if j==Nseg-1:
                f.write('\n')
            else:
                f.write(' ')
            f.close()
            print 'Computing PearsonR ...'
            PccVal=np.nan_to_num(abs(pearsonr(AuxResamp.data.data[Npsec*j:Npsec*(j+1)], HoftResamp.data.data[Npsec*j:Npsec*(j+1)])[0]))
            print 'PearsonR:', PccVal
            print 'Recording results...'
            f=open(ChanDir+'/'+'Correlation.Result.PCC'+'.'+str(stime)+'.'+str(dur)+'.'+RunData+'.'+str(TStride)+'.'+str(SamRate)+'.txt','a')
            f.write(str(PccVal))
            if j==Nseg-1:
                f.write('\n')
            else:
                f.write(' ')
            f.close()
            print 'Computing Kendall Tau ...'
            KtauVal=np.nan_to_num(abs(kendalltau(AuxResamp.data.data[Npsec*j:Npsec*(j+1)], HoftResamp.data.data[Npsec*j:Npsec*(j+1)])[0]))
            print 'Kendall tau:', KtauVal
            print 'Recording results...'
            f=open(ChanDir+'/'+'Correlation.Result.Ktau'+'.'+str(stime)+'.'+str(dur)+'.'+RunData+'.'+str(TStride)+'.'+str(SamRate)+'.txt','a')
            f.write(str(KtauVal))
            if j==Nseg-1:
                f.write('\n')
            else:
                f.write(' ')
            f.close()

    ##########################
    # Drawing Scattered Plot #
    ##########################
            print 'Drawing scattered plot...'
            fig, ax=plt.subplots()
            AuxRescal=AuxResamp.data.data/np.median(AuxResamp.data.data)
            HoftRescal=HoftResamp.data.data/np.median(HoftResamp.data.data)
            fig=plt.scatter(AuxRescal, HoftRescal, c='r', s=10, lw=0, alpha=0.8)
            ax.set_xlabel(AuxChan[i][0])
            ax.set_ylabel(GWChan)
            ax.set_title('Scattered Plot between Two Channels_'+RunData+'.'+stime+'.'+str(dur))
            plt.savefig(ChanDir+'/'+'Scatter.Plot.'+stime+'.'+str(dur)+'.'+AuxChan[i][0]+'.'+RunData+'.'+str(TStride)+'.'+str(SamRate)+'.png')

########################################################
#
#  Drawing a Correlation Matrix for each subsystem
#
########################################################
MicMat=np.loadtxt(ChanDir+'/'+'Correlation.Result.MIC'+'.'+str(stime)+'.'+str(dur)+'.'+RunData+'.'+str(TStride)+'.'+str(SamRate)+'.txt')
PccMat=np.loadtxt(ChanDir+'/'+'Correlation.Result.PCC'+'.'+str(stime)+'.'+str(dur)+'.'+RunData+'.'+str(TStride)+'.'+str(SamRate)+'.txt')
KtauMat=np.loadtxt(ChanDir+'/'+'Correlation.Result.Ktau'+'.'+str(stime)+'.'+str(dur)+'.'+RunData+'.'+str(TStride)+'.'+str(SamRate)+'.txt')

print 'Creating Correlation Matrix... and Saving...'

colors=[('black')]+[(cm.jet(i))for i in xrange(1,256)]
new_map = matplotlib.colors.LinearSegmentedColormap.from_list('new_map', colors, N=256)

ChanInputX=np.loadtxt(ChanList,dtype=np.str)
ChanListX=ChanInputX.T[0].tolist()

#rows, cols=np.indices((len(ChanInputX),Nseg))
row_labels = ChanListX
column_labels=[]
for i in range(Nseg+1):
    column_labels.append(i*TStride)

for mla in [['MIC',MicMat], ['PCC', PccMat], ['Ktau',KtauMat]]:
    fig, ax = plt.subplots()
    heatmap=ax.imshow(mla[1], cmap=new_map,  interpolation='none', origin='lower', vmin=0.0, vmax=1.0)
    plt.colorbar(heatmap)
    ax.set_xticks(np.arange(mla[1].shape[1]+1)-0.5, minor=False)
    ax.set_yticks(np.arange(mla[1].shape[0]), minor=False)
    mpl.rc('text', usetex=False)
    plt.title('Correlation Matrix via '+mla[0]+' between Auxiliary and GW Channels', fontsize=10)
    ax.invert_yaxis()
#    ax.xaxis.tick_top()
    plt.xlabel('GPS:'+str(stime)+'_'+'Dur:'+str(dur)+'_'+'Stride:'+str(TStride), fontsize=10)
    plt.xticks(rotation=90)
    ax.set_yticklabels(row_labels, minor=False, fontsize=3)
    ax.set_xticklabels(column_labels, minor=False, fontsize=3)

    fig.savefig(ChanDir+'/'+'CMatrix_'+mla[0]+'.'+RunData+'.'+str(stime)+'.'+str(dur)+'.'+str(TStride)+'.'+str(SamRate)+'.png',dpi=256)

#############################################################
#                                                           #
#                BAND-PASSED ANALSYS                        #
#                                                           #
#############################################################



print 'The Analysis Done.'


