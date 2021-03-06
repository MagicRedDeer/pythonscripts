from hiero.core import events
import PySide.QtGui as gui


class DisplaySelection(gui.QDialog):
    def __init__(self, selection):
        gui.QDialog.__init__(self)

        self.setWindowTitle("Selected Items")

        layout = gui.QVBoxLayout()
        for sel in selection:
            item = gui.QLabel(sel.name())
            layout.addWidget(item)
        self.setLayout(layout)

        box = gui.QDialogButtonBox(gui.QDialogButtonBox.StandardButton.Ok)
        box.button(gui.QDialogButtonBox.StandardButton.Ok).set("Got It")
        layout.addWidget(box)

def event_handler(event, *args):
    def click(*args):
        dialog = DisplaySelection(event.sender.selection())
        dialog.exec_()
    action = gui.QAction(event.menu)
    action.setText("Display Selected Items")
    action.triggered.connect(click)
    event.menu.addAction(action)

events.registerInterest("kShowContextMenu/kTimeline", event_handler)
#events.unregisterInterest("kShowContextMenu/kTimeline", event_handler)

