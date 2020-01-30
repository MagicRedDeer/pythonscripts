# An example of creating a dockable panel from Python.
# This script creates a simple PySide Qt web browser.

import hiero.ui
from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtWebKit import *

class WebBrowserWidget(QWidget):
    def changeLocation(self):
        self.webView.load( QUrl(self.locationEdit.text()) )

    def __init__(self):
        QWidget.__init__( self )

        self.setObjectName( "uk.co.thefoundry.webwidget.1" )
        self.setWindowTitle( "Web Browser" )

        # If we set WA_DeleteOnClose, the widget will be destroyed when closed. If not, it'll remain in the Windows menu and can be shown again.
        #self.setAttribute( Qt.WA_DeleteOnClose, True )

        self.webView = QWebView();

        self.setLayout( QVBoxLayout() )

        self.locationEdit = QLineEdit( 'http://www.thefoundry.co.uk' )
        self.locationEdit.setSizePolicy( QSizePolicy.Expanding, self.locationEdit.sizePolicy().verticalPolicy() )

        QObject.connect( self.locationEdit, SIGNAL('returnPressed()'),  self.changeLocation )

        self.layout().addWidget( self.locationEdit )

        bar = QToolBar()
        bar.addAction( self.webView.pageAction(QWebPage.Back))
        bar.addAction( self.webView.pageAction(QWebPage.Forward))
        bar.addAction( self.webView.pageAction(QWebPage.Stop))
        bar.addAction( self.webView.pageAction(QWebPage.Reload))
        bar.addSeparator()

        self.layout().addWidget( bar )
        self.layout().addWidget( self.webView )

        self.webView.load( QUrl( self.locationEdit.text() ) )

webBrowser = WebBrowserWidget()
wm = hiero.ui.windowManager()
wm.addWindow( webBrowser )

