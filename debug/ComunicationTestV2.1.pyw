# ToDo
# X: shared cableList
# X: send reserve for selected cable

# 1: simulate boat movement
# 2: random errors
# 5:  #


# from time import sleep
from concurrent.futures import ThreadPoolExecutor, thread
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets
from pyModbusTCP.server import ModbusServer, DataBank
from pyModbusTCP.client import ModbusClient
import sys, time, random, tools, threading, string, socket
from http.server import HTTPServer, BaseHTTPRequestHandler

from debug.API_debugConsole import Ui_API_debugConsole
from debug.PLC_debugConsole import Ui_PLC_debugConsole

cableList = []
class API_Listener(BaseHTTPRequestHandler): #handler žádostí keepalive
    def do_GET(self): #Odpověď na GET
        pathDict = getDictionaryfromUrl(self.path)
        time.sleep(0.1)
        print(self.server.server_address, "recieved:")
        '''for key in pathDict:
            print ("    " + key + "=" + pathDict[key])'''
        if pathDict["type"] == "app":
            if "action" in pathDict.keys():
                action = int(pathDict["action"])
            if "index" in pathDict.keys():
                index = int(pathDict["index"])
            if "item" in pathDict.keys():
                item = int(pathDict["item"])
        api.request = [action, index, item]

        api.api_response(self, api.request)

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

