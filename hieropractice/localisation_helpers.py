# Localisation Helper Functions -
# These methods allow you to Localise Clips on Bins, Shots, Tracks and Sequences
import hiero.core
import PySide.QtGui
import PySide.QtCore

# This is just a convenience method for returning QActions with a title, triggered method and icon.
def createMenuAction(title, method, icon = None ):
    action = PySide.QtGui.QAction(title,None)
    action.setIcon(PySide.QtGui.QIcon(icon))
    action.triggered.connect( method )
    return action

def setlocalisationPolicyOnTrack(track, extensionList = [None], policy = hiero.core.Clip.kAlwaysLocalise ):
    """Localises all TrackItems in a Track
    setlocalisationPolicyOnTrack( track, policy = hiero.core.Clip.kAlwaysLocalise ):
    @param: track - a list of hiero.core.Clip objects
    @param: extensionList - a list of file extensions, e.g. ['dpx','exr','mov']
    @param: policy - the localisation policy (kAlwaysLocalise,kAutoLocalise,kNeverLocalise)"""
    if not isinstance(track,(hiero.core.VideoTrack,hiero.core.AudioTrack)):
        hiero.core.log.info('First argument must be a hiero.core.VideoTrack/hiero.core.AudioTrack')
        return
    else:
        for ti in track:
            ti.source().setLocalisationPolicy( policy )


def setlocalisationPolicyOnTrackItem(trackItem, extensionList = [None], policy = hiero.core.Clip.kAlwaysLocalise ):
    """Localises all TrackItems in a Track
    setlocalisationPolicyOnTrack( track, policy = hiero.core.Clip.kAlwaysLocalise ):
    @param: track - a list of hiero.core.Clip objects
    @param: extensionList - a list of file extensions, e.g. ['dpx','exr','mov']
    @param: policy - the localisation policy (kAlwaysLocalise,kAutoLocalise,kNeverLocalise)"""
    if not isinstance(trackItem,(hiero.core.TrackItem)):
        hiero.core.log.info('First argument must be a hiero.core.TrackItem')
        return
    else:
        trackItem.source().setLocalisationPolicy( policy )

def setlocalisationPolicyOnSequence(sequence, extensionList = [None], policy = hiero.core.Clip.kAlwaysLocalise ):
    """Localises all Clips used in a Sequence
    @param: clipList - a list of hiero.core.Clip objects
    @param: extensionList - a list of file extensions, e.g. ['dpx','exr','mov']
    @param: policy - the localisation policy (kAlwaysLocalise,kAutoLocalise,kNeverLocalise)"""
    if not isinstance(sequence,(hiero.core.Sequence)):
        hiero.core.log.info('First argument must be a hiero.core.Sequence')
        return
    else:
        for track in sequence.items():
            for ti in track:
                if isinstance(ti,(hiero.core.TrackItem)):
                    clip = ti.source()
                    if clip.localisationPolicy != policy:
                        clip.setLocalisationPolicy(policy)

def setlocalisationPolicyOnBin(bin, extensionList = [None], policy = hiero.core.Clip.kAlwaysLocalise, recursive = True ):
    """Localises all Clips, recursively found in all Sub-Bins
    @param: clipList - a list of hiero.core.Clip objects
    @param: extensionList - a list of file extensions, e.g. ['dpx','exr','mov']
    @param: policy - the localisation policy (kAlwaysLocalise,kAutoLocalise,kNeverLocalise)"""

    clips =[]

    if not isinstance(bin,(hiero.core.Bin)):
        hiero.core.log.info('First argument must be a hiero.core.Bin')
        return
    else:
        if recursive:
            # Here we're going to walk the entire Bin view, for all Clips contained in this Bin
            clips += hiero.core.findItemsInBin(bin, filter = hiero.core.Clip)
        else:
            # Here we just get Clips at the 1st level of the Bin
            clips = bin.clips()

    for clip in clips:
        if clip.localisationPolicy != policy:
            clip.setLocalisationPolicy(policy)


def setlocalisationPolicyOnClipWithExtension(clip, extensionList = [None], policy = hiero.core.Clip.kAlwaysLocalise ):
    """Localises Clips in clipList with a given file extension in extensionList
    localiseClipsWithExtension(clipList, extensionList = None, policy = hiero.core.Clip.kAlwaysLocalise ):
    @param: clipList - a list of hiero.core.Clip objects
    @param: extensionList - a list of file extensions, e.g. ['dpx','exr','mov']
    @param: policy - the localisation policy (kAlwaysLocalise,kAutoLocalise,kNeverLocalise)"""

    if type(extensionList) != list:
        print "Please supply a list of file extensions, e.g. extensionList=['dpx','exr','mov']"
        return
    else:
        clipPath = clip.mediaSource().filename()
        hiero.core.log.info('clipPath is'+str(clipPath))
        if clipPath.lower().endswith( tuple(extensionList) ):
            clip.setLocalisationPolicy( policy )

