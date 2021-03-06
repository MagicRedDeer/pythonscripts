# This example opens the current Hiero Viewer frame in Nuke
# Note: You must specify a valid Nuke path in Hiero's 'Nuke / Export' preferences

import os.path
import tempfile
from hiero.core import *
from hiero.ui import *
from PySide.QtGui import *
from PySide.QtCore import *
import hiero.core.nuke

def mapRetime(ti, timelineTime):
    return ti.sourceIn() + int((timelineTime - ti.timelineIn()) * ti.playbackSpeed())

def getCurrentViewerFrameInfo():
    # Get current Viewer Frame
    cv = hiero.ui.currentViewer()

    # Get the Current Player Object
    p = cv.player()

    # Get the current Time in the Player
    T = p.time()

    # Get the current Sequence in the Viewer
    seq = p.sequence().binItem().activeItem()

    # Must cater for Sequences and Clips...
    if isinstance(seq,hiero.core.Sequence):
        # Get the TrackItem at Time T
        trackItem = seq.trackItemAt(T)
        clip = trackItem.source()
        first_last_frame = int(mapRetime(trackItem,T)+clip.sourceIn())
    elif isinstance(seq,hiero.core.Clip):
        clip = seq
        first_last_frame = int(T+clip.sourceIn())

    # File Source
    # Check if media is offline first!
    if clip.mediaSource().isOffline():
        return None, None, None
    file_knob = clip.mediaSource().fileinfos()[0].filename()
    # Adjust by 1 frame if it's a QuickTime
    if file_knob.find('.mov')!=-1:
        first_last_frame+=1
    return file_knob, first_last_frame, clip

class OpenFrameWithNuke(QAction):

    def __init__(self):
            QAction.__init__(self, "Open Frame With Nuke", None)
            self.triggered.connect(self.generateClipFromCurrentFrame)
            hiero.core.events.registerInterest("kShowContextMenu/kViewer", self.eventHandler)

    def generateClipFromCurrentFrame(self):
        fileKnob,first_last_frame,clip = getCurrentViewerFrameInfo()
        if fileKnob==None:
            msg = QMessageBox()
            msg.setText("Media is Offline. Cannot open with Nuke.")
            msg.exec_()
            return 1
        newClip = Clip(MediaSource(fileKnob),first_last_frame,first_last_frame)

        # If you wish to create a new Clip containing this still frame, uncomment this block
        """p = clip.project()
        rt = p.clipsBin()
        try:
            B = rt['Stills']
        except:
            B = rt.addItem(hiero.core.Bin('Stills'))
            B = rt['Stills']
        BI = BinItem(newClip)
        B.addItem(BI)"""

        # Create a Nuke Script for this Frame
        rootNode = hiero.core.nuke.RootNode(first_last_frame,first_last_frame,25)
        writer = hiero.core.nuke.ScriptWriter()
        writer.addNode(rootNode)
        readNode = hiero.core.nuke.ReadNode(fileKnob,firstFrame=first_last_frame,lastFrame=first_last_frame)
        newClipName = newClip.name()
        readNode.setKnob('name',newClipName)
        writer.addNode(readNode)
        #writeNode = hiero.core.nuke.WriteNode(fileKnob)
        #writer.addNode(writeNode)
        viewerNode = hiero.core.nuke.Node("Viewer")
        writer.addNode(viewerNode)

        tmpDir = tempfile.gettempdir()
        scriptPathExt = 'HieroFrameExport_%s.nk' % (newClipName)
        scriptPath = os.path.join(tmpDir,scriptPathExt)
        print 'Writing to: %s' % str(scriptPath)
        writer.writeToDisk(scriptPath)
        hiero.core.nuke.Script.launchNuke(scriptPath)
        return 0


    def eventHandler(self, event):
        enabled = True
        title = "Open Frame With Nuke"
        self.setText(title)
        event.menu.addAction( self )

# Instantiate the action to get it to register itself.
openFrameWithNuke = OpenFrameWithNuke()

