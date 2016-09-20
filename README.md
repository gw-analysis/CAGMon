########################################################################
#
#                            CAGMon 2.0 README
#
#    This program generates correlation analysis result between both 
#   different channel data.
#            - Drawing correlation matrix & scattered plots
#                             Sep. 19. 2016
#
########################################################################

Copyright@John J. Oh
<johnoh@nims.re.kr, john.oh@ligo.org>

+ Requirement:
 - python 2.7 >=
 - numpy
 - scipy
 - minepy
 - matplotlib
 - pylal
 - glue

+ Code Location: seikai.icrr.u-tokyo.ac.jp:/johnoh/CAGMon/
  - CAGConfig.ini # Configuration setting
  - CAGMonLK.py   # Main CAGMon Code -- computing correlation values and plotting
  - CAGMkSh.py    # Generating shell script for multi-jobs (serial)
  - CAGWebBuild.py # Generating result HTML pages
  - CAGWebUtils.py # Utils for generating HTML pages
  - mkcache.py     # Extracting Data from iKAGRA data path
  - Channel Files: K1_KAGRA.DQ.Channel.IMC.PSL, K1_KAGRA.DQ.Channel.LSC, K1_KAGRA.DQ.Channel.PEM, K1_KAGRA.DQ.Channel.VIS  # Auxiliary Channel File List

+ Download: https://github.com/gw-analysis/CAGMon.git or ssh://git@github.com/gw-analysis/CAGMon.git

+ Environment Setting for PyLAL and LALSuite
  # source /home/johnoh/.local/etc/lscsoftrc

+ Instruction: 
 o Shell Script Seirial Job Submission
 - Preparing Auxiliary Channel List:
   * Each list file divided by at least one '_', 
    ex) K1_KAGRA.DQ.Channel.LSC
   * There are four files containing channel names : IMC.PSL, LSC, PEM, VIS
 - Modifying Configuration file:
   * Open "CAGConfig.ini" file and setting up appropriately
 - Creating .sh file:
   * Just executing "./CAGMkSh.py" 
 - Run Shell Script
 - Making Result Page:
   * python CAGWebBuil.py
 o Single job running
 - $ python CAGMonLK.py -t [start-gps] -e [end-gps] -o [ifo / L H K ] -r [DataType/ ER8, O1, iKAGRA] -c [ChannelList File_Divided by '-'] -t [time stride] -f [resampled frequency]
    ex) python CAGMonLK.py -t 1145621579 -e 1145621609 -o K -r iKAGRA -c K1_KAGRA.DQ.Channel.LSC -t 1.0 -f 1024

+ Help
$ python CAGMonLK.py --help
Usage: CAGMon
Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -s GPS_START_TIME, --gps-start-time=GPS_START_TIME
                        start gps time
  -e GPS_END_TIME, --gps-end-time=GPS_END_TIME
                        end gps time
  -o IFO, --ifo=IFO     ifos:L, H, K
  -r RUN_DATA, --run-data=RUN_DATA
                        ER8, O1, O2, K1
  -f SAMPLING_RATE, --sampling-rate=SAMPLING_RATE
                        sampling rate: 2048, 4098, 8196, etc
  -c CHANNEL_LIST, --channel-list=CHANNEL_LIST
                        auxiliary channel list
  -v MIC_THRESH, --mic-thresh=MIC_THRESH
                        MIC threshold value - default is 0.09
  -t TIME_STRIDE, --time-stride=TIME_STRIDE
                        time stride to be splitted


