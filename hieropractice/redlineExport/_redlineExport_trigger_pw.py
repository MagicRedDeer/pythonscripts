# _redlineExport_pw by Paul Wiens, November 30 2012
# v1b1
# Usage:
# Copy these files to:  ../Hiero1.5v1.app/Contents/Plugins/site-packages/hiero/exporters/
    # _redlineExport_pw.py
    # _redlineExport_trigger_pw.py
    # _redLineRender_OSA.scpt
# Open the __init__.py found in the Hiero folder above, and add this line of code under "try:" on line 11:  import _redlineExport_trigger_pw

# This script adds a right-click menu item to the Timeline View to export a .r3d clip using redLine

from PySide.QtGui import *
from hiero.core import *
import hiero, hiero.ui
import os,sys
from _redlineExport_pw import *

class SelectedShotAction(QAction):
    def __init__(self):
        QAction.__init__(self, "Redline Export Tool", None)
        self.triggered.connect(self.getShotSelection)
        hiero.core.events.registerInterest("kShowContextMenu/kTimeline", self.eventHandler)

    def getShotSelection(self):
        #Get the shot selection and stuff it in: hiero.selectedShots
        selection = self._selection
        if len(selection)==1:
            selection = selection[0]
        hiero.selectedShots = selection
        selShots = hiero.selectedShots
        try :
            for i in selShots :
                self.a = redlineExport(i)
                self.a.show()
        except  :
            self.a = redlineExport(selShots) #actually only sends one shot
            self.a.show()

    def eventHandler(self, event):
        self._selection = None
        if hasattr(event.sender, 'getSelection') and event.sender.getSelection() is not None and len( event.sender.getSelection() ) != 0:
            selection = event.sender.getSelection() # Here, you could also use: hiero.ui.activeView().selection()
            self._selection = [shot for shot in selection if isinstance(shot,hiero.core.TrackItem)] # Filter out just TrackItems
          # Add the Menu to the right-click menu with an appropriate title
            if len(selection)>0:
                title = "Redline Export" if len(self._selection)==1 else "Redline Exports"
                self.setText(title)
                event.menu.addAction( self )

SelectedShotAction = SelectedShotAction()
