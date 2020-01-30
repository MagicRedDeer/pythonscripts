'''
# Execute in Maya
import maya.cmds as cmds

cmds.loadPlugin('tempJiggleNode.py')

obj = cmds.polySphere()[0]

jiggleNode = cmds.createNode('tempJiggleNode')
cmds.connectAttr('{0}.output'.format(jiggleNode), '{0}.t'.format(obj) ) # Connect output to sphere's translate

#cmds.unloadPlugin('tempJiggleNode.py')
'''

import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya

commandName = 'tempJiggleNode'

class TempJiggleNode(OpenMayaMPx.MPxNode):
    kPluginNodeId = OpenMaya.MTypeId(0x00000003)

    output_value = OpenMaya.MObject()
    currentTime = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        self.pos = [0,0,0]

    def postConstructor(self):
        # Set node's default name
        thisObj = self.thisMObject()
        fnNode = OpenMaya.MFnDependencyNode( thisObj )
        fnNode.setName('jiggleShape#')

        # Connect time1.outTime to jiggleNode.currentTime
        currentTimePlug = fnNode.findPlug('currentTime')
        timeDepNode = OpenMaya.MItDependencyNodes( OpenMaya.MFn.kTime )
        if not timeDepNode.isDone():
            timeObj = timeDepNode.thisNode()
            fnNode.setObject(timeObj)
            outTimePlug = fnNode.findPlug('outTime')
            dgMod = OpenMaya.MDGModifier()
            dgMod.connect(outTimePlug, currentTimePlug)
            dgMod.doIt()
        else:
            print 'Cannot find time node in the scene.'

    def compute(self, plug, data):
        print 'compute called'
        if plug != TempJiggleNode.output_value:
            return super(TempJiggleNode, self).compute(plug, data)

        # First get all attribute from data block
        aCurrentTime = data.inputValue(TempJiggleNode.currentTime)
        # Sim if we above frame 1, otherwise reset
        if aCurrentTime.asTime().value() > 1:
            self.pos[1] -= 0.1
        else:
            # Reset values to 0
            self.pos = [0,0,0]

        # Add pos to final output
        outValue = data.outputValue(TempJiggleNode.output_value)
        outValue.set3Double(self.pos[0], self.pos[1], self.pos[2])
        outValue.setClean()

        data.setClean(plug)
        return True

def creator():
    return OpenMayaMPx.asMPxPtr( TempJiggleNode() )

def initialize():
    print 'Jiggle loaded!'

    nAttr = OpenMaya.MFnNumericAttribute()

    TempJiggleNode.output_value = nAttr.create('output', 'output', OpenMaya.MFnNumericData.k3Double)
    nAttr.setWritable(False)
    nAttr.setStorable(False)
    nAttr.setCached(True)
    TempJiggleNode.addAttribute(TempJiggleNode.output_value)

    uAttr = OpenMaya.MFnUnitAttribute()

    TempJiggleNode.currentTime = uAttr.create('currentTime', 'currentTime', OpenMaya.MFnUnitAttribute.kTime, 0.0)
    uAttr.setKeyable(True)
    TempJiggleNode.addAttribute(TempJiggleNode.currentTime)
    TempJiggleNode.attributeAffects(TempJiggleNode.currentTime, TempJiggleNode.output_value)

def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'Jason Labbe', '1.0', 'Any')
    try:
        plugin.registerNode(commandName, TempJiggleNode.kPluginNodeId, creator, initialize)
    except:
        raise RuntimeError, 'Failed to register node: {0}'.format(commandName)

def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(TempJiggleNode.kPluginNodeId)
    except:
        raise RuntimeError, 'Failed to register node: {0}'.format(commandName)
