

from PyQt5 import QtCore
from PyQt5.QtCore import QThread
import threading
from time import sleep

def run_in_main_thread(tup):
    """Triggered by mainThread, executes the function provided in tuple"""
    func, args, kwargs = tup
    return func(args=args, kwargs=kwargs)

class TMT(QThread):
    mainThread = QtCore.pyqtSignal(tuple)
    '''Hosts the mainThread signal which is connected in the mainThread at launch'''
    def __init__(self, parent=None):
        super(TMT, self).__init__(parent)
        self.mainThread.connect(run_in_main_thread)

tmt = TMT()

def toMainThread(func):
    """Passes function and its arguments through an emit() into run_in_main_thread(). Use this method as a decorator:\n
    @toMainThread\n
    foo(arg, kwarg)"""
    def wrapper(*args, **kwargs):
        if threading.current_thread() is not threading.main_thread():
            tuple = (func, args, kwargs)
            tmt.mainThread.emit(tuple)
            sleep(0.01)
            return
        else:
            return func(args=args, kwargs=kwargs)
    return wrapper

