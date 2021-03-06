# Class to show how to handle drop events in the bin view
from hiero.core.events import *


class BinViewDropHandler:
    kTextMimeType = "text/plain"

    def __init__(self):
        # hiero doesn't deal with drag and drop for text/plain data, so tell it to allow it
        hiero.ui.registerBinViewCustomMimeDataType(BinViewDropHandler.kTextMimeType)

        # register interest in the drop event now
        registerInterest((EventType.kDrop, EventType.kBin), self.dropHandler)

    def dropHandler(self, event):

        # get the mime data
        print "mimeData: ", event.mimeData

        # fast/easy way to get at text data
        #if event.mimeData.hasText():
        #  print event.mimeData.text()

        # more complicated way
        if event.mimeData.hasFormat(BinViewDropHandler.kTextMimeType):
            byteArray = event.mimeData.data(BinViewDropHandler.kTextMimeType)
            print byteArray.data()

            # signal that we've handled the event here
            event.dropEvent.accept()

        # get custom hiero objects if drag from one view to another (only present if the drop was from one hiero view to another)
        if hasattr(event, "items"):
            print "hasItems"
            print event.items

        # figure out which item it was dropped onto
        print "dropItem: ", event.dropItem

        # get the widget that the drop happened in
        print "dropWidget: ", event.dropWidget

        # get the higher level container widget (for the Bin View, this will be the Bin View widget)
        print "containerWidget: ", event.containerWidget

        # can also get the sender
        print "eventSender: ", event.sender

    def unregister(self):
        unregisterInterest((EventType.kDrop, EventType.kBin), self.dropHandler)
        hiero.ui.unregisterBinViewCustomMimeDataType(BinViewDropHandler.kTextMimeType)

# Instantiate the handler to get it to register itself.
dropHandler = BinViewDropHandler()
