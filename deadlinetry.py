#Python.NET
import Deadline.Plugins
from Deadline.Plugins import *

def __main__():
    print GetPulseDirectory()
    print Deadline.Plugins
    obj =  Deadline.Plugins.DeadlinePlugin()
    print obj
    print help(
            Deadline.Plugins.DeadlinePlugin.WriteStdinToMonitoredManagedProcess
            )
    # print dir(Deadline.Plugins.DeadlinePlugin)
