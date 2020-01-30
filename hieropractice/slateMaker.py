import hiero.core as hcore
import hiero.ui as hui


import PySide.QtGui as gui


class SlateDialog(gui.QDialog):
    pass

class SlateMaker(gui.QAction):

    def __init__(self):
        gui.QAction.__init__(self, "Slate Maker", None)
        self.triggered.connect(self.doit)
        hcore.registerInterest("kShowContextMenu/kTimeline", self.doit)

    def doit(self):
        pass

    def eventHandler(self, event):
        if not hasattr(event.sender, "selection"):
            return

        selection = event.sender.selection()
        if selection is None:
            s = []

