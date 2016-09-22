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
CAGMkSub - Generating a one-shot build shell script to compute CAGMon
"""
__author__ ="John J. Oh <john.oh@ligo.org>"
#__version__ = git_version.id                                                                                                         
#__date__    = git_version.date                                                                                                       
               
 
import numpy as np
from os import makedirs
from os.path import isdir, exists
from sys import exit
import ast
import os, sys
import ConfigParser
config=ConfigParser.ConfigParser()
config.read("CAGConfig.ini")

BaseDir=config.get('Parameter','Base_Directory')
stime=int(config.get('Parameter','start_time'))
etime=int(config.get('Parameter','end_time'))
srate=int(config.get('Parameter','sampling_rate'))
stride=float(config.get('Parameter','time_stride'))
runs=config.get('Parameter','runs')
datype=config.get('Parameter','datype')
chlist=ast.literal_eval(config.get('Parameter','chlist'))
Nseg=int(config.get('Parameter','Nseg'))

logdir='logs'
if isdir(logdir):
    print "Directory exists:", logdir
else:
    print "Creating directory:", logdir
    makedirs(logdir)

dur=int(etime)-int(stime)
SegTime=int(Nseg*stride)
base_tag='CAGMonLK.'+str(stime)+'.'+str(dur)+'.'+str(srate)+'.'+str(stride)+'.'+datype
print 'Creating a Multi-Job Script file...'
for chl in chlist:
    for i in range(dur/Nseg):
        tag=base_tag+'.'+chl
        CMD=" python "+BaseDir+"CAGMonLK.py -s "+str(stime+SegTime*i)+" -e "+str(stime+SegTime*(i+1))+" -o "+runs+" -r "+datype+" -c "+BaseDir+chl+" -f "+str(srate)+" -t "+str(stride)
        f=open(base_tag+'.sh','a')
        f.write(CMD+'\n')
        f.write('\n')
        f.close()
print 'Writing Web-builder for Result Page'
f=open(base_tag+'.sh','a')
CAGWeb=" python CAGWebBuild.py -s "+str(stime)+" -e "+str(etime)
f.write(CAGWeb+'\n')
f.close()

CMODE=" chmod a+x "+base_tag+'.sh'
os.system(CMODE)

tmpdir='tmp'
if isdir(tmpdir):
    pass
else:
    print 'Creating directory and copying configure:', tmpdir
    makedirs(tmpdir)

CPConfig=" cp CAGConfig.ini "+tmpdir+'/CAGConfig.'+str(stime)+'.'+str(dur)+'.'+str(srate)+'.'+str(stride)+'.ini'
os.system(CPConfig)
print "Configuration file copied to:", tmpdir
print 'All Jobs Done'
print 'Type "./'+base_tag+'.sh"'
