
# Bugs:
# Sometimes the background disappears and defaults into white background.
# Retry change crashed once

# To do:
# Fix graph


from ui.MasterAPPV4 import Ui_MasterAPP
from ui.NewDomain import Ui_EnterNewDomain
import ui.Images_rc  #Important! Do not delete.
from pyModbusTCP.client import ModbusClient
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread
from tkinter import messagebox
from http.server import HTTPServer, BaseHTTPRequestHandler
from http.client import HTTPConnection
import sys, time, threading, datetime, socket, os, tkinter
import ftplib
from configparser import ConfigParser
from cryptography.fernet import Fernet
from tkinter import filedialog
from concurrent.futures import ThreadPoolExecutor
from pyqtgraph import PlotWidget
import random


# Periodically calls deciphers if there is change in api/plc response
# Can only be used by the main thread due to addCableItem()
class ToMainThread(QThread): # class Has to be defined. Cannot be empty '()'
    # Signals and slots:
    # A way to pass variables between Classes and into the main thread
    api_decypher = QtCore.pyqtSignal(bool) # this is Signal
    plc_decypher = QtCore.pyqtSignal(bool)
    w_addCable = QtCore.pyqtSignal(bool)
    updateGraphs = QtCore.pyqtSignal(bool)
    setupGraphs = QtCore.pyqtSignal(int)
    clearText = QtCore.pyqtSignal(bool)
    pH = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None, index=0, item=0):
        super(ToMainThread, self).__init__(parent)
        self.index = index
        self.item = item
        self.is_running = True
    def run(self):
        if self.index == 0:
            #print("ToMainThread - Decypher Executed")  #! PLC and API both fire ToMainThread! Possibility of deciphers firing twice!
            while True:
                if api.api_recieved:
                    self.api_decypher.emit(True) # this is emitting the signal with a variable
                    time.sleep(0.01) # Wait for the signal to process
                    api.api_recieved = False
                if plc.plc_recieved:
                    self.plc_decypher.emit(True)
                    time.sleep(0.01) # Wait for the signal to process
                    plc.plc_recieved = False
                time.sleep(0.1)
        elif self.index == 1:
            #print("ToMainThread - addCable Executed", self.index)
            self.w_addCable.emit(True)
        elif self.index == 2:
            #print("ToMainThread - updateGraphs Executed", self.index)
            self.updateGraphs.emit(self.item)
        elif self.index == 3:
            #print("ToMainThread - setupGraphs Executed", self.index)
            self.setupGraphs.emit(self.item)
        elif self.index == 4:
            print("ToMainThread - setupGraphs Executed", self.index)
            self.clearText.emit(self.item)
        elif self.index == 5:
            #print("ToMainThread - printHistory Executed", self.index)
            self.pH.emit(True)
        #self.stop()

    def stop(self):
        print("ToMainThread - Exited")
        self.is_running = False
        self.terminate()

class Worker(QThread):  # Thread Handler
    def __init__(self, parent=None, thread=""):
        super(Worker, self).__init__(parent)
        self.threadName = thread
        self.is_running = True

    def run(self):
        if self.threadName == 'retry':
            Retry()                 # One shot
            self.is_running = False
            pass
        elif self.threadName == 'loopretry':
            loop_Retry()            # Loop
            self.is_running = False
            pass
        elif self.threadName == 'API':
            api.API_Listener()      # Loop
            self.is_running = False
            pass
        elif self.threadName == 'PLC':
            plc.PLC_Listener()      # Loop
            self.is_running = False
            pass
        elif self.threadName == 'AX':
            ax.AX_Listener()        # Loop
            self.is_running = False
            pass
        elif self.threadName == 'AXserve':
            ax.AX_ServeForever()    # Loop
            self.is_running = False
            pass
        elif self.threadName == 'update':
            update_CableItems()     # Loop
            self.is_running = False
            pass

    def stop(self):
        print("Worker - Exited")
        self.is_running = False
        self.terminate()

class AXHandler(BaseHTTPRequestHandler):  # handler žádostí
    def do_POST(self):  # Odpověď na GET
        pass

    def do_GET(self):  # Odpověď na GET
        keepAlive = True

        pathDict = getDictionaryfromUrl(self.path)
        time.sleep(0.1)
        print("received:")
        for key in pathDict:
            print("    " + key + "=" + str(pathDict[key]))
        ax.AX_Decypher(self, pathDict, keepAlive)

class NewDomainDialog(Ui_EnterNewDomain):
    def __init__(self, dialog) -> None:
        self.setupUi(dialog)

