#!/usr/bin/env/ python
from os import listdir

class PNGList:
    from os import listdir
    def __init__(self):
        self.list=0
    def ListGet(self, path):
        self.list=[f for f in listdir(path) if f.split('.')[-1]=='png']
        return self.list

def CAGHeader(gps_start, gps_end, dur, srate, stride, run, Nseg, chlist):
    BaseDir=run+'.'+str(gps_start)+'.'+str(dur)+'.'+str(srate)+'.'+str(stride)
    header = """
<html>
<head>                                                                                                                           
<title>CAGMon Analysis Results</title>                                                                                                
</head>                                                                                                                           
<body>                                                                                                                            
<h1>CAGMon Analysis Results</h1>
<h3>-- Correlation analysis using MIC, PearsonR, and Kendall's tau coefficients</h3>
<li>Analyzed GPS Time: %s - %s (%s sec)</li>
<li>Sampling Frequency: %s</li>
<li>Run Type (IFO): %s</li>
<li>Time Stride (Each Pixel): %s (sec)</li>
<li>Analyzed Segment (Each Figure): %s (sec)</li>
<p>This page shows the global trend of the correlation between GW channel and auxiliary channels during the analyzed time period. If you click the individual figure, then you find the CMatrix and the relavent scattered plots during the time segment.</p>
<p align="center">|<a href="%s.html"> %s </a>|<a href="%s.html"> %s</a> |<a href="%s.html"> %s</a> |<a href="%s.html"> %s</a> |</p>
<hr>                                                                                                                              
"""
    for m in chlist:
        filename ='CAGMon.'+str(gps_start)+'-'+str(gps_end)+'.'+run+'.'+str(srate)+'.'+str(stride)
        chname=m.split('_')[1]
        mname1=filename+'.'+chlist[0].split('_')[1]
        mname2=filename+'.'+chlist[1].split('_')[1]
        mname3=filename+'.'+chlist[2].split('_')[1]
        mname4=filename+'.'+chlist[3].split('_')[1]
        heads=header % (gps_start, gps_end, dur, srate, run, stride, Nseg, mname1, chlist[0].split('_')[1], mname2, chlist[1].split('_')[1], mname3, chlist[2].split('_')[1], mname4, chlist[3].split('_')[1])
        filename ='CAGMon.'+str(gps_start)+'-'+str(gps_end)+'.'+run+'.'+str(srate)+'.'+str(stride)
        f=open(BaseDir+'/'+filename+'.'+chname+'.html','a')
        f.write(heads)
        f.close()
    return filename


