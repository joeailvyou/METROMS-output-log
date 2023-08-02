from GlobalParams import *
from Constants import *
from Utils import *
import sys
from datetime import datetime, timedelta
import netCDF4

class Params(object):
    RUNPATH=None
    KEYWORDFILE=None
    ROMSINFILE=None
    FELT_CLMFILE=None
    KEYWORDLIST=None
    XCPU=None
    YCPU=None
    TSTEPS=None
    NRREC=None
    START_DATE=None
    END_DATE=None
    
    def __init__(self,app,xcpu,ycpu,start_date,end_date,nrrec=-1,cicecpu=0,restart=False):
        self.KEYWORDFILE=GlobalParams.COMMONORIGPATH+"/roms_keyword.in_roms-trunk"
        self.XCPU=xcpu
        self.YCPU=ycpu
        self.CICECPU=cicecpu
        self.FCLEN=(end_date-start_date).total_seconds()
        self.NRREC=nrrec
        self.TIMEREF=datetime(1970,01,01,00)
        self.RESTART=restart
        self.START_DATE=start_date
        self.END_DATE=end_date
        if app=='arctic-20km':
            ########################################################################
            # Name of roms.in keyword-file:
            ########################################################################
            self.RUNPATH=GlobalParams.RUNDIR+"/arctic-20km"
            self.ROMSINFILE=self.RUNPATH+"/roms.in"
            #self.CICEKEYWORDFILE=self.RUNPATH + "/ice_in_keyword"
            #self.CICEINFILE=GlobalParams.CICERUNDIR + "/ice_in"
            self.CICERUNDIR=self.RUNPATH+'/cice/rundir'
            self.CICEINFILE=self.RUNPATH + "/ice_in"
            self.CICEKEYWORDFILE=self.CICERUNDIR + "/ice_in"
            self.FELT_CLMFILE=self.RUNPATH+"/FOAM.felt"
            self.DELTAT=1200 
            self.CICEDELTAT=3600.0
            self.COUPLINGTIME_I2O=3600.0
            #self.ROMSINIFILE=self.RUNPATH+"/"+INIFILE
            # Find restart-time of CICE:
            cice_start_step = (start_date-datetime(start_date.year,01,01,00)).total_seconds()/self.CICEDELTAT
            if restart == True:
                f = open(self.CICERUNDIR+'/restart/ice.restart_file', 'r')
                cice_restartfile = f.readline().strip()
                cice_rst_time = netCDF4.Dataset(cice_restartfile).istep1
                #cice_rst_day = netCDF4.Dataset(cice_restartfile).mday
                cicerst_truefalse = ".true."
            else:
                cice_rst_time = cice_start_step
                #cice_rst_day = start_date.day
                cicerst_truefalse = ".false."
            ########################################################################
            # List of keywords:
            ########################################################################
            self.KEYWORDLIST=[
            ['APPTITLE',"ROMS 3.6 - Arctic-20km - Coupled ROMS-CICE"],
            ['MYAPPCPPNAME',"ARCTIC20KM"],
            #['VARFILE',GlobalParams.COMMONPATH+"/include/varinfo.dat"],
            ['VARFILE',self.RUNPATH+"/varinfo.dat"], #jiao
            ['XPOINTS',"320"],  #Could read from grd-file?
            ['YPOINTS',"240"],  #Could read from grd-file?
            ['NLEVELS',"35"],  #Could read from grd-file?
            ['GRDTHETAS',"6.0d0"],
            ['GRDTHETAB',"0.1d0"],
            ['GRDTCLINE',"100.0d0"],            
            ['_TNU2_',"2*1.0d2"],
            ['_TNU4_',"1.6d8"],
            ['_VISC2_',"1.0d2"],
            ['_VISC4_',"1.6d8"],
            ['XCPU',str(self.XCPU)],
            ['YCPU',str(self.YCPU)],
            ['TSTEPS',str(self.FCLEN/self.DELTAT)], #jiao roms full steps
            ['DELTAT',str(self.DELTAT)],            #jiao roms steps length
            ['RATIO',"20"], #['RATIO',"30"],
            ['IRESTART',str(self.NRREC)],           # -1
            ['RSTSTEP',str(30*24*3600/int(self.DELTAT))],  # about output to rst file steps
            ['STASTEP',str(24*3600/int(self.DELTAT))],
            ['INFOSTEP', str(1*3600/int(self.DELTAT))],
            ['HISSTEPP', str(1*3600/int(self.DELTAT))],
            ['DEFHISSTEP',str(30*24*3600/int(self.DELTAT))],  #if 0; all output in one his-file
            ['AVGSTEPP',str(1*24*3600/int(self.DELTAT))],
            ['STARTAVG',"1"],
            ['DEFAVGSTEP',str(30*24*3600/int(self.DELTAT))],  #if 0; all output in one avg-file
            ['STARTTIME',str((start_date-self.TIMEREF).total_seconds()/86400)],  # jiao days of start relative to reference time 1970 01 01
            ['TIDEREF',str((start_date-self.TIMEREF).total_seconds()/86400)],    # jiao days of start relative to reference time 1970 01 01
            ['TIMEREF',self.TIMEREF.strftime("%Y%m%d.00")],  # jiao formated the TIMEREF
            ['V_TRANS',"2"],
            ['V_STRETCH',"4"],  # jiao in file
            ['_TNUDG_',"15.0d0 15.0d0"],     # jiao in file, Nudging/relaxation time scales
            ['OBCFAKTOR',"1.0"],
            ['NUDGZONEWIDTH',"10"],
            #['GRDFILE',GlobalParams.COMMONPATH+"/grid/A20_grd_openBering.nc"],
            ['GRDFILE',self.RUNPATH+"/A20_grd_openBering.nc"],   #jiao
            ['RUNDIR',self.RUNPATH],
            ['_CLMNAME_',self.RUNPATH+"/ocean_1993_clm.nc | \n"+self.RUNPATH+"/ocean_1994_clm.nc | \n"+self.RUNPATH+"/ocean_1995_clm.nc | \n"+self.RUNPATH+"/ocean_1996_clm.nc | \n"+self.RUNPATH+"/ocean_1997_clm.nc"],
            ['_BRYNAME_',self.RUNPATH+"/ocean_1993_bry.nc | \n"+self.RUNPATH+"/ocean_1994_bry.nc | \n"+self.RUNPATH+"/ocean_1995_bry.nc | \n"+self.RUNPATH+"/ocean_1996_bry.nc | \n"+self.RUNPATH+"/ocean_1997_bry.nc"],
            ['TIDEDIR',self.RUNPATH],
            ['ATMDIR',self.RUNPATH+"/AN_1993_unlim.nc | \n"+self.RUNPATH+"/AN_1994_unlim.nc | \n"+self.RUNPATH+"/AN_1995_unlim.nc | \n" +self.RUNPATH+"/AN_1996_unlim.nc | \n" +self.RUNPATH+"/AN_1997_unlim.nc \ \n"+self.RUNPATH+"/FC_1993_unlim.nc | \n"+self.RUNPATH+"/FC_1994_unlim.nc | \n"+self.RUNPATH+"/FC_1995_unlim.nc | \n"+self.RUNPATH+"/FC_1996_unlim.nc | \n"+self.RUNPATH+"/FC_1997_unlim.nc"],
            #['RIVERFILE',GlobalParams.COMMONPATH+"/rivers/newA20_rivers_mitya.nc"],
            ['RIVERFILE',self.RUNPATH+"/newA20_rivers_mitya.nc"],    #jiao
            ['FORCEFILES',"3"], # The files should be specified here as well
            #['ROMS/External/coupling.dat', self.RUNPATH + "/coupling.dat"],
            ['COUPLINGTIMEI2O',str(self.COUPLINGTIME_I2O)],    #jiao coupling step (unit in second)
            ['ROMSINFILE', self.ROMSINFILE ],  # jiao roms.in in the RUNPATH. (not the template in the common/include)
            ['CICEINFILE', self.CICEINFILE ],  # jiao ice_in in the RUNPATH.
            ['NUMROMSCORES',str(int(self.XCPU)*int(self.YCPU))], # number of cores ROMS used
            ['NUMCICECORES',str(int(self.CICECPU))]              # number of cores CICE used
            ]
            ########################################################################
            # List of CICE keywords:
            ########################################################################
            #if (cice_rst_day == start_date.day):
            # if (restart == True):
            #     cicerst_truefalse = ".true."
            # else:
            #     cicerst_truefalse = ".false."
            self.CICEKEYWORDLIST=[
            ['CICEYEARSTART',start_date.strftime("%Y")],  # jiao start year
            ['CICESTARTSTEP',str(int(cice_start_step))],  #number of hours after 00:00 Jan 1st # jiao steps from start_date year Jan 1st, numbers of hours because the step = 1 hour for CICE
            ['CICEDELTAT',str(self.CICEDELTAT)],          # jiao CICE step (unit in second)
            ['CICENPT',str(int((self.FCLEN/self.CICEDELTAT)-(cice_rst_time - cice_start_step)))],   # minus diff restart og start_date # jiao cice_rst_time==cice_start_step when restart is false
            ['CICERUNTYPE',"'continue'"],
            ['CICEIC',"'default'"],
            ['CICEREST',".true."],
            ['CICERSTTIME',cicerst_truefalse],
            #['<cicedir>',GlobalParams.COMMONPATH + "/../../../tmproms/cice"]
            ]
            ########################################################################
            ########################################################################
            ########################################################################
            ########################################################################
        else:
            print 'Unknown application, will exit now'
            sys.exit()

    def change_run_param(self,keyword,value):
        for keyvalue in self.KEYWORDLIST:
            if keyvalue[0]==keyword:
                keyvalue[1]=str(value)
