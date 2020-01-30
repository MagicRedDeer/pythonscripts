# This is a little snippet to clear the Viewer cache prior to raising the Export dialog.
# The advantage of doing this for a local Nuke transcode is that you will regain some extra RAM, which hopefully helps the machine stay responsive and fast.
# To get the best transcode times, you should use this in conjunction with the Preferences > Nuke / Export > "Do not limit Nuke" option.
# Usage: Copy to ~/.hiero/Python/Startup
# Note: This will clear all your Viewer caches every time the Export dialog is raised - NOT prior to transcoding.
import hiero.ui
import hiero.core

def clearCache(event):
    print 'Export dialog shown. Clearing all viewer caches'
    hiero.ui.flushAllViewersCache()

hiero.core.events.registerInterest('kExportDialog', clearCache)
