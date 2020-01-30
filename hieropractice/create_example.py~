# Shows how to create a new project, add clips, and create a sequence

from hiero.core import newProject
from hiero.core import BinItem
from hiero.core import MediaSource
from hiero.core import Clip
from hiero.core import Sequence
from hiero.core import VideoTrack
import os.path
import sys

# create a new project
myProject = newProject()

# create some bins for it
bin1 = Bin("Bin 1")
bin2 = Bin("Bin 2")
bin3 = Bin("Bin 3")

# make bin2 a sub bin of bin1
bin1.addItem(bin2)

# attach the bins to the project
clipsBin = myProject.clipsBin()
clipsBin.addItem(bin1)
clipsBin.addItem(bin3)

def findResourcePath():
    import PySide.QtCore

    hieroExecutablePath = PySide.QtCore.QCoreApplication.applicationDirPath()
    resourcesPath = str(os.path.abspath(os.path.join(hieroExecutablePath, "Documentation", "Python", "Resources")))

    # OS X paths are a bit different...
    if sys.platform.startswith("darwin")    :
        hieroExecutablePath = os.path.join(hieroExecutablePath, "..")
        resourcesPath = str(os.path.abspath(os.path.join(hieroExecutablePath, "Resources", "Python", "Resources")))

    return resourcesPath

# find the path to the resources that ship with Hiero
resourcesPath = findResourcePath()

# make some media sources
source1 = MediaSource(os.path.join(resourcesPath, "blue_green_checkerboard.mov"))
source2 = MediaSource(os.path.join(resourcesPath, "red_black_checkerboard.mov"))
source3 = MediaSource(os.path.join(resourcesPath, "colour_bars.mov"))
source4 = MediaSource(os.path.join(resourcesPath, "colour_wheel.mov"))
source5 = MediaSource(os.path.join(resourcesPath, "purple.######.dpx"))

# make some clips from the media sources
clip1 = Clip(source1)
clip2 = Clip(source2)
clip3 = Clip(source3)
clip4 = Clip(source4)
clip5 = Clip(source5)

# add the clips to the bins
clipsBin.addItem(BinItem(clip1))
bin1.addItem(BinItem(clip2))
bin2.addItem(BinItem(clip3))
bin3.addItem(BinItem(clip4))
bin3.addItem(BinItem(clip5))

# create a new sequence and attach it to the project
sequence = Sequence("NewSequence")
clipsBin.addItem(BinItem(sequence))

# helper method for creating track items from clips
def createTrackItem(track, trackItemName, sourceClip, lastTrackItem=None):
    # create the track item
    trackItem = track.createTrackItem(trackItemName)

    # set it's source
    trackItem.setSource(sourceClip)

    # set it's timeline in and timeline out values, offseting by the track item before if need be
    if lastTrackItem:
        trackItem.setTimelineIn(lastTrackItem.timelineOut() + 1)
        trackItem.setTimelineOut(lastTrackItem.timelineOut() + sourceClip.duration())
    else:
        trackItem.setTimelineIn(0)
        trackItem.setTimelineOut(trackItem.sourceDuration()-1)

    # add the item to the track
    track.addItem(trackItem)
    return trackItem

# create a track to add items/clips to
track = VideoTrack("VideoTrack")

# create the track items, each one offset from the one before it
trackItem1 = createTrackItem(track, "TrackItem1", clip1)
trackItem2 = createTrackItem(track, "TrackItem2", clip2, lastTrackItem=trackItem1)
trackItem3 = createTrackItem(track, "TrackItem3", clip3, lastTrackItem=trackItem2)
trackItem4 = createTrackItem(track, "TrackItem4", clip4, lastTrackItem=trackItem3)
trackItem5 = createTrackItem(track, "TrackItem5", clip5, lastTrackItem=trackItem4)

# add the track to the sequence now
sequence.addTrack(track)
