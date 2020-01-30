# getShotsHelper.py
#
# This gets you a list of Shot objects from a Sequence as Python Dictionaries, with original TrackItem, shot name, source file path and a QImage of the Shot Thumbnail.
# It can be used as the preparation stage of uploading thumbnails, shots, etc. to your Shotgun/FTrack database.
#
# Usage:
# ------------------------------
# myShots = getShotsFromSequence( mySequence ), where mySequence is a hiero.core.Sequence object
# myShots = getShotsFromSequenceInCurrentViewer() - gets shots from the Sequence currently in the Viewer
# Get the name of the first shot: myShots[0]['shotName']
# Get the source file path used in the first shot: myShots[0]['sourceFile']

# If you want to interrogate the Shot's in/out points etc, get the TrackItem object via: myShot[trackItem]

# Notes on Saving out thumbnails
# ------------------------------
# This code does not save any image files for you as it stands, but it stores images as QImages, which can later be saved/manipulated.
# If you want to save the QImage to disk from a shot dictionary, myShot, do: myShot['shotThumb'].save('/tmp/some/path.png')
# For more on QImage, check out: http://qt-project.org/doc/qt-4.8/qimage.html, in particular, save()
# If you need more control over the output of your images, check out the QImageWriter Docs.
# QImageWrite Docs: https://deptinfo-ensip.univ-poitiers.fr/ENS/pyside-docs/PySide/QtGui/QImageWriter.html
#
# Antony Nasce, 2013

import hiero.ui
from PySide import QtCore

# Returns a list of Shots in a Sequence
def getShotsFromSequence(sequence):
    """getShotsFromSequence(sequence) ->
    @param: sequence - a hiero.core.Sequence
    return: A list of shots found in the Sequence, with TrackItem, name and QImage thumbnail.
    """
    if not sequence:
        raise "No valid Viewer found"

    SHOTS = []
    mbar = hiero.ui.mainWindow().statusBar()
    mbar.setHidden(False)
    if isinstance(sequence,hiero.core.Clip):
        raise 'Input must be a Sequence with TrackItems'
    else:
        tracks = sequence.items()
        for track in tracks:
            shots = list(track.items())
            for shot in shots:
                mbar.showMessage('Generating Shot Thumbs: Processing Track %s, Shot %s' % (shot.parent(),shot.name()))
                QtCore.QCoreApplication.processEvents()
                SHOTS+=[getShotWithNameAndThumbnail(shot)]
    mbar.setHidden(True)
    return SHOTS

# This can be called to get a list of Shots from the Sequence in the current Viewer
def getShotsFromSequenceInCurrentViewer(viewer = hiero.ui.currentViewer() ):
    """getShotsFromSequenceInCurrentViewer(sequence) ->
    @param: sequence - a hiero.core.Sequence
    return: A list of shots found in the Sequence, with TrackItem, name and QImage thumbnail.
    """
    if not isinstance(viewer, hiero.ui.Viewer):
        raise "No valid Viewer found"

    # Get the current Sequence in the Viewer
    currentSequence = viewer.player().sequence()

    # Go through each shot in this Sequence and get a Shot Dictionary
    shotDict = getShotsFromSequence(currentSequence)
    return shotDict

# Just a convenience method for getting a dictionary of Shots, with TrackItems, the shotName, and a QImage thumbnail
def getShotWithNameAndThumbnail(shot):
    shotDict = {}
    shotDict['trackItem'] = shot
    shotDict['shotName'] = shot.name()
    shotDict['sourceFile'] = shot.source().mediaSource().fileinfos()[0].filename()

    try:
        shotDict['shotThumb'] = shot.thumbnail()
    except:
        print 'Unable to get thumbnail for TrackItem %s' % shot.name()
        pass

    return shotDict
