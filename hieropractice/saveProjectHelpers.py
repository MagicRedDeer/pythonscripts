# saveProjectHelpers - Adds two actions to the Bin view:
# 1) Save All Projects - saves all opened Projects
# 2) Save New Version - ups the version number (v#) of a project, from v01.hrox to v02.hrox
# Install in ~/.hiero/Python/StartupUI
# Requires Hiero 1.5v1 or later

from hiero.core import *
from hiero.core.util import *
from hiero.ui import *
from PySide.QtGui import *
from PySide.QtCore import *

# Method to Save a new Version of the activeHrox Project
class SaveAllProjects(QAction):

    def __init__(self):
        QAction.__init__(self, "Save All Projects...", None)
        self.triggered.connect(self.projectSaveAll)
        hiero.core.events.registerInterest("kShowContextMenu/kBin", self.eventHandler)

    # Action to Save all currently opened User Projects
    def projectSaveAll(self):
        allProjects = hiero.core.projects(hiero.core.Project.kUserProjects)
        for proj in allProjects:
            try:
                proj.save()
                print 'Saved Project to:\n%s ' % (proj.path())
            except:
                msgBox = QMessageBox()
                msgBox.setText('Unable to save Project: %s to: %s. Check file permissions.' % (proj.name(),proj.path()));
                msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel);
                msgBox.setDefaultButton(QMessageBox.Ok);
                ret = msgBox.exec_()
                print 'Unable to save Project: %s to: %s. Check file permissions.' % (proj.name(),proj.path())
                return
        msgBox = QMessageBox()
        msgBox.setText('All projects saved:\n %s ' % (str(allProjects)));
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel);
        msgBox.setDefaultButton(QMessageBox.Ok);
        ret = msgBox.exec_()

    def eventHandler(self, event):
        event.menu.addAction( self )

# For projects with v# in the path name, saves out a new Project with v#+1
class SaveNewProjectVersion(QAction):

    def __init__(self):
        QAction.__init__(self, "Save New Version...", None)
        self.triggered.connect(self.saveNewVersion)
        hiero.core.events.registerInterest("kShowContextMenu/kBin", self.eventHandler)
        self.selection = None

    # Action to Save a New Version for projects with _v# in the project name
    def saveNewVersion(self):
        if len(self.selectedProjects) is not None:
            for proj in self.selectedProjects:
                oldName = proj.name()
                path = proj.path()
                v = None
                prefix = None
                try:
                    (prefix,v) = version_get(path,'v')
                except ValueError, msg:
                    print msg

                if (prefix is not None) and (v is not None):
                    v = int(v)
                    newPath = version_set(path,prefix,v,v+1)
                    try:
                        proj.saveAs(newPath)
                        msgBox = QMessageBox()
                        msgBox.setText('Saved new project version to:\n%s ' % (newPath));
                        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel);
                        msgBox.setDefaultButton(QMessageBox.Ok);
                        ret = msgBox.exec_()
                        print 'Saved new project version to:\n%s ' % (newPath)
                    except:
                        msgBox = QMessageBox()
                        msgBox.setText('Unable to save Project: %s. Check file permissions.' % (oldName));
                        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel);
                        msgBox.setDefaultButton(QMessageBox.Ok);
                        ret = msgBox.exec_()
                        print 'Unable to save Project: %s. Check file permissions.' % (oldName)
                else:
                    print 'Project: ',proj, ' does not contain a version string (v#)'
                    msgBox = QMessageBox()
                    msgBox.setText('No "_v#" found in %s.\nSave as %s_v01?' % (oldName,oldName));
                    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel);
                    msgBox.setDefaultButton(QMessageBox.Ok);
                    ret = msgBox.exec_()
                    if ret == QMessageBox.Ok:
                            print 'Saving to:  +_v01'
                            try:
                                newPath = path.replace(oldName+'.hrox',oldName+'_v01.hrox')
                                proj.saveAs(newPath)
                                msgBox = QMessageBox()
                                msgBox.setText('Saved new project version to:\n%s ' % (newPath));
                                msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel);
                                msgBox.setDefaultButton(QMessageBox.Ok);
                                ret = msgBox.exec_()
                                print 'Saved new project version to:\n%s ' % (newPath)
                            except:
                                print 'Unable to save Project: %s. Check file permissions.' % (oldName)

                    elif ret == QMessageBox.Cancel:
                            print 'do nothing'

    def eventHandler(self, event):
        self.selection = None
        if hasattr(event.sender, 'selection') and event.sender.selection() is not None and len( event.sender.selection() ) != 0:
            selection = event.sender.selection()
            self.selectedProjects = uniquify([item.project() for item in selection])
            event.menu.addAction( self )

# Instantiate the actions
saveAllAct = SaveAllProjects()
saveNewAct = SaveNewProjectVersion()
