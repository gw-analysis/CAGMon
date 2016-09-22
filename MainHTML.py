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

def CAGHeader(chlist):
    BaseDir=os.getenv("HOME")+'/public_html'
    header = """
<html>
<head>                                                                                                                           
<title>CAGMon as a DetChar Tool</title>
</head>                                                                                                                           
<body color="gray">
<h1 align="center">CAGMon Project: Analysis Results</h1>
<h3 align="center" style="italic">- Correlation analysis based Detchar Tool using MIC, PearsonR, and Kendall's tau coefficients -</h3>
<h4 align="center">Developer: John J OH (KGWG & NIMS, South Korea) </h4>
<h4 align="center">Contact Email: <a href="mailto:johnoh@nims.re.kr">johnoh@nims.re.kr</a></h4>
<h4 align="center">iKAGRA Runs: 1142899217-1143446417 (1st) / 1144368017-1145606417 (2nd)</h4>
<h4 align="center">Code: <a href="https://github.com/gw-analysis/CAGMon.git">https://github.com/gw-analysis/CAGMon.git</a></h4>
<p align="center">| DQ.Channel Info. |<a href="%s.txt"> %s </a>|<a href="%s.txt"> %s</a> |<a href="%s.txt"> %s</a> |<a href="%s.txt"> %s</a> |</p>
<hr>                                                                                                                              
"""
    filename ='index'
    heads=header % (chlist[0], chlist[0].split('_')[1], chlist[1], chlist[1].split('_')[1], chlist[2], chlist[2].split('_')[1], chlist[3], chlist[3].split('_')[1])
    f=open(BaseDir+'/'+filename+'.html','a')
    f.write(heads)
    f.close()
    return filename


def CAGBody(filename):
    BaseDir=os.getenv("HOME")+'/public_html'
    CRDirs=DirsList().ListDirs(BaseDir)
    BodyHead="""
<h3>Project Goal</h3>
<p> CAGMon 2.0 is an integrated tool for finding correlation between gravitational wave channel and thousands of auxiliary channels of gravitational-wave detector. It computes Pearson correlation coefficient, Kendall's tau coefficient, and Maximal Information Coefficient (MIC) between both channel data and generate channel list with high-scored correlation value. The version 2.0 uses 1) time series data segment 2) unsafe channel list for O1 3) simple summary webpage generator.</p>
<h3>Theoretical Basis</h3>
<h3>Software Requirement</h3>
<li>python 2.7 >=</li>
<li>matplotlib, numpy, scipy</li>
<li>minepy</li>
<li>pylal, lalsuite, glue</li>
<h3>User's Guide</h3>
<li>Guide for only LVC member (access limited): <a href="https://kgwg.nims.re.kr/cbcwiki/CAGMon2.0" target="_blank">Link</a></li>
<li>User's guide for LVC and KAGRA member: <a href="https://github.com/gw-analysis/CAGMon.git">README.md@GITHUB</a></li>
<hr>
<h3>Analyzed Result Lists:</h3>
<hr>
<table>
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
<td>
<li><a href="%s/%s">%s</a></li>
</td>
"""
            bodybody=Bodybody % (CRDirs[m], subfilename, CRDirs[m])
            f=open(BaseDir+'/'+filename+'.html', 'a')
            f.write(bodybody)
            f.close()

def CAGFoot(filename):
    BaseDir=os.getenv("HOME")+'/public_html'
    Foot="""
</table>
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