class API_Client():
    def __init__(self) -> None:
        self.api_recieved = False
        self.api_client_allowed = True
        self.api_port = 1000
        self.api_host = socket.gethostbyname(socket.gethostname())
        self.api_listener = QThread()
        self.api_listener_Allowed = False
        self.api_retry_success = False
        self.api_requestInterval = 0.1
        self.api_idleInterval = 100  # 300 * 0.1s = 30s
        self.api_idleInterval = 30

    # API listener Thread
    def API_Listener_Start(self): #deactivated
        global api_server
        if self.api_retry_success:
            return True
        self.api_retry_success = False

        printH("API client", 2)
        time.sleep(0.1)
        printH("Connecting to Host...", 3, str(self.api_host) + ":" + str(self.api_port) + " <---- MasterAPP")
        try:
            if not os.system("ping -c 1" + self.api_host):
                raise Exception("Address")
        except:
            printH(
                    "An error occurred while connecting to" + str(self.api_host) + ":" + str(self.api_port) +
                    "\nMost likely case is that this address is" + "invalid or otherwise could not be used.",
                    4, "Unsupported address:" + str(self.api_host))
            return self.api_retry_success
        '''try:
            api_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            api_socket.settimeout(20.0)
            api_socket.connect((self.api_host, self.api_port))
        except:
            printH(
                "An error occurred while connecting to\n" +
                str(self.api_host) + ":" + str(self.api_port) + "\n" +
                "Most likely case is that port on this\n" +
                "address is either not binded or in use\n" +
                "by another instance of MasterAPP or\n" +
                "other application.",
                4, str(self.api_host) + ":" + str(self.api_port) + " Unavailable", isRootEnd=True)
            return self.api_retry_success

        api_socket.close()
        api_server.host(self.api_host)
        api_server.port(self.api_port)'''
        api_server = HTTPConnection(self.api_host, self.api_port)  # Instance of http connection with server

        printH("Success!", 4, str(self.api_host) + ":" + str(self.api_port) + " <---> MasterAPP")

        time.sleep(0.1)

        printH("Connecting to API...", 3, "API <---- " + str(self.api_host) + ":" + str(self.api_port))
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

        printH("Success!", 4, "API <---> " + str(self.api_host) + ":" + str(self.api_port))
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
            if stopClients or not self.api_client_allowed:
                printH("Connection with " + str(self.api_host) + " interrupted\nAPI-Listener Offline", 0, "API <-X-> MasterAPP", isRootEnd=True)
                api_server.close()
                self.plc_retry_success = False
                break

            time.sleep(self.api_requestInterval)

            if api_server_online == 0: # incase of connection loss
                printH(
                    "Connection lost with API\n" +
                    "Testing connection", 0, "API --X-> MasterAPP")
                if testConnection("api") is True:
                    printH("Test Success", 1, "API ----> MasterAPP", True)
                else:
                    printH("Test Failed", 1, "API --X-> MasterAPP", True)
                    printH("Connection lost with " + str(self.api_host) + " \nAPI-Listener Offline", 0, "API <-X-> MasterAPP", isRootEnd=True)
                    self.api_listener_Allowed = False
                    self.api_retry_success = False
                    if autoRetry_allowed:
                        plc.plc_listener_Allowed = False
                        plc.plc_retry_success = False
                        retry = threadPool.submit(Retry) #! Possible Error!
                    break

            if self.api_listener_Allowed: # Expecting a message. Switched by API_Caller()
                time.sleep(0.1) #change?
                success, reason = self.API_Response()  #returns (bool, reason/exception)
                self.api_listener_Allowed = False
                if success:
                    if reason == "MESSAGE":
                        printH("Response received:", 0, "API ----> MasterAPP")
                        self.api_recieved = True
                        idleInterval = -10
                        time.sleep(0.1) #?
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
                        "Another attempt in " + str(self.api_requestInterval) + "s", 0, reason)
                    api_server_online -= 1
            elif idleInterval >= self.api_idleInterval:
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
                "Failed to send request", 2, reason, True)
            time.sleep(self.api_requestInterval)
            return False
        else:
            time.sleep(0.2)
            #response = self.API_Response()
            self.api_listener_Allowed = res
            return True

    # Decyphers the response of API
    def API_Decypher(self, handler: AXHandler = None):
        global cableUpdateProceed

        self.api_recieved = False
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
                    "Received a request cancelation for Cable" + str(index) + "\n " +
                    "Request accepted", 2, str(response) + " -> ACCEPTED")
                dictionary["RS"] = "0"  # RiderState 0 = Rider Empty
                dictionary["IDR"] = "####"
                self.API_Caller("Reservation", index, "1")
            elif CableDictionary[index]["RS"] == "2":
                if CableDictionary[index]["CS"] == "0":
                    printH(
                        "Received a request cancelation for Cable" + str(index) + "\n " +
                        "Request accepted", 2, str(response) + " -> ACCEPTED")
                    self.API_Caller("Reservation", index, "1")
                    dictionary["RS"] = "0"  # RiderState 0 = Rider Empty
                    dictionary["IDR"] = "####"
                else:
                    printH(
                        "Received a request cancelation for Cable" + str(index) + "\n " +
                        "Request refused as Cable" + str(index) + " is not stationary", 2, str(response) + " -> DENIED")
                    self.API_Caller("Reservation", index, "0")
            else:
                printH(
                    "Received a request cancelation for Cable" + str(index) + "\n " +
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
        elif action == 5:     # Received RFID flomAX
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
            window.add_CableItem()
            index = len(CableItems) - 1
        import_CableItemInfo(index, dictionary)

        cableUpdateProceed = True

    # Sends a request to API
    def API_Request(self, request = None):
        global writing
        try:
            while True:
                while writing:  # Queue
                    time.sleep(0.1)
                writing = True

                time.sleep(0.1)  # Wait for listener to be done with listening
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
                time.sleep(0.1)
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

class PLC_Client(): # slot has to be in undefined class
    def __init__(self):
        self.plc_recieved = False
        self.plc_client_allowed = True
        self.plc_port = 502
        self.plc_host = socket.gethostbyname(socket.gethostname())
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
        time.sleep(0.1)
        printH("Connecting to Address...", 3, "MasterAPP ----> " + str(self.plc_host) + ":" + str(self.plc_port))
        try:  # Port test
            plc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            plc_socket.settimeout(20.0)
            plc_socket.connect((self.plc_host, self.plc_port))
        except:
            plc_socket.close()
            printH(
                "An error occurred while connecting to " + str(self.plc_host) + ":" + str(self.plc_port) + "\n" +
                "Most likely case is that port on this " + "address is either not binded or in use\n" +
                "by another instance of MasterAPP or " + "other application.",
                4, str(self.plc_host) + ":" + str(self.plc_port) + " Unavailable", isRootEnd=True)
            return self.plc_retry_success
        plc_socket.close()
        plc_server.host(self.plc_host)
        plc_server.port(self.plc_port)
        printH("Success!", 4, "MasterAPP <---> " + str(self.plc_host) + ":" + str(self.plc_port))

        time.sleep(0.1)

        printH("Connecting to PLC...", 3, str(self.plc_host) + ":" + str(self.plc_port) + " ----> PLC")

        if self.plc_stateOnly:
            printH(
                "StateOnly mode!\n"+
                "No additional information will "+ "be attempted to be retrieved.", 4, str(self.plc_host) + ":" + str(self.plc_port) + " <---> Quido <-X-> PLC")
            self.plc_retry_success = True
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
                4, err)
            return self.plc_retry_success

        printH("Success!", 4, str(self.plc_host) + ":" + str(self.plc_port) + " <---> PLC")
        self.plc_retry_success = True
        return self.plc_retry_success
    def PLC_Listener(self):  # Thread only! switched on by retry
        global cableUpdateProceed
        global response
        global retry
        global decypher

        printH("PLC-Listener Online", 2, "MasterAPP <---> PLC")

        while True:
            if stopClients or not self.plc_client_allowed:
                printH("Connection with " + str(self.plc_host) + " interrupted. PLC-Listener Offline", 0, "MasterAPP <-X-> PLC", isRootEnd=True)
                plc_server.close()
                self.plc_retry_success = False
                decypher.stop()
                break

            time.sleep(self.plc_requestInterval)
            if not plc_server.is_open():
                printH(
                    "Connection lost with PLC. " +
                    "Testing connection", 0, "MasterAPP <-?-- PLC")

                if not testConnection("plc"):
                    printH("Test Failed", 1, "MasterAPP <-X-- PLC", True)
                    printH("Connection lost with " + str(self.plc_host) + ". PLC-Listener Offline", 0, "MasterAPP <-X-> PLC", isRootEnd=True)
                    self.plc_listener_Allowed = False
                    self.plc_retry_success = False
                    if autoRetry_allowed:
                        api.api_listener_Allowed = False
                        '''retry = Worker(None, 'retry')'''
                        retry = threadPool.submit(Retry)
                else:
                    printH("Test Success", 1, "MasterAPP <---- PLC", True)
                break

            if self.plc_listener_Allowed and self.PLC_Response(False): #Read ControlWord
                response = self.PLC_Response()
                if response is False or response == "ERR":
                    printH(
                        "Failed to read response. " +
                        "Another attempt in " + str(self.plc_requestInterval) + "s", 0, "MasterAPP <-?-- PLC")
                    cableUpdateProceed = True

                else:
                    printH("Response received:", 0, "MasterAPP <---- PLC")
                    self.plc_listener_Allowed = False
                    self.plc_recieved = True

    # PLC Caller
    def PLC_Caller(self, action, index=0, item=0):
        global retry
        global response
        global cableUpdateInterrupt
        start_time = time.time()
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
                    time.sleep(self.plc_timeoutInterval)
                    response = self.PLC_Response()
                    if response is False:
                        printH("Connection lost with " + str(self.plc_host) + ". PLC-Listener Offline", 0, "MasterAPP <-X-> PLC", isRootEnd=True)
                        api.api_listener_Allowed = False
                        self.plc_listener_Allowed = False
                        cableUpdateInterrupt = True
                        time.sleep(.2)
                        for i in range(cablecount):
                            import_CableItemInfo(i, dictionary={"CS": "3", "RS": "", "IDR": "", "Position": "", "Speed": "", "Error": ""})
                        retry = threadPool.submit(Retry)
                        return
                response[0] = 4
                response[1] = index #unnecessary
                self.plc_recieved = True
                self.plc_listener_Allowed = True
                return
        words[1] = index
        words[2] = item

        printH("Request sent:", 0, "MasterAPP ----> PLC")
        printH(
            "Request: '" + str(action) + "'\n" +
            "Cable: '" + str(index) + "'\n"
            "Request item: " + str(item),
            2, str(words), isRootEnd=True)

        for i in range(0, 5):
            if not self.PLC_Request(words):
                printH(
                    "Failed to send request - " + str(i) + "/5" + ". " +
                    "Another attempt in " + str(self.plc_timeoutInterval) + "s", 2, "MasterAPP --?-> PLC", True)
                time.sleep(self.plc_timeoutInterval)
            else:
                self.plc_listener_Allowed = True
                return
        printH("Connection lost with " + str(self.plc_host) + ". PLC-Listener Offline", 0, "MasterAPP <-X-> PLC", isRootEnd=True)
        api.api_listener_Allowed = False
        self.plc_listener_Allowed = False
        cableUpdateInterrupt = True
        retry = threadPool.submit(Retry)

    # Decyphers the response of PLC
    def PLC_Decypher(self):
        global CableItems
        global cablecount
        global cableUpdateProceed
        global cableUpdateInterrupt
        global forceCableUpdate
        global cableUpdate

        global Watcher3

        Watcher3 = time.time()

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

        if action == 1:  # RecievedCableCount
            printH("Received CableCount: " + str(response_item[0]), 2, "Response: " + str(response), True)
            if response_item[0] <= 0:
                printH("ERROR: PLC has zero registered cables", 2, "Zero cables")
            cablecount = response_item[0]
            window.recievedCableCount()
            #time.sleep(0.1)  # wait for RecievedCableCount to process
            forceCableUpdate = True
            self.plc_recieved = False
            self.plc_listener_Allowed = True
            '''if not cableUpdate.running():
                cableUpdate = threadPool.submit(update_CableItems)'''
            return
        elif action == 2:  # Received Cable
            if str(response_item[4]) == "0404":
                dictionary["CS"] = 3
                printH("Cable" + str(index) + " not found", 2, "Error Message: " + str(response_item[3]))
                self.plc_recieved = False
                cableUpdateInterrupt = True
                self.plc_listener_Allowed = True
                return
            else:
                printH("Received Cable" + str(index), 2, "Response: " + str(response))
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
            Watcher3 = time.time() - Watcher3
            return

        if index > len(CableItems) - 1:
            window.add_CableItem()
            index = len(CableItems) - 1
        import_CableItemInfo(index, dictionary)

        cableUpdateProceed = True
        self.plc_listener_Allowed = True
    def getCableState(self, index):
        cableState = 3
        if quidoinputs[index][0]:
            if quidoinputs[index][1]:
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
                    time.sleep(0.1)
                writing = True

                plc.plc_listener_Allowed = False
                server = plc_server
                if not server.is_open():
                    if not server.open():
                        break

                time.sleep(0.01)  # Wait for listener to be done with listening
                if words is not None: #V5.0 Communication
                    server.write_multiple_registers(5, [0]*9)   #clear Databank
                    server.write_multiple_registers(5, words)   #Write prepared words
                    server.write_single_register(1, 1)          #Write True on control word (PLC read message)

                time.sleep(0.2)
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

            quidoinputs.clear()
            i = 0
            while i < quidoMaxInput:
                quidoinputs.append([random.randrange(0, 2), random.randrange(0, 2)])
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
            quidoinputs.clear()
            i = 0
            while i < quidoMaxInput:
                quidoinputs.append([inputs[i], inputs[i + 1]])
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
            plc_server.close()
            return response
        except:
            plc_server.close()
            reading = False
            return False