def CAGBody(gps_start, dur, srate, stride, Nseg, run, chlist, filename):
    BaseDir=run+'.'+str(gps_start)+'.'+str(dur)+'.'+str(srate)+'.'+str(stride)
    meth=['PCC', 'MIC', 'Ktau']
    for m in chlist:
        chname=m.split('_')[1]
        BodyHead="""
<h3>%s</h3>
<hr>
"""
        bodyhead=BodyHead % chname
        f=open(BaseDir+'/'+filename+'.'+chname+'.html', 'a')
        f.write(bodyhead)
        f.close()
        for k in meth:
            t=['Pearson Correlation Coefficient', 'Maximal Information Coefficient', 'Kendall tau Coefficient']
            Subsect="""
<h4>%s</h4>
<hr>
<table>
"""
            subsect=Subsect % t[meth.index(k)]
            f=open(BaseDir+'/'+filename+'.'+chname+'.html', 'a')
            f.write(subsect)
            f.close()
            for i in range(int(dur)/int(Nseg)):
                BdHead="""
<tr>
"""
                bdhead=BdHead
                if divmod(i,3)[1]==0:
                    f=open(BaseDir+'/'+filename+'.'+chname+'.html','a')
                    f.write(bdhead)
                    f.close()
                else:
                    pass
                nts=int(gps_start)+i*int(Nseg)
                nte=int(gps_start)+(i+1)*int(Nseg)
                ResDir=str(nts)+'-'+str(nte)+'.'+str(srate)+'.'+str(stride)
                path=BaseDir+'/'+ResDir+'/'+chname+'/'
                scatlist=PNGList().ListGet(path)
                scatlist.sort()
                scatfile='ScatterPlots'+'.'+ResDir+'.'+chname+'.html'
                BodyDraw ="""
<td>
<figure>
<a href="%s"><img src="%s/%s/CMatrix_%s.%s.%s.%s.%s.%s.png" width="350"></img></a>
<figcaption fontsize="6" align="center">
%s: %s+%s
</figcaption>
</figure>
</td>
"""
                bodydraw=BodyDraw % (scatfile, ResDir, chname, k, run, str(nts), str(Nseg), stride, srate, t[meth.index(k)], nts, Nseg)
                BdFoot="""
</tr>
"""
                bdfoot=BdFoot
                f=open(BaseDir+'/'+filename+'.'+chname+'.html', 'a')
                if divmod(i,3)[1]==2:
                    f.write(bodydraw)
                    f.write(bdfoot)
                else:
                    f.write(bodydraw)
                f.close()
                ### Scatter.Plot.Starts ###
                if k=='PCC':
                    Scathead="""
<h3>Scattered Plots: %s.%s.%s.%s.%s</h3>
<h4>%s</h4>                                                                                                                           
<table>                                                                                                                               
"""
                    scathead =Scathead% (run, str(nts), str(Nseg), srate, stride, chname)
                    f=open(BaseDir+'/'+scatfile, 'a')
                    f.write(scathead)
                    f.close()
                    for n in scatlist:
                        TrHead="""   
<tr>                                                                                                                                  
"""
                        trhead=TrHead
                        ScattDraw="""
<td>                                                                                                                                  
<figure>                                                                                                                              
<img src="%s/%s/%s" width="350"></img>                                                                                                
<figcaption align="center"fontsize="6"> 
%s: %s+%s - %s                                                                                                                        
</figcaption>                                                                                                                         
</figure>                                                                                                                             
</td>                                                                                                                                 
"""
                        TrFoot="""
</tr>                                                                                                                                 
"""
                        trfoot=TrFoot
                        tag=n.split('.')[0]
                        if tag == 'Scatter':
                            scattdraw=ScattDraw% (ResDir, chname, n, tag+'.Plot', nts, Nseg, n.split(':')[1].split('.')[0])
                        else:
                            scattdraw=ScattDraw% (ResDir, chname, n, tag.split('_')[0], nts, Nseg, tag.split('_')[-1])
                        f=open(BaseDir+'/'+scatfile,'a')
                        if divmod(scatlist.index(n),3)[1]==0:
                            f.write(trhead)
                        else:
                            pass
                        if divmod(scatlist.index(n),3)[1]==2:
                            f.write(scattdraw)
                            f.write(trfoot)
                        else:
                            f.write(scattdraw)
                        f.close()
                else:
                    pass
                scatfoot="""
</table>                                                                                                                              
"""
                f=open(BaseDir+'/'+scatfile,'a')
                f.write(scatfoot)
                f.close()
                ### Scatter.Plot.Ends ###
            Subfoot="""
</table>
"""
            subfoot=Subfoot
            f=open(BaseDir+'/'+filename+'.'+chname+'.html', 'a')
            f.write(subfoot)
            f.close()

def CAGFoot(gps_start, dur, srate, stride, run, filename, chlist):
    for m in chlist:
        chname=m.split('_')[1]
        BaseDir=run+'.'+str(gps_start)+'.'+str(dur)+'.'+str(srate)+'.'+str(stride)
        Foot="""
</body>
<hr>
<p style="italic">Created by CAGWebBuilder</p>
<p style="italic">Copyright@John.Oh</p>
</html>
"""
        foot=Foot 
        f=open(BaseDir+'/'+filename+'.'+chname+'.html', 'a')
        f.write(foot)
        f.close()
