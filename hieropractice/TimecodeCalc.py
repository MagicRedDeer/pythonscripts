# Nuke/Hiero Timecode Calculator Panel v1, 31/07/2012, Matt Brealey
# A simple but hopefully useful timecode calculator with Add, Subtract, Mult, Divide and Convert functionality

# Usage:
# For Nuke, copy this file to ~/.nuke and add 'import TimecodeCalc' to your menu.py file.
# For Hiero, copy this file to ~/.hiero/Python/StartupUI/

import PySide, sys, fnmatch

class TimecodeCalculator(PySide.QtGui.QWidget):

    #initialise function
    def __init__(self):

        #initialise widget
        PySide.QtGui.QWidget.__init__( self )

        #set main params
        self.setObjectName( "uk.co.thefoundry.timecodeCalculator" )
        self.setWindowTitle( "Timecode Calculator" )

        #Make main layout
        self._layout = PySide.QtGui.QVBoxLayout()

        #Make Sub Layouts
        self._labelsLayout = PySide.QtGui.QVBoxLayout()
        self._widgetsLayout = PySide.QtGui.QVBoxLayout()
        self._topLayout = PySide.QtGui.QHBoxLayout()

        #Make widgets
        self._timecode1Label =  PySide.QtGui.QLabel('Timecode 1 :')
        self._timecode2Label =  PySide.QtGui.QLabel('Timecode 2 :')
        self._modeLabel =  PySide.QtGui.QLabel('Mode :')
        self._sourceFPSLabel =  PySide.QtGui.QLabel('Source FPS :')
        self._targetFPSLabel =  PySide.QtGui.QLabel('Target FPS :')
        self._multiplierLabel =  PySide.QtGui.QLabel('Multiply By :')
        self._resultLabel =  PySide.QtGui.QLabel('Result :')

        self._timecode1 = PySide.QtGui.QLineEdit()
        self._timecode2 = PySide.QtGui.QLineEdit()
        self._mode = PySide.QtGui.QComboBox()
        self._sourceFPS = PySide.QtGui.QLineEdit()
        self._targetFPS = PySide.QtGui.QLineEdit()
        self._multiplier = PySide.QtGui.QLineEdit()
        self._result = PySide.QtGui.QLineEdit()

        #Set widget state
        for mode in "Add Subtract Multiply Divide Convert".split(" ") :
                self._mode.addItem(mode)

        self._sourceFPS.setText("25")
        self._sourceFPS.setInputMask("09")

        self._targetFPSLabel.setVisible(False)
        self._targetFPS.setInputMask("09")
        self._targetFPS.setVisible(False)
        self._targetFPS.setText("24")

        self._timecode1.setInputMask("00:00:00:09")
        self._timecode1.setText("01:00:00:00")

        self._timecode2.setInputMask("00:00:00:09")
        self._timecode2.setText("00:00:00:00")

        self._multiplierLabel.setVisible(False)
        self._multiplier.setText("1")
        self._multiplier.setVisible(False)
        self._multiplier.setInputMask("0009")

        self._result.setReadOnly(True)

        #Add widgets to layouts
        self._labelsLayout.addWidget(self._modeLabel)
        self._labelsLayout.addWidget(self._sourceFPSLabel)
        self._labelsLayout.addWidget(self._targetFPSLabel)
        self._labelsLayout.addWidget(self._timecode1Label)
        self._labelsLayout.addWidget(self._timecode2Label)
        self._labelsLayout.addWidget(self._multiplierLabel)
        self._labelsLayout.addWidget(self._resultLabel)

        self._widgetsLayout.addWidget(self._mode)
        self._widgetsLayout.addWidget(self._sourceFPS)
        self._widgetsLayout.addWidget(self._targetFPS)
        self._widgetsLayout.addWidget(self._timecode1)
        self._widgetsLayout.addWidget(self._timecode2)
        self._widgetsLayout.addWidget(self._multiplier)
        self._widgetsLayout.addWidget(self._result)

        self._topLayout.addLayout(self._labelsLayout)
        self._topLayout.addLayout(self._widgetsLayout)

        self._layout.addLayout(self._topLayout)

        #Set Main Layout
        self.setLayout(self._layout)

        #
        self._mode.currentIndexChanged.connect(self.modeChanged)
        self._sourceFPS.textChanged.connect(self.calculateTC)
        self._targetFPS.textChanged.connect(self.calculateTC)
        self._timecode1.textChanged.connect(self.calculateTC)
        self._timecode2.textChanged.connect(self.calculateTC)
        self._multiplier.textChanged.connect(self.calculateTC)

        self.calculateTC()

    def modeChanged(self) :
        if str(self._mode.currentText()) in ['Multiply', 'Divide'] :
                self._multiplierLabel.setVisible(True)
                self._multiplier.setVisible(True)
                self._timecode2Label.setVisible(False)
                self._timecode2.setVisible(False)
                self._targetFPSLabel.setVisible(False)
                self._targetFPS.setVisible(False)
                if str(self._mode.currentText()) == 'Multiply' :
                        self._multiplierLabel.setText('Multiply By :')
                else :
                        self._multiplierLabel.setText('Divide By :')
        elif str(self._mode.currentText()) in ['Add', 'Subtract'] :
                self._multiplierLabel.setVisible(False)
                self._multiplier.setVisible(False)
                self._timecode2Label.setVisible(True)
                self._timecode2.setVisible(True)
                self._targetFPSLabel.setVisible(False)
                self._targetFPS.setVisible(False)

        else :
                self._multiplierLabel.setVisible(False)
                self._multiplier.setVisible(False)
                self._timecode2Label.setVisible(False)
                self._timecode2.setVisible(False)
                self._targetFPSLabel.setVisible(True)
                self._targetFPS.setVisible(True)

        self.calculateTC()


    def calculateTC(self) :

        #Get vars with safety
        timecode1 = self._timecode1.text()
        mode = self._mode.currentText()
        origFps = None
        destFps = None
        divMultVal = None
        timecode2 = None

        if mode in ["Add", "Subtract"] :
                timecode2 = self._timecode2.text()
                try :
                        origFps = int(self._sourceFPS.text())
                except :
                        origFps == None

                if len(timecode1) < 11 or len(timecode2) < 11 or origFps == None :
                        return

        elif mode in ["Divide", "Multiply"] :
                timecode2 = "00:00:00:00"
                try :
                        origFps = int(self._sourceFPS.text())
                except :
                        origFps == None

                try :
                        divMultVal = int(self._multiplier.text())
                except :
                        divMultVal = None

                if len(timecode1) < 11 or origFps == None or divMultVal == None :
                        return

        elif mode == "Convert" :
                timecode2 = "00:00:00:00"
                try :
                        origFps = int(self._sourceFPS.text())
                except :
                        origFps == None
                try :
                        destFps = int(self._targetFPS.text())
                except :
                        destFps = None

                if len(timecode1) < 11 or origFps == None or destFps == None :
                        return

        #remove any ":" from timecode
        timecode1 = timecode1.replace(":", "")
        timecode2 = timecode2.replace(":", "")

        #Split to hmsf
        split1 = []
        split2 = []
        for i in range(0,8,2):
                split1.append(timecode1[i:i+2])
                split2.append(timecode2[i:i+2])

        #get total frames of both
        timecode1Total = 0
        timecode2Total = 0
        for x in range(0,4) :
                if x == 0 :
                        timecode1Total += int(split1[3-x])
                        timecode2Total += int(split2[3-x])
                elif x == 1 :
                        timecode1Total += origFps * int(split1[3-x])
                        timecode2Total += origFps * int(split2[3-x])
                elif x == 2 :
                        timecode1Total += 60 * origFps * int(split1[3-x])
                        timecode2Total += 60 * origFps * int(split2[3-x])
                elif x == 3 :
                        timecode1Total += 60 * 60 * origFps * int(split1[3-x])
                        timecode2Total += 60 * 60 * origFps * int(split2[3-x])

        #do operation
        if mode == "Add" :
                result = timecode1Total + timecode2Total
        elif mode == "Subtract" :
                result = timecode1Total - timecode2Total
        elif mode == "Divide" :
                if divMultVal == 0 :
                        result = 0
                else :
                        result = int(timecode1Total / divMultVal)
        elif mode == "Multiply" :
                result = timecode1Total * divMultVal
        elif mode == "Convert" :
                result = timecode1Total
                origFps = destFps

        #now convert back to timecode using origFps
        minusChecker = ""
        if result < 0 :
                minusChecker = "-"

        runningTotal = abs(result)

        h = int(float(runningTotal) / float(60*60*origFps))
        runningTotal -= h*60*60*origFps

        m = int(float(runningTotal) / float(60*origFps))
        runningTotal -= m*60*origFps

        s = int(float(runningTotal) / float(origFps))
        runningTotal -= s*origFps

        final = ":".join([str(h).zfill(2), str(m).zfill(2), str(s).zfill(2), str(runningTotal).zfill(2)])

        self._result.setText("%s%s" % (minusChecker, str(final)) )


#Make this work in either Nuke OR Hiero via startup folders OR script editor 
hostApp = ''
if fnmatch.fnmatch( sys.executable, '*Nuke*'): 
        import nuke
        import nukescripts
        from nukescripts import panels

        moduleName = __name__
        if moduleName == '__main__':
                moduleName = ''
        else:
                moduleName = moduleName + '.'

        panels.registerWidgetAsPanel(moduleName + 'TimecodeCalculator', 'Timecode Calculator','uk.co.thefoundry.timecodeCalculator')

elif fnmatch.fnmatch( sys.executable, '*Hiero*'):
        import hiero
        tcCalc = TimecodeCalculator()
        wm = hiero.ui.windowManager()
        wm.addWindow( tcCalc )