class AX_Server():
    def __init__(self) -> None:
        self.ax_server_allowed = True
        self.ax_host = '192.168.11.50'
        self.ax_port = 11854
        self.ax_server = None
        self.ax_listener = threading.Thread()
        self.ax_retry_success = False
        self.ax_message = None
        self.ax_requestInterval = window.ax_doubleSpinBox.value()

    # AX listener Thread
    def AX_Listener_Start(self):
        if self.ax_retry_success:
            return True
        self.ax_retry_success = False

        printH("AX server", 2)
        time.sleep(0.1)
        printH("Starting server...", 3, "MasterAPP ----> \n" + str(self.ax_host) + ":" + str(self.ax_port))
        try:
            self.ax_server = HTTPServer((self.ax_host, self.ax_port), AXHandler)  # Instance http serveru[adresa serveru, handler žádostí]
        except:
            printH(
                    "An error occurred while connecting to\n" +
                    str(self.ax_host) + ":" + str(self.ax_port) +
                    "\nMost likely case is that this address is\n" +
                    "invalid or otherwise could not be used.",
                    4, "Unsupported address:\n" + str(self.ax_host))
            return self.ax_retry_success
        printH("Success!", 4, "MasterAPP <---> \n" + str(self.ax_host) + ":" + str(self.ax_port))
        try:
            printH("Waiting for KeepAlive...", 3, str(self.ax_host) + ":" + str(self.ax_port) + "\n <---- AX-DOOR")

            '''client = hClient.HTTPConnection(self.ax_host, port=self.ax_port) # An instance of entrance connection
            client.set_tunnel(self.ax_host)
            client.request(
                method="GET",
                url=str(self.ax_host) + ":7/keepalive_req.cgi")'''
            AXserve = Worker(None, 'AXserve')
            '''AXserve =threading.Thread(target=self.AX_ServeForever)'''
            AXserve.start()
            while not self.ax_retry_success:
                if stopRetry:
                    self.ax_server.shutdown()
                    return
                time.sleep(0.1)

            self.ax_server.shutdown()

        except:
            pass
        printH("Success!", 4, "MasterAPP <---> AX-DOOR")

    def AX_ServeForever(self):
        self.ax_server.serve_forever()

    def AX_Listener(self):  # Thread only! switched on by retry
        printH("AX-Listener Online", 2, "MasterAPP <---> AX-DOOR", isRootEnd=True)
        AXserve = Worker(None, 'AXserve')
        '''AXserve =threading.Thread(target=self.AX_ServeForever)'''
        AXserve.start()
        while True:
            if stopClients:
                self.ax_server.shutdown()
                printH("Connection with " + str(self.ax_host) + " interrupted\nAX-Listener Offline", 0, "MasterAPP <-X-> AX-DOOR", isRootEnd=True)
                break

            time.sleep(plc.plc_requestInterval)

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

    # Decyphers the request of AX
    def AX_Decypher(self, handler: AXHandler, pathDict: dict, keepAlive):
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
            if api.api_client_allowed:
                response = [4, readerIndex, readerCode]
                api.API_Decypher(handler=handler)
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
                    self.AX_Caller(handler, "beep=1&keepaliveperiod=" + self.ax_requestInterval)
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

