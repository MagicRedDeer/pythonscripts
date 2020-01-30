import pymel.core as pc

class PostfixHierarchyUI(object):
    winName = 'PostfixHierarchyUI'

    def __init__(self):

        if pc.window(self.winName, exists=True):
            pc.deleteUI(self.winName)

        with pc.window(self.winName) as self.win:
            with pc.columnLayout(adj=True):
                self.hierBox = pc.checkBox('Select by Hierarchy', value=True)
                with pc.rowLayout(nc=2):
                    with pc.optionMenu(cc=self.changeOption) as self.postfixOption:
                        pc.menuItem(label='low')
                        pc.menuItem(label='high')
                        pc.menuItem(label='custom')
                    self.customText = pc.textField(text='high')

                self.doButton = pc.button('Apply Postfix', c=self.do)
        self.customText.setEnable(False)

    def show(self):
        self.win.showWindow()

    def do(self, *args):
        postfix = self.postfixOption.getValue()
        if postfix == 'custom':
            postfix = self.customText.getText().strip().strip('_')
        postfix.replace(' ', '_')
        postfixHierarchy(word=postfix, hier=self.hierBox.getValue())

    def changeOption(self, *args):
        if self.postfixOption.getValue() == 'custom':
            self.customText.setEnable(True)
        else:
            self.customText.setEnable(False)


def postfixHierarchy(word='low', sep='_', hier=False):
    for node in pc.ls(sl=1, dag=hier, type='transform'):
        name = node.name()
        parents = name.split('|')
        splits = parents[-1].split('_')
        if len(splits) >= 2:
            splits.pop()
            parents[-1] = '_'.join(splits)
            name = '|'.join(parents)
        node.rename(name + sep + word)

if __name__ == "__main__":
    PostfixHierarchyUI()
