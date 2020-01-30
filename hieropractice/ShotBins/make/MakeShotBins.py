# Make Shot Bins Tool v1, 17/09/2012, Matt Brealey
# A tool for creating a single bin for every selected track.
# Combined with the shot bins exporter this makes it easy to export files to a nuke file.

# Usage:
# For Hiero, copy this file to ~/.hiero/Python/StartupUI/

import PySide, hiero

class MakeShotBins_AutoAction(PySide.QtGui.QAction):

    def __init__(self):
         PySide.QtGui.QAction.__init__(self, "Make Shot Bins", None)
         self.triggered.connect(self.MakeShotBins_Auto)
         hiero.core.events.registerInterest("kShowContextMenu/kTimeline", self.eventHandler)



    def MakeShotBins_Auto(self) :

        #Get selected items
        selected = hiero.ui.activeView().getSelection()
        seq = selected[0].parent().parent()
        proj = seq.project()

        #begin Undo
        proj.beginUndo('Make Shot Bins')

        #Make Main Folder if needed
        clipsBin = proj.clipsBin()
        mainFolder = None
        for item in clipsBin.items() :
            if isinstance(item, hiero.core.Bin) and item.name() == "Shot Bins" :
                mainFolder = item
                break
        if type(mainFolder) != hiero.core.Bin :
            mainFolder = hiero.core.Bin("Shot Bins")
            clipsBin.addItem(mainFolder)

        #Get contents of main folder
        mainFolderNames = [x.name() for x in mainFolder.items()]

        #Make all folder
        if "All Shots" not in mainFolderNames :
            mainFolder.addItem(hiero.core.Bin("All Shots"))
            mainFolderNames.append("All Shots")

        #Loop through selected and make Bins
        for item in selected :
            if item.name() not in mainFolderNames :
                mainFolder.addItem(hiero.core.Bin(item.name()))
                mainFolderNames.append(item.name())

        #end Undo
        hiero.ui.activeView().sequence().project().endUndo()


    def eventHandler(self, event):
        if not hasattr(event.sender, 'selection'):
                # Something has gone wrong, we shouldn't only be here if raised
                # by the timeline view which will give a selection.
                return

        s = event.sender.selection()
        if s is None:
            s = [] #hide on empty selection.
        title = "Make Shot Bins"
        self.setText(title)
        self.setVisible(len(s)>0)
        event.menu.addAction(self)

# Instantiate the action to get it to register itself.
MakeShotBins_AutoAction = MakeShotBins_AutoAction()