autoStart_allowed = False
class MainWindow(Ui_MasterAPP):
    resized = QtCore.pyqtSignal()

    def __init__(self, window) -> None:
        self.setupUi(window)
        self.cableItem_1.setVisible(False)
        self.graphFrame_1.setVisible(False)
        self.start_pushButton.setEnabled(True)
        self.retry_pushButton.setEnabled(False)
        self.auto_checkBox_3.setEnabled(False)
        self.stop_pushButton.setEnabled(False)
        self.gc_pushButton.setEnabled(False)

        self.wl_pyqtGraph_1.plotItem.setLabel('left', "Cable0")
        self.wl_pyqtGraph_1.plotItem.setLabel('bottom', 'Time (HHMM.SS)')
        self.wl_pyqtGraph_1.plotItem.getViewBox().setLimits(yMin=-0.2, yMax=2.2, xMin=0, xMax=240000, minYRange=-0.2, maxYRange=2.2, minXRange=0, maxXRange=240000)
        self.wl_pyqtGraph_1.plotItem.getViewBox().setMouseEnabled(x=True,y=False)
        self.wl_pyqtGraph_1.plotItem.getViewBox().setRange(yRange=(0,2))
        self.wl_pyqtGraph_1.plotItem.showGrid(True,False)
        # EventHandlers
        self.tabWidget_2.currentChanged.connect(self.splitter_resize)
        self.tabWidget_2.currentChanged.connect(self.updateSettings)
        self.splitter.splitterMoved.connect(self.splitter_resize)
        self.rcc = ToMainThread(None, 1) # The class emitting signal
        self.rcc.w_addCable.connect(self.add_CableItem) # the slot connected to signal
        self.upGr = ToMainThread(None, 2)
        self.upGr.updateGraphs.connect(self.updateGraph2)
        self.cl = ToMainThread(None, 4)
        self.cl.clearText.connect(self.clearH, False)

        self.ri_spinBox.valueChanged.connect(self.updateSettings)
        self.aui_doubleSpinBox.valueChanged.connect(self.updateSettings)
        self.auto_doubleSpinBox.valueChanged.connect(self.updateSettings)
        self.ax_doubleSpinBox.valueChanged.connect(self.updateSettings)
        self.cc_SpinBox.valueChanged.connect(self.updateSettings)
        self.aa_lineEdit.editingFinished.connect(self.updateSettings)
        self.aa_lineEdit_2.editingFinished.connect(self.updateSettings)
        self.pa_lineEdit.editingFinished.connect(self.updateSettings)
        self.pa_lineEdit_2.editingFinished.connect(self.updateSettings)
        self.ra_lineEdit.editingFinished.connect(self.updateSettings)
        self.ra_lineEdit_2.editingFinished.connect(self.updateSettings)
        self.a_checkBox.stateChanged.connect(self.updateSettings)
        self.p_checkBox.stateChanged.connect(self.updateSettings)
        self.ax_checkBox.stateChanged.connect(self.updateSettings)
        self.auto_checkBox.stateChanged.connect(self.updateSettings)
        self.auto_checkBox_2.stateChanged.connect(self.updateSettings)
        self.auto_checkBox_3.stateChanged.connect(self.updateSettings)
        self.auto_checkBox_4.stateChanged.connect(self.updateSettings)
        self.ss_comboBox.currentIndexChanged.connect(self.updateSettings)
        self.ss_spinBox.valueChanged.connect(self.updateSettings)
        self.d_lineEdit.editingFinished.connect(self.updateSettings)

        # UIButtons
        self.start_pushButton.pressed.connect(self.StartButton)
        self.retry_pushButton.pressed.connect(self.RetryButton)
        self.stop_pushButton.pressed.connect(self.StopButton)
        self.gc_pushButton.pressed.connect(self.GetCablesButton)
        self.ss_pushButton_1.pressed.connect(self.workloadPath)
        self.ss_pushButton_2.pressed.connect(self.SaveStateDataButton)
        self.d_pushButton.pressed.connect(self.ChangeDomainButton)

        self.historyButton.pressed.connect(self.clearH)
        self.historyButton_2.pressed.connect(self.exportH)
        #self.historyButton_3.pressed.connect(self.colapseH)
        #self.historyCheckBox.stateChanged.connect(self.updateSettings)

    # Startup part 1: Window setup and Settings
    def StartPart1(self):
        global cableUpdate
        global logFilePath

        logFilePath = "HistoryLog" + str(datetime.datetime.now().month).zfill(2) + str(datetime.datetime.now().day).zfill(2) + ".txt"
        printH("Startup", 0, "MasterAPP", False)
        self.splitter.setSizes([self.tableWidget.width() + 9, self.splitter.sizes()[1] + 135])
        self.tableWidget.horizontalHeader().setDefaultSectionSize(self.tableWidget.width())
        self.loadSettings()
        if plc.plc_client_allowed:
            self.gc_pushButton.setEnabled(False)
        self.updateSettings()

        if autoStart_allowed:  # auto start
            self.StartButton()

    # UI Settings
    def loadSettings(self):
        global checkSettings
        global cablecount
        global config
        global retryInterval
        global autoStart_allowed
        global autoRetry_allowed
        global autoUpdate_allowed
        global autoUpdate_Interval
        global localPath
        global domainHost
        global domainPort
        global domainUser
        global domainPassword
        global saveStyle
        global areal
        global minMinuteState

        # load default settings
        self.aa_lineEdit.setPlaceholderText(api.api_host + " (This Machine)")
        self.aa_lineEdit_2.setPlaceholderText(str(api.api_port))
        self.pa_lineEdit.setPlaceholderText(plc.plc_host + " (This Machine)")
        self.pa_lineEdit_2.setPlaceholderText(str(plc.plc_port))
        self.ra_lineEdit.setPlaceholderText(ax.ax_host)
        self.ra_lineEdit_2.setPlaceholderText(str(ax.ax_port))

        overWriteConfig = False
        try:
            config.read('config.ini')
        except 2:
            time.sleep(1)
            config.read('config.ini')
        except:
            overWriteConfig = True
        else:
            if (not config.has_section("retry") or
                not config.has_section("api") or
                not config.has_section("plc") or
                not config.has_section("ax") or
                not config.has_section("domain") or
                not config.has_section("auto")):
                overWriteConfig = True

        if overWriteConfig:
            printH("An error uccured while loading settings.", 0)
            root = tkinter.Tk()
            root.withdraw()
            fail = True
            test = True

            tries = 0
            while fail and test:
                time.sleep(1)
                #test = messagebox.askretrycancel(title="Error with Config File", message="MasterAPP encountered an error while loading Config file. (" + str(tries) + " tries out of 5)" + " \nDo you wish to try again? \n\nCancel: Rewrite Config file. Settings will be lost.", master=root)
                #Doesn't work
                try:
                    config.read('config.ini')
                except:
                    tries += 1
                else:
                    if (not config.has_section("retry") or
                        not config.has_section("api") or
                        not config.has_section("plc") or
                        not config.has_section("ax") or
                        not config.has_section("domain") or
                        not config.has_section("auto")):
                        tries += 1
                    else:
                        fail = False
                if tries == 6: break
            if fail:
                self.createConfigFile()

        # Load Config File
        retryInterval = config.getfloat("retry", "interval")
        autoStart_allowed = config.getboolean('auto', 'allowStart')
        autoRetry_allowed = config.getboolean('auto', 'allowRetry')
        autoUpdate_allowed = config.getboolean('auto', 'allowUpdate')
        api.api_idleInterval = config.getfloat('api', 'interval')
        api.api_client_allowed = config.getboolean('api', 'allowed')
        api.api_host = config.get('api', 'host')
        api.api_port = config.getint('api', 'port')
        autoUpdate_Interval = config.getfloat('plc', 'interval')
        plc.plc_client_allowed = config.getboolean('plc', 'allowed')
        plc.plc_host = config.get('plc', 'host')
        plc.plc_port = config.getint('plc', 'port')
        plc.plc_getCableCount_allowed = config.getboolean('auto', 'allowGetCount')
        cablecount = config.getint('auto', 'cableCount')
        ax.ax_requestInterval = config.getfloat('ax', 'interval')
        ax.ax_server_allowed = config.getboolean('ax', 'allowed')
        ax.ax_host = config.get('ax', 'host')
        ax.ax_port = config.getint('ax', 'port')

        cipher_suite = Fernet(key)

        domainHost = config.get('domain', 'host')
        domainPort = config.getint('domain', 'port')
        try:
            domainUser = cipher_suite.decrypt(bytes(config.get('domain', 'user') + '=', 'utf8')).decode('utf8')
            domainPassword = cipher_suite.decrypt(bytes(config.get('domain', 'password') + '=', 'utf8')).decode('utf8')
        except:
            domainUser = ''
            domainPassword = ''
        saveStyle = config.getint('domain', 'saveState')
        localPath = config.get('domain', 'localPath')
        areal = config.get('domain', 'areal')
        minMinuteState = config.getint('domain', 'minState')

        # Misc
        #collapseH = config.getboolean('auto', 'allowCollapse')

        # Express settings
        checkSettings = False
        self.aa_lineEdit.setText(api.api_host)
        self.aa_lineEdit_2.setText(str(api.api_port))
        self.pa_lineEdit.setText(plc.plc_host)
        self.pa_lineEdit_2.setText(str(plc.plc_port))
        self.ra_lineEdit.setText(ax.ax_host)
        self.ra_lineEdit_2.setText(str(ax.ax_port))
        self.ri_spinBox.setValue(int(retryInterval))
        self.aui_doubleSpinBox.setValue(api.api_idleInterval)
        self.auto_doubleSpinBox.setValue(autoUpdate_Interval)
        self.ax_doubleSpinBox.setValue(ax.ax_requestInterval)
        self.cc_SpinBox.setValue(cablecount)
        #self.cc_SpinBox.setEnabled(not plc.plc_getCableCount_allowed) #Set to four. Enable for debug
        self.a_checkBox.setChecked(api.api_client_allowed)
        self.p_checkBox.setChecked(plc.plc_client_allowed)
        self.ax_checkBox.setChecked(ax.ax_server_allowed)
        self.auto_checkBox.setChecked(autoStart_allowed)
        self.auto_checkBox_2.setChecked(autoRetry_allowed)
        self.auto_checkBox_3.setChecked(autoUpdate_allowed)
        self.auto_checkBox_4.setChecked(plc.plc_getCableCount_allowed)
        #self.historyCheckBox.setChecked(collapseH)

        self.d_label.setText(domainHost)
        self.ss_comboBox.setCurrentIndex(saveStyle)
        self.ss_spinBox.setValue(minMinuteState)
        self.ss_label_2.setText(localPath)
        self.d_lineEdit.setText(areal)

        checkSettings = True
        pass

    def updateSettings(self):
        global retry
        global autoStart_allowed
        global autoRetry_allowed
        global autoUpdate_allowed
        global autoUpdate_Interval
        global retryInterval
        global stopClients
        global collapseH
        global checkSettings
        global cablecount
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

        time_start = time.time()
        if not checkSettings:
            return

        checkSettings = False
        if autoRetry_allowed != self.auto_checkBox_2.isChecked():
            stopRetry = autoRetry_allowed
        '''if plc.plc_getCableCount_allowed != self.auto_checkBox_4.isChecked():
            self.cc_SpinBox.setEnabled(plc.plc_getCableCount_allowed)''' #Disabled. Debug only

        #Synchronization
        retryInterval = self.ri_spinBox.value()
        cablecount = self.cc_SpinBox.value()
        autoStart_allowed = self.auto_checkBox.isChecked()
        autoRetry_allowed = self.auto_checkBox_2.isChecked()
        api.api_idleInterval = self.aui_doubleSpinBox.value()
        autoUpdate_Interval = self.auto_doubleSpinBox.value()
        autoUpdate_allowed = self.auto_checkBox_3.isChecked()
        cableUpdateAllowed = self.auto_checkBox_3.isEnabled()
        plc.plc_getCableCount_allowed = self.auto_checkBox_4.isChecked()
        ax.ax_requestInterval = self.ax_doubleSpinBox.value()
        ax.ax_server_allowed = self.ax_checkBox.isChecked()
        #collapseH = self.historyCheckBox.isChecked()

        saveStyle = self.ss_comboBox.currentIndex()
        minMinuteState = self.ss_spinBox.value()
        areal = self.d_lineEdit.text()

        #Special behavior

        if not areal == '':
            areal += '/'

        self.ss_spinBox.setSuffix("/" + str(int(60 / self.auto_doubleSpinBox.value())) + "s")
        self.ss_spinBox.setMaximum(int(60 / self.auto_doubleSpinBox.value()))
        if autoUpdate_allowed:
            cableUpdateEnabled = True
            '''if plc.plc_retry_success:
                if not CableItems[0].isVisible():
                    self.GetCablesButton()
                if not cableUpdate.running():
                    cableUpdate = threadPool.submit(update_CableItems)'''
        else:
            cableUpdateEnabled = False

        stop = False
        start = False
        if api.api_client_allowed != self.a_checkBox.isChecked():
            if not (api.api_retry_success or plc.plc_retry_success):
                api.api_client_allowed = self.a_checkBox.isChecked()
            elif self.a_checkBox.isChecked():
                start = True
            else:
                stop = True

        if plc.plc_client_allowed != self.p_checkBox.isChecked():
            if not (api.api_retry_success or plc.plc_retry_success):
                plc.plc_client_allowed = self.p_checkBox.isChecked()
            elif self.p_checkBox.isChecked():
                start = True
            else:
                stop = True

        if not (api.api_client_allowed or plc.plc_client_allowed or ax.ax_server_allowed):
            self.retry_pushButton.setEnabled(False)
        elif not self.start_pushButton.isEnabled():
            self.retry_pushButton.setEnabled(True)

        restart = False
        if api.api_host != self.aa_lineEdit.text():  # API Address(host)
            if self.aa_lineEdit.text() != '':
                api.api_host = self.aa_lineEdit.text()
                restart = True
            else:
                api.api_host = socket.gethostbyname(socket.gethostname())
                self.aa_lineEdit.setText('')
        if str(api.api_port) != self.aa_lineEdit_2.text():  # API Address(port)
            if self.aa_lineEdit_2.text() != '' and self.aa_lineEdit_2.text().isdigit():
                api.api_port = int(self.aa_lineEdit_2.text())
                restart = True
            else:
                api.api_port = 1000
                self.aa_lineEdit_2.setText('')
        if plc.plc_host != self.pa_lineEdit.text():  # PLC Address(host)
            if self.pa_lineEdit.text() != '':
                plc.plc_host = self.pa_lineEdit.text()
                restart = True
            else:
                plc.plc_host = socket.gethostbyname(socket.gethostname())
                self.pa_lineEdit.setText('')
        if str(plc.plc_port) != self.pa_lineEdit_2.text():  # PLC Address(port)
            if self.pa_lineEdit_2.text() != '' and self.pa_lineEdit_2.text().isdigit():
                plc.plc_port = int(self.pa_lineEdit_2.text())
                restart = True
            else:
                plc.plc_port = 502
                self.pa_lineEdit_2.setText('')
        if str(ax.ax_host) != self.ra_lineEdit.text():  # AX Address(host)
            if self.ra_lineEdit.text() != '' and self.ra_lineEdit.text().isdigit():
                ax.ax_host = int(self.ra_lineEdit.text())
                restart = True
            else:
                ax.ax_host = "192.168.11.50"
                self.ra_lineEdit.setText('')
        if str(ax.ax_port) != self.ra_lineEdit_2.text():  # AX Address(port)
            if self.ra_lineEdit_2.text() != '' and self.ra_lineEdit_2.text().isdigit():
                ax.ax_port = int(self.ra_lineEdit_2.text())
                restart = True
            else:
                ax.ax_port = 11854
                self.ra_lineEdit_2.setText('')
        #Config backup
        config.set('retry', 'interval', str(retryInterval))
        config.set('auto', 'allowStart', str(self.auto_checkBox.isChecked()))
        config.set('auto', 'allowRetry', str(self.auto_checkBox_2.isChecked()))
        config.set('auto', 'allowUpdate', str(self.auto_checkBox_3.isChecked()))
        config.set('auto', 'allowGetCount', str(self.auto_checkBox_4.isChecked()))
        config.set('auto', 'allowCollapse', str(collapseH))
        config.set('auto', 'cableCount', str(cablecount))
        config.set('api', 'interval', str(api.api_idleInterval))
        config.set('api', 'allowed', str(self.a_checkBox.isChecked()))
        config.set('api', 'host', str(api.api_host))
        config.set('api', 'port', str(api.api_port))
        config.set('plc', 'interval', str(autoUpdate_Interval))
        config.set('plc', 'allowed', str(self.p_checkBox.isChecked()))
        config.set('plc', 'host', str(plc.plc_host))
        config.set('plc', 'port', str(plc.plc_port))
        config.set('ax', 'interval', str(ax.ax_requestInterval))
        config.set('ax', 'allowed', str(self.ax_checkBox.isChecked()))
        config.set('ax', 'host', str(ax.ax_host))
        config.set('ax', 'port', str(ax.ax_port))

        cipher_suite = Fernet(key)

        config.set('domain', 'host', str(domainHost))
        config.set('domain', 'port', str(domainPort))
        config.set('domain', 'user', cipher_suite.encrypt(bytes(domainUser, 'utf8')).decode('utf8'))
        config.set('domain', 'password', cipher_suite.encrypt(bytes(domainPassword, 'utf8')).decode('utf8'))
        config.set('domain', 'saveState', str(saveStyle))
        config.set('domain', 'localPath', str(localPath))
        config.set('domain', 'areal', str(areal))
        config.set('domain', 'minState', str(minMinuteState))

        with open('config.ini', 'w') as f:
            config.write(f)
            f.close()
        if (restart or start) and (api.api_retry_success or plc.plc_retry_success):
            root = tkinter.Tk()
            root.withdraw()
            if messagebox.askokcancel("Confirm Action", "Variables of either API or PLC have been changed during runtime. \nThis change can only be implemented after restart. \n\nDo you wish to proceed?"):
                stopClients = True
                time.sleep(1)
                stopClients = False
                api.api_client_allowed = self.a_checkBox.isChecked()
                plc.plc_client_allowed = self.p_checkBox.isChecked()

                '''retry = Worker(None, 'retry')'''
                retry = threadPool.submit(Retry)#! starts a loop either way
            else:
                self.aa_lineEdit.setText(api.api_host)
                self.aa_lineEdit_2.setText(str(api.api_port))
                self.pa_lineEdit.setText(plc.plc_host)
                self.pa_lineEdit_2.setText(str(plc.plc_port))
                self.a_checkBox.setChecked(api.api_client_allowed)
                self.p_checkBox.setChecked(plc.plc_client_allowed)
        elif stop:
            root = tkinter.Tk()
            root.withdraw()
            if messagebox.askokcancel("Confirm Action", "Variables of either API or PLC have been changed during runtime. \nServer will now stop. \n\nDo you wish to proceed?"):
                api.api_client_allowed = self.a_checkBox.isChecked()
                plc.plc_client_allowed = self.p_checkBox.isChecked()
            else:
                self.a_checkBox.setChecked(api.api_client_allowed)
                self.p_checkBox.setChecked(plc.plc_client_allowed)
        checkSettings = True

    def createConfigFile(self):
        if not config.has_section("retry"):
            config.add_section('retry')
            config.set('retry', 'interval', str(retryInterval))

        if not config.has_section("api"):
            config.add_section('api')
            config.set('api', 'interval', str(api.api_idleInterval))
            config.set('api', 'allowed', str(self.a_checkBox.isChecked()))
            config.set('api', 'host', str(api.api_host))
            config.set('api', 'port', str(api.api_port))

        if not config.has_section("plc"):
            config.add_section('plc')
            config.set('plc', 'interval', str(autoUpdate_Interval))
            config.set('plc', 'allowed', str(self.p_checkBox.isChecked()))
            config.set('plc', 'host', str(plc.plc_host))
            config.set('plc', 'port', str(plc.plc_port))

        if not config.has_section("ax"):
            config.add_section('ax')
            config.set('ax', 'interval', str(ax.ax_requestInterval))
            config.set('ax', 'allowed', str(self.ax_checkBox.isChecked()))
            config.set('ax', 'host', str(ax.ax_host))
            config.set('ax', 'port', str(ax.ax_port))

        if not config.has_section("auto"):
            config.add_section('auto')
            config.set('auto', 'allowStart', str(self.auto_checkBox.isChecked()))
            config.set('auto', 'allowRetry', str(self.auto_checkBox_2.isChecked()))
            config.set('auto', 'allowUpdate', str(self.auto_checkBox_3.isChecked()))
            config.set('auto', 'allowGetCount', str(self.auto_checkBox_4.isChecked()))
            config.set('auto', 'allowCollapse', str(collapseH))
            config.set('auto', 'cableCount', str(cablecount))

        if not config.has_section("domain"):
            config.add_section('domain')
            config.set('domain', 'host', str(domainHost))
            config.set('domain', 'port', str(domainPort))
            config.set('domain', 'user', str(domainUser))
            config.set('domain', 'password', str(domainPassword))
            config.set('domain', 'saveState', str(self.ss_comboBox.currentIndex()))
            config.set('domain', 'localPath', str(self.ss_label_2.text()))
            config.set('domain', 'areal', str(areal))
            config.set('domain', 'minState', str(minMinuteState))

        with open('config.ini', 'w') as f:
            config.write(f)
            f.close()
        pass

    #Updates Graph of every cable
    autoMove = True
    lastData = None
    graphData = []
    def updateGraph1(self, loadFile=True):
        dateTime = datetime.datetime.now()
        wPath = localPath + "/" + areal + str(dateTime.year) + '/' + str(dateTime.month).zfill(2) + '/' + str(dateTime.day).zfill(2) + '/'

        state = None
        time = None
        self.graphData = []
        #graphData
        #   [Cable0
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
            for filedir in os.listdir(wPath):
                with open(wPath + filedir, 'r') as file:
                    lines = file.readlines()
                    while len(self.graphData) < len(lines):
                        self.graphData.append([[],[]])
                    for line in lines:
                        index = line[0]
                        state = int(line[22])
                        hour = line[13:15]
                        minute = line[16:18]
                        second = line[19:21]
                        time = hour + minute + second

                        graphTime: list = self.graphData[int(index)][0] #X
                        graphState: list = self.graphData[int(index)][1] #Y
                        i = len(graphState)
                        if int(i) != 0:
                            if graphState[-1] != state:
                                graphTime.append(graphTime[-1])
                                graphState.append(state)
                        graphTime.append(float(time)/100)
                        graphState.append(state)

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
        self.lastData = [graphTime[-1], graphState[-1]]

        self.updateGraph2()
    def updateGraph2(self):
        if self.graphData == []:
            return
        if not isinstance(threading.current_thread(), threading._MainThread):
            self.upGr.start()
            return
        index = 0
        for graphitem in graphItems:
            #Clear and update the graph
            graphitem.clear()
            graphitem.plot(self.graphData[index][0], self.graphData[index][1])
            index += 1
        printH("Graphs updated!", 2, "Graphs updated from File.")

    # Cables
    def recievedCableCount(self):
        global CableItems
        global cablecount
        global cableUpdateProceed
        global cableUpdate
        try:
            if cablecount == len(CableItems):
                pass
            elif cablecount > 0:
                CableItems[0].setVisible(True)
                CableGraph[0].setVisible(True)

                printH("Registering new cables...", 1, str(cablecount) + " cables")
                c = 0
                while c < cablecount:
                    time.sleep(.1)
                    if cablecount > len(CableItems):
                        if isinstance(threading.current_thread(), threading._MainThread):
                            self.add_CableItem()
                        else:
                            self.rcc.start() # add Cable in the main thread
                    sg = ToMainThread(None, 3, c)
                    sg.setupGraphs.connect(self.setupGraphs)
                    sg.start()

                    t = 0 # timeout
                    while len(CableItems) != c + 1: # wait for mainThread to add Cable
                        if t >= 1000:
                            t = 0
                        t += 1
                        time.sleep(0.01)
                        if stopRetry:
                            printH("Interrupted", 2, "stop button")
                            return False
                    CableItems[c].setVisible(True) # Enable already created CableItems
                    CableGraph[c].setVisible(True) # Enable already created graphs

                    printH("Cable" + str(c) + " registered", 2, str(len(CableItems)) + "/" + str(cablecount))
                    c += 1
                c = len(CableItems)
                while cablecount < c:
                    CableItems[c - 1].setVisible(False)
                    CableGraph[c - 1].setVisible(False)
                    printH("Cable" + str(c - 1) + " removed", 2, str(c) + "/" + str(cablecount))
                    c -= 1
                time.sleep(0.02)
                printH("Updating Graphs.", 1)
                self.updateGraph1(True)
            else:
                CableItems[0].setVisible(False)
                CableGraph[0].setVisible(False)
                return False
        except:
            printH("Error encountered.", 1)
            window.StopButton()
            window.StartButton()
            return False
        return True
    def setupGraphs(self, index):
        graphItems[len(CableItems) - 1].setLabel('left', "Cable" + str(index))
        graphItems[len(CableItems) - 1].setLabel('bottom', 'Time (HHMM.SS)')
        graphItems[len(CableItems) - 1].getViewBox().setLimits(yMin=-0.2, yMax=2.2, xMin=0, xMax=240000, minYRange=-0.2, maxYRange=2.2, minXRange=0, maxXRange=240000)
        graphItems[len(CableItems) - 1].getViewBox().setMouseEnabled(x=True,y=False)
        graphItems[len(CableItems) - 1].getViewBox().setRange(yRange=(0,2))
        graphItems[len(CableItems) - 1].showGrid(True,False)

    # Add another CableItem by copying template(CableItems[0])
    def add_CableItem(self):
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

            spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

            newstatusImage = QtWidgets.QLabel(newCableItem)
            newstatusImage.setStyleSheet(self.statusImage_1.styleSheet())
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

            #New cable graph
            newgraphFrame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
            newgraphFrame.setFrameShape(self.graphFrame_1.frameShape())
            newgraphFrame.setFrameShadow(self.graphFrame_1.frameShadow())
            newgraphFrame.setLineWidth(self.graphFrame_1.lineWidth())
            newgraphFrame.setSizePolicy(self.graphFrame_1.sizePolicy())
            newgraphFrame.setMinimumSize(self.graphFrame_1.minimumSize())
            newgraphFrame.setMaximumSize(self.graphFrame_1.maximumSize())
            newgraphFrame.setObjectName("graphFrame_" + str(len(CableItems)))

            newgridLayout = QtWidgets.QGridLayout(newgraphFrame)
            newgridLayout.setContentsMargins(0, 0, 0, 0)
            newgridLayout.setSpacing(0)
            newgridLayout.setObjectName("gridLayout_" + str(len(CableItems)))

            newpyqtGraph = PlotWidget(newgraphFrame)
            newpyqtGraph.setSizePolicy(self.wl_pyqtGraph_1.sizePolicy())
            newpyqtGraph.setObjectName("wl_pyqtGraph_" + str(len(CableItems)))

            newgridLayout.addWidget(newpyqtGraph, 0, 0, 1, 1)
            self.verticalLayout_6.addWidget(newgraphFrame)

            layout = self.scrollAreaWidgetContents.layout()
            layout.insertWidget(layout.count() - 2, newgraphFrame)

            CableItems.append(newCableItem)
            CableGraph.append(newgraphFrame)

            graphItem = newgraphFrame.children()[1]
            graphItem: PlotWidget
            graphItems.append(graphItem)
            graphItems[len(CableItems) - 1].setLabel('left', newviewImage.text())
            graphItems[len(CableItems) - 1].setLabel('bottom', 'Time (HHMM.SS)')
            graphItems[len(CableItems) - 1].getViewBox().setLimits(yMin=-0.2, yMax=2.2, xMin=0, xMax=240000, minYRange=-0.2, maxYRange=2.2, minXRange=0, maxXRange=240000)
            graphItems[len(CableItems) - 1].getViewBox().setMouseEnabled(x=True,y=False)
            graphItems[len(CableItems) - 1].getViewBox().setRange(yRange=(0,2))
            graphItems[len(CableItems) - 1].showGrid(True,False)
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
                CableGraph.pop(i).deleteLater()
            CableItems[0].setVisible(False)
            CableGraph[0].setVisible(False)
        else:
            printH("Removing Cable" + str(index), 0, str(index) + "/" + str(len(CableItems)))
            CableItems[index].setVisible(False)
            CableGraph[index].setVisible(False)
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

        stopRetry = False
        stopClients = False
        retry = threading.Thread(target=Retry)# Try to connect. If fails, loop to try
        retry.start()
        '''retry = threadPool.submit(Retry)'''# Cannot be set inside a threadPool. Weird error where it sits open forever
        self.start_pushButton.setEnabled(False)
        self.stop_pushButton.setEnabled(True)

    def RetryButton(self):
        global stopRetry
        global stopClients
        global retry

        stopRetry = False
        stopClients = False
        self.retry_pushButton.setEnabled(False)
        self.stop_pushButton.setEnabled(True)
        self.gc_pushButton.setEnabled(False)
        self.auto_checkBox_3.setEnabled(False)
        self.auto_doubleSpinBox.setEnabled(True)
        retry = threadPool.submit(Retry)# Try to connect. If fails, loop to try

    def GetCablesButton(self):
        global cableUpdate
        global forceCableUpdate

        if cableUpdate.running():
            forceCableUpdate = True
        elif plc.plc_client_allowed:
            if not CableItems[0].isVisible():
                printH("Updating Cable objects...", 0)
                if plc.plc_getCableCount_allowed:
                    plc.PLC_Caller("GetCableCount")  # Get number of available cables from plc
                else:
                    printH("Received cable count: " + str(cablecount), 2, "Preset cable count: " + str(cablecount), True)
                    self.recievedCableCount()

            if not cableUpdate.running():
                cableUpdate = threadPool.submit(update_CableItems)
                if not autoUpdate_allowed:
                    forceCableUpdate = True

    def ChangeDomainButton(self):
        dialogWindow.show()
        dialogWindow.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        dialog.buttonBox.accepted.connect(self.ChangeDomainResult)
    def ChangeDomainResult(self):
        global domainHost
        global domainPort
        global domainUser
        global domainPassword
        domainHost = dialog.d_lineEdit_1.text()
        domainPort = dialog.d_lineEdit_2.text()
        domainUser = dialog.d_lineEdit_3.text()
        domainPassword = dialog.d_lineEdit_4.text()
        self.d_label.setText(domainHost)
        self.updateSettings()

    def SaveStateDataButton(self):
        global forceSaveStateData

        if ssdt.running():
            forceSaveStateData = True

    def StopButton(self, restart = False):
        global stopRetry
        global stopClients
        global cableUpdateEnabled
        global saveStateAllowed
        printH("Cleanup:", 0)
        saveStateAllowed = False
        self.start_pushButton.setEnabled(True)
        self.retry_pushButton.setEnabled(False)
        self.stop_pushButton.setEnabled(False)
        self.gc_pushButton.setEnabled(False)
        self.auto_checkBox_3.setEnabled(False)
        self.auto_doubleSpinBox.setEnabled(True)
        self.tabWidget_2.setTabEnabled(1, True)
        stopRetry = True
        stopClients = True

        cableUpdateEnabled = not cableUpdateEnabled
        time.sleep(.2)
        cableUpdateEnabled = not cableUpdateEnabled

        printH("Clients/Servers Stopped", 1)

        if restart:
            printH("Restart Allowed...")
            cableUpdateEnabled = False
            time.sleep(.2)
            os.execl(sys.executable, sys.executable, *sys.argv)
    def Cleanup(self):
        printH("New Day!", 0, "Cleaning old files.")
        self.cl.start()
        time.sleep(0.1)
        printH("New Day!", 0, "Cleanup Complete.")

    def CrashCatch(self):
        self.exportH(fileH + "crashLog.txt")
        pass

    def clearH(self, ask=True):
        global parentTree
        global parentitem
        self.historyButton.setEnabled(False)
        if ask:
            root = tkinter.Tk()
            root.withdraw()
            if not messagebox.askyesno("Confirm Action", "This action cannot be reversed.\nDo you wish to clear the history?"):
                return
        parentTree = []
        parentitem = []
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
        self.ss_label_2.setText(localPath)
        self.updateSettings()

    '''def colapseH(self):
        self.historyButton_2.setEnabled(False)
        for i in range(self.historyList.topLevelItemCount()):
            self.historyList.topLevelItem(i).setExpanded(False)
        pass
        self.historyButton_2.setEnabled(True)'''