# API
class MainWindow(Ui_API_debugConsole):
    def __init__(self, window) -> None:
        self.setupUi(window)
        self.response = ""
        self.request = []

        self.cableList = cableList
        self.api_host = socket.gethostbyname(socket.gethostname())
        self.api_port = 1000

        # MasterApp listener thread
        '''self.MasterApp_listener = threading.Thread(target=self.API_Listener)
        self.MasterApp_listener_Listening = True
        self.MasterApp_listener.start()'''

        self.listWidget.itemActivated.connect(self.listWidgetOptions)
        self.api_server = HTTPServer((self.api_host, self.api_port), API_Listener)
        pass

    def API_ServeForever(self):
        self.api_server.serve_forever()

    # Thread only! switched on by self.MasterApp_listener
    '''def API_Listener(self):
        while True:
            time.sleep(0.5)
            # If listener is allowed to listen and
            # channel 0 has incoming message
            if DataBank.get_bits(0, 1)[0] and DataBank.get_bits(2, 1)[0]:
                # If listener is allowed to listen and channel 1 has incoming message
                try:
                    response = DataBank.get_words(1, DataBank.get_words(0, 1)[0])
                    DataBank.set_bits(0, [0])  # Request Recieved
                    DataBank.set_bits(2, [0])  # Request Recieved
                    DataBank.set_words(0, 300*[0])  # Clear the databank

                    self.api_response(response)
                except:
                    self.MasterApp_listener_Listening = True'''

    # simulates API response
    def api_response(self, listener: API_Listener = None, request: list = []):
        # request = str(self.listWidget.selectedIndexes()[0].row())
        # Action - Do this
        # index - Over Here
        # Response_item - With this

        self.MasterApp_listener_Listening = False
        err = (False, '')
        if not isinstance(request, list) or request == '' or request == 'ERR':
            err = (True, '')
            self.MasterAPP_listener_Listening = True
            return

        actionIndex = request[0]                            # Decides what to do
        cableIndex = request[1]                             # Decides on which cable
        request_item = request[2]                           # Decides with what to work with

        if actionIndex != 8 and cableIndex > len(self.cableList) - 1:
            err = (True, "ZEROCABLES")

        # MasterAPP communication
        if actionIndex == 0: # "Idle"
            time.sleep(0.1)
            if self.response == "":
                self.response = 'idle'
                err = (False, '')
        elif actionIndex == 1:  # "Reservation Confirmed"
            if request_item == 1:
                cableName = self.listWidget_2.item(cableIndex).text()  # Debug name
                self.listWidget_2.item(cableIndex).setText("#" + cableName)
            self.MasterApp_listener_Listening = True  # Start Listening on channel 0
            return
        elif actionIndex == 2:  # "Cancelation Confirmed"
            if request_item == 1:
                cableName = self.listWidget_2.item(cableIndex).text()  # Debug name
                self.listWidget_2.item(cableIndex).setText(cableName[1:])
            self.MasterApp_listener_Listening = True  # Start Listening on channel 0
            return
        elif actionIndex == 3:  # "Confirm RFID":
            response_item = 0
            '''if request_item != "9":
                response_item = request_item
            else:'''
            for i in range(self.listWidget.count() - 1):
                if request_item[0] == self.listWidget_3.item(i).text():
                    response_item = 1
                    break
            self.response = [
                3,  # Action - CornfirmRFID
                cableIndex,  # index 0 - n
                response_item  # Response_item 0/1
            ]
            pass
        elif actionIndex == 4:  # "Send Rider info":
            response_item = 0
            self.response = [
                4,  # Action - CornfirmRFID
                cableIndex,
            ]
            if self.cableList[cableIndex]["IDR"] == '0':
                self.response.append(0)
            else:
                self.response.append(str(self.cableList[cableIndex]["IDR"])) # Rider ID
            pass
        elif actionIndex == 8:  # "Test"
            self.response = [x+1 for x in request]
        else:
            self.response = ''
        if self.response == '' or self.response == 'EMPTY':
            err = (True, "NOT-OK")

        self.sendMessage(self.response, err, listener)

        self.MasterApp_listener_Listening = True  # Start Listening on channel 0

    def listWidgetOptions(self):
        if len(self.listWidget_2.selectedIndexes()) == 0:
            return

        cableIndex = self.listWidget_2.selectedIndexes()[0].row()
        if self.listWidget.selectedIndexes()[0].row() == 0:
            newRider = tools.rnd_string(4, string.ascii_uppercase + string.digits)
            self.response = [
                1,  # Action - NewReservation
                cableIndex,  # index 0 - n
                newRider  # Response_item - RiderID
            ]
            cableList[cableIndex]["RS"] = "1"
            cableList[cableIndex]["IDR"] = newRider

        elif self.listWidget.selectedIndexes()[0].row() == 1:
            self.response = [
                2,  # Action - ReservationCanceled
                cableIndex,  # index 0 - n
                0  # Response_item - None
            ]

            cableList[cableIndex]["RS"] = "0"
            cableList[cableIndex]["IDR"] = "0"
            '''sendMessage(response)
            DataBank.set_bits(0, [1])       # Let channel 0 know there is a message
            DataBank.set_bits(2, [0])       # message for MasterAPP'''

    def updateDataBank(self):
        self.label_5.setText("Request: " + str(api.request))
        self.label_4.setText("Response: " + str(api.response))
        #self.label_3.setText("Message:" + str(DataBank.get_words(1, DataBank.get_words(0, 1)[0])))

    def sendMessage(self, response: list, error, listener: API_Listener):
        if error[0]:
            listener.send_response_only(500, error[1])
            listener.end_headers()
        elif response == "idle":
            listener.send_response_only(200, "OK")
            listener.end_headers()
        else:
            listener.send_response_only(200, "MESSAGE")
            listener.send_header("action", response[0])
            listener.send_header("index", response[1])
            listener.send_header("item", response[2])
            listener.end_headers()
        self.response = ""


# shows API console
def show_API_Console(b=True):
    if b:
        apiWindow.show()
    else:
        apiWindow.hide()


app = QtWidgets.QApplication(sys.argv)
apiWindow = QtWidgets.QWidget()
apiWindow.setGeometry(1200, 130, 500, 400)
api = MainWindow(apiWindow)
threading.Thread(target=api.API_ServeForever).start()

