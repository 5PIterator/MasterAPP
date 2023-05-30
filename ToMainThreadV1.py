

from PyQt5 import QtCore
from PyQt5.QtCore import QThread
import threading
from time import sleep


class TMT(QThread):
    '''Passes a function into the mainThread'''
    def __init__(self, parent=None, function=None, argument=None):
        super(TMT, self).__init__(parent)
        self.func = function
        self.arg = argument
        self.signalList = {}
        self.is_running = True
    '''def getSignal(self, name:str=None):
        return self.signal_map[name]
    def addSignal(signal_map:dict=None, signal=None, name:str=None):
        if signal_map is not None:
            TMT.signal_map = signal_map
        else:
            if type is None:
                TMT.signal_map[name] = signal
            else:
                TMT.signal_map[name] = signal
            return TMT.signal_map[name]
        pass'''

    def run(self):
        if self.arg is None: self.signalList[self.func].emit()
        else: self.signalList[self.func].emit(self.arg)
        self.stop()

    def stop(self):
        self.is_running = False
        self.terminate()

tmt = TMT()
# in MainThread
def FuncToMain(func, arg=None):
    '''
    Checks if current thread is MainThread.\n
    If yes, returns 'False'.\n
    If no, calls 'func' in the main thread and returns 'True'
    For correct functionality, addSignalDict() has to be used
    '''
    if isinstance(threading.current_thread(), threading._MainThread):
        return func()

    tmt.func = func
    tmt.arg = arg
    tmt.start()  # Trigger MainThread
    sleep(0.01)

def addSignalList(signalList:dict=None, name:str=None, signal:QtCore.pyqtSignal=None):
    '''Accepts a dictionary of pyqtSignals, or a name and a pyqtSignal'''
    if signalList is not None:
        tmt.signalList = signalList
    elif name is not None and signal is not None:
        tmt.signalList[name] = signal
        return signal
    pass