class CustomLocalisationDialog(PySide.QtGui.QDialog):

    def __init__(self,itemSelection=None,parent=None):
        super(CustomLocalisationDialog, self).__init__(parent)
        self.setWindowTitle("Select File Extensions to Localise")
        self.setWindowIcon(PySide.QtGui.QIcon("icons:BlendingDisabled.png"))
        self.setSizePolicy( PySide.QtGui.QSizePolicy.Expanding, PySide.QtGui.QSizePolicy.Fixed )

        layout = PySide.QtGui.QFormLayout()
        self._itemSelection = itemSelection

        self._formatFilterEdit = PySide.QtGui.QLineEdit()
        self._formatFilterEdit.setToolTip('Enter a comma separated list of file extensions to localise, e.g. dpx, exr')
        self._formatFilterEdit.setText('dpx')
        layout.addRow("Extension: ",self._formatFilterEdit)

        # Standard buttons for Add/Cancel
        self._buttonbox = PySide.QtGui.QDialogButtonBox(PySide.QtGui.QDialogButtonBox.Ok | PySide.QtGui.QDialogButtonBox.Cancel)
        self._buttonbox.button(PySide.QtGui.QDialogButtonBox.Ok).setText("Add")
        self._buttonbox.accepted.connect(self.accept)
        self._buttonbox.rejected.connect(self.reject)
        layout.addRow("",self._buttonbox)

        self.setLayout(layout)

    def convertFormatStringToFormatList(self):
        formatString = self._formatFilterEdit.text()
        formats = formatString.split(',')
        return formats


    # Set Tag dialog with Note and Selection info. Adds Tag to entire object, not over a range of frames
    def showDialogAndLocaliseSelection(self):

        if len(self._itemSelection)<1:
            hiero.core.log.info('No valid selected Items can be localised')
            return
        items = []

        clips = [item for item in self._itemSelection if isinstance(item, hiero.core.Clip)]

        if len(clips)==0:
            return

        if self.exec_():
            exts = self.convertFormatStringToFormatList()
            hiero.core.log.info('Got this extension list:'+str(exts))
            for clip in clips:
                setlocalisationPolicyOnClipWithExtension(clip, extensionList = exts)
            return



