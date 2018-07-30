import sys
import os
import ctypes

#sys.path.append(os.path.abspath('/home/tango-cs/OmniDriverSPAM/include'))
#sys.path.append(os.path.abspath('/usr/lib/jvm/java-8-openjdk-amd64/include'))
#sys.path.append(os.path.abspath('/usr/lib/jvm/java-8-openjdk-amd64/include/linux'))
#--------------------------------------------------------------------------
#sys.path.append(os.path.abspath('/home/tango-cs/OmniDriverSPAM'))
#sys.path.append(os.path.abspath('/home/tango-cs/OmniDriverSPAM/OOI_HOME'))
#sys.path.append(os.path.abspath('/home/tango-cs/OmniDriverSPAM/OOI_HOME'))
#sys.path.append(os.path.abspath('PATH'))
#sys.path.append(os.path.abspath('/home/tango-cs/OmniDriverSPAM/_jvm'))
#sys.path.append(os.path.abspath('/usr/lib/jvm/java-8-openjdk-amd64'))
#sys.path.append(os.path.abspath('/home/tango-cs/OmniDriverSPAM/OOI_HOME/lib/amd64/server'))
#--------------------------------------------------------------------------

#for i in range(0, len(sys.path)):
#print(sys.path[i])

#libomni = ctypes.CDLL('/home/tango-cs/OmniDriverSPAM/OOI_HOME/libOmniDriver.so')
libomni = ctypes.CDLL('/usr/lib/libOmniDriver.so')
#libcommon = ctypes.CDLL('/home/tango-cs/OmniDriverSPAM/OOI_HOME/libOmniDriver.so',mode=ctypes.RTLD_GLOBAL)


