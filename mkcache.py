#!/usr/bin/env python2

from os import listdir
from os.path import isdir
from numpy import array
from optparse import OptionParser

parser=OptionParser()
parser.add_option("-o", "--observatory", action="store", type="string", default="K", help="Observatory: H, L, V or K (default)")
parser.add_option("-t", "--type", action="store", type="string", default="K1_C", help="Data type: H1_HOFT_C02, L1_RDS, etc.; default: K1_C")
parser.add_option("-r", "--run", action="store", type="string", default="iKAGRA", help="Run name: ER8, O1, etc.; default: iKAGRA")
parser.add_option("-c", "--cache-file", action="store", type="string", default=None, help="output LAL cache file path")
parser.add_option("-s", "--gps-start-time", action="store", type="float", default=0., help="GPS start time")
parser.add_option("-e", "--gps-end-time", action="store", type="float", default=9999999999., help="GPS end time")

(opts,files)=parser.parse_args()

if opts.observatory == "K":
    basedir = "/data/kagra/"
elif (opts.observatory == "H") or (opts.observatory == "L") or (opts.observatory == "V"):
    basedir = "/data/ligo/archive/frames/"
else:
    raise ValueError("Observatory should be one of H, L, V or K")

if opts.run == "iKAGRA":
    if opts.type == "K1_C":
        tmp0 = "raw"
        tmp1 = "full"
    else:
        raise ValueError("Wrong values for --type option: {0}".format(opts.type))
    basedir += "{0}/{1}/".format(tmp0, tmp1)
    predir = None
    DT      = 100000
elif (opts.run == "ER8") or (opts.run == "O1"):
    basedir += "{0}/{1}/{2}/".format(opts.run, opts.type, opts.observatory)
    predir = None
    DT      = 1000000
elif (opts.run == "S5") or (opts.run == "S6"):
    if opts.run == "S5":
        tmp = "strain-{0}".format(opts.type.split('_')[-1])
    elif opts.type.split('_')[1] == "LDAS":
        tmp = "LDAShoft{0}".format(opts.type.split('_')[-2])
    elif opts.type.split('_')[1] == "RDS":
        tmp = opts.type.split('_')[-1]
    else:
        raise ValueError("Wrong values for --type option: {0}".format(opts.type))
    basedir += "{0}/{1}/L{2}O/".format(opts.run, tmp, opts.observatory)
    predir = "{0}-{1}-".format(opts.observatory, opts.type)
    DT      = 100000
elif (opts.run == "VSR1") or (opts.run == "VSR2") or (opts.run == "VSR3") or (opts.run == "VSR4"):
    basedir += opts.run + "/"
    predir = "{0}-{1}-".format(opts.observatory, opts.type)
    DT      = 1000000
else:
    raise ValueError("Wrong values for --run option: {0}".format(opts.run))

cachefile = opts.cache_file
ls_out = []

if not isdir(basedir):
    raise ValueError("You might have given a wrong observatory, type or run")

d = sorted(listdir(basedir))
for j in d:
    if (j[0] == '.') or (j[-3:] != 'gwf'):
        continue
    tmp = j.split('.')[0].split('-')
    start = int(tmp[-2])
    stop = start + int(tmp[-1])
    if stop <= opts.gps_start_time:
        continue
    if start >= opts.gps_end_time:
        break
    ls_out.append(' '.join(tmp + ['file://localhost{0}/{1}'.format(basedir, j)]))

if cachefile is None:
    for i in ls_out:
        print i
else:
    with open(cachefile, 'w') as f:
        f.write('\n'.join(ls_out)+'\n')