# PLC
class MainWindow(Ui_PLC_debugConsole):
    def __init__(self, window) -> None:
        self.setupUi(window)

        self.cablecount = 0
        self.cableList = cableList

        self.listWidget.itemActivated.connect(self.listWidgetOptions)

        self.plc_server = ModbusServer(host=socket.gethostbyname(socket.gethostname()), port=502, no_block=True)
        self.stateOnly = True
        self.MasterApp_listener_switch = True  # MasterApp listener switch
        self.MasterAPP_listener_Listening = True
        self.MasterApp_listener = threadpool.submit(self.PLC_Listener)  # MasterApp listener thread
        pass

    def PLC_Listener(self):  # Thread only! switched on by self.MasterApp_listener
        if not self.stateOnly:
            while True:
                time.sleep(0.1)
                if self.MasterAPP_listener_Listening and DataBank.get_words(1, 1)[0]:
                    # If listener is allowed to listen and channel 1 has incoming message
                    try:
                        #DataBank.set_words(1, [DataBank.get_words(1, 1)[0] + 1]*100)
                        #DataBank.set_words(101, [0])
                        DataBank.set_words(1, [0])
                        words = DataBank.get_words(5, 3)
                        self.plc_response(requestWords=words)
                    except:
                        continue
        else: # Quido version
            while True:
                time.sleep(1)
                Quido.open()
                if self.MasterAPP_listener_Listening and Quido.read_holding_registers(0, 6)[5]:
                    # If listener is allowed to listen and channel 1 has incoming message
                    try:
                        Quido.write_multiple_registers(1, [0])
                        words = Quido.read_holding_registers(5, 3)
                        self.plc_response(requestWords=words)
                    except:
                        continue

    # Generates a new
    def generateCable(self, blank=False):
        cableDictionary = {"CS": "0", "RS": "0", "IDR": "0", "Position": "0", "Speed": "0", "Error": "0000"}

        if not blank:
            cableDictionary["CS"] = str(random.randrange(0, 4))
            cableDictionary["RS"] = str(random.randrange(0, 2))
            if cableDictionary["RS"] == "1":
                cableDictionary["IDR"] = tools.rnd_string(4, string.ascii_uppercase + string.digits)
            cableDictionary["Position"] = str(random.randrange(0, 100))
            cableDictionary["Speed"] = str(random.randrange(0, 50))
            cableDictionary["Error"] = tools.rnd_string(4, string.digits)
        self.cableList.append(cableDictionary)
        item = QtWidgets.QListWidgetItem()
        item.setText("Cable" + str(len(self.cableList) - 1))
        self.listWidget_2.addItem(item)

        item = QtWidgets.QListWidgetItem()
        if cableDictionary["RS"] == "1":
            item.setText("#Cable" + str(len(self.cableList) - 1))
        else:
            item.setText("Cable" + str(len(self.cableList) - 1))
        api.listWidget_2.addItem(item)
        self.cablecount += 1

    # simulates PLC response
    def plc_response(self, requestWords = None):

        self.MasterApp_listener_Listening = False
        # Action - Do this
        # index - Over Here
        # Response_item - With this

        words = [requestWords[0], requestWords[1], requestWords[2]]
        action = format(requestWords[0], "04b")     #[100] - bit array, decide what to do
        index = requestWords[1]                     # Decides on which cable
        item = requestWords[2]                      # Decides with what to work with

        if not not int(action[3]):          # SendCableCount
            words.append(self.cablecount) #words[3]
            pass
        elif not not int(action[2]):       # SendCable
            if self.cablecount > index:
                words.extend(   #words[3, 4, 5, 6]
                    [
                    int(self.cableList[index]["CS"]),       # CableState
                    int(self.cableList[index]["Position"]), # Position
                    int(self.cableList[index]["Speed"]),    # Speed
                    int(self.cableList[index]["Error"])     # Error
                    ])
            else: # error
                words.extend(   #words[3, 4, 5, 6]
                    [
                    0,          # CableState
                    0,          # Position
                    0,          # Speed
                    404,        # Error
                    ])
            pass
        elif not not int(action[1]):         # AllowAccess
            if item == 1:
                cableName = self.listWidget_2.item(index).text()  # Debug name
                self.listWidget_2.item(index).setText("#" + cableName)
            else:
                cableName = self.listWidget_2.item(index).text()  # Debug name
                self.listWidget_2.item(index).setText(cableName[1:])
            pass
        elif not not int(action[0]):           # Test 888 -> 999
            words.append(requestWords[0] + 1)
            words.append(requestWords[1] + 1)
            words.append(requestWords[2] + 1)
        else:
            sendMessage(None, None, True)
            self.MasterAPP_listener_Listening = True
            return
        '''if response == '' or response == 'EMPTY':
            self.MasterAPP_listener_Listening = True
            return''' #Probably unnecessary

        sendMessage(words=words)

        self.MasterAPP_listener_Listening = True

    def listWidgetOptions(self):
        if self.listWidget.selectedIndexes()[0].row() == 0:
            self.generateCable()
        elif self.listWidget.selectedIndexes()[0].row() == 1:
            self.generateCable(True)
        '''elif self.listWidget.selectedIndexes()[0].row() == 2:
            self.plc_response(self, "610", debug=True)'''

    def updateDataBank(self):
        self.label_5.setText("ControlWord: " + format(DataBank.get_words(1, 1)[0], 'b') + " / StatusWord: " + format(DataBank.get_words(4, 1)[0], 'b'))
        self.label_4.setText("ResponseWords: " + str(DataBank.get_words(5, 7)))
        #self.label_3.setText("Message:" + str(DataBank.get_words(1, DataBank.get_words(0, 1)[0])))