# Menu which adds a Tags Menu to the Viewer, Project Bin and Timeline/Spreadsheet
class CustomLocaliseMenu:

    def __init__(self):
            self._localiseMenu = None
            self._customLocaliseDialog = None

            # These actions in the viewer are a special case, because they drill down in to what is currrenly being
            self._localiseBinContents = createMenuAction("This Bin", self.localiseBinSelection,icon="icons:Bin.png")
            self._localiseThisBinSequence = createMenuAction("This Sequence", self.localiseBinSelection,icon="icons:TimelineStroked.png")
            self._localiseBinContentsCustom = createMenuAction("This Bin Custom...", self.localiseBinSelectionCustom,icon="icons:BlendingDisabled.png")
            self._localiseThisSequence  = createMenuAction("This Sequence", self.localiseTimelineSpreadsheetSequence,icon="icons:TimelineStroked.png")
            self._localiseThisTrack  = createMenuAction("This Track", self.localiseTimelineSpreadsheetSelection,icon="icons:Tracks.png")
            self._localiseThisShot  = createMenuAction("This Shot", self.localiseTimelineSpreadsheetSelection,icon="icons:Mask.png")

            hiero.core.events.registerInterest("kShowContextMenu/kBin", self.binViewEventHandler)
            hiero.core.events.registerInterest("kShowContextMenu/kTimeline", self.timelineSpreadsheetEventHandler)
            hiero.core.events.registerInterest("kShowContextMenu/kSpreadsheet", self.timelineSpreadsheetEventHandler)

    def createLocaliseMenuForView(self, viewName):
        localiseMenu = PySide.QtGui.QMenu("Localise")
        if viewName == 'kBin':
            localiseMenu.addAction(self._localiseBinContents)
            localiseMenu.addAction(self._localiseBinContentsCustom)
            localiseMenu.addAction(self._localiseThisBinSequence)

        elif viewName == 'kTimeline/kSpreadsheet':
            localiseMenu.addAction(self._localiseThisSequence)
            localiseMenu.addAction(self._localiseThisTrack)
            localiseMenu.addAction(self._localiseThisShot)

        return localiseMenu

    # Called from the Bin View, to a BinItem selection.
    # Note: A mixed selection of Bins AND Sequences is not currently supported.
    def localiseBinSelection(self):
        if self._selection == None:
            return
        elif isinstance(self._selection[0],hiero.core.Bin):
            for bin in self._selection:
                setlocalisationPolicyOnBin(bin)

        elif isinstance(self._selection[0],hiero.core.Sequence):
            for seq in self._selection:
                setlocalisationPolicyOnSequence(seq)

    # Called from the Bin View, to localise all Clips with a custom Extension
    def localiseBinSelectionCustom(self):
        if self._selection == None:
            return
        elif isinstance(self._selection[0],hiero.core.Bin):
            clips = []
            for bin in self._selection:
                clips += hiero.core.findItemsInBin(bin, filter = hiero.core.Clip)
            # Present Custom Localise Dialog:
            if len(clips)>=1:
                CustomLocalisationDialog(itemSelection=clips).showDialogAndLocaliseSelection()

    # Called from the Spreadsheet or Timeline View, to localise all Clips in the Shot or Track
    def localiseTimelineSpreadsheetSelection(self):
        if self._selection == None:
            return

        elif isinstance(self._selection[0],hiero.core.TrackItem):
            for ti in self._selection:
                setlocalisationPolicyOnTrackItem(ti)

        elif isinstance(self._selection[0],(hiero.core.VideoTrack,hiero.core.AudioTrack)):
            for track in self._selection:
                setlocalisationPolicyOnTrack(track)

    # Called from the Spreadsheet or Timeline View, to localise all Clips in the current Sequence
    def localiseTimelineSpreadsheetSequence(self):
        if self._selection == None:
            return

        # We should only have one Sequence to localise. Take just the first item
        sequenceItem = self._selection[0]

        if isinstance(sequenceItem,(hiero.core.VideoTrack,hiero.core.AudioTrack)):
            sequence = sequenceItem.parent()
        elif isinstance(sequenceItem,hiero.core.TrackItem):
            sequence = sequenceItem.parent().parent()

        if isinstance(sequence,hiero.core.Sequence):
            setlocalisationPolicyOnSequence(sequence)

    # This handles events from the Project Bin View
    def binViewEventHandler(self,event):

        if not hasattr(event.sender, 'selection'):
            # Something has gone wrong, we should only be here if raised
            # by the Bin view which gives a selection.
            return
        s = event.sender.selection()

        # Return if there's no Selection. We won't add the Localise Menu.
        if s == None:
            return

        # Filter the selection to only act on Bins
        binSelection = [item for item in s if isinstance(item, (hiero.core.Bin))]
        binItemSelection = [item for item in s if isinstance(item,hiero.core.BinItem)]
        sequenceSelection = [item.activeItem() for item in binItemSelection if isinstance(item.activeItem(),hiero.core.Sequence)]
        self._selection = binSelection+sequenceSelection
        hiero.core.log.info('selection is'+ str(self._selection))

        if len(binSelection)>=1 and len(sequenceSelection)>=1:
            hiero.core.log.debug('Selection must either be a Bin selection or Sequence Selection')
            return

        # Only add the Menu if Bins or Sequences are selected (this ensures menu isn't added in the Tags Pane)
        if len(self._selection) > 0:
            self._localiseMenu = self.createLocaliseMenuForView('kBin')
            binsSelected = len(binSelection)>=1
            sequencesSelected = len(sequenceSelection)>=1
            self._localiseBinContents.setEnabled(len(binSelection)>=1)
            self._localiseBinContentsCustom.setEnabled(len(binSelection)>=1)
            self._localiseThisBinSequence.setEnabled(len(sequenceSelection)>=1)

            # Insert the Tags menu with the Localisation Menu
            hiero.ui.insertMenuAction(self._localiseMenu.menuAction(), event.menu)
        return


    # This handles events from the Project Bin View
    def timelineSpreadsheetEventHandler(self,event):

        if not hasattr(event.sender, 'selection'):
            # Something has gone wrong, we should only be here if raised
            # by the timeline view which gives a selection.
            return
        s = event.sender.selection()

        # Return if there's no Selection. We won't add the Tags Menu.
        if s == None:
            return

        # Filter the selection to only act on TrackItems, not Transitions etc.
        shotSelection = [item for item in s if isinstance(item, (hiero.core.TrackItem))]
        trackSelection = [item for item in s if isinstance(item, (hiero.core.VideoTrack,hiero.core.AudioTrack))]

        if len(shotSelection)>=1 and len(trackSelection)>=1:
            hiero.core.log.debug('Selection must either be a Shot selection or a Track Selection')
            return

        # We don't currently get a mixture of TrackItem and Tracks but combine the two lists to make a selection
        self._selection = shotSelection+trackSelection

        if len(self._selection) > 0:
            self._localiseMenu = self.createLocaliseMenuForView('kTimeline/kSpreadsheet')
            self._localiseThisShot.setEnabled(len(shotSelection)>=1)
            self._localiseThisTrack.setEnabled(len(trackSelection)>=1)

            # Insert the Tags menu with the Clear Tags Option
            hiero.ui.insertMenuAction(self._localiseMenu.menuAction(),  event.menu)
        return

# Instantiate the Menu to get it to register itself.
customLocaliseMenu = CustomLocaliseMenu()




