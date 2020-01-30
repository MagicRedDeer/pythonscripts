# This example shows how you can add custom keyboard shortcuts to Hiero.
# If you wish for this code to be run on startup, copy it to your <HIERO_PATH>/Startup directory.

from hiero.ui import findMenuAction
from PySide import QtGui

### ADD YOUR CUSTOM SHORTCUTS BELOW

# Examples of adding keyboard shortcuts for 'Show Metadata', and 'Open In Spreadsheet View' and the 'Expand Pane' action
# See also: http://www.pyside.org/docs/pyside/PySide/QtGui/QAction.html#PySide.QtGui.PySide.QtGui.QAction.setShortcut

myMenuItem = findMenuAction('Show Metadata')
myMenuItem.setShortcut(QtGui.QKeySequence('Alt+M'))

# This sets a keyboard shortcut for opening the Spreadsheet View
myMenuItem = findMenuAction('foundry.project.openInSpreadsheet')
myMenuItem.setShortcut(QtGui.QKeySequence('S'))

# This allows you to override the Expand Pane (~) keyboard shortcut
for a in hiero.ui.registeredActions():
    if a.objectName() == "foundry.application.expandPane":
        a.setShortcut("Space")
        break

playButton = hiero.ui.findMenuAction('Play/Pause')
playButton.setShortcut("")
