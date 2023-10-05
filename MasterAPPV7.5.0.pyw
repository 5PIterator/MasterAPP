'''
pyinstaller --onefile --distpath G:\My' 'Drive\MasterAPPEXE --windowed MasterAPPV7.4.2.pyw
'''
# Bugs:
# Sometimes the background disappears and defaults into white background.
# Retry change crashed once

# To do:
# Fix graph


from pyModbusTCP.client import ModbusClient
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread
from tkinter import messagebox
from http.server import HTTPServer, BaseHTTPRequestHandler
from http.client import HTTPConnection
import sys, threading, socket, os, tkinter, numpy
import ftplib
from datetime import datetime, timedelta
from time import sleep, time
from tkinter import filedialog
from concurrent.futures import ThreadPoolExecutor
from pyqtgraph import PlotWidget, mkPen
import random

from ui.MasterAPPV8_ui import Ui_MasterAPP
from ui.NewDomain import Ui_EnterNewDomain
import ui.Images_rc  #Important! Do not delete.

from ToMainThreadV2 import toMainThread
import LocalRegistryLibraryV9 as LRLibrary
import SettingsManagerV3 as SM
from SettingsManagerV3 import settingsDict as SD

class MainWindow(Ui_MasterAPP):
    def __init__(self, window) -> None:
        self.setupUi(window)
        self.cableItem_1.setVisible(False)
        self.pb_startClients.setEnabled(True)
        self.pb_retry.setEnabled(False)
        self.cb_auto_cableUpdate.setEnabled(False)
        self.pb_stopClients.setEnabled(False)
        self.pb_updateCables.setEnabled(False)

        self.pg_workload_1.plotItem.setLabel('left', "Cable0")
        self.pg_workload_1.plotItem.setLabel('top', 'Time [HHMM.SS]')
        self.pg_workload_1.plotItem.showAxis("right")
        self.pg_workload_1.plotItem.getViewBox().setLimits(yMin=-0.2, yMax=2.2, xMin=-0.2, minYRange=-0.2, maxYRange=2.2, minXRange=-0.2)
        self.pg_workload_1.plotItem.getViewBox().setMouseEnabled(x=True,y=False)
        self.pg_workload_1.plotItem.getViewBox().setRange(yRange=(0,2), xRange=(0,60))
        self.pg_workload_1.plotItem.getAxis("left").setWidth(40)
        self.pg_workload_1.plotItem.getAxis("right").setWidth(40)
        self.pg_workload_1.plotItem.showGrid(True,False)
        self.pg_workload_1.plotItem.getViewBox().enableAutoRange(x=True)

        # EventHandlers
        self.tabWidget_2.tabBarClicked.connect(self.splitter_resize)
        self.splitter.splitterMoved.connect(self.splitter_resize)

        self.sb_retryInterval.valueChanged.connect(self.SaveSettings)
        self.dsb_apiInterval.valueChanged.connect(self.SaveSettings)
        self.dsb_axInterval.valueChanged.connect(self.SaveSettings)
        self.dsb_plcInterval.valueChanged.connect(self.SaveSettings)
        self.sb_cableCount.valueChanged.connect(self.SaveSettings)
        self.le_apiAddress.editingFinished.connect(self.SaveSettings)
        self.le_apiPort.editingFinished.connect(self.SaveSettings)
        self.le_plcAddress.editingFinished.connect(self.SaveSettings)
        self.le_plcPort.editingFinished.connect(self.SaveSettings)
        self.le_axAddress.editingFinished.connect(self.SaveSettings)
        self.le_axPort.editingFinished.connect(self.SaveSettings)
        self.cb_apiAllowed.stateChanged.connect(self.SaveSettings)
        self.cb_plcAllowed.stateChanged.connect(self.SaveSettings)
        self.cb_axAllowed.stateChanged.connect(self.SaveSettings)
        self.cb_auto_startClients.stateChanged.connect(self.SaveSettings)
        self.cb_auto_retry.stateChanged.connect(self.SaveSettings)
        self.cb_auto_cableUpdate.stateChanged.connect(self.SaveSettings)
        self.cb_auto_cableCount.stateChanged.connect(self.SaveSettings)
        self.cb_SaveStyle.currentIndexChanged.connect(self.SaveSettings)
        self.pb_MMState.valueChanged.connect(self.SaveSettings)
        self.le_areal.editingFinished.connect(self.SaveSettings)

        # UIButtons
        self.pb_startClients.pressed.connect(self.StartButton)
        self.pb_retry.pressed.connect(self.RetryButton)
        self.pb_stopClients.pressed.connect(self.StopButton)
        self.pb_updateCables.pressed.connect(self.GetCablesButton)
        self.pb_changeDir.pressed.connect(self.workloadPath)
        self.pb_SaveStateData.pressed.connect(self.SaveStateDataButton)
        self.pb_changeDomain.pressed.connect(self.ChangeDomainButton)

        self.historyButton.pressed.connect(self.clearH)
        self.historyButton_2.pressed.connect(self.exportH)
        #self.historyButton_3.pressed.connect(self.colapseH)
        #self.historyCheckBox.stateChanged.connect(self.updateSettings)
        self.graphItems = [
            self.pg_workload_1
        ]

    # Startup part 1: Window setup and Settings
    def StartPart1(self):
        global cableUpdate
        global checkSettings
        global logFilePath

        logFilePath = "HistoryLog" + str(datetime.now().month).zfill(2) + str(datetime.now().day).zfill(2) + ".txt"
        printH("Startup", 0, "MasterAPP", False)
        self.splitter.setSizes([self.tableWidget.width() + 9, self.splitter.sizes()[1] + 135])
        self.tableWidget.horizontalHeader().setDefaultSectionSize(self.tableWidget.width())

        self.setupSettings()
        checkSettings = False
        SM.loadSettings()
        checkSettings = True
        if plc.client_allowed:
            self.pb_updateCables.setEnabled(False)
        self.SaveSettings()

        if autoStart_allowed:  # auto start
            self.StartButton()

    # Save Settings
    def setupSettings(self):
        SM.addFile('MAIN', "configFiles/configMAIN")

        SM.addSection('MAIN', 'masterAPP')
        SM.addOption('masterAPP', 'autoStart_allowed', autoStart_allowed, self.cb_auto_startClients)
        SM.addOption('masterAPP', 'autoRetry_allowed', autoRetry_allowed, self.cb_auto_retry)
        SM.addOption('masterAPP', 'cableUpdateAllowed', cableUpdateAllowed)
        SM.addOption('masterAPP', 'autoUpdate_allowed', autoUpdate_allowed, self.cb_auto_cableUpdate)
        SM.addOption('masterAPP', 'cableCount', cableCount, self.sb_cableCount)
        SM.addOption('masterAPP', 'retryInterval', retryInterval, self.sb_retryInterval)

        SM.addSection('MAIN', 'api')
        SM.addOption('api', 'host', api.host, self.le_apiAddress)
        SM.addOption('api', 'port', api.port, self.le_apiPort)
        SM.addOption('api', 'client_allowed', api.client_allowed, self.cb_apiAllowed)
        SM.addOption('api', 'idle_Interval', api.idle_Interval, self.dsb_apiInterval)

        SM.addSection('MAIN', 'plc')
        SM.addOption('plc', 'host', plc.host, self.le_plcAddress)
        SM.addOption('plc', 'port', plc.port, self.le_plcPort)
        SM.addOption('plc', 'client_allowed', plc.client_allowed, self.cb_plcAllowed)
        SM.addOption('plc', 'autoUpdate_Interval', autoUpdate_Interval, self.dsb_plcInterval)

        SM.addSection('MAIN', 'ax')
        SM.addOption('ax', 'host', ax.host, self.le_axAddress)
        SM.addOption('ax', 'port', ax.port, self.le_axPort)
        SM.addOption('ax', 'server_allowed', ax.server_allowed, self.cb_axAllowed)
        SM.addOption('ax', 'request_Interval', ax.request_Interval, self.dsb_axInterval)

        SM.addSection('MAIN', 'domain')
        SM.addOption('domain', 'domainHost', domainHost, dialog.d_lineEdit_1)
        SM.addOption('domain', 'domainPort', domainPort, dialog.d_lineEdit_2)
        SM.addOption('domain', 'domainUser', domainUser, dialog.d_lineEdit_3, b'6araaoXwfSsMllEYNf8JHN1kePLImcCsbAQ8AB8-xDM=')
        SM.addOption('domain', 'domainPassword', domainPassword, dialog.d_lineEdit_4, b'6araaoXwfSsMllEYNf8JHN1kePLImcCsbAQ8AB8-xDM=')
        SM.addOption('domain', 'saveStyle', saveStyle, self.cb_SaveStyle)
        SM.addOption('domain', 'localPath', localPath, self.l_workloadPath)
        SM.addOption('domain', 'areal', areal, self.le_areal)
        SM.addOption('domain', 'minMinuteState', minMinuteState, self.pb_MMState)

    def SaveSettings(self):
        global retry
        global autoStart_allowed
        global autoRetry_allowed
        global autoUpdate_allowed
        global autoUpdate_Interval
        global retryInterval
        global stopClients
        global collapseH
        global checkSettings
        global cableCount
        global stopRetry
        global cableUpdate
        global cableUpdateEnabled
        global cableUpdateAllowed
        global domainHost
        global domainPort
        global domainUser
        global domainPassword
        global quidoMaxInput
        global saveStyle
        global localPath
        global minMinuteState
        global areal

        if not checkSettings:
            return
        checkSettings = False
        SM.getValues()

        #plc.plc_getCableCount_allowed = SD["masterAPP"]["plc_getCableCount_allowed"][0]
        retryInterval = SD["masterAPP"]["retryInterval"][0]
        cableCount = SD["masterAPP"]["cableCount"][0]
        autoStart_allowed = SD["masterAPP"]["autoStart_allowed"][0]
        autoRetry_allowed = SD["masterAPP"]["autoRetry_allowed"][0]
        api.idle_Interval = SD["api"]["idle_Interval"][0]
        autoUpdate_Interval = SD["plc"]["autoUpdate_Interval"][0]
        autoUpdate_allowed = SD["masterAPP"]["autoUpdate_allowed"][0]
        #cableUpdateAllowed = SD["masterAPP"]["cableUpdateAllowed"][0]
        ax.request_Interval = SD["ax"]["request_Interval"][0]
        ax.server_allowed = SD["ax"]["server_allowed"][0]
        saveStyle = SD["domain"]["saveStyle"][0]
        minMinuteState = SD["domain"]["minMinuteState"][0]
        localPath = SD["domain"]["localPath"][0]
        areal = SD["domain"]["areal"][0]
        domainHost = SD["domain"]["domainHost"][0]
        domainPort = SD["domain"]["domainPort"][0]
        domainUser = SD["domain"]["domainUser"][0]
        domainPassword = SD["domain"]["domainPassword"][0]


        if not areal == '':
            areal += '/'

        self.pb_MMState.setSuffix("/" + str(int(60 / self.dsb_plcInterval.value())) + "s")
        self.pb_MMState.setMaximum(int(60 / self.dsb_plcInterval.value()))
        if autoUpdate_allowed:
            cableUpdateEnabled = True
        else:
            cableUpdateEnabled = False

        stop = False
        start = False
        if api.client_allowed != self.cb_apiAllowed.isChecked():
            if not (api.api_retry_success or plc.plc_retry_success):
                api.client_allowed = self.cb_apiAllowed.isChecked()
            elif self.cb_apiAllowed.isChecked():
                start = True
            else:
                stop = True

        if plc.client_allowed != self.cb_plcAllowed.isChecked():
            if not (api.api_retry_success or plc.plc_retry_success):
                plc.client_allowed = self.cb_plcAllowed.isChecked()
            elif self.cb_plcAllowed.isChecked():
                start = True
            else:
                stop = True

        if not (api.client_allowed or plc.client_allowed or ax.server_allowed):
            self.pb_retry.setEnabled(False)
        elif not self.pb_startClients.isEnabled():
            self.pb_retry.setEnabled(True)

        restart = False
        if api.host != self.le_apiAddress.text():  # API Address(host)
            if self.le_apiAddress.text() != '':
                api.host = self.le_apiAddress.text()
                restart = True
            else:
                api.host = socket.gethostbyname(socket.gethostname())
                self.le_apiAddress.setText('')
        if str(api.port) != self.le_apiPort.text():  # API Address(port)
            if self.le_apiPort.text() != '' and self.le_apiPort.text().isdigit():
                api.port = int(self.le_apiPort.text())
                restart = True
            else:
                api.port = 1000
                self.le_apiPort.setText('')
        if plc.host != self.le_plcAddress.text():  # PLC Address(host)
            if self.le_plcAddress.text() != '':
                plc.host = self.le_plcAddress.text()
                restart = True
            else:
                plc.host = socket.gethostbyname(socket.gethostname())
                self.le_plcAddress.setText('')
        if str(plc.port) != self.le_plcPort.text():  # PLC Address(port)
            if self.le_plcPort.text() != '' and self.le_plcPort.text().isdigit():
                plc.port = int(self.le_plcPort.text())
                restart = True
            else:
                plc.port = 502
                self.le_plcPort.setText('')
        if str(ax.host) != self.le_axAddress.text():  # AX Address(host)
            if self.le_axAddress.text() != '' and self.le_axAddress.text().isdigit():
                ax.host = int(self.le_axAddress.text())
                restart = True
            else:
                ax.host = "192.168.11.50"
                self.le_axAddress.setText('')
        if str(ax.port) != self.le_axPort.text():  # AX Address(port)
            if self.le_axPort.text() != '' and self.le_axPort.text().isdigit():
                ax.port = int(self.le_axPort.text())
                restart = True
            else:
                ax.port = 11854
                self.le_axPort.setText('')

        SD["masterAPP"]["retryInterval"][0] = retryInterval
        SD["masterAPP"]["cableCount"][0] = cableCount
        SD["masterAPP"]["autoStart_allowed"][0] = autoStart_allowed
        SD["masterAPP"]["autoRetry_allowed"][0] = autoRetry_allowed
        SD["masterAPP"]["autoUpdate_allowed"][0] = autoUpdate_allowed
        #SD["masterAPP"]["cableUpdateAllowed"][0] = cableUpdateAllowed
        SD["api"]["idle_Interval"][0] = api.idle_Interval
        SD["plc"]["autoUpdate_Interval"][0] = autoUpdate_Interval
        SD["ax"]["request_Interval"][0] = ax.request_Interval
        SD["ax"]["server_allowed"][0] = ax.server_allowed
        SD["domain"]["saveStyle"][0] = saveStyle
        SD["domain"]["minMinuteState"][0] = minMinuteState
        SD["domain"]["areal"][0] = areal
        SD["domain"]["localPath"][0] = localPath
        SD["api"]["host"][0] = api.host
        SD["api"]["port"][0] = api.port
        SD["plc"]["host"][0] = plc.host
        SD["plc"]["port"][0] = plc.port
        SD["ax"]["host"][0] = ax.host
        SD["ax"]["port"][0] = ax.port

        SM.saveToConfig()

        if (restart or start) and (api.api_retry_success or plc.plc_retry_success):
            root = tkinter.Tk()
            root.withdraw()
            if messagebox.askokcancel("Confirm Action", "Variables of either API or PLC have been changed during runtime. \nThis change can only be implemented after restart. \n\nDo you wish to proceed?"):
                stopClients = True
                sleep(1)
                stopClients = False
                api.client_allowed = self.cb_apiAllowed.isChecked()
                plc.client_allowed = self.cb_plcAllowed.isChecked()

                '''retry = Worker(None, 'retry')'''
                retry = threadPool.submit(Retry)#! starts a loop either way
            else:
                self.le_apiAddress.setText(api.host)
                self.le_apiPort.setText(str(api.port))
                self.le_plcAddress.setText(plc.host)
                self.le_plcPort.setText(str(plc.port))
                self.cb_apiAllowed.setChecked(api.client_allowed)
                self.cb_plcAllowed.setChecked(plc.client_allowed)
        elif stop:
            root = tkinter.Tk()
            root.withdraw()
            if messagebox.askokcancel("Confirm Action", "Variables of either API or PLC have been changed during runtime. \nServer will now stop. \n\nDo you wish to proceed?"):
                api.client_allowed = self.cb_apiAllowed.isChecked()
                plc.client_allowed = self.cb_plcAllowed.isChecked()
            else:
                self.cb_apiAllowed.setChecked(api.client_allowed)
                self.cb_plcAllowed.setChecked(plc.client_allowed)

        SD["api"]["client_allowed"][0] = api.client_allowed
        SD["plc"]["client_allowed"][0] = plc.client_allowed
        checkSettings = True

    #Updates Graph of every cable
    autoMove = True
    lastData = None # Variable to keep track of the previous state
    graphData = []
    def updateGraph1(self, loadFile=True):
        """Pre-calculation for graphs"""
        dateTime = datetime.now()
        wPath = localPath + "/" + areal + str(dateTime.year) + '/' + str(dateTime.month).zfill(2) + '/' + str(dateTime.day).zfill(2) + '/'

        state = None
        time = None
        index = 0
        self.graphData = []
        #graphData
        #   [
        #       Cable0
        #       [
        #           X-Time[Value1, Value2],
        #           Y-State[Value1, Value2]
        #       ],
        #       CableN[],
        #       ...
        #   ]
        if loadFile:
            if not os.path.exists(wPath):
                os.makedirs(wPath)
            if len(os.listdir(wPath)) == 0:
                while len(self.graphData) < len(CableItems):
                    self.graphData.append([[],[]])
                return

            DataX: list = [[],[],[],[]] #X
            DataY: list = [[],[],[],[]] #Y
            for filedir in os.listdir(wPath): #Each file is a datapoint
                with open(wPath + filedir, 'r') as file:
                    lines = file.readlines()
                    while len(self.graphData) < len(lines):
                        self.graphData.append([[],[]])
                    for line in lines:
                        index = int(line[0])                             # index indicates the pyqtgraph
                        state = int(line[22])                       # state indicates the Y value
                        hour = line[13:15]
                        minute = line[16:18]
                        second = line[19:21]
                        time = hour + minute + second


                        i = len(DataY[index])
                        if int(i) != 0:
                            if DataY[index][-1] != state:
                                DataX[index].append(DataX[index][-1])
                                DataY[index].append(state)
                        DataX[index].append(float(time)/100)
                        DataY[index].append(state)

        self.setPlots((DataX, DataY, True))
        self.lastData = [DataX[-1], DataY[-1]]

        '''else:
            if len(os.listdir(wPath)) > 1:
                dirList = os.listdir(wPath)[-2:]
            else:
                dirList = os.listdir(wPath)
            for filedir in dirList:
                with open(wPath + filedir, 'r') as file:
                    lines = file.readlines()
                    while len(graphData) < len(lines):
                        graphData.append([[],[]])
                    for line in lines:
                        index = line[0]
                        state = int(line[22])
                        hour = line[13:15]
                        minute = line[16:18]
                        second = line[19:21]
                        time = hour + minute + second

                        graphData[int(index)][0].append(float(time)/100)
                        graphData[int(index)][1].append(state)'

            time = graphData[int(index)][0][1]
            state = graphData[int(index)][1][1] # - current
            graphTime: list = graphData[int(index)][0] #X - last
            graphState: list = graphData[int(index)][1] #Y
            i = len(graphState)
            if int(i) != 0:
                if graphState[-1] != state:
                    graphTime.append(graphTime[-1])
                    graphState.append(state)
            graphTime.append(time)
            graphState.append(state)'''

        #self.updateGraph2()
    @toMainThread
    def setPlots(self, data, clear=False):
        dataX, dataY, check = data

        for i, graphitem in enumerate(self.graphItems):
            if len(dataX[i]) != len(dataY[i]) or (len(dataX[i]) == 0 or len(dataY[i]) == 0): # skips if data aren't the same length or are zero
                continue
            """if check: # Checks if Position data is in view
                #check = False
                curViewRange = 3600 #graphitem.plotItem.getViewBox().state["viewRange"][0][1]
                spacing = abs(curViewRange - int(curViewRange))
                if int(dataX[i][-1]) > int(curViewRange):
                    graphitem.plotItem.getViewBox().setRange(xRange=(dataX[i][-1] - spacing, dataX[i][-1] + curViewRange), padding=0)
                    #graphitem.plotItem.getViewBox().setRange(xRange=(dataX[dataType][-1] + 0.5, dataX[dataType][-1] + (mes.sampletime * (mes.samplelenght * 10))))
                    '''for tw2 in ("L1", "L2", "R1", "R2"): # Clears graphs of Position only
                        graphList[tw2]["Pos"].plotItem.clear()'''"""
            #graphitem.plotItem.getViewBox().enableAutoRange(x=True)

            if len(graphitem.plotItem.items) > 10 or clear:
                clear = True
                steps = 1
                dataY[i] = self.graphData[i][1][::steps]
                dataX[i] = self.graphData[i][0][::steps]
                pass
            graphitem.plotItem.plot(dataX[i], dataY[i], pen=mkPen(color='white', width=2), clear=clear)
        #printH("Graphs updated!", 2, "Graphs updated from File.")
    '''def updateGraph2(self):
        """Graph update"""
        if self.graphData == []:
            return

        index = 0
        for graphitem in self.graphItems:
            #Clear and update the graph
            graphitem.clear()
            graphitem.plot(self.graphData[index][0], self.graphData[index][1])
            index += 1'''

    """timeIndex = 0
    def refreshPlot(self, blank=False):
        '''adds value to all plots'''
        if blank: return
        if self.measurementEnabled:

            DataYL1 = {"Pos": [], "For": []}
            DataYL2 = {"Pos": [], "For": []}
            DataYR1 = {"Pos": [], "For": []}
            DataYR2 = {"Pos": [], "For": []}
            DataXL1 = {"Pos": [], "For": []}
            DataXL2 = {"Pos": [], "For": []}
            DataXR1 = {"Pos": [], "For": []}
            DataXR2 = {"Pos": [], "For": []}
            DataY = {
                "L1": (DataYL1),
                "L2": (DataYL2),
                "R1": (DataYR1),
                "R2": (DataYR2)
            }
            DataX = {
                "L1": DataXL1,
                "L2": DataXL2,
                "R1": DataXR1,
                "R2": DataXR2
            }
            steps = window.sb_graphStep.value()
            #plotting graphs 'plot' is always 'None'. All graphs update at once
            for tw in ("L1", "L2", "R1", "R2"):
                dataType = "Pos"
                if self.timeIndex > steps - 1:
                    timePeriod = self.timeIndex - steps
                    DataX[i] = [self.dataTime[timePeriod]]
                    DataY[i] = [mes.measuredData[i][timePeriod]]
                else:
                    DataX[i] = []
                    DataY[i] = []

                dataType = "For"
                if self.timeIndex > steps - 1:
                    timePeriod = self.timeIndex - steps
                    DataX[i] = [mes.measuredData[i][timePeriod]]
                    DataY[i] = [mes.measuredData[i][timePeriod]] #Force uses Position as Y
                else:
                    DataX[i] = []
                    DataY[i] = []
            while self.timeIndex < len(self.dataTime):
                for tw in ("L1", "L2", "R1", "R2"):
                    for dataType in ("Pos", "For"):
                        if len(mes.measuredData[i]) <= self.timeIndex:
                            continue
                    DataY[i].append(mes.measuredData[i][self.timeIndex])
                    DataX[i].append(self.dataTime[self.timeIndex])
                    DataY[i].append(DataY[i][-1])
                    DataX[i].append(mes.measuredData[i][self.timeIndex])
                self.timeIndex += steps

            window.setPlots((DataX, DataY, True))
            pass
    plotThread = threadpool.submit(refreshPlot, blank=True)
    def resetPlot(self, blank=False):
        '''Resets the value of all graphs'''
        if blank: return
        if len(self.dataTime) < 2: return
        #plotting graphs
        DataX1 = {"Pos": [], "For": []}
        DataX2 = {"Pos": [], "For": []}
        DataX3 = {"Pos": [], "For": []}
        DataX4 = {"Pos": [], "For": []}
        DataL1 = {"Pos": [], "For": []}
        DataL2 = {"Pos": [], "For": []}
        DataR1 = {"Pos": [], "For": []}
        DataR2 = {"Pos": [], "For": []}

        #self.timeIndex = 0
        steps = window.sb_graphStep.value()
        while len(self.dataTime) / steps > 1000:
            steps += 1

        #self.clearPlots()

        for t, tw in enumerate(("L1", "L2", "R1", "R2")):
            dataX = (DataX1, DataX2, DataX3, DataX4)[t]
            dataY = (DataL1, DataL2, DataR1, DataR2)[t]
            #j = 0

            for i in range(0, len(self.dataTime), steps):
                dataY["Pos"].append(mes.measuredData[i][i])
                dataX["Pos"].append(self.dataTime[i])
                dataY["For"].append(dataY["Pos"][-1])
                dataX["For"].append(mes.measuredData[i][i])
            #j = t
        #self.timeIndex = len(self.dataTime)

        DataX = {
            "L1": DataX1,
            "L2": DataX2,
            "R1": DataX3,
            "R2": DataX4
        }
        DataY = {
            "L1": DataL1,
            "L2": DataL2,
            "R1": DataR1,
            "R2": DataR2
        }
        window.setPlots((DataX, DataY, False), True)
        sleep(0.01)
        '''for tw in ("L1", "L2", "R1", "R2"):
            dataType = "Pos"
            graphitem.plotItem.plot(dataX[dataType], dataY[dataType], pen=mkPen(color='black',width=2))
            pass'''
        #window.printS("Grafy resetovány!")
    resetting = threadpool.submit(resetPlot, blank=True)
    def clearPlots(self, plot:tuple=None, type=None, start=False, blank=False):
        if blank: return

        clearThread = {
            "L1":{"Pos": None, "For": None},
            "L2":{"Pos": None, "For": None},
            "R1":{"Pos": None, "For": None},
            "R2":{"Pos": None, "For": None},
        }

        if type is not None:
            for tw in ("L1", "L2", "R1", "R2"):
                    graphList[tw][type].plotItem.clear()
                    sleep(0.05)
        elif plot is None:
            for tw in ("L1", "L2", "R1", "R2"):
                for type in ("Pos", "For"):
                    graphList[tw][type].plotItem.clear()
        else:
            graphList[plot[0]][plot[1]].plotItem.clear()
        pass

        while True:
            escape = True
            for tw in ("L1", "L2", "R1", "R2"):
                for type in ("Pos", "For"):
                    if clearThread[tw][type] is None: continue
                    if clearThread[tw][type].running():
                        escape = False
                        break
                if not escape:
                    break
            if escape: break
            else: sleep(0.1)

        if start:
            self.startMeasurement(True)"""
    #clearing = threadpool.submit(clearPlots, blank=True)
    # Cables
    def receivedCableCount(self):
        global CableItems
        global cableCount
        global cableUpdateProceed
        global cableUpdate
        try:
            if cableCount == len(CableItems):
                pass
            elif cableCount > 0:
                CableItems[0].setVisible(True)
                self.graphItems[0].setVisible(True)

                printH("Registering new cables...", 1, str(cableCount) + " cables")
                c = 0
                while c < cableCount:
                    sleep(.1)
                    if cableCount > len(CableItems):
                        self.addCableItem()

                    t = 0 # timeout
                    while len(CableItems) != c + 1 or len(self.graphItems) != c + 1: # wait for mainThread to add Cable
                        if t >= 1000:
                            t = 0
                        t += 1
                        sleep(0.01)
                        if stopRetry:
                            printH("Interrupted", 2, "stop button")
                            return False
                    CableItems[c].setVisible(True) # Enable already created CableItems
                    self.graphItems[c].setVisible(True) # Enable already created graphs

                    printH("Cable" + str(c) + " registered", 2, str(len(CableItems)) + "/" + str(cableCount))
                    c += 1
                c = len(CableItems)
                while cableCount < c:
                    CableItems[c - 1].setVisible(False)
                    self.graphItems[c - 1].setVisible(False)
                    printH("Cable" + str(c - 1) + " removed", 2, str(c) + "/" + str(cableCount))
                    c -= 1
                sleep(0.02)
                printH("Updating Graphs.", 1)
                self.updateGraph1(True)
            else:
                CableItems[0].setVisible(False)
                self.graphItems[0].setVisible(False)
                return False
        except:
            printH("Error encountered.", 1)
            window.StopButton()
            window.StartButton()
            return False
        return True
    @toMainThread
    def addGraph(self):
        newpyqtGraph = PlotWidget()
        newpyqtGraph.setObjectName("pg_workload_" + str(len(self.graphItems)))
        newpyqtGraph.setSizePolicy(self.pg_workload_1.sizePolicy())
        newpyqtGraph.setMinimumSize(self.pg_workload_1.minimumSize())
        newpyqtGraph.setMaximumSize(self.pg_workload_1.maximumSize())
        newpyqtGraph.plotItem.getViewBox().enableAutoRange(x=True)

        newpyqtGraph.plotItem.setLabel('left', "Cable" + str(len(self.graphItems)))
        newpyqtGraph.plotItem.showAxis("right")
        newpyqtGraph.plotItem.setLabel('bottom', 'Time [s]')
        newpyqtGraph.plotItem.hideAxis('top')
        newpyqtGraph.plotItem.getViewBox().state = self.pg_workload_1.plotItem.getViewBox().state
        newpyqtGraph.plotItem.showGrid(True, False)
        newpyqtGraph.plotItem.getAxis("left").setWidth(40)
        newpyqtGraph.plotItem.getAxis("right").setWidth(40)
        layout: QtWidgets.QLayout
        layout = self.scrollAreaWidgetContents.layout()
        layout.insertWidget(layout.count() - 1, newpyqtGraph)
        #self.graphItems[-1].setXLink(newpyqtGraph)
        self.graphItems[-1].plotItem.setLabel('bottom', '')
        self.graphItems[-1].plotItem.getAxis("top").setStyle(showValues=False)
        self.graphItems.append(newpyqtGraph)

        '''for graph in self.graphItems:
            graph.plotItem.getViewBox().setXLink(self.graphItems[0].plotItem.getViewBox())''' #doesn't work

    # Add another CableItem by copying template(CableItems[0])
    @toMainThread
    def addCableItem(self):
        global isStart
        global CableItems
        if not isStart:
            # Copy Frame
            newCableItem = QtWidgets.QFrame()
            newCableItem.setStyleSheet(CableItems[0].styleSheet())
            newCableItem.setMaximumSize(CableItems[0].maximumSize())
            newCableItem.setStyleSheet(CableItems[0].styleSheet())
            newCableItem.setObjectName("CableItem_" + str(len(CableItems)))

            # Copy layout
            newverticalLayout = QtWidgets.QVBoxLayout(newCableItem)
            newverticalLayout.setContentsMargins(self.verticalLayout.contentsMargins())
            newverticalLayout.setSpacing(self.verticalLayout.spacing())
            newverticalLayout.setObjectName("verticalLayout_" + str(len(CableItems)))
            spacerItem = QtWidgets.QSpacerItem(23, 43, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

            newviewImage = QtWidgets.QLabel(newCableItem)
            newviewImage.setFont(self.cableLabel_1.font())
            newviewImage.setStyleSheet(self.cableLabel_1.styleSheet())
            newviewImage.setObjectName("cableLabel_" + str(len(CableItems)))
            newviewImage.setAlignment(self.cableLabel_1.alignment())
            newviewImage.setText("Cable" + str(len(CableItems)))
            newverticalLayout.addWidget(newviewImage)
            newverticalLayout.addItem(spacerItem)

            spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

            newstatusImage = QtWidgets.QLabel(newCableItem)
            newstatusImage.setStyleSheet(self.statusImage_1.styleSheet())
            newstatusImage.setSizePolicy(self.statusImage_1.sizePolicy())
            newstatusImage.setText("")
            newstatusImage.setPixmap(QtGui.QPixmap(":/img/Img/GreenLight.png"))
            newstatusImage.setScaledContents(self.statusImage_1.hasScaledContents())
            newstatusImage.setAlignment(self.statusImage_1.alignment())
            newstatusImage.setObjectName("statusImage_" + str(len(CableItems)))
            newverticalLayout.addWidget(newstatusImage)
            newverticalLayout.addItem(spacerItem2)

            # Copy Widget
            newtableWidget = QtWidgets.QTableWidget(newCableItem)
            newtableWidget.setStyleSheet(self.tableWidget_1.styleSheet())
            newtableWidget.setSizePolicy(self.tableWidget_1.sizePolicy())
            newtableWidget.setMinimumSize(self.tableWidget_1.minimumSize())
            newtableWidget.setMaximumSize(self.tableWidget_1.maximumSize())
            newtableWidget.setFont(self.tableWidget_1.font())
            newtableWidget.setObjectName("tableWidget_" + str(len(CableItems)))
            newtableWidget.setColumnCount(self.tableWidget_1.columnCount())
            newtableWidget.setRowCount(self.tableWidget_1.rowCount())

            for i in range(newtableWidget.rowCount()):
                newtableWidget.setVerticalHeaderItem(i, self.tableWidget_1.verticalHeaderItem(i))
            newtableWidget.setHorizontalHeaderItem(i, self.tableWidget_1.horizontalHeaderItem(i))

            for i in range(newtableWidget.rowCount()):
                newtableWidget.setVerticalHeaderItem(i, self.tableWidget_1.verticalHeaderItem(i))
                item = QtWidgets.QTableWidgetItem(self.tableWidget_1.item(i, 0))
                newtableWidget.setItem(i, 0, item)

            newtableWidget.horizontalHeader().setVisible(self.tableWidget_1.horizontalHeader().isVisible())
            newtableWidget.horizontalHeader().setDefaultSectionSize(self.tableWidget_1.horizontalHeader().defaultSectionSize())
            newtableWidget.horizontalHeader().setMinimumSectionSize(self.tableWidget_1.horizontalHeader().minimumSectionSize())
            newtableWidget.verticalHeader().setVisible(self.tableWidget_1.verticalHeader().isVisible())
            newtableWidget.verticalHeader().setDefaultSectionSize(self.tableWidget_1.verticalHeader().defaultSectionSize())
            newtableWidget.verticalHeader().setMinimumSectionSize(self.tableWidget_1.verticalHeader().minimumSectionSize())
            newverticalLayout.addWidget(newtableWidget)
            self.horizontalLayout.addWidget(newCableItem)

            layout: QtWidgets.QLayout
            layout = self.CableScrollAreaWidgetContents.layout()
            layout.insertWidget(layout.count() - 2, newCableItem)
            CableItems.append(newCableItem)

            self.addGraph()

            #New cable graph
            '''newgraphFrame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
            newgraphFrame.setFrameShape(self.graphFrame_1.frameShape())
            newgraphFrame.setFrameShadow(self.graphFrame_1.frameShadow())
            newgraphFrame.setLineWidth(self.graphFrame_1.lineWidth())
            newgraphFrame.setSizePolicy(self.graphFrame_1.sizePolicy())
            newgraphFrame.setMinimumSize(self.graphFrame_1.minimumSize())
            newgraphFrame.setMaximumSize(self.graphFrame_1.maximumSize())
            newgraphFrame.setObjectName("graphFrame_" + str(len(CableItems)))'''
            '''newgridLayout = QtWidgets.QGridLayout(newgraphFrame)
            newgridLayout.setContentsMargins(0, 0, 0, 0)
            newgridLayout.setSpacing(0)
            newgridLayout.setObjectName("gridLayout_" + str(len(CableItems)))'''

        else:
            isStart = False
        import_CableItemInfo(len(CableItems) - 1, new=True)

    # Remove a CableItem
    def remove_CableItem(self, index=None):
        if index is None:
            i = len(CableItems) - 1
            while i <= 1:
                printH("Removing Cable" + str(i), 0, str(i + 1) + "/" + str(len(CableItems)))
                CableItems.pop(i).deleteLater()
                self.graphItems.pop(i).deleteLater()
            CableItems[0].setVisible(False)
            self.graphItems[0].setVisible(False)
        else:
            printH("Removing Cable" + str(index), 0, str(index) + "/" + str(len(CableItems)))
            CableItems[index].setVisible(False)
            self.graphItems[index].setVisible(False)
        pass

    # Create Splitter Auto resize
    # The container of itemWidget automatically resizes as necessary
    def splitter_resize(self):
        if self.tableWidget.width() != self.tableWidget.horizontalHeader().defaultSectionSize():
            self.tableWidget.horizontalHeader().setDefaultSectionSize(self.tableWidget.width())
        if self.splitter.sizes()[0] < 20:
            self.CableScrollAreaWidgetContents.layout().setContentsMargins(9, 9, 9, 9)
        else:
            self.CableScrollAreaWidgetContents.layout().setContentsMargins(0, 9, 9, 9)

    # UI Buttons
    def StartButton(self):
        global stopRetry
        global stopClients
        global retry
        global cableUpdateAllowed

        stopRetry = False
        stopClients = False
        cableUpdateAllowed = False
        retry = threading.Thread(target=Retry)# Try to connect. If fails, loop to try
        retry.start()
        '''retry = threadPool.submit(Retry)'''# Cannot be set inside a threadPool. Weird error where it sits open forever
        self.pb_startClients.setEnabled(False)
        self.pb_stopClients.setEnabled(True)

    def StopButton(self, restart = False):
        global stopRetry
        global stopClients
        global stopUpdate
        global cableUpdateEnabled
        global saveStateAllowed
        global cableUpdateAllowed
        SM.getValues()

        printH("Cleanup:", 0)
        saveStateAllowed = False
        cableUpdateAllowed = False
        stopRetry = True
        stopClients = True
        stopUpdate = True
        cableUpdateEnabled = False
        self.pb_startClients.setEnabled(True)
        self.pb_retry.setEnabled(False)
        self.pb_stopClients.setEnabled(False)
        self.pb_updateCables.setEnabled(False)
        self.cb_auto_cableUpdate.setEnabled(False)
        self.dsb_plcInterval.setEnabled(True)
        self.tabWidget_2.setTabEnabled(1, True)

        printH("Clients/Servers Stopped", 1)

        if restart:
            printH("Restart Allowed...")
            cableUpdateEnabled = False
            sleep(.2)
            os.execl(sys.executable, sys.executable, *sys.argv)
    '''def Cleanup(self):
        printH("New Day!", 0, "Cleaning old files.")
        self.cl.start()
        sleep(0.1)
        printH("New Day!", 0, "Cleanup Complete.")'''

    def CrashCatch(self):
        self.exportH(fileH + "crashLog.txt")
        pass

    def RetryButton(self):
        global stopRetry
        global stopClients
        global retry
        global cableUpdateAllowed

        stopRetry = False
        stopClients = False
        cableUpdateAllowed = False
        self.pb_retry.setEnabled(False)
        self.pb_stopClients.setEnabled(True)
        self.pb_updateCables.setEnabled(False)
        self.cb_auto_cableUpdate.setEnabled(False)
        self.dsb_plcInterval.setEnabled(True)
        retry = threadPool.submit(Retry)# Try to connect. If fails, loop to try

    def GetCablesButton(self):
        global cableUpdate
        global forceCableUpdate

        if cableUpdate.running():
            forceCableUpdate = True
        elif plc.client_allowed:
            if not CableItems[0].isVisible():
                printH("Updating Cable objects...", 0)
                if plc.plc_getCableCount_allowed:
                    plc.PLC_Caller("GetCableCount")  # Get number of available cables from plc
                else:
                    printH("Received cable count: " + str(cableCount), 2, "Preset cable count: " + str(cableCount), True)
                    self.receivedCableCount()

            if not cableUpdate.running():
                cableUpdate = threadPool.submit(updateValues)
                if not autoUpdate_allowed:
                    forceCableUpdate = True

    def ChangeDomainButton(self):
        dialogWindow.show()
        dialogWindow.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        dialog.buttonBox.accepted.connect(self.ChangeDomaIREGsult)
    def ChangeDomaIREGsult(self):
        global domainHost
        global domainPort
        global domainUser
        global domainPassword
        domainHost = dialog.d_lineEdit_1.text()
        domainPort = dialog.d_lineEdit_2.text()
        domainUser = dialog.d_lineEdit_3.text()
        domainPassword = dialog.d_lineEdit_4.text()
        self.l_domainHost.setText(domainHost)
        SM.getValues()

    def SaveStateDataButton(self):
        global forceSaveStateData

        if ssdt.running():
            forceSaveStateData = True

    @toMainThread
    def updateLabelCounter(self, label:QtWidgets.QLabel, number, description=None):
        label.setText(('(' + description + ') ' if description is not None else '') + str(number))

    @toMainThread
    def clearH(self, ask):
        global parentTree
        global parentItem
        self.historyButton.setEnabled(False)
        if ask:
            root = tkinter.Tk()
            root.withdraw()
            if not messagebox.askyesno("Confirm Action", "This action cannot be reversed.\nDo you wish to clear the history?"):
                return
        parentTree = []
        parentItem = []
        '''i = self.historyList.topLevelItemCount()
        for x in range(1, self.historyList.topLevelItemCount()):
            i -= 1
            self.historyList.invisibleRootItem().removeChild(
                self.historyList.invisibleRootItem().child(i))''' # Obsolete
        self.historyList.clear()
        self.historyButton.setEnabled(True)

    def exportH(self, file_path = None):
        global fileH
        self.historyButton_2.setEnabled(False)
        if file_path is None:
            root = tkinter.Tk()
            root.withdraw()
            file_path = filedialog.asksaveasfile(initialdir=fileH, defaultextension=".txt", initialfile="log.txt", filetypes=[("Text files", ".txt")])
            root.destroy()

        fileH = file_path.name
        '''fileString = ""
        date = ""
        for i in range(self.historyList.topLevelItemCount()):
            rootItem = self.historyList.topLevelItem(i)
            date = (rootItem.text(1) + "/" + rootItem.text(0))
            blank = " "*self.historyList.columnWidth(0)

            for j in range(rootItem.childCount()):
                childItem = rootItem.child(j)

                blank = getBlankSpacing(int(widthH / 3), date + " - " + childItem.text(0))
                fileString += (date + " - " + childItem.text(0) +
                    blank + " - " + childItem.text(1) + "\n")

                for k in range(childItem.childCount()):
                    childItem2 = childItem.child(k)

                    blank = getBlankSpacing(int(widthH / 3), date + " - " + childItem2.text(0))
                    fileString += (date + " - " + childItem2.text(0) +
                        blank + " - " + childItem2.text(1) + "\n")

                    for l in range(childItem2.childCount()):
                        childItem3 = childItem2.child(l)

                        blank = getBlankSpacing(int(widthH / 3), date + " - " + childItem3.text(0))
                        fileString += (date + " - " + childItem3.text(0) +
                            blank + " - " + childItem3.text(1) + "\n")

                        for m in range(childItem3.childCount()):
                            childItem4 = childItem3.child(m)

                            blank = getBlankSpacing(int(widthH / 3), date + " - " + childItem4.text(0))
                            fileString += (date + " - " + childItem4.text(0) +
                                blank + " - " + childItem4.text(1) + "\n")''' #Obsolete

        file_path.write(self.historyList.toPlainText())
        file_path.close()
        self.historyButton_2.setEnabled(True)

    def workloadPath(self):
        global localPath
        root = tkinter.Tk()
        root.withdraw()
        path = filedialog.askdirectory(initialdir=localPath)
        root.destroy()
        if path is None or path == '':
            return
        localPath = path
        self.l_workloadPath.setText(localPath)
        SM.getValues()

    '''def colapseH(self):
        self.historyButton_2.setEnabled(False)
        for i in range(self.historyList.topLevelItemCount()):
            self.historyList.topLevelItem(i).setExpanded(False)
        pass
        self.historyButton_2.setEnabled(True)'''
class NewDomainDialog(Ui_EnterNewDomain):
    def __init__(self, dialog) -> None:
        self.setupUi(dialog)

# Create Window Instance
app = QtWidgets.QApplication(sys.argv)
mainWindow = QtWidgets.QMainWindow()
window = MainWindow(mainWindow)
dialogWindow = QtWidgets.QDialog()
dialog = NewDomainDialog(dialogWindow)

class AXHandler(BaseHTTPRequestHandler):  # handler žádostí
    def do_POST(self):  # Odpověď na GET
        pass

    def do_GET(self):  # Odpověď na GET
        keepAlive = True

        pathDict = getDictionaryfromUrl(self.path)
        sleep(0.1)
        print("received:")
        for key in pathDict:
            print("    " + key + "=" + str(pathDict[key]))
        ax.AX_Decipher(self, pathDict, keepAlive)

class API_Client():
    def __init__(self) -> None:
        self.api_received = False
        self.client_allowed = False
        self.port = 1000
        self.host = socket.gethostbyname(socket.gethostname())
        self.api_listener = QThread()
        self.api_listener_Allowed = False
        self.api_retry_success = False
        self.api_requestInterval = 0.1
        self.idle_Interval = 100  # 300 * 0.1s = 30s
        self.idle_Interval = 30

    # API listener Thread
    def API_Listener_Start(self): #deactivated
        global api_server
        if self.api_retry_success:
            return True
        self.api_retry_success = False

        printH("API client", 2)
        sleep(0.1)
        printH("Connecting to Host...", 3, str(self.host) + ":" + str(self.port) + " <---- MasterAPP")
        try:
            if not os.system("ping -c 1" + self.host):
                raise Exception("Address")
        except:
            printH(
                    "An error occurred while connecting to" + str(self.host) + ":" + str(self.port) +
                    "\nMost likely case is that this address is" + "invalid or otherwise could not be used.",
                    4, "Unsupported address:" + str(self.host))
            return self.api_retry_success
        '''try:
            api_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            api_socket.settimeout(20.0)
            api_socket.connect((self.host, self.port))
        except:
            printH(
                "An error occurred while connecting to\n" +
                str(self.host) + ":" + str(self.port) + "\n" +
                "Most likely case is that port on this\n" +
                "address is either not bound or in use\n" +
                "by another instance of MasterAPP or\n" +
                "other application.",
                4, str(self.host) + ":" + str(self.port) + " Unavailable", isRootEnd=True)
            return self.api_retry_success

        api_socket.close()
        api_server.host(self.host)
        api_server.port(self.port)'''
        api_server = HTTPConnection(self.host, self.port)  # Instance of http connection with server

        printH("Success!", 4, str(self.host) + ":" + str(self.port) + " <---> MasterAPP")

        sleep(0.1)

        printH("Connecting to API...", 3, "API <---- " + str(self.host) + ":" + str(self.port))
        try:
            test = testConnection("api")

            if test is False:
                return False
            elif test is True:
                pass
            else:
                raise Exception(test)
        except Exception as err:
            printH(
                "An error occurred while connecting to API." + "No API instance detected on the other side" + "of this port.",
                4, str(err))
            return self.api_retry_success

        printH("Success!", 4, "API <---> " + str(self.host) + ":" + str(self.port))
        self.api_retry_success = True

        return self.api_retry_success

    # Reads the next http message when enabled
    def API_Listener(self):  # Thread only! switched on by retry
        global response
        global stopClients
        global retry
        idle = False
        idleInterval = 0
        api_server_online = 5  # counts down number of missed idle messages

        printH("API-Listener Online", 2, "API <---> MasterAPP")

        while True:
            if stopClients or not self.client_allowed:
                printH("Connection with " + str(self.host) + " interrupted\nAPI-Listener Offline", 0, "API <-X-> MasterAPP", isRootEnd=True)
                api_server.close()
                self.plc_retry_success = False
                break

            sleep(self.api_requestInterval)

            if api_server_online == 0: # incase of connection loss
                printH(
                    "Connection lost with API\n" +
                    "Testing connection", 0, "API --X-> MasterAPP")
                if testConnection("api") is True:
                    printH("Test Success", 1, "API ----> MasterAPP", True)
                else:
                    printH("Test Failed", 1, "API --X-> MasterAPP", True)
                    printH("Connection lost with " + str(self.host) + " \nAPI-Listener Offline", 0, "API <-X-> MasterAPP", isRootEnd=True)
                    self.api_listener_Allowed = False
                    self.api_retry_success = False
                    if autoRetry_allowed:
                        plc.plc_listener_Allowed = False
                        plc.plc_retry_success = False
                        retry = threadPool.submit(Retry) #! Possible Error!
                    break

            if self.api_listener_Allowed: # Expecting a message. Switched by API_Caller()
                sleep(0.1) #change?
                success, reason = self.API_Response()  #returns (bool, reason/exception)
                self.api_listener_Allowed = False
                if success:
                    if reason == "MESSAGE":
                        printH("Response received:", 0, "API ----> MasterAPP")
                        self.api_received = True
                        idleInterval = -10
                        sleep(0.1) #?
                    elif idle:
                        if reason == "OK":
                            api_server_online = 5
                        else:
                            api_server_online -= 1
                        printH("Idle message sent", 0, "API: " + str(reason) + " " + str(api_server_online) + "/5")
                        idle = False
                else:
                    printH(
                        "Failed to read response from API server\n" +
                        "Another attempt in " + str(self.api_requestInterval) + "s", 0, str(reason))
                    api_server_online -= 1
            elif idleInterval >= self.idle_Interval:
                idle = True
                if not self.API_Caller("Idle"):
                    api_server_online -= 1
                else:
                    idleInterval = 0
            idleInterval += 1

    # API Caller
    def API_Caller(self, action="0", index="0", item="0"):
        global retry
        idle = False
        res = False

        request = ""
        if action == "Idle" or action == "0":
            request = "0" + str(index) + str(item)
            idle = True
            res = True
        elif action == "Reservation" or action == "1":
            request = "1" + str(index) + str(item)
        elif action == "CancelReservation" or action == "2":
            request = "2" + str(index) + str(item)
        elif action == "ConfirmRFID" or action == "3":
            request = "3" + str(index) + str(item)
            res = True
        elif action == "GetRider" or action == "4":
            request = "4" + str(index) + str(item)
            res = True

        if not idle:
            printH("Request sent:", 0, "API <---- MasterAPP")
            printH(
                "Request: '" + str(action) + "'\n" +
                "Cable: '" + str(index) + "'\n"
                "Request item: " + str(item),
                2, str(request), isRootEnd=True)

        # for i in range(0, 5):
        success, reason = self.API_Request(request)
        if not success:
            printH(
                "Failed to send request", 2, str(reason), True)
            sleep(self.api_requestInterval)
            return False
        else:
            sleep(0.2)
            #response = self.API_Response()
            self.api_listener_Allowed = res
            return True

    # Deciphers the response of API
    @toMainThread
    def API_Decipher(self, handler: AXHandler):
        global cableUpdateProceed

        self.api_received = False
        self.api_listener_Allowed = False

        # Check for error message
        if response == 69 or response == None:
            printH("API sends error message.", 0, "API Error")
            return False

        action = response[0]                    # Decides what to do
        index = response[1]                     # Decides on which cable
        response_item = response[2]             # Decides with what to work with

        dictionary = {
            "CS": "",
            "RS": "",
            "IDR": "",
            "Position": "",
            "Speed": "",
            "Error": "",
            "TEMP1": "",
            "TEMP2": ""
         }
        cableUpdateProceed = True

        if action == 1:       # ReservationRequest
            if CableDictionary[index]["RS"] == "0" or True:  # Is Rider Empty #!unnecessary, disabled by True
                if CableDictionary[index]["CS"] == "0" or True:  # is Cable Stationary #!unnecessary, disabled by True
                    printH(
                        "Received new reservation for Cable" + str(index) + "\n " +
                        "Waiting for RFID confirmation from AX", 2, str(response) + " -> ACCEPTED")
                    dictionary["RS"] = "1"  # RiderState 1 = Rider Ready
                    dictionary["IDR"] = response_item
                    self.API_Caller("Reservation", index, "1")  # For confirmation
                else:
                    printH(
                        "Received new reservation for Cable" + str(index) + "\n " +
                        "Request refused as Cable" + str(index) + " is currently unavailable", 2, str(response) + " -> DENIED")
                    self.API_Caller("Reservation", index, "0")  # For Confirmation
            else:  # is Rider Ready
                printH(
                    "Received new reservation for Cable" + str(index) + "\n " +
                    "Request refused as Cable" + str(index) + " is already booked or occupied", 2, str(response) + " -> DENIED")
                self.API_Caller("Reservation", index, "0")  # For Confirmation
            pass
        elif action == 2:     # ReservationCanceled
            if CableDictionary[index]["RS"] == "1" or True:  # is Rider Ready #!unnecessary, disabled by True
                printH(
                    "Received a request cancellation for Cable" + str(index) + "\n " +
                    "Request accepted", 2, str(response) + " -> ACCEPTED")
                dictionary["RS"] = "0"  # RiderState 0 = Rider Empty
                dictionary["IDR"] = "####"
                self.API_Caller("Reservation", index, "1")
            elif CableDictionary[index]["RS"] == "2":
                if CableDictionary[index]["CS"] == "0":
                    printH(
                        "Received a request cancellation for Cable" + str(index) + "\n " +
                        "Request accepted", 2, str(response) + " -> ACCEPTED")
                    self.API_Caller("Reservation", index, "1")
                    dictionary["RS"] = "0"  # RiderState 0 = Rider Empty
                    dictionary["IDR"] = "####"
                else:
                    printH(
                        "Received a request cancellation for Cable" + str(index) + "\n " +
                        "Request refused as Cable" + str(index) + " is not stationary", 2, str(response) + " -> DENIED")
                    self.API_Caller("Reservation", index, "0")
            else:
                printH(
                    "Received a request cancellation for Cable" + str(index) + "\n " +
                    "Request refused as Cable" + str(index) + "has no reservation", 2, str(response) + " -> DENIED")
                self.API_Caller("Reservation", index, "0")
            pass
        elif action == 3:     # RFIDConfirmation
            if response_item == 1:
                printH(
                    "Received RFID confirmation for Cable" + str(index) + "\n" +
                    "Correct RFID", 2, str(response) + " -> ACCEPTED")
                dictionary["RS"] = "2"  # RiderState 2 = Rider Boarded
                ax.AX_Caller(handler, "beep=1&relay=1,100")
                plc.PLC_Caller("3", index, "1")
            else:
                printH(
                    "Received RFID confirmation for Cable" + str(index) + "\n" +
                    "Incorrect RFID", 2, str(response) + " -> DENIED")
                ax.AX_Caller(handler, "beep=2")
            pass
        elif action == 4:     # RiderInfo
            if response_item == '0':
                dictionary["RS"] = "0"
                dictionary["IDR"] = "####"
            else:
                dictionary["RS"] = "2"  # RiderState 1 = Rider Boarded
                dictionary["IDR"] = response_item
            pass
        elif action == 5:     # Received RFID fromAX
            if CableDictionary[index]["RS"] != "0" or True: #!unnecessary, disabled by True
                printH(
                    "Received RFID code for Cable" + str(index) + "\n " +
                    "Sending code to API for confirmation", 2, str(response) + " -> ACCEPTED")
                self.API_Caller("ConfirmRFID", index, response_item)
            else:
                printH(
                    "Received RFID code for Cable" + str(index) + "\n " +
                    "But Cable" + str(index) + " does not expect one", 2, str(response) + " -> DENIED")
                ax.AX_Caller(handler, "beep=2")
            pass
        else:
            printH("ERROR: " + str(response), 3, "Unknown Response", True)

        if index > len(CableItems) - 1:
            window.addCableItem()
            index = len(CableItems) - 1
        import_CableItemInfo(index, dictionary)

        cableUpdateProceed = True

    # Sends a request to API
    def API_Request(self, request = None):
        global writing
        try:
            while True:
                while writing:  # Queue
                    sleep(0.1)
                writing = True

                sleep(0.1)  # Wait for listener to be done with listening
                if request is not None:
                    #headers = ["action", request[0],"index", request[1],"item", request[2]]
                    api_server.close()
                    api_server.request(
                        "GET",
                        "/app?action=" + request[0] + "&index=" + request[1] + "&item=" + request[2:])

                writing = False
                #self.api_listener_Allowed = True
                return (True, None)
        except Exception as err:
            writing = False
            return (False, err)

    # Returns a response from channel (0, 1) in form of a list [0, 0, 0]
    def API_Response(self):
        global reading
        global response
        try:
            while reading:
                sleep(0.1)
            reading = True

            reason = "NO-API"
            pureResponse = api_server.getresponse()
            code = pureResponse.getcode()
            reason = pureResponse.reason

            if code == 200 and reason == "MESSAGE":
                headers = dict((x, y) for x, y in pureResponse.getheaders())
                response = [int(headers["action"]), int(headers["index"]), headers["item"]]
            elif code == 200 and reason == "OK":
                pass
            else:
                raise Exception(reason)

            reading = False
            return (True, reason)
        except Exception as err:
            reading = False
            return (False, err)
api = API_Client()
class PLC_Client(): # slot has to be in undefined class
    def __init__(self):
        self.plc_received = False
        self.client_allowed = False
        self.port = 502
        self.host = socket.gethostbyname(socket.gethostname())
        self.plc_listener = threading.Thread()
        self.plc_listener_Allowed = False
        self.plc_retry_success = False
        self.plc_requestInterval = 0.1
        self.plc_timeoutInterval = 1
        self.debug = False

        self.plc_getCableCount_allowed = False
        self.plc_stateOnly = True #allows plc_Caller to get only state and temp of a cable

    # PLC listener Thread
    def PLC_Listener_Start(self):
        if self.plc_retry_success:
            return True
        self.plc_retry_success = False

        printH("PLC client", 2)
        sleep(0.1)
        printH("Connecting to Address...", 3, "MasterAPP ----> " + str(self.host) + ":" + str(self.port))
        try:  # Port test
            plc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            plc_socket.settimeout(20.0)
            plc_socket.connect((self.host, self.port))
        except:
            plc_socket.close()
            printH(
                "An error occurred while connecting to " + str(self.host) + ":" + str(self.port) + "\n" +
                "Most likely case is that port on this " + "address is either not bound or in use\n" +
                "by another instance of MasterAPP or " + "other application.",
                4, str(self.host) + ":" + str(self.port) + " Unavailable", isRootEnd=True)
            return self.plc_retry_success
        plc_socket.close()
        plc_server.host(self.host)
        plc_server.port(self.port)
        printH("Success!", 4, "MasterAPP <---> " + str(self.host) + ":" + str(self.port))

        sleep(0.1)

        printH("Connecting to PLC...", 3, str(self.host) + ":" + str(self.port) + " ----> PLC")

        if self.plc_stateOnly:
            printH(
                "StateOnly mode!\n"+
                "No additional information will "+ "be attempted to be retrieved.", 4, str(self.host) + ":" + str(self.port) + " <---> Quido <-X-> PLC")
            self.plc_retry_success = True
            LRLibrary.add_client("PLC", host=self.host, port=self.port, highestAddress=10, DInp=True, IReg=True, HReg=True)
            return self.plc_retry_success
        try:
            test = testConnection("plc")

            if test is False:
                return False
            elif test is True:
                pass
            else:
                raise Exception(test)
        except Exception as err:
            printH(
                "An error occurred while connecting to PLC " + "No compatible PLC instance detected on the other side " + "of this port",
                4, str(err))
            return self.plc_retry_success

        printH("Success!", 4, str(self.host) + ":" + str(self.port) + " <---> PLC")
        LRLibrary.add_client("PLC", host=self.host, port=self.port, highestAddress=10, DInp=True, IReg=True, HReg=True)
        self.plc_retry_success = True
        return self.plc_retry_success
    def PLC_Listener(self):  # Thread only! switched on by retry
        global cableUpdateProceed
        global response
        global retry

        printH("PLC-Listener Online", 2, "MasterAPP <---> PLC")

        while True:
            if stopClients or not self.client_allowed:
                printH("Connection with " + str(self.host) + " interrupted. PLC-Listener Offline", 0, "MasterAPP <-X-> PLC", isRootEnd=True)
                plc_server.close()
                self.plc_retry_success = False
                break

            sleep(self.plc_requestInterval)
            if not plc_server.is_open():
                if not plc_server.open():
                    printH(
                        "Connection lost with PLC. " +
                        "Testing connection", 0, "MasterAPP <-?-- PLC")

                    if not testConnection("plc"):
                        printH("Test Failed", 1, "MasterAPP <-X-- PLC", True)
                        printH("Connection lost with " + str(self.host) + ". PLC-Listener Offline", 0, "MasterAPP <-X-> PLC", isRootEnd=True)
                        self.plc_listener_Allowed = False
                        self.plc_retry_success = False
                        if autoRetry_allowed:
                            api.api_listener_Allowed = False
                            '''retry = Worker(None, 'retry')'''
                            retry = threadPool.submit(Retry)
                        break
                    else:
                        printH("Test Success", 1, "MasterAPP <---- PLC", True)

            """if self.plc_listener_Allowed and self.PLC_Response(False): #Read ControlWord
                response = self.PLC_Response()
                if response is False or response == "ERR":
                    printH(
                        "Failed to read response. " +
                        "Another attempt in " + str(self.plc_requestInterval) + "s", 0, "MasterAPP <-?-- PLC")
                    cableUpdateProceed = True

                else:
                    printH("Response received:", 0, "MasterAPP <---- PLC")
                    self.plc_listener_Allowed = False
                    self.plc_received = True
                    self.PLC_Decipher()"""

    # PLC Caller
    def PLC_Caller(self, action, index=0, item=0):
        global retry
        global response
        global cableUpdateInterrupt
        '''
        Word addresses
        0 - Control Word
        1 - Reference Word
        2 - Reference Word
        3 - Status Word
        2 - index
        3 - item
        '''
        words = [0, 0, 0]
        if action == "GetCableCount" or action == "1":
            words[0] = 1
        elif action == "GetCable" or action == "2":
            words[0] = 2
        elif action == "SendAccess" or action == "3":
            words[0] = 4
        elif action == "GetAll" or action == "4":
            if self.plc_stateOnly:
                response = self.PLC_Response()
                if response is False:
                    sleep(self.plc_timeoutInterval)
                    response = self.PLC_Response()
                    if response is False:
                        printH("Connection lost with " + str(self.host) + ". PLC-Listener Offline", 0, "MasterAPP <-X-> PLC", isRootEnd=True)
                        api.api_listener_Allowed = False
                        self.plc_listener_Allowed = False
                        cableUpdateInterrupt = True
                        sleep(.2)
                        for i in range(cableCount):
                            import_CableItemInfo(i, dictionary={"CS": "3", "RS": "", "IDR": "", "Position": "", "Speed": "", "Error": ""})
                        retry = threadPool.submit(Retry)
                        return
                response[0] = 4
                response[1] = index #unnecessary
                self.plc_received = True
                self.plc_listener_Allowed = True
                self.PLC_Decipher()
                return
        words[1] = index
        words[2] = item

        """printH("Request sent:", 0, "MasterAPP ----> PLC")
        printH(
            "Request: '" + str(action) + "'\n" +
            "Cable: '" + str(index) + "'\n"
            "Request item: " + str(item),
            2, str(words), isRootEnd=True)"""

        for i in range(0, 5):
            if not self.PLC_Request(words):
                printH(
                    "Failed to send request - " + str(i) + "/5" + ". " +
                    "Another attempt in " + str(self.plc_timeoutInterval) + "s", 2, "MasterAPP --?-> PLC", True)
                sleep(self.plc_timeoutInterval)
            else:
                self.plc_listener_Allowed = True
                return
        printH("Connection lost with " + str(self.host) + ". PLC-Listener Offline", 0, "MasterAPP <-X-> PLC", isRootEnd=True)
        api.api_listener_Allowed = False
        self.plc_listener_Allowed = False
        cableUpdateInterrupt = True
        retry = threadPool.submit(Retry)

    # Deciphers the response of PLC
    @toMainThread
    def PLC_Decipher(self, response=None):
        global CableItems
        global cableCount
        global cableUpdateProceed
        global cableUpdateInterrupt
        global forceCableUpdate
        global cableUpdate
        global Watcher3

        Watcher3 = time()

        action = response[0]                            # Decides what to do
        index = response[1]                             # Decides on which cable
        response_item = response[2:]                    # Decides with what to work with

        while len(response_item) < 6:
            response_item.append(0)

        dictionary = {
            "CS": "",
            "RS": "",
            "IDR": "",
            "Position": "",
            "Speed": "",
            "Error": ""
        }

        if action == 1:  # ReceivedCableCount
            printH("Received CableCount: " + str(response_item[0]), 2, "Response: " + str(response), True)
            if response_item[0] <= 0:
                printH("ERROR: PLC has zero registered cables", 2, "Zero cables")
            cableCount = response_item[0]
            window.receivedCableCount()
            #sleep(0.1)  # wait for ReceivedCableCount to process
            forceCableUpdate = True
            self.plc_received = False
            self.plc_listener_Allowed = True
            '''if not cableUpdate.running():
                cableUpdate = threadPool.submit(update_CableItems)'''
            return
        elif action == 2:  # Received Cable
            if str(response_item[4]) == "0404":
                dictionary["CS"] = 3
                printH("Cable" + str(index) + " not found", 2, "Error Message: " + str(response_item[3]))
                self.plc_received = False
                cableUpdateInterrupt = True
                self.plc_listener_Allowed = True
                return
            else:
                #printH("Received Cable" + str(index), 2, "Response: " + str(response))
                # dictionary format:        [P, S, E]
                # register Address            0, 1, 2
                # P = CablePosition
                # S = CableSpeed
                # E = Alarm

                # Quido inputs:
                #   [0, X] = 0, Offline
                #   [1, 0] = 1, Stationary
                #   [1, 1] = 2, In progress
                #   error  = 3, Error


                dictionary["CS"] = str(self.getCableState(index))
                window.t_label_2.setText(str(response_item[0]) + "°C")
                window.t_label_4.setText(str(response_item[1]) + "°C")
                if not self.plc_stateOnly:
                    dictionary["Position"] = str(response_item[2])
                    dictionary["Speed"] = str(response_item[3])
                    dictionary["Error"] = str(response_item[4])
            pass
        elif action == 4:
            for i in range(len(CableItems)):
                dictionary["CS"] = str(self.getCableState(i))
                import_CableItemInfo(i, dictionary)
            window.t_label_2.setText(str(response_item[0]) + "°C")
            window.t_label_4.setText(str(response_item[1]) + "°C")
            cableUpdateProceed = True
            self.plc_listener_Allowed = True
            Watcher3 = time() - Watcher3
            return

        if index > len(CableItems) - 1:
            window.addCableItem()
            index = len(CableItems) - 1
        import_CableItemInfo(index, dictionary)

        cableUpdateProceed = True
        self.plc_listener_Allowed = True
    def getCableState(self, index):
        cableState = 3
        if quidoInputs[index][0]:
            if quidoInputs[index][1]:
                cableState = 2
            else:
                cableState = 1
        else:
            cableState = 0
        return cableState

    # Sends a request to plc
    def PLC_Request(self, words = None):
        global writing
        try:
            while True:
                while writing:  # Queue
                    sleep(0.1)
                writing = True

                plc.plc_listener_Allowed = False
                server = plc_server
                if not server.is_open():
                    if not server.open():
                        break

                sleep(0.01)  # Wait for listener to be done with listening
                if words is not None: #V5.0 Communication
                    server.write_multiple_registers(5, [0]*9)   #clear Databank
                    server.write_multiple_registers(5, words)   #Write prepared words
                    server.write_single_register(1, 1)          #Write True on control word (PLC read message)

                sleep(0.2)
                writing = False
                server.close()
                return True
        except:
            server.close()
            pass
        writing = False
        return False

    # Returns a response from channel in form of a list [0, 0, 0]
    def PLC_Response(self, readResponse=True):
        global reading

        plc_server: ModbusClient = LRLibrary.clientList["PLC"].get_client()
        if self.debug:
            words = [0]*7
            words[0] = 2
            temp = [random.randrange(0, 999), random.randrange(0, 999)]
            temp[0] = "{:.1f}".format(temp[0] / 10)
            temp[1] = "{:.1f}".format(temp[1] / 10)

            action = random.randrange(1, 4)
            index = random.randrange(0, len(CableItems))
            item = temp
            item.extend(words[3:])

            while item[-1] == 0 and item[-1] is not item[0]:
                item.pop()

            quidoInputs.clear()
            i = 0
            while i < quidoMaxInput:
                quidoInputs.append([random.randrange(0, 2), random.randrange(0, 2)])
                i += 2

            response = [action, index]
            response.extend(item)
            return response
        try:
            if not plc_server.is_open():      # retry if channel is not open
                if not plc_server.open():
                    return False
            '''
            Holding registers:
                4 - Status Word (Message indication)
                6..8 - Request Values
                8..13 - Response Values
            Discrete inputs:
                0 - Cable0 ON/OFF
                1 - Cable0 Moving/Stationary
                2..n - CableN
            Input Registers:
                1 - Water Temperature
                2 - Air Temperature
            '''

            if not self.plc_stateOnly:
                message = format(plc_server.read_holding_registers(4, 1)[0], '04b')
                if not int(message[5]):  #Return False if PLC has no message
                    return False
                if not readResponse:  #Check if PLC has message
                    return True
                if not not int(message[5]):  #Return False if PLC sends error message
                    return False

            inputs = plc_server.read_discrete_inputs(0, quidoMaxInput) #Quido discrete inputs
            temp = plc_server.read_input_registers(1, 2)
            temp[0] = "{:.1f}".format(temp[0] / 10)
            temp[1] = "{:.1f}".format(temp[1] / 10)
            if inputs is None:
                inputs = [False]*quidoMaxInput
            quidoInputs.clear()
            i = 0
            while i < quidoMaxInput:
                quidoInputs.append([inputs[i], inputs[i + 1]])
                i += 2

            words = plc_server.read_holding_registers(5, 9)  #read all Actual Values
            if words is None:
                words = [0]*7
                words[0] = 2

            action = words[0]
            index = words[1]
            item = temp
            item.extend(words[3:])

            while item[-1] == 0 and item[-1] is not item[0]:
                item.pop()

            response = [action, index]
            response.extend(item)

            plc_server.write_multiple_registers(5, [0]*9)   #clear Databank(Message read)

            reading = False
            #plc_server.close()
            return response
        except:
            plc_server.close()
            reading = False
            return False
plc = PLC_Client()
class AX_Server():
    def __init__(self) -> None:
        self.server_allowed = False
        self.host = '192.168.11.50'
        self.port = 11854
        self.ax_server = None
        self.ax_listener = threading.Thread()
        self.ax_retry_success = False
        self.ax_message = None
        self.request_Interval = window.dsb_axInterval.value()

    # AX listener Thread
    def AX_Listener_Start(self):
        if self.ax_retry_success:
            return True
        self.ax_retry_success = False

        printH("AX server", 2)
        sleep(0.1)
        printH("Starting server...", 3, "MasterAPP ----> \n" + str(self.host) + ":" + str(self.port))
        try:
            self.ax_server = HTTPServer((self.host, self.port), AXHandler)  # Instance http serveru[adresa serveru, handler žádostí]
        except:
            printH(
                    "An error occurred while connecting to\n" +
                    str(self.host) + ":" + str(self.port) +
                    "\nMost likely case is that this address is\n" +
                    "invalid or otherwise could not be used.",
                    4, "Unsupported address:\n" + str(self.host))
            return self.ax_retry_success
        printH("Success!", 4, "MasterAPP <---> \n" + str(self.host) + ":" + str(self.port))
        try:
            printH("Waiting for KeepAlive...", 3, str(self.host) + ":" + str(self.port) + "\n <---- AX-DOOR")

            '''client = hClient.HTTPConnection(self.host, port=self.port) # An instance of entrance connection
            client.set_tunnel(self.host)
            client.request(
                method="GET",
                url=str(self.host) + ":7/keepalive_req.cgi")'''
            AXserve = threadPool.submit(ax.AX_ServeForever)
            '''AXserve =threading.Thread(target=self.AX_ServeForever)'''
            while not self.ax_retry_success:
                if stopRetry:
                    self.ax_server.shutdown()
                    return
                sleep(0.1)

            self.ax_server.shutdown()

        except:
            pass
        printH("Success!", 4, "MasterAPP <---> AX-DOOR")

    def AX_ServeForever(self):
        self.ax_server.serve_forever()

    def AX_Listener(self):  # Thread only! switched on by retry
        printH("AX-Listener Online", 2, "MasterAPP <---> AX-DOOR", isRootEnd=True)
        AXserve = threadPool.submit(ax.AX_ServeForever)
        '''AXserve =threading.Thread(target=self.AX_ServeForever)'''
        while True:
            if stopClients:
                self.ax_server.shutdown()
                printH("Connection with " + str(self.host) + " interrupted\nAX-Listener Offline", 0, "MasterAPP <-X-> AX-DOOR", isRootEnd=True)
                break

            sleep(plc.plc_requestInterval)

    # AX Caller
    def AX_Caller(self, handler: AXHandler, message: str = None, request=False):
        try:
            if request:
                pass
            else:
                handler.send_response(200)
                handler.end_headers()
                if message is None:
                    return
                handler.wfile.write(message.encode())
                printH("Response sent:\n" + message, 0, "MasterAPP ----> AX")
                self.ax_message = None
        except:
            self.ax_message = message
            printH("Failed to send response:" + message + "\nAnother attempt at next keepAlive", 0, "MasterAPP --?-> AX")

    # Deciphers the request of AX
    def AX_Decipher(self, handler: AXHandler, pathDict: dict, keepAlive):
        global response
        if pathDict["type"] == "online":
            '''
            0 - date (YYYYMMDD)
            1 - time (HHMMSS)
            2 - DIRECTION:  0=exit
                            1=entry
            4 - USER_CODE
            5 - CONTROLS:   00 = OK
                            33 = Badge not valid
                            34 = Invalid edition
                            35 = User disabled
                            36 = Badge disabled
                            37 = User expired
                            38 = Not authorized
                            39 = Out of hours user
                            41 = Missing auth. group
                            42 = Missing Timemod
                            43 = Missing Term Id
                            45 = Invalid day
                            48 = Invalid edition
                            52 = Card expired
                            53 = Missing both CARDS.TXT and CARDRNGE.TXT tables
                            54 = Missing AUTHGRP.TXT table
                            55 = Missing AUTH.TXT table
                            56 = Missing TIMEMOD.TXT table
                            59 = Wrong facility code (aka “common code”)
                            60 = Transaction denied by the host in online mode
                            (unlock relay not activated, see §9.2 at page 77)
            6 - RESULT:     0 = Transaction completed
                            1 = Transaction not completed,
            7 - SOURCE:     1 = “console” reader with TTL levels output
                            2 = “console” serial reader with EIA-RS232 levels output
                            8 = Manual gate unlock
            8 - EDITION*
            9 - GATE:       Number of the gate associated to the reader
            10 - UTC:        difference between local time and UTC/GMT time
            11 - DAYLIGHT:  0 = transaction done during winter time,
                            1 = summer time
            12.. - RFU:       more fields to be added in future releases
            '''

            if "trsn" in pathDict.keys():
                readerIndex = int(pathDict["trsn"][9]) - 1
                readerCode = int(pathDict["trsn"][4])
                printH(
                    "Received Reader message:\nGate" + str(readerIndex) +
                    "\nCode: " + readerCode, 0, "MasterURL <-RD-- AX", True)
            if api.client_allowed:
                response = [4, readerIndex, readerCode]
                api.API_Decipher(handler=handler)
            pass
        if pathDict["type"] == "keepalive":
            if not self.ax_retry_success:
                printH("Received KeepAlive", 4, "MasterURL <-KA-- AX", True)
            '''else:
                printH("Received KeepAlive", 0,"MasterURL <-KA-- AX", True)  '''
            if "rdrReply" in pathDict.keys():
                print("MasterURL <-RDR-- AX\nReader reply = " + pathDict["rdrReply"])
                keepAlive = False
            if "cmd" in pathDict.keys():
                if pathDict["cmd"] == "ok":
                    print("MasterURL <-OK-- AX\nOK")
                    keepAlive = False
                if pathDict["cmd"] == "error":
                    print("MasterURL <-ERR-- AX\nError")
                    keepAlive = False

            if keepAlive:
                if not self.ax_retry_success:
                    self.ax_retry_success = True
                    print("MasterURL --BP-> AX\nBeep")
                    self.AX_Caller(handler, "beep=1&keepaliveperiod=" + self.request_Interval)
                else:
                    if self.ax_message is None:
                        # printH("MasterURL --OK-> AX", 0)
                        self.AX_Caller(handler)
                    else:
                        printH("MasterURL ---> AX\nSending last message", 0)
                        self.AX_Caller(handler, self.ax_message)
            pass
        if pathDict["type"] == "batch":
            print("MasterURL <-KA-- AX\nBatch")
            if self.ax_message is not None:
                printH("MasterURL ---> AX\nSending last message", 0)
                self.AX_Caller(handler, self.ax_message)
            else:
                self.AX_Caller(handler, "ack=1")
                print("MasterURL --ACK-> AX\nAcknowledged")
        pass
    pass
ax = AX_Server()

# Public variables
isStart = True
checkSettings = True
firstAttempt = True
collapseH = False
widthH = 0
fileH = ""

# Communication
reading = False
writing = False
response = ""
stopClients = False
autoStart_allowed = False
autoUpdate_allowed = False
autoUpdate_Interval = 60
quidoMaxInput = 10
quidoInputs = []

quidoMaxInput = window.sb_cableCount.value() * 2

# Threads
threadPool = ThreadPoolExecutor(max_workers=10)
retry = None

# MasterAPP Communication
api_server = HTTPConnection
plc_server = ModbusClient()

# QObject lists
cableCount = 4
CableItems = [
    window.cableItem_1,
]
CableDictionary = []
CableGraph = [
    window.pg_workload_1,
]

parentItem = QtWidgets.QTreeWidgetItem()
parentTree = [
    parentItem,
]
# debug

Watcher0 = 0
Watcher1 = 0
Watcher2 = 0
Watcher3 = 0
Watcher = []

def StartPart2():
    '''Startup part 2: Connections and Cable Updates'''
    global stopClients
    global retryInProgress
    global cableUpdate
    global forceCableUpdate
    global logFilePath
    global saveStateAllowed
    global cableUpdateAllowed

    stopClients = False
    api.api_listener_Allowed = False
    plc.plc_listener_Allowed = True
    saveStateAllowed = True
    cableUpdateAllowed = True

    window.pb_updateCables.setEnabled(True)
    window.cb_auto_cableUpdate.setEnabled(True)
    window.pb_stopClients.setEnabled(True)
    window.pb_retry.setEnabled(True)

    import_CableItemInfo(0, new=True)  # Create a template CableItem
    if plc.client_allowed and autoUpdate_allowed:
        window.GetCablesButton()

# Retry for Connections
stopRetry = False
autoRetry_allowed = False
retryInProgress = False
retryInterval = 0
def Retry(loop = False):
    """Retry for Connections"""
    global retryInProgress
    global retryInterval
    global stopClients
    global stopRetry
    global firstAttempt
    global retry

    if stop_Retry(): return
    if retryInProgress:
        return
    if not (api.client_allowed or plc.client_allowed or ax.server_allowed):
        printH("Connection failed. No clients selected.")
        return
    retryInProgress = True
    if not firstAttempt and not loop:
        retryInProgress = False
        retry = threadPool.submit(loop_Retry)
        return
    if loop:
        printH("Restarting clients", 0)
    else:
        printH("Starting clients", 0)

    if api.client_allowed:
        api.api_retry_success = False
        api.API_Listener_Start()
        if stop_Retry(): return
    if plc.client_allowed:
        plc.plc_retry_success = False
        plc.PLC_Listener_Start()
        if stop_Retry(): return

    success = False
    if ((not api.client_allowed or api.api_retry_success) and
            (not plc.client_allowed or plc.plc_retry_success)):
        if ax.server_allowed:
            ax.ax_retry_success = False
            ax.AX_Listener_Start()
            if stop_Retry(): return
    if ((not api.client_allowed or api.api_retry_success) and
        (not plc.client_allowed or plc.plc_retry_success) and
            not ax.server_allowed or ax.ax_retry_success):
        success = True

        if api.host == plc.host and api.client_allowed and plc.client_allowed:
            printH(
                "API/PLC Connection successfully established with: " +
                str(api.host), 1, "Test success")
            api.api_listener = threadPool.submit(api.API_Listener)
            if not plc.plc_stateOnly:
                plc.plc_listener = threadPool.submit(plc.PLC_Listener)
        else:
            if api.client_allowed:         # If allowed, turn on api listener
                printH(
                    "API Connection successfully established with: " +
                    str(api.host), 1, "Test success")
                api.api_listener = threadPool.submit(api.API_Listener)
            if plc.client_allowed:         # If allowed, turn on plc listener
                printH(
                    "PLC Connection successfully established with: " +
                    str(plc.host), 1, "Test success")
                if not plc.plc_stateOnly:
                    plc.plc_listener_Allowed = True
                    plc.plc_listener = threadPool.submit(plc.PLC_Listener)
        if ax.server_allowed:         # If allowed, turn on ax listener
            printH(
                "AX Connection successfully established with " +
                "AX-DOOR terminal on " + str(ax.host), 1, "Test success")
            ax.ax_listener = threadPool.submit(ax.AX_Listener)

        firstAttempt = False
    else:
        success = False

    retryInProgress = False
    if not success:
        if autoRetry_allowed:
            printH(
                "Connection failed for either API, PLC or AX. " +
                "Another attempt will occur in " + str(retryInterval) + " seconds", 1, "Test failed", isRootEnd=True)
            firstAttempt = False
            for i in range(int(retryInterval) + 1):  # Timeout
                sleep(1)
                window.updateLabelCounter(window.l_retryInterval, str(int(retryInterval) - i).zfill(2))
                if stop_Retry():
                    break
            window.updateLabelCounter(window.l_retryInterval, str(0).zfill(2))
            if not loop:
                retry = threadPool.submit(loop_Retry) # Connection retry for API and PLC (30s)
        else:
            printH(
            "Connection failed for either API, PLC or AX. " +
            "Press Retry to try again.", 1, "Test failed. No Retry.", isRootEnd=True)
            window.pb_retry.setEnabled(True)
    elif success:
        StartPart2()
        if loop:
            return False

    retryInProgress = False
    if loop:
        return True
    return
def loop_Retry(loop = True):
    global stopClients

    while loop and autoRetry_allowed:
        stopClients = True
        sleep(plc.plc_requestInterval)
        stopClients = False

        loop = Retry(loop)

def stop_Retry():
    global retryInProgress
    if stopRetry:
        printH("Retry interrupted", 1)
        retryInProgress = False
        window.pb_retry.setEnabled(True)
        return True
    return False


saveStateAllowed = False
def saveStateDataTimer(blank: bool = False):
    if blank: return

    global autoUpdate_Interval
    global forceSaveStateData
    global updateInProgress
    global minuteState
    global saveInProgress

    '''while datetime.now().time().second != 0: #synchronize to a minute
        if forceCableUpdate or not cableUpdateEnabled: break
        window.auto_label_1.setText(str(timedelta(minutes=1) - datetime.now().time().second).zfill(2))
        sleep(1)'''
    backupInterval = autoUpdate_Interval

    minuteState = [[3]*len(CableItems)]*60
    nextMinute = None
    while saveStateAllowed or forceSaveStateData:
        currentTime = datetime(
        datetime.now().year,datetime.now().month,datetime.now().day,
        hour=datetime.now().time().hour,
        minute=datetime.now().time().minute,
        second=datetime.now().time().second,
        microsecond=0)

        if currentTime.minute == nextMinute or forceSaveStateData:
            print("sstd: Enter")
            forceSaveStateData = False
            while updateInProgress and (cableUpdateEnabled and cableUpdateAllowed) and plc.plc_retry_success:
                pass #Wait till update ends
            saveInProgress = True

            start_timec = time()

            saveStateData()
            #printH("Completed in " + str(time() - start_timec)[:5] + "s", 1, isRootEnd=True)
            if (window.tabWidget_2.currentIndex() == 3):
                window.updateGraph1()
                sleep(0.01)
            elif window.tabWidget_2.currentIndex() == 2:
                window.updateLabelCounter(window.l_saveStateTimer, str(0).zfill(2))
            minuteState = [[3]*len(CableItems)]*60

            if backupInterval < autoUpdate_Interval:
                printH("Resuming regular update rate (-1s).", 1)
                window.dsb_plcInterval.setValue(float(window.dsb_plcInterval.value() - 1))
                autoUpdate_Interval = window.dsb_plcInterval.value()

            saveInProgress = False
            print("sstd: Exit")
        sleep(.5)

        #nextTime = (currentTime + timedelta(seconds=int(autoUpdate_Interval))).time()
        nextMinute = currentTime.minute + 1

        window.updateLabelCounter(window.l_saveStateTimer, str((timedelta(minutes=1) - timedelta(seconds=datetime.now().time().second)).seconds).zfill(2))
ssdt = threadPool.submit(saveStateDataTimer, True)

# Imports new Cable information into tableWidget
@toMainThread
def import_CableItemInfo(index=0, dictionary={"CS": "", "RS": "", "IDR": "", "Position": "", "Speed": "", "Error": ""}, new=False):
    tableWidget: QtWidgets.QTableWidget
    tableWidget = CableItems[index].children()[3]
    image: QtWidgets.QLabel
    image = CableItems[index].children()[2]
    if index >= len(CableDictionary):
        d = {"I": index}
        d.update(dictionary)
        CableDictionary.append(d)

    if new or dictionary["CS"] != "":
        if dictionary["CS"] == "0":  # Offline
            image.setPixmap(QtGui.QPixmap(":/img/Img/RedLight.png"))
            tableWidget.item(0, 0).setText("OFFLINE")
            tableWidget.item(0, 0).setBackground(QtGui.QColor(0, 0, 0))
            tableWidget.item(0, 0).setForeground(QtGui.QColor(255, 255, 255))
        elif dictionary["CS"] == "1":  # Stationary
            image.setPixmap(QtGui.QPixmap(":/img/Img/YellowLight.png"))
            tableWidget.item(0, 0).setText("STATIONARY")
            tableWidget.item(0, 0).setBackground(QtGui.QColor(255, 255, 0))
            tableWidget.item(0, 0).setForeground(QtGui.QColor(0, 0, 0))
        elif dictionary["CS"] == "2": # Moving
            image.setPixmap(QtGui.QPixmap(":/img/Img/GreenLight.png"))
            tableWidget.item(0, 0).setText("MOVING")
            tableWidget.item(0, 0).setBackground(QtGui.QColor(0, 255, 0))
            tableWidget.item(0, 0).setForeground(QtGui.QColor(0, 0, 0))
        else: #dictionary["CS"] == "3": # Error
            image.setPixmap(QtGui.QPixmap(":/img/Img/RedLight.png"))
            tableWidget.item(0, 0).setText("ERR/UNKNOWN")
            tableWidget.item(0, 0).setBackground(QtGui.QColor(255, 0, 0))
            tableWidget.item(0, 0).setForeground(QtGui.QColor(0, 0, 0))
        if not new:
            #printH("Cable" + str(index) + " State set on " + tableWidget.item(0, 0).text(), 10, isRootEnd=True)
            pass
        CableDictionary[index]["CS"] = dictionary["CS"]
    if new or dictionary["RS"] != "":
        if dictionary["RS"] == "1":  # Ready
            tableWidget.item(1, 0).setText("READY")
            tableWidget.item(1, 0).setBackground(QtGui.QColor(255, 255, 0))
        elif dictionary["RS"] == "2":  # Boarded
            tableWidget.item(1, 0).setText("BOARDED")
            tableWidget.item(1, 0).setBackground(QtGui.QColor(0, 255, 0))
        else:  # dictionary["RS"] == "0": # Empty
            dictionary["RS"] = "0"
            tableWidget.item(1, 0).setText("EMPTY")
            tableWidget.item(1, 0).setBackground(QtGui.QColor(255, 0, 0))
        if not new:
            #printH("Cable" + str(index) + " Rider state set on " + tableWidget.item(1, 0).text(), isRootEnd=True)
            pass
        CableDictionary[index]["RS"] = dictionary["RS"]
    if new or dictionary["IDR"] != "":
        if dictionary["IDR"] != "":
            tableWidget.item(2, 0).setText(dictionary["IDR"])
        else:
            tableWidget.item(2, 0).setText("####")
        if not new:
            #printH("Cable" + str(index) + " Rider ID set on " + tableWidget.item(2, 0).text(), isRootEnd=True)
            pass
        CableDictionary[index]["IDR"] = dictionary["IDR"]
    if new or dictionary["Position"] != "":
        if dictionary["Position"] != "":
            tableWidget.item(3, 0).setText(str(int(dictionary["Position"])) + "m")
        else:
            tableWidget.item(3, 0).setText("0m")
        if not new:
            #printH("Cable" + str(index) + " Position set on " + tableWidget.item(3, 0).text(), isRootEnd=True)
            pass
        CableDictionary[index]["Position"] = dictionary["Position"]
    if new or dictionary["Speed"] != "":
        if dictionary["Speed"] != "":
            tableWidget.item(4, 0).setText(str(int(dictionary["Speed"])) + "km/h")
        else:
            tableWidget.item(4, 0).setText("0km/h")
        if not new:
            #printH("Cable" + str(index) + " Speed set on " + tableWidget.item(4, 0).text(), isRootEnd=True)
            pass
        CableDictionary[index]["Speed"] = dictionary["Speed"]
    if new or dictionary["Error"] != "":
        if dictionary["Error"] != "":
            tableWidget.item(5, 0).setText("X " + dictionary["Error"])
        else:
            tableWidget.item(5, 0).setText("X 0000")
        if not new:
            #printH("Cable" + str(index) + " Error set on " + tableWidget.item(5, 0).text(), isRootEnd=True)
            pass
        CableDictionary[index]["Error"] = dictionary["Error"]
# ##COMMUNICATION
#Returns an html response in form of a dictionary
def getDictionaryfromUrl(url: str):
        dictionary = {}
        lastKeyIndex = 0
        messageIndex = url.find("?", 0)
        message = url[1: messageIndex]
        dictionary["type"] = message
        i = messageIndex - 1
        while i < len(url) - 1:
            i += 1
            if url[i] == "&" or url[i] == "?":
                if url[i] == "&":
                    keyIndex = url.find("&", lastKeyIndex + 1)
                elif url[i] == "?":
                    keyIndex = url.find("?", lastKeyIndex + 1)

                nextKeyIndex = url.find("&", keyIndex + 1)
                valueIndex = url.find("=", keyIndex)
                key = url[keyIndex + 1: valueIndex]
                if nextKeyIndex != -1:
                    value = url[valueIndex + 1: nextKeyIndex]
                    i = nextKeyIndex - 1
                else:
                    value = url[valueIndex + 1:]

                if not str(value).find(",") == -1:
                    value = value.split(",")

                lastKeyIndex = keyIndex
                dictionary[key] = value
        return dictionary

# test a connection with server
def testConnection(server):
    try:
        if server == "plc":
            if not plc_server.open():
                raise Exception('Address error')
            if not plc.PLC_Request(words=[8, 8, 8]):
                raise Exception('Could not send request')
            sleep(1)
            testResponse = plc.PLC_Response(True)[4:7]
            if testResponse is False:
                raise Exception('Could not read response')

            if (testResponse[0] != 9 or testResponse[1] != 9 or testResponse[2] != 9):
                printH(
                    "An error occurred while connecting to PLC " +
                    "PLC instance did not respond with '999'",
                    4, "Unsupported response format: " + str(testResponse))
                return False
            else:
                return True
        elif server == "api":
            success, reason = api.API_Request("888")
            if not success: #Sends Http test message
                raise Exception('Could not send request: ' + str(reason)) # Raises error when channel is already in use
            sleep(1)
            success, reason = api.API_Response()
            if not success:
                raise Exception('Could not read response: API - ' + str(reason))
            testResponse = response
            if testResponse[0] != 9 or testResponse[1] != 9 or testResponse[2] != '9':
                printH(
                    "An error occurred while connecting to API. " +
                    "API instance did not respond with '999'",
                    4, "Unsupported response format: " + str(testResponse))
                return False
            else:
                return True
        elif server == "ax":
            pass
    except Exception as err:
        return err
    pass

# ##HISTORY
lastLevel = 0
@toMainThread
def printH(string='', level=lastLevel, description='', isRootEnd=False, inPool=False, blank=False):
    ''' Prints an item in historyList. !Processed in the MainThread!'''
    global lastLevel
    if blank: return

    try:
        if description != "":
            description = "(" + description + ")"
        if level == 100:
            level = lastLevel + 1

        if level == 0:
            newline = "\n" + str(datetime.today().strftime("%Y:%m:%d")) + "/" + str(datetime.today().strftime("%H:%M:%S")) + ": " + " "*level + string + " - " + description
            lastLevel = 0
        else:
            newline = "  "*level + "— "+ string + " - " + description
            lastLevel = level
        print(newline)
        window.historyList.appendPlainText(newline)
        window.historyList.moveCursor(QtGui.QTextCursor.End)

        newline = newline + "\n"
        with open(logFilePath, 'a') as logfile:
            logfile.write(newline)
            logfile.close()
        print("Print: Exit - " + string)
    except:
        pass

    ''' if not isinstance(threading.current_thread(), threading._MainThread):
        hTuple = (string, level, description, isRootEnd)
        pHistory.start()
        sleep(0.001) #Delay from the previous printH
        return
    if hTuple is not None:
        string = hTuple[0]
        level = hTuple[1]
        description = hTuple[2]
        isRootEnd = hTuple[3]
        hTuple = None
    elif string is True: #emit(64) byproduct workaround
        return

    if hItemCount > 10000:
        window.clearH(True)
        hItemCount = 0
    if level == 0:  # Is the root
        rootItem = QtWidgets.QTreeWidgetItem()
        dateItem = QtWidgets.QTreeWidgetItem()
        rootItem.setText(0, str(string))
        rootItem.setText(1, str(description))
        dateItem.setText(0, str(datetime.today().strftime("%H:%M:%S")))
        dateItem.setText(1, str(datetime.today().strftime("%Y:%m:%d")))
        window.historyList.addTopLevelItem(dateItem)
        dateItem.addChild(rootItem)
        print(datetime.today().strftime("%H:%M:%S"), datetime.today().strftime("%Y:%m:%d"))
        parentTree = [dateItem, rootItem]            # [root, child, childOfChild]
        dateItem.setExpanded(not collapseH)
        rootItem.setExpanded(not collapseH)

        returnItem =  rootItem
    else:  # Is the child
        childItem = QtWidgets.QTreeWidgetItem()
        childItem.setText(0, str(string))
        childItem.setText(1, str(description))
        if level >= len(parentTree):
            level = len(parentTree)
            parentTree[level - 1].addChild(childItem)
            if not isRootEnd:
                parentTree.append(childItem)
        else:
            if not isRootEnd:
                parentTree[level] = childItem
            parentTree[level - 1].addChild(childItem)

        childItem.setExpanded(not collapseH)
        returnItem = childItem

    widthH = window.historyList.columnWidth(0)
    window.historyList.resizeColumnToContents(0)
    if window.historyList.columnWidth(0) < widthH:
        window.historyList.setColumnWidth(0, widthH)



    return returnItem
    '''
pr = threadPool.submit(printH, blank=True)

# save workload into file then send it
saveStyle = 1
# 0 = Dont save
# 1 = Only save
# 2 = Save and send last
# 3 = Save and send all
domainHost = ""
domainPort = 0
domainUser = ""
domainPassword = ""
localPath = ""
minMinuteState = 10
minuteState = []
forceSaveStateData = False
areal = ""
saveInProgress = False
def saveStateData():
    global minuteState
    global minMinuteState
    global areal
    global saveStateAllowed
    global forceSaveStateData
    #if saveInProgress: return

    if saveStateAllowed or forceSaveStateData == True:
        forceSaveStateData = False

        if saveStyle == 0 or cableCount == 0: # Don't save
            #saveInProgress = False
            return
        print("Check1")
        #Check time
        dateTime = datetime.now()
        if dateTime.second >= 30:
            newTime = dateTime + timedelta(
                minutes=1,
                seconds=-dateTime.second,
                microseconds=-dateTime.microsecond)
        else:
            newTime = dateTime + timedelta(
                minutes=0,
                seconds=-dateTime.second,
                microseconds=-dateTime.microsecond)
        wPath = localPath + '/' + areal + str(dateTime.year) + '/' + str(dateTime.month).zfill(2) + '/' + str(dateTime.day).zfill(2) + '/'
        printH("Saving to local directory...", 0)
        try:
            #Check if file exists, 000000xxx + 1
            if not os.path.exists(wPath):
                os.makedirs(wPath)
            i = 0
            while os.path.exists(wPath + str(i).zfill(9) + ".wl"):
                i += 1
            dataPath = str(i).zfill(9) + ".wl"


            #Calculate minuteState
            completeState = [0] * len(CableItems)
            for index in range(len(CableItems)):
                if cableUpdateEnabled and cableUpdateAllowed and plc.plc_retry_success:
                    OFFscore = 0
                    STATscore = 0
                    MOVEscore = 0
                    for secondState in minuteState:
                        if secondState[index] == 0:
                            OFFscore += 1
                        elif secondState[index] == 1:
                            STATscore += 1
                        elif secondState[index] == 2:
                            MOVEscore += 1
                        else:
                            continue

                    if MOVEscore >= minMinuteState:
                        completeState[index] = 2
                    elif OFFscore < STATscore:
                        completeState[index] = 1
                    else:
                        completeState[index] = 0
                else:
                    completeState[index] = 0 #ERROR SIGNAL can be changed to 3
                    pass

            minuteState = [] #reset minute state


            #Write File
            with open(wPath + dataPath, 'a') as file:
                for index in range(len(CableItems)):
                    temp1 = window.t_label_2.text()[:-2]
                    temp2 = window.t_label_4.text()[:-2]
                    line = (
                        str(index) + ";" +
                        str(dateTime.date()) + " " + str(newTime.time().strftime("%H:%M:%S")) + ";" +
                        str(completeState[index]) + ";" +
                        temp1 + ";" +
                        temp2 + "\n")
                    file.write(line)
                    printH(line + "saved.", 2, dataPath)
        except Exception as err:
            printH("Could not save.", 100, str(err))
        else:
            printH("Success!", 100)

    if saveStyle == 1: # Only save
        #saveInProgress = False
        return

    #Connect to domain and send the file
    try:
        printH("Connecting to " + str(domainHost) + "...", 1)
        with ftplib.FTP(domainHost) as ftp:
            ftp.login(domainUser,domainPassword)

            '''transport = paramiko.Transport((domainHost,domainPort))
            transport.connect(username=domainUser, password=domainPassword)'''

            #sftp = paramiko.SFTPClient.from_transport(transport)
            printH("Success!", 2)

            completePath = []
            if areal != '':
                completePath.append(areal)
            completePath.append(str(dateTime.year).zfill(2) + '/')
            completePath.append(str(dateTime.month).zfill(2) + '/')
            completePath.append(str(dateTime.day).zfill(2) + '/')

            #Check if the dir exist and create if not
            for step in completePath:
                try:
                    ftp.cwd(step)
                    #sftp.stat(step)
                except:
                    ftp.mkd(step)
                    ftp.cwd(step)
                #sftp.chdir(step)

            printH("Sending to " + str(domainHost) + "...", 1, str(completePath))

            if saveStyle == 3:
                for filedir in os.listdir(wPath):
                    if filedir in ftp.nlst():
                        continue
                    file = open(wPath + filedir, 'rb')
                    ftp.storbinary("STOR " + filedir, file)
            else:
                file = open(wPath + dataPath, 'rb')
                ftp.storbinary("STOR " + dataPath, file)
                #sftp.put(localpath=wPath + dataPath, remotepath=dataPath)
                completePath.append(dataPath)
                printH(dataPath + " sent.", 2, str(completePath))
            #sftp.close()
            #transport.close()
    except Exception as err:
        if err.args[0] == 'size mismatch in put!  152 != 144':
            err = "The remote filesystem is full!"
        printH(
            "Process Failed! Couldn't send " + dataPath, 1, description=str(err))
    else:
        printH("Success!", 2)
    #saveInProgress = False
    return

def getBlankSpacing(space: int, string: str):
    if string.rfind("\n") == -1:
        lowestLine = string
    else:
        lowestLine = string[string.rfind("\n") + 1:]
    blank = " "*(space - len(lowestLine))
    return blank

### New VUZ experimental communication


class Communication():
    def __init__(self) -> None:
        self.IPList = [
            "0.0.0.0",          #None
            "192.168.11.21",    #PLC1
            socket.gethostbyname(socket.gethostname()), #PLC8 - Debug (This machine)
        ]
        self.plc_client = ModbusClient(timeout=5, auto_close=False, auto_open=True)
        self.readyToSend = False
        self.cancelConn = False

        self.status_word = [False]*8
        '''discrete_00-07\n
        [0] - cable0_ON\n
        [1] - cable0_MOV\n
        [2] - cable1_ON\n
        [3] - cable1_MOV\n
        [4] - cable2_ON\n
        [5] - cable2_MOV\n
        [6] - cable3_ON\n
        [7] - cable3_MOV\n
        '''
        self.rider_word = [False]*8
        '''register_01\n
        [0] - rider0_ON\n
        [1] - rider0_MOV\n
        [2] - rider1_ON\n
        [3] - rider1_MOV\n
        [4] - rider2_ON\n
        [5] - rider2_MOV\n
        [6] - rider3_ON\n
        [7] - rider3_MOV\n
        '''
        self.input_00 = 0
        '''tempAir'''
        self.input_01 = 1
        '''tempWater'''

        self.heather_01 = 1
        '''
        rider0_ON\n
        rider0_MOV\n
        rider1_ON\n
        rider1_MOV\n
        rider2_ON\n
        rider2_MOV\n
        rider3_ON\n
        rider3_MOV\n
        '''
        self.heather_02 = 2
        '''riderID'''
        self.register_00 = 3
        '''position(m)'''
        self.register_01 = 4
        '''speed(m/s)'''
        self.register_02 = 5
        '''alarm'''
        pass
    def connect(self, index=-1, blank=False):
        '''Connects either using Modbus'''
        global stopUpdate
        global cableUpdate
        if blank: return #blank is just a set up. If thread is already running, return

        self.cancelConn = False
        '''if index < 5:
            return True #Debug'''

        #window.updateSettings()
        if self.readyToSend:
            self.readyToSend = False
        try:
            self.plc_client.host(self.IPList[index])
        except:
            return False

        printH(string="Connecting to " + str(self.IPList[index]) + ":" + str(self.plc_client.port()))

        try:
            if not self.plc_client.open():  # Connection Fail
                # self.plc_server.host(self.IPList[index])
                if self.cancelConn:
                    self.cancelConn = False
                    # self.plc_server.close()
                    return False
                return False
            else:                           # Connection Success
                self.plc_client.host(self.IPList[index])
                if self.cancelConn:
                    self.cancelConn = False
                    return False
                LRLibrary.clientList["PLC"].set_highestAddress(20)
                self.readyToSend = True
                return True
        except:
            return False
    conThread = threadPool.submit(connect, blank=True)
    def connectionLost(self):
        global stopUpdate

        self.readyToSend = False
        stopUpdate = True
        self.disconnect()

        printH("Connection Lost.")
        pass
    """def testConnection(self):
        '''Tries to connect ten times. If fails, connection is lost'''
        # if com.comForm == "Modbus":
        i = 0

        while not self.plc_client.open() and i < 10:
            sleep(0.1)
            i += 1
        if i >= 10:
            return False

        return True"""
    def disconnect(self):
        global stopUpdate
        self.cancelConn = True
        self.readyToSend = False
        stopUpdate = True
        while cableUpdate.running():
            continue
        if self.plc_client.is_open():
            self.plc_client.close()
        return True

com = Communication()

forceCableUpdate = False
cableUpdateProceed = False
cableUpdateInterrupt = False
cableUpdateEnabled = False
cableUpdateAllowed = False
lastUpdate = None
updateInProgress = False
def updateValues(blank=False):
    '''The update loop. Will repeat until stopUpdate is set to True\n
    Only in ThreadPool!'''
    global stopUpdate
    global valuesUpdated
    global cableUpdate
    global cableUpdate
    global autoUpdate_Interval
    global cableUpdateProceed
    global saveStateAllowed
    global cableCount
    global cableUpdateInterrupt
    global forceCableUpdate
    global updateInProgress
    global minuteState
    global ssdt
    if blank: return #blank is just a set up. If thread is already running, return
    SM.getValues()

    #LRLibrary.UpdateLibrary() # strange critical failure
    cableUpdateInterrupt = False

    printH("CableUpdate:", 0 , "Online")
    # Get first values
    '''statV = LRLibrary.getRegisters("PLC", "DINP", 0, 8)
    riderV = LRLibrary.getRegisters("PLC", "DINP", 8, 7)
    tempV = LRLibrary.getRegisters("PLC", "IREG", 1, 2)
    cableV = LRLibrary.getRegisters("PLC", "HREG", 0, cableCount*3)'''
    '''printH("Hit: \n" +
           "HREG: " + str(LRLibrary.clientList["PLC"]._localHoldingRegisters) + "\n" +
           "IREG: " + str(LRLibrary.clientList["PLC"]._localInputRegisters) + "\n" +
           "DINP: " + str(LRLibrary.clientList["PLC"]._localDiscreteInputs) + "\n" +
           "COIL: " + str(LRLibrary.clientList["PLC"]._localCoils)
           )'''
    '''if not LRLibrary.clientList["PLC"].get_client().is_open():
        LRLibrary.clientList["PLC"].get_client().open()
    statV = LRLibrary.clientList["PLC"].get_client().read_discrete_inputs(0, 8)
    tempV = LRLibrary.clientList["PLC"].get_client().read_input_registers(1, 2)
    riderV = LRLibrary.clientList["PLC"].get_client().read_discrete_inputs(8, 7)
    if not plc.plc_stateOnly:
        cableV = LRLibrary.clientList["PLC"].get_client().read_holding_registers(5, 9)
    else:
        cableV = [2, 0]'''
    response = plc.PLC_Response()
    for i in range(cableCount):
        #cableV = [2, i]
        response[0] = 2
        response[1] = i
        plc.PLC_Decipher(response=response)
    printH("response:", 1 , str(response))
    printH("quidoInputs:", 2 , str(quidoInputs))

        #printH("cableV:", 1 , str(cableV))
        #printH("riderV:", 1 , str(riderV))
    #printH("statV:", 1 , str(statV))
    #printH("tempV:", 1 , str(tempV))


    # Setup updater values
    useDebugValues = False
    stopUpdate = False
    '''statVLast = statV
    riderVLast = riderV
    tempVLast = tempV
    cableVLast = cableV'''
    lastTime = 0
    atpw = [0]*20

    sleep(0.1)
    printH("CableUpdate: Waiting for new minute...", 0)
    #synchronize to a minute
    while datetime.now().time().second != 0 and not ssdt.running() and not stopUpdate:
        if forceCableUpdate or not cableUpdateEnabled: break
        window.updateLabelCounter(window.l_plcInterval, str((timedelta(minutes=1) - timedelta(seconds=datetime.now().time().second)).seconds).zfill(2), 'minute sync')
        sleep(1)
    window.updateLabelCounter(window.l_plcInterval, str(0).zfill(2))
    if not cableUpdateEnabled and not forceCableUpdate: return
    window.dsb_plcInterval.setEnabled(False)
    #window.tabWidget_2.setTabEnabled(1, False)
    backupInterval = autoUpdate_Interval

    printH("CableUpdate: Start!", 0)
    while ssdt.running():
        saveStateAllowed = False
    saveStateAllowed = True

    ssdt = threadPool.submit(saveStateDataTimer)
    try:
        # Start main loop
        while (cableUpdateEnabled and cableUpdateAllowed and not stopUpdate) or forceCableUpdate:
            currentTime = datetime(
                datetime.now().year,
                datetime.now().month,
                datetime.now().day,
                hour=datetime.now().time().hour,
                minute=datetime.now().time().minute,
                second=datetime.now().time().second,
                microsecond=0)
            nextTime = (currentTime + timedelta(seconds=int(autoUpdate_Interval)))
            # test connection
            valuesUpdated = False
            t = 0
            while not LRLibrary.UpdateLibrary() and t < 3:
                t +=1
                sleep(0.1)
            if t >= 3:
                threadPool.submit(com.connectionLost)
                break
            #com.plc_client.close()

            start_time = time()
            response = plc.PLC_Response()
            if response is False: continue

            printH("CableUpdate:", 0)
            for i in range(cableCount):
                #cableV = [2, i]
                response[0] = 2
                response[1] = i
                plc.PLC_Decipher(response=response)
            printH("response:", 1 , str(response))
            printH("quidoInputs:", 2 , str(quidoInputs))
            # Update values
            '''statV = LRLibrary.getRegisters("PLC", "DINP", 0, 8)
            tempV = LRLibrary.getRegisters("PLC", "IREG", 1, 2)
            riderV = LRLibrary.getRegisters("PLC", "DINP", 8, 7)
            cableV = LRLibrary.getRegisters("PLC", "HREG", 5, 9)'''
            '''if not LRLibrary.clientList["PLC"].get_client().is_open():
                LRLibrary.clientList["PLC"].get_client().open()
            statV = LRLibrary.clientList["PLC"].get_client().read_discrete_inputs(0, 8)
            tempV = LRLibrary.clientList["PLC"].get_client().read_input_registers(1, 2)
            riderV = LRLibrary.clientList["PLC"].get_client().read_discrete_inputs(8, 7)
            if not plc.plc_stateOnly:
                cableV = LRLibrary.clientList["PLC"].get_client().read_holding_registers(5, 9)
            else:
                cableV = [2, 0]

            if (statV, riderV, tempV, cableV) != (statVLast, riderVLast, tempVLast, cableVLast) or plc.debug:
                Watcher2 = time()
                start_time = time()
                if statV is None or riderV is None or tempV is None or cableV is None:
                    printH("Failure to read Values.", description=str((statV, riderV, tempV, cableV)))
                    com.status_word = LRLibrary.wordToList(LRLibrary.registerToWord(statV, length=len(com.status_word)))
                else:
                    printH("CableUpdate:", 0)
                    for i in range(cableCount):
                        cableV = [2, i]
                        plc.PLC_Decipher(response=wrap_Response(statV, tempV, cableV))

                        #printH("cableV:", 1 , str(cableV))
                        #printH("riderV:", 1 , str(riderV))
                    printH("statV:", 1 , str(statV))
                    printH("tempV:", 1 , str(tempV))
                Watcher2 = time() - Watcher2'''

                #printH("Completed in " + str(time() - start_time)[:5] + "s", 1)

            '''statVLast = statV
            riderVLast = riderV
            tempVLast = tempV
            cableVLast = cableV'''
            valuesUpdated = True #Flag for something

            if time() - start_time > autoUpdate_Interval:
                print("Delay Check: Enter")
                printH("MasterAPP cannot keep up! Reducing update rate by 1s.", 1, str(time() - start_time)[:5] + " > " + str(autoUpdate_Interval))
                sleep(0.1)
                #window.dsb_plcInterval.setValue(float(window.dsb_plcInterval.value() + 1))
                autoUpdate_Interval = window.dsb_plcInterval.value() + 1
                print("Delay Check: Exit")
            forceCableUpdate = False

            state = []
            for i in range(len(CableItems)): # stores state of every update
                if str(CableDictionary[i]["CS"]).isnumeric():
                    state.append(int(CableDictionary[i]["CS"]))
                else:
                    state.append(3)

            minuteState[currentTime.second] = state

            currentTime = datetime.now()

            updateInProgress = False
            print("Wait: Enter")
            while currentTime < nextTime or saveInProgress:
                newLabelTime = str((nextTime - timedelta(seconds=datetime.now().time().second)).second).zfill(2)
                if window.l_plcInterval.text() != newLabelTime:
                    window.updateLabelCounter(window.l_plcInterval, newLabelTime)
                    sleep(1)
                currentTime = datetime.now()
                if currentTime.time().hour == 0 and currentTime.time().minute == 0:
                    window.StopButton(True)
                    break
                if forceCableUpdate or not cableUpdateEnabled: break
            updateInProgress = True
            window.updateLabelCounter(window.l_plcInterval, str(0).zfill(2))
            print("Wait: Exit")


            atpw.append((time() - start_time) + LRLibrary.readTime + LRLibrary.writeTime)
            atpw.pop(0)
            processingTime = numpy.average(atpw)

            delay = max(0, plc.plc_requestInterval - processingTime)
            print(delay + processingTime , "("+ str(processingTime) +")")

            #sleep(delay)
    except Exception as err:
        printH(str(err))
        pass
    if (cableUpdateEnabled and cableUpdateAllowed):
        cableUpdate = threadPool.submit(updateValues)
        printH("Cable Update restarted.", 0)
    else:
        printH("Cable Update terminated.", 0)
        stopUpdate = False
        LRLibrary.clientList["PLC"].get_client().close()
cableUpdate = threadPool.submit(updateValues, blank=True)

def wrap_Response(statV:list, tempV:list, cableV:list, readResponse=True):
    '''
    Holding registers:
        4 - Status Word (Message indication)
        6..8 - Request Values
        8..13 - Response Values
    Discrete inputs:
        0 - Cable0 ON/OFF
        1 - Cable0 Moving/Stationary
        2..n - CableN
    Input Registers:
        1 - Water Temperature
        2 - Air Temperature
    '''

    if not plc.plc_stateOnly:
        message = format(plc_server.read_holding_registers(4, 1)[0], '04b')
        if not int(message[5]):  #Return False if PLC has no message
            return False
        if not readResponse:  #Check if PLC has message
            return True
        if not not int(message[5]):  #Return False if PLC sends error message
            return False

    #statV = statV.copy() #Quido discrete inputs
    temp = [0, 0]
    if tempV is None:
        temp[0] = window.t_label_2.text()[:-2]
        temp[1] = window.t_label_4.text()[:-2]
    else:
        temp[0] = "{:.1f}".format(tempV[0] / 10)
        temp[1] = "{:.1f}".format(tempV[1] / 10)
    if statV is None:
        statV = [False]*quidoMaxInput
    quidoInputs.clear()
    i = 0
    while i < quidoMaxInput:
        quidoInputs.append([statV[i], statV[i + 1]])
        i += 2

    if cableV is None:
        words = [0]*7
        words[0] = 2
    else:
        words = cableV  #read all Actual Values

    action = words[0]
    index = words[1]
    item = temp
    item.extend(words[3:])

    while item[-1] == 0 and item[-1] is not item[0]:
        item.pop()

    response = [action, index]
    response.extend(item)

    #plc_server.write_multiple_registers(5, [0]*9)   #clear Databank(Message read)

    #reading = False
    return response


# Call start on first launch

if __name__ == "__main__":
    mainWindow.show()
    window.StartPart1()
    mainWindow.show()
    app.aboutToQuit.connect(window.StopButton)
    sys.exit(app.exec_())