#!/usr/bin/env python
from CAGWebUtils import *
import ast
import ConfigParser
config=ConfigParser.ConfigParser()
config.read("CAGConfig.ini")

BaseDir=config.get('Parameter','Base_Directory')
stime=int(config.get('Parameter','start_time'))
etime=int(config.get('Parameter','end_time'))
srate=config.get('Parameter','sampling_rate')
stride=config.get('Parameter','time_stride')
runs=config.get('Parameter','runs')
datype=config.get('Parameter','datype')
chlist=ast.literal_eval(config.get('Parameter','chlist'))
Nseg=int(config.get('Parameter','Nseg'))
dur=str(etime-stime)

filename=CAGHeader(stime, etime, dur, srate, stride, datype, Nseg, chlist)
CAGBody(stime, dur, srate, stride, Nseg, datype, chlist, filename)
CAGFoot(stime, dur, srate, stride, datype, filename, chlist)