# Create Window Instance
app = QtWidgets.QApplication(sys.argv)
mainWindow = QtWidgets.QMainWindow()
window = MainWindow(mainWindow)
dialogWindow = QtWidgets.QDialog()
dialog = NewDomainDialog(dialogWindow)

api = API_Client()
plc = PLC_Client()
ax = AX_Server()

# Public variables
isStart = True
checkSettings = False
firstAttempt = True
collapseH = False
widthH = 0
fileH = ""
config = ConfigParser()
key = b'6araaoXwfSsMllEYNf8JHN1kePLImcCsbAQ8AB8-xDM='

# Communication
reading = False
writing = False
response = ""
stopClients = False
autoUpdate_allowed = False
autoUpdate_Interval = 60
quidoMaxInput = 10
quidoinputs = []

quidoMaxInput = window.cc_SpinBox.value() * 2

# Threads
threadPool = ThreadPoolExecutor(max_workers=5)
retry = None
decypher = ToMainThread() # The class emitting signal
pHistory = ToMainThread(None, 5)
decypher.plc_decypher.connect(plc.PLC_Decypher) # the slot connected to signal
decypher.api_decypher.connect(api.API_Decypher) # the slot connected to signal

# MasterAPP Communication
api_server = HTTPConnection
plc_server = ModbusClient()