# shows PLC console
def show_PLC_Console(b=True):
    if b:
        plcWindow.show()
    else:
        plcWindow.hide()

def sendMessage(response: list = None, words=None, error=False):
    if plc.stateOnly:
        Quido.open()
        if response is not None:
            message = response
            if error:
                message = list("E".encode())
            message.insert(0, int(len(response)))
            Quido.write_multiple_registers(0, message) # Save response into Quido for MasterApp pickup
        elif words is not None:
            if error:
                Quido.write_multiple_registers(4, [2])
            else:
                Quido.write_multiple_registers(5, words)
                Quido.write_multiple_registers(1, [0])
                Quido.write_multiple_registers(4, [1])
        Quido.close()
    else:
        if response is not None:
            message = response
            if error:
                message = list("E".encode())
            message.insert(0, int(len(response)))
            DataBank.set_words(0, message)  # Save response into databank for MasterApp pickup
        elif words is not None:
            if error:
                DataBank.set_words(4, [2])
            else:
                DataBank.set_words(5, words)
                DataBank.set_words(1, [0])
                DataBank.set_words(4, [1])

def cableSimulation():
    # CS:
    #   0 - STATIONARY
    #   1 - MOVING
    #   2 - ERR/UNKNOWN
    #   3 - OFFLINE
    # RS:
    #   0 - EMPTY
    #   1 - BOARDED
    # #

    while True:
        time.sleep(50)
        for i, cableDict in enumerate(cableList):
            if cableDict["RS"] == "1":
                newCableDict = cableDict.copy()

                newCableDict["CS"] = str(random.randrange(0, 4))
                newCableDict["Position"] = str(random.randrange(0, 100))
                newCableDict["Speed"] = str(random.randrange(0, 50))
                newCableDict["Error"] = tools.rnd_string(4, string.digits)

                threadpool.submit(cableUpdateDelay, i, newCableDict)

def cableUpdateDelay(index, newCableDict):
    global cableList
    time.sleep(random.randrange(5, 15))
    cableList[index] = newCableDict


threadpool = ThreadPoolExecutor(5)
threadpool.submit(cableSimulation)

plcWindow = QtWidgets.QWidget()
plcWindow.setGeometry(1200, 570, 500, 400,)
plc = MainWindow(plcWindow)
#plc.plc_server.start()
timer = QTimer()
timer.timeout.connect(plc.updateDataBank)
timer.timeout.connect(api.updateDataBank)
timer.start(500)

Quido = ModbusClient("192.168.0.186", 502)

show_API_Console()
show_PLC_Console()

sys.exit(app.exec_())
