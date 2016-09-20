#########################################################################################
#                                    CAGMon 2.0 README                                  #
#########################################################################################
 This program generates correlation analysis result between both different channel data,
 drawing correlation matrix & scattered plots

Copyright@John J. Oh
20 Sep. 2016
<johnoh@nims.re.kr, john.oh@ligo.org>

+ Requirement:
 - python 2.7 >=
 - numpy
 - scipy
 - minepy
 - matplotlib
 - pylal
 - glue
 - and other dependencies

+ Code Contents
  - CAGConfig.ini # Configuration setting
  - CAGMonLK.py   # Main CAGMon Code -- computing correlation values and plotting
  - CAGMkSh.py    # Generating shell script for multi-jobs (serial)
  - CAGWebBuild.py # Generating result HTML pages
  - CAGWebUtils.py # Utils for generating HTML pages
  - mkcache.py     # Extracting Data from iKAGRA data path
  - Channel Files: K1_KAGRA.DQ.Channel.IMC.PSL, K1_KAGRA.DQ.Channel.LSC, K1_KAGRA.DQ.Channel.PEM, K1_KAGRA.DQ.Channel.VIS  # Auxiliary Channel File List

+ Download: https://github.com/gw-analysis/CAGMon.git or ssh://git@github.com/gw-analysis/CAGMon.git
 - $ git clone https://github.com/gw-analysis/CAGMon.git
 - $ cd CAGMon

+ Environment Setting for PyLAL and LALSuite

 -$ source /home/johnoh/.local/etc/lscsoftrc

+ Instruction: 

 o Serial Job Running with Shell Script:
  - Preparing Auxiliary Channel List:
    * Each list file divided by at least one '_', 
      * ex) K1_KAGRA.DQ.Channel.LSC
    * There are four files containing channel names : IMC.PSL, LSC, PEM, VIS
  - Modifying Configuration file:
    * Open "CAGConfig.ini" file and setting up appropriately
  - Creating .sh file:
    * Just executing "./CAGMkSh.py" 
  - Run Shell Script with "CAGMonLK.[gps_start].[dur].[stride].[freq].sh"
  - Then the result has been stored in your "$HOME/public_html" directory.

 o Single Job Running:
  - $ python CAGMonLK.py -t [start-gps] -e [end-gps] -o [ifo / L H K ] -r [DataType/ ER8, O1, iKAGRA] -c [ChannelList File_Divided by '-'] -t [time stride] -f [resampled frequency]
    * ex) python CAGMonLK.py -t 1145621579 -e 1145621609 -o K -r iKAGRA -c K1_KAGRA.DQ.Channel.LSC -t 1.0 -f 1024

+ Help
 - $ python CAGMonLK.py --help