# QObject lists
cablecount = 4
CableItems = [
    window.cableItem_1,
]
CableDictionary = []
CableGraph = [
    window.graphFrame_1,
]
graphItems = [
    window.wl_pyqtGraph_1.plotItem
]

parentitem = QtWidgets.QTreeWidgetItem(),
parentTree = [
    parentitem,
]
# debug

Watcher0 = 0
Watcher1 = 0
Watcher2 = 0
Watcher3 = 0
Watcher = []

# Startup part 2: Connections and Cable Updates
def StartPart2():
    global stopClients
    global retryInProgress
    global cableUpdate
    global forceCableUpdate
    global decypher
    global logFilePath
    global saveStateAllowed

    stopClients = False
    api.api_listener_Allowed = False
    plc.plc_listener_Allowed = True
    saveStateAllowed = True

    window.gc_pushButton.setEnabled(True)
    window.auto_checkBox_3.setEnabled(True)
    window.stop_pushButton.setEnabled(True)
    window.retry_pushButton.setEnabled(True)
    decypher.start() # Starting the decypher Thread

    import_CableItemInfo(0, new=True)  # Create a template CableItem
    if plc.plc_client_allowed and autoUpdate_allowed:
        window.GetCablesButton()
        '''if not cableUpdate.running():
            cableUpdate = threadPool.submit(update_CableItems)'''
    '''
    if cableUpdate.running():
        forceCableUpdate = False'''
    #window.updateSettings()

# Retry for Connections
stopRetry = False
autoRetry_allowed = False
retryInProgress = False
retryInterval = 0.0
def Retry(loop = False):
    global retryInProgress
    global retryInterval
    global stopClients
    global stopRetry
    global firstAttempt
    global retry

    if stop_Retry(): return
    if retryInProgress:
        return
    if not (api.api_client_allowed or plc.plc_client_allowed or ax.ax_server_allowed):
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

    if api.api_client_allowed:
        api.api_retry_success = False
        api.API_Listener_Start()
        if stop_Retry(): return
    if plc.plc_client_allowed:
        plc.plc_retry_success = False
        plc.PLC_Listener_Start()
        if stop_Retry(): return

    success = False
    if ((not api.api_client_allowed or api.api_retry_success) and
            (not plc.plc_client_allowed or plc.plc_retry_success)):
        if ax.ax_server_allowed:
            ax.ax_retry_success = False
            ax.AX_Listener_Start()
            if stop_Retry(): return
    if ((not api.api_client_allowed or api.api_retry_success) and
        (not plc.plc_client_allowed or plc.plc_retry_success) and
            not ax.ax_server_allowed or ax.ax_retry_success):
        success = True

        if api.api_host == plc.plc_host and api.api_client_allowed and plc.plc_client_allowed:
            printH(
                "API/PLC Connection successfully estabilished with: " +
                str(api.api_host), 1, "Test success")
            api.api_listener = threadPool.submit(api.API_Listener)
            if not plc.plc_stateOnly:
                plc.plc_listener = threadPool.submit(plc.PLC_Listener)
        else:
            if api.api_client_allowed:         # If allowed, turn on api listener
                printH(
                    "API Connection successfully estabilished with: " +
                    str(api.api_host), 1, "Test success")
                api.api_listener = threadPool.submit(api.API_Listener)
            if plc.plc_client_allowed:         # If allowed, turn on plc listener
                printH(
                    "PLC Connection successfully estabilished with: " +
                    str(plc.plc_host), 1, "Test success")
                if not plc.plc_stateOnly:
                    plc.plc_listener_Allowed = True
                    plc.plc_listener = threadPool.submit(plc.PLC_Listener)
        if ax.ax_server_allowed:         # If allowed, turn on ax listener
            printH(
                "AX Connection successfully estabilished with " +
                "AX-DOOR terminal on " + str(ax.ax_host), 1, "Test success")
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
            for i in range(int(retryInterval)):  # Timeout
                time.sleep(1)
                window.auto_label_4.setText(str(int(retryInterval) - i).zfill(2))
                if stop_Retry(): return
            window.auto_label_4.setText(str(0).zfill(2))
            if not loop:
                retry = threadPool.submit(loop_Retry) # Connection retry for API and PLC (30s)
        else:
            printH(
            "Connection failed for either API, PLC or AX. " +
            "Press Retry to try again.", 1, "Test failed. No Retry.", isRootEnd=True)
            window.retry_pushButton.setEnabled(True)
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

    while loop:
        stopClients = True
        time.sleep(plc.plc_requestInterval)
        stopClients = False

        loop = Retry(loop)

