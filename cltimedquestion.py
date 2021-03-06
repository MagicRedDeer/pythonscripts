from PyQt4.QtGui import QApplication

import sys


def askQuestion(q='Question'):
    sys.stdout.writelines([ q ])
    return sys.stdin.readline()

def askTimedQuestion(q='Question', default='Answer', time=5000):
    sys.stdout.writelines([ q ])
    sys.stdout.readline()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    print askQuestion('How are you today?')
    print askQuestion('How you doing?')
