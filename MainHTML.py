#!/usr/bin/env/ python
from os import listdir
import os, sys

class FileList:
    from os import listdir
    def __init__(self):
        self.list=0
    def ListGet(self, path):
        self.list=[f for f in listdir(path) if f.split('.')[0]=='CAGMon']
        return self.list

class DirsList:
    from os import listdir
    import os, sys
    def __init__(self):
        self.list=0
    def ListDirs(self, path):
        return [i for i in os.listdir(path) if os.path.isdir(os.path.join(path,i))]

def CAGHeader(gps_start, gps_end, dur, srate, stride, run, Nseg, chlist):
    BaseDir='../public_html'
    header = """
<html>
<head>                                                                                                                           
<title>CAGMon Analysis Results</title>                                                                                                
</head>                                                                                                                           
<body color="gray">
<h1 align="center">CAGMon Analysis Results</h1>
<h2 align="center">-- Correlation analysis using MIC, PearsonR, and Kendall's tau coefficients</h2>
<h4 align="center">Developer: John J OH (KGWG & NIMS, South Korea) </h4>
<h4 align="center">Contact Email: <a href="mailto:johnoh@nims.re.kr">johnoh@nims.re.kr</a></h4>
<h4 align="center">iKAGRA Runs: 1142899217-1143446417 (1st) / 1144368017-1145606417 (2nd)</h4>
<h4 align="center">Code: <a href="https://github.com/gw-analysis/CAGMon.git">https://github.com/gw-analysis/CAGMon.git</a></h4>
<p align="center">This page shows the global trend of the correlation between GW channel and auxiliary channels during the analyzed time period.<br> If you click the individual figure, then you find the CMatrix and the relavent scattered plots during the time segment.</p>
<p align="center">| DQ.Channel Info. |<a href="%s"> %s </a>|<a href="%s"> %s</a> |<a href="%s"> %s</a> |<a href="%s"> %s</a> |</p>
<hr>                                                                                                                              
"""
    filename ='index'
    heads=header % (chlist[0], chlist[0].split('_')[1], chlist[1], chlist[1].split('_')[1], chlist[2], chlist[2].split('_')[1], chlist[3], chlist[3].split('_')[1])
    f=open(BaseDir+'/'+filename+'.html','a')
    f.write(heads)
    f.close()
    return filename


def CAGBody(gps_start, dur, srate, stride, Nseg, run, chlist, filename):
    BaseDir='../public_html'
    CRDirs=DirsList().ListDirs(BaseDir)
    BodyHead="""
<h2>Analysis Lists:</h2>
<hr>
"""
    bodyhead=BodyHead
    f=open(BaseDir+'/'+filename+'.html','a')
    f.write(bodyhead)
    f.close()
    for m in range(len(CRDirs)):
        path=BaseDir+'/'+CRDirs[m]
        tmp=FileList().ListGet(path)
        tmp.sort()
        try:
            subfilename=tmp[0]
        except:
            pass
        else:
            Bodybody="""
<li><a href="%s/%s">%s</a></li>
<br>
"""
            bodybody=Bodybody % (CRDirs[m], subfilename, CRDirs[m])
            f=open(BaseDir+'/'+filename+'.html', 'a')
            f.write(bodybody)
            f.close()

def CAGFoot(gps_start, dur, srate, stride, run, filename, chlist):
    BaseDir='../public_html'
    Foot="""
</body>
<hr>
<p style="italic">Created by MainWebBuilder</p>
<p style="italic">Copyright@John.Oh</p>
</html>
"""
    foot=Foot 
    f=open(BaseDir+'/'+filename+'.html', 'a')
    f.write(foot)
    f.close()