def stop_Retry():
    global retryInProgress
    if stopRetry:
        printH("Retry interrupted", 1)
        retryInProgress = False
        window.retry_pushButton.setEnabled(True)
        return True
    return False

# Thread Only! Periodically Updates all Cables. Turned on by GetCableButton
forceCableUpdate = False
cableUpdateProceed = False
cableUpdateInterrupt = False
cableUpdateEnabled = False
cableUpdateAllowed = False
lastUpdate = None
updateInProgress = False
def update_CableItems(blank: bool = False):
    if blank: return
    global autoUpdate_Interval
    global cableUpdateProceed
    global cablecount
    global cableUpdateInterrupt
    global forceCableUpdate
    global updateInProgress
    global minuteState
    global ssdt

    global Watcher0
    global Watcher1
    global Watcher2
    global Watcher3

    window.updateSettings()
    cableUpdateInterrupt = False
    time.sleep(0.1)
    printH("CableUpdate: Waiting for new minute...", 0)
    while datetime.datetime.now().time().second != 0 and not ssdt.running(): #synchronize to a minute
        if forceCableUpdate or not cableUpdateEnabled: break
        window.auto_label_1.setText(str(60 - datetime.datetime.now().time().second).zfill(2))
        time.sleep(1)
    window.auto_label_1.setText(str(0).zfill(2))
    if not cableUpdateEnabled and not forceCableUpdate: return
    window.auto_doubleSpinBox.setEnabled(False)
    #window.tabWidget_2.setTabEnabled(1, False)
    backupInterval = autoUpdate_Interval

    printH("CableUpdate: Start!", 0)
    if not ssdt.running():
        ssdt = threadPool.submit(saveStateDataTimer)
    while (cableUpdateEnabled and cableUpdateAllowed) or forceCableUpdate:
        try:
            currentTime = datetime.datetime(
                datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day,
                hour=datetime.datetime.now().time().hour,
                minute=datetime.datetime.now().time().minute,
                second=datetime.datetime.now().time().second,
                microsecond=0)
            '''if currentTime.minute == nextMinute:
                #start_timec = time.time()
                #saveStateDataTimer()
                #printH("Completed in " + str(time.time() - start_timec)[:5] + "s", 1, isRootEnd=True)

                if backupInterval < autoUpdate_Interval:
                    printH("Resuming regular update rate (-1s).", 1)
                    window.auto_doubleSpinBox.setValue(window.auto_doubleSpinBox.value() - 1)
                    autoUpdate_Interval = window.auto_doubleSpinBox.value()'''

            nextTime = (currentTime + datetime.timedelta(seconds=int(autoUpdate_Interval))).time()
            #nextMinute = currentTime.minute + 1
            start_time = time.time()

            aE = 0  # api error
            aF = 0  # api finished
            pE = 0  # plc error
            pF = 0  # plc finished
            Watcher0 = time.time()
            printH("Updating Cables...", 0)
            if plc.plc_stateOnly:
                if plc.plc_retry_success:
                    cableUpdateProceed = False
                    Watcher2 = time.time()
                    plc.PLC_Caller("GetAll", 0)  # Performs request 'GetCable' for all cable items
                    Watcher2 = time.time() - Watcher2
                    start_timeb = time.time()
                    t = 0
                    Watcher1 = time.time()
                    print("PLC Wait: Enter")
                    while not cableUpdateProceed:  # Wait for PLC process
                        if cableUpdateInterrupt or not plc.plc_retry_success:
                            print("PLC Wait: Error")
                            break

                        '''if t >= 1000:
                            printH("Retried", 2)
                            plc.PLC_Caller("GetAll", 0)
                            t = 0
                        t += 1''' #obsolete
                        time.sleep(0.001)
                        if stopRetry:
                            printH("Update interrupted", 1, "stop button")
                            break
                    print("PLC Wait: Exit")
                    Watcher1 = time.time() - Watcher1
                    if cableUpdateInterrupt:
                        not cableUpdateInterrupt
                        pE += 1
                    elif not plc.plc_retry_success:
                        cableUpdateInterrupt = True
                        break
                    else:
                        pF += 4
                printH("Completed in " + str(time.time() - start_timeb)[:5] + "s", 1)
            else:
                for i in range(0, cablecount):  # Does support double digit cables!
                    start_timeb = time.time()
                    printH("Cable" + str(i), 1, str(i + 1) + "/" + str(cablecount))
                    if plc.plc_retry_success:
                        cableUpdateProceed = False
                        plc.PLC_Caller("GetCable", i)  # Performs request 'GetCable' for all cable items
                        t = 0
                        while not cableUpdateProceed:  # Wait for PLC process
                            if cableUpdateInterrupt or not plc.plc_retry_success: break
                            if t >= 100:
                                printH("Retried", 2)
                                plc.PLC_Caller("GetCable", i)
                                t = 0
                            t += 1
                            time.sleep(0.01)
                            if stopRetry:
                                break
                        if cableUpdateInterrupt:
                            not cableUpdateInterrupt
                            pE += 1
                        elif not plc.plc_retry_success:
                            cableUpdateInterrupt = True
                            break
                        else:
                            pF += 1
                    printH("Completed in " + str(time.time() - start_timeb)[:5] + "s", 1)

                    if api.api_retry_success:
                        cableUpdateProceed = False
                        api.API_Caller("GetRider", i)  # Performs request 'GetRider' for all cable items
                        t = 0
                        while not cableUpdateProceed:  # Wait for API process
                            if cableUpdateInterrupt or not api.api_retry_success: break
                            if t >= 1000:
                                api.API_Caller("GetRider", i)
                                t = 0
                            t += 1
                            time.sleep(0.01)
                            if stopRetry:
                                break
                        if cableUpdateInterrupt:
                            not cableUpdateInterrupt
                            aE += 1
                        elif not api.api_retry_success:
                            cableUpdateInterrupt = True
                            break
                        else:
                            aF += 1
            if cableUpdateInterrupt:
                printH("Cable update interrupted! (" + str(time.time() - start_time)[:5] + "s)", 0,
                        "api:" + str(aF) + "/" + str(cablecount) + "(" + str(aE) + "E), " +
                        "plc:" + str(pF) + "/" + str(cablecount) + "(" + str(pE) + "E)",
                        isRootEnd=True)
                break
            else:
                printH("Cable update complete! (" + str(time.time() - start_time)[:5] + "s)", 0,
                        "api:" + str(aF) + "/" + str(cablecount) + "(" + str(aE) + "E), " +
                        "plc:" + str(pF) + "/" + str(cablecount) + "(" + str(pE) + "E)",
                        isRootEnd=True)
            if stopRetry:
                printH("Update interrupted", 1, "stop button")
                break
            Watcher0 = time.time() - Watcher0
            #Watcher.append([Watcher0, Watcher1, Watcher2, Watcher3])
            #print("Final time:", str(Watcher0)[:5], "\nWait time:", str(Watcher1)[:5], "\nCall Time:", str(Watcher2)[:5], "\nUpdate time:", str(Watcher3)[:5], "\nComplete time:" ,str(Watcher1+Watcher2+Watcher3)[:5])

            time.sleep(0.01)
            if time.time() - start_time > autoUpdate_Interval:
                print("Keep up: Enter")
                printH("MasterAPP cannot keep up! Reducing update rate by 1s.", 1, str(time.time() - start_time)[:5] + " > " + str(autoUpdate_Interval))
                time.sleep(0.1)
                #window.auto_doubleSpinBox.setValue(float(window.auto_doubleSpinBox.value() + 1))
                autoUpdate_Interval = window.auto_doubleSpinBox.value() + 1
                print("Keep up: Exit")
            forceCableUpdate = False

            state = []
            for i in range(len(CableItems)): # stores state of every update
                if str(CableDictionary[i]["CS"]).isnumeric():
                    state.append(int(CableDictionary[i]["CS"]))
                else:
                    state.append(3)

            minuteState[currentTime.second] = state

            currentTime = datetime.datetime.now().time()

            '''while currentTime < nextTime or (nextTime.hour == 0 and nextTime.minute == 0):
                newLabelTime = str(nextTime.second - datetime.datetime.now().time().second).zfill(2)
                if window.auto_label_1.text() != newLabelTime:
                    window.auto_label_1.setText(newLabelTime)
                time.sleep(0.1)
                #! Can trigger several times!
                if currentTime.hour == 0 and currentTime.minute == 0 and not clean:
                    while saveInProgress:
                        pass #Wait till save ends
                    window.StopButton(True)
                clean = True

                currentTime = datetime.datetime.now().time()
                if forceCableUpdate or not cableUpdateEnabled: break
            clean = False'''
            time.sleep(0.01)

            updateInProgress = False
            print("Wait: Enter")
            while currentTime < nextTime or saveInProgress:
                newLabelTime = str(nextTime.second - datetime.datetime.now().time().second).zfill(2)
                if window.auto_label_1.text() != newLabelTime:
                    window.auto_label_1.setText(newLabelTime)
                    time.sleep(0.01)
                currentTime = datetime.datetime.now().time()
                if currentTime.hour == 0 and currentTime.minute == 0:
                    window.StopButton(True)
                    break
                if forceCableUpdate or not cableUpdateEnabled: break
            updateInProgress = True
            window.auto_label_1.setText(str(0).zfill(2))
            print("Wait: Exit")

            if not cableUpdateEnabled:
                window.ss_label_1.setText(str(0).zfill(2))
                window.auto_label_1.setText(str(0).zfill(2))
                window.auto_doubleSpinBox.setEnabled(True)
                #window.tabWidget_2.setTabEnabled(1, True)
                break
            time.sleep(0.01)

        except Exception as err:
            updateInProgress = True
            printH(err)
            continue

    printH("CableUpdate: End!", 0)
    updateInProgress = False
    autoUpdate_Interval = backupInterval
    window.auto_doubleSpinBox.setValue(backupInterval)
