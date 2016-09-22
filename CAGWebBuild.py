#!/usr/bin/env python
from CAGWebUtils import *
import ast
from optparse import *
import ConfigParser
config=ConfigParser.ConfigParser()
parser=OptionParser(usage="CAGWebBuild", version="2.0")
parser.add_option("-s", "--gps-start-time", action="store", type="int", default="00000", help="start gps time")
parser.add_option("-e", "--gps-end-time", action="store", type="int", default="00000", help="end gps time")
(opts, files)=parser.parse_args()
stime=str(opts.gps_start_time)
etime=str(opts.gps_end_time)
dur=int(etime)-int(stime)

tmpdir='tmp'
for i in range(len(listdir(tmpdir))):
    gstart=int(listdir(tmpdir)[i].split('.')[1])
    gdur=int(listdir(tmpdir)[i].split('.')[2])
    gend=int(gstart+gdur)
    if gstart <= stime and gend >= etime:
        config.read(listdir(tmpdir)[i])
    else:
        pass

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

print 'Generating HTML result page...'
filename=CAGHeader(stime, etime, dur, srate, stride, datype, Nseg, chlist)
CAGBody(stime, dur, srate, stride, Nseg, datype, chlist, filename)
CAGFoot(stime, dur, srate, stride, datype, filename, chlist)

print 'All Processes Done.'





