from hiero.core import *
from hiero.ui import *
from PySide.QtGui import *
from PySide.QtCore import *

class ReinstateAudioFromSource(QAction):

    def __init__(self):
            QAction.__init__(self, "Reinstate Audio", None)
            self.triggered.connect(self.doit)
            hiero.core.events.registerInterest("kShowContextMenu/kTimeline", self.eventHandler)
            hiero.core.events.registerInterest("kShowContextMenu/kSpreadsheet", self.eventHandler)

    def trackExists(self, sequence, trackName):
        for track in sequence:
            if track.name() == trackName:
                return track
        return None

    def reAddAudioFromSource(self, selection):
        for item in selection:
            track = item.parent()
            sequence = track.parent()
            bin = sequence.project().clipsBin()

            if item.source().mediaSource().hasAudio() and isinstance(item.parent(), hiero.core.VideoTrack):
                inTime = item.timelineIn()
                outTime = item.timelineOut()
                sourceIn = item.sourceIn()
                sourceOut = item.sourceOut()
                newclip = Clip(MediaSource(item.source().mediaSource()))
                bin.addItem(BinItem(newclip))
                newclip.setInTime(0)
                newclip.setOutTime(newclip.duration())
                newclip.setInTime(sourceIn)
                newclip.setOutTime(sourceOut)
                videoClip = track.addTrackItem(newclip, inTime)
                for i in range(item.source().numAudioTracks()):
                    newName = "Audio " + str( i+1 )
                    mediaOnTrack = False
                    if self.trackExists(sequence, newName) is None:
                        audiotrack = sequence.addTrack(hiero.core.AudioTrack("Audio " + str( i+1 )))
                    else:
                        audiotrack = self.trackExists(sequence, newName)
                    if len(audiotrack.items()) > 0:
                        for item in audiotrack.items():
                            if item.timelineIn() in range(inTime, outTime) or item.timelineOut() in range(inTime, outTime):
                                mediaOnTrack = True
                                break
                    if mediaOnTrack:
                        newaudiotrack = sequence.addTrack(hiero.core.AudioTrack("New Track " + str( i + 1)))
                        audioClip = newaudiotrack.addTrackItem(newclip, i, inTime)
                    else:
                        audioClip = audiotrack.addTrackItem(newclip, i, inTime)

                    audioClip.link(videoClip)

    def doit(self):
        selection = hiero.ui.activeView().selection()
        self.reAddAudioFromSource(selection)

    def eventHandler(self, event):
        if not hasattr(event.sender, 'selection'):
            return

        s = event.sender.selection()
        if s is None:
            s = ()

        title = "Reinstate Audio"
        self.setText(title)
        self.setEnabled( len(s) > 0 )
        event.menu.addAction(self)

action = ReinstateAudioFromSource()