cableUpdate = threadPool.submit(update_CableItems, True)

saveStateAllowed = False
def saveStateDataTimer(blank: bool = False):
    if blank: return

    global autoUpdate_Interval
    global forceSaveStateData
    global updateInProgress
    global minuteState
    global saveInProgress

    '''while datetime.datetime.now().time().second != 0: #synchronize to a minute
        if forceCableUpdate or not cableUpdateEnabled: break
        window.auto_label_1.setText(str(60 - datetime.datetime.now().time().second).zfill(2))
        time.sleep(1)'''
    backupInterval = autoUpdate_Interval

    minuteState = [[3]*len(CableItems)]*60
    nextMinute = None
    while saveStateAllowed or forceSaveStateData:
        currentTime = datetime.datetime(
        datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day,
        hour=datetime.datetime.now().time().hour,
        minute=datetime.datetime.now().time().minute,
        second=datetime.datetime.now().time().second,
        microsecond=0)

        if currentTime.minute == nextMinute or forceSaveStateData:
            print("sstd: Enter")
            forceSaveStateData = False
            while updateInProgress and (cableUpdateEnabled and cableUpdateAllowed) and plc.plc_retry_success:
                pass #Wait till update ends
            saveInProgress = True

            start_timec = time.time()

            saveStateData()
            printH("Completed in " + str(time.time() - start_timec)[:5] + "s", 1, isRootEnd=True)
            if (window.tabWidget_2.currentIndex() == 3):
                window.updateGraph1()
                time.sleep(0.01)

            window.ss_label_1.setText(str(0).zfill(2))
            minuteState = [[3]*len(CableItems)]*60

            if backupInterval < autoUpdate_Interval:
                printH("Resuming regular update rate (-1s).", 1)
                window.auto_doubleSpinBox.setValue(float(window.auto_doubleSpinBox.value() - 1))
                autoUpdate_Interval = window.auto_doubleSpinBox.value()

            saveInProgress = False
            print("sstd: Exit")
        time.sleep(.5)

        #nextTime = (currentTime + datetime.timedelta(seconds=int(autoUpdate_Interval))).time()
        nextMinute = currentTime.minute + 1

        window.ss_label_1.setText(str(60 - datetime.datetime.now().time().second).zfill(2))
ssdt = threadPool.submit(saveStateDataTimer, True)

# Imports new Cable information into tableWidget
def import_CableItemInfo(index=0, dictionary: dict={"CS": "", "RS": "", "IDR": "", "Position": "", "Speed": "", "Error": ""}, new=False):
    tableWidget: QtWidgets.QTableWidget
    tableWidget = CableItems[index].children()[3]
    image: QtWidgets.QLabel
    image = CableItems[index].children()[2]
    if index >= len(CableDictionary):
        d = {"I": index}
        d.update(dictionary)
        CableDictionary.append(d)

    if new or (dictionary["CS"] != "" and dictionary["CS"] != CableDictionary[index]["CS"]):
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
            printH("Cable" + str(index) + " State set on " + tableWidget.item(0, 0).text(), 10, isRootEnd=True)
        CableDictionary[index]["CS"] = dictionary["CS"]
    if new or (dictionary["RS"] != "" and dictionary["RS"] != CableDictionary[index]["RS"]):
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
            printH("Cable" + str(index) + " Rider state set on " + tableWidget.item(1, 0).text(), isRootEnd=True)
        CableDictionary[index]["RS"] = dictionary["RS"]
    if new or (dictionary["IDR"] != "" and dictionary["IDR"] != CableDictionary[index]["IDR"]):
        if dictionary["IDR"] != "":
            tableWidget.item(2, 0).setText(dictionary["IDR"])
        else:
            tableWidget.item(2, 0).setText("####")
        if not new:
            printH("Cable" + str(index) + " Rider ID set on " + tableWidget.item(2, 0).text(), isRootEnd=True)
        CableDictionary[index]["IDR"] = dictionary["IDR"]
    if new or (dictionary["Position"] != "" and dictionary["Position"] != CableDictionary[index]["Position"]):
        if dictionary["Position"] != "":
            tableWidget.item(3, 0).setText(str(int(dictionary["Position"])) + "m")
        else:
            tableWidget.item(3, 0).setText("0m")
        if not new:
            printH("Cable" + str(index) + " Position set on " + tableWidget.item(4, 0).text(), isRootEnd=True)
        CableDictionary[index]["Position"] = dictionary["Position"]
    if new or (dictionary["Speed"] != "" and dictionary["Speed"] != CableDictionary[index]["Speed"]):
        if dictionary["Speed"] != "":
            tableWidget.item(4, 0).setText(str(int(dictionary["Speed"])) + "km/h")
        else:
            tableWidget.item(4, 0).setText("0km/h")
        if not new:
            printH("Cable" + str(index) + " Speed set on " + tableWidget.item(5, 0).text(), isRootEnd=True)
        CableDictionary[index]["Speed"] = dictionary["Speed"]
    if new or (dictionary["Error"] != "" and dictionary["Error"] != CableDictionary[index]["Error"]):
        if dictionary["Error"] != "":
            tableWidget.item(5, 0).setText("X " + dictionary["Error"])
        else:
            tableWidget.item(5, 0).setText("X 0000")
        if not new:
            printH("Cable" + str(index) + " Error set on " + tableWidget.item(6, 0).text(), isRootEnd=True)
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
            time.sleep(1)
            testresponse = plc.PLC_Response(1)[2:5]
            if testresponse is False:
                raise Exception('Could not read response')

            if (testresponse[0] != 9 or testresponse[1] != 9 or testresponse[2] != 9):
                printH(
                    "An error occurred while connecting to PLC " +
                    "PLC instance did not respond with '999'",
                    4, "Unsupported response format: " + str(testresponse))
                return False
            else:
                return True
        elif server == "api":
            success, reason = api.API_Request("888")
            if not success: #Sends Http test message
                raise Exception('Could not send request: ' + str(reason)) # Raises error when channel is already in use
            time.sleep(1)
            success, reason = api.API_Response()
            if not success:
                raise Exception('Could not read response: API - ' + str(reason))
            testresponse = response
            if testresponse[0] != 9 or testresponse[1] != 9 or testresponse[2] != '9':
                printH(
                    "An error occurred while connecting to API. " +
                    "API instance did not respond with '999'",
                    4, "Unsupported response format: " + str(testresponse))
                return False
            else:
                return True
        elif server == "ax":
            pass
    except Exception as err:
        return err
    pass

# ##HISTORY
# Prints an item in historyList. !Processed in the MainThread!
lastLevel = 0
hTuple = None
logFilePath = None
hItemCount = 0
def printH(string: str, level=lastLevel, description="", isRootEnd=False, inPool=False, blank = False):
    if blank: return
    global lastLevel
    global pr

    global parentitem
    global parentTree
    global hTuple
    global hItemCount
    '''try:
        print("Print: Enter - " + string)
        if not inPool:
            while not pr.done():
                pass
            pr = threadPool.submit(printH, string, level, description, isRootEnd, True)
            return

        if description != "":
            description = "(" + description + ")"
        if level == 100:
            level = lastLevel + 1

        if level == 0:
            newline = "\n" + str(datetime.datetime.today().strftime("%Y:%m:%d")) + "/" + str(datetime.datetime.today().strftime("%H:%M:%S")) + ": " + " "*level + string + " - " + description
            lastLevel = 0
        else:
            newline = "  "*level + "— "+ string + " - " + description
            lastLevel = level
        print("Print: Test1")
        window.historyList.append(newline)
        window.historyList.moveCursor(QtGui.QTextCursor.End)

        print("Print: Test2")
        #print(newline)
        newline = newline + "\n"
        with open(logFilePath, 'a') as logfile:
            print("Print: Test3")
            logfile.write(newline)
            logfile.close()
        print("Print: Exit - " + string)
    except:
        pass'''

    if not isinstance(threading.current_thread(), threading._MainThread):
        hTuple = (string, level, description, isRootEnd)
        pHistory.start()
        time.sleep(0.001) #Delay from the previous printH
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
        dateItem.setText(0, str(datetime.datetime.today().strftime("%H:%M:%S")))
        dateItem.setText(1, str(datetime.datetime.today().strftime("%Y:%m:%d")))
        window.historyList.addTopLevelItem(dateItem)
        dateItem.addChild(rootItem)
        print(datetime.datetime.today().strftime("%H:%M:%S"), datetime.datetime.today().strftime("%Y:%m:%d"))
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
pr = threadPool.submit(printH, blank=True)
pHistory.pH.connect(printH)

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
    #if saveInProgress: return

    if saveStateAllowed or forceSaveStateData == True:
        forceSaveStateData = False

        if saveStyle == 0 or cablecount == 0: # Don't save
            #saveInProgress = False
            return
        print("Check1")
        #Check time
        dateTime = datetime.datetime.now()
        if dateTime.second >= 30:
            newTime = dateTime + datetime.timedelta(
                minutes=1,
                seconds=-dateTime.second,
                microseconds=-dateTime.microsecond)
        else:
            newTime = dateTime + datetime.timedelta(
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
            savedText = ""
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
                    savedText = savedText + line
            printH(savedText, 2, dataPath)
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

# Call start on first launch
mainWindow.show()
window.StartPart1()

app.aboutToQuit.connect(window.StopButton)
sys.exit(app.exec_())

