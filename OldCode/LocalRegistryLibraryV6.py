from math import ceil
from socket import timeout
from time import time
from pyModbusTCP.client import ModbusClient


class LRLClient():
    def __init__(self, client: ModbusClient = None, name:str = "MAIN", host:str = None, port:int = None, highestAddress:int = 1000, transferLimit:int = 100):
        self._name = name
        self._host = host
        self._port = port
        self._client = client
        self._highestAddress = highestAddress
        self._transferLimit = transferLimit
        self._transferSize = 100
        self._localRegisters = []
        self._newRegisters = []
        self._newRegisterSet = []

    # client method
    def get_client(self):
        return self._client
    def set_client(self, x):
        self._client = x
        self.setup_localRegisters()

    # host method
    def get_host(self):
        return self._host
    def set_host(self, x):
        self._host = x
        self._client.host(self._host)

    # port method
    def get_port(self):
        return self._port
    def set_port(self, x):
        self._client.port(self._port)
        self._port = x

    # highestAddress method
    def get_highestAddress(self):
        return self._highestAddress
    def set_highestAddress(self, x):
        self._highestAddress = x
        self.setup_localRegisters()

    # transferLimit method
    def get_transferLimit(self):
        return self._transferLimit
    def set_transferLimit(self, x):
        self._transferLimit = x
        self.setup_localRegisters()

    def setup_localRegisters(self):
        i = 1
        self._transferSize = self._highestAddress
        while self._transferSize > self._transferLimit:
            self._transferSize = ceil(self._highestAddress / i)
            i += 1
        self._localRegisters = [0 for _ in range(self._highestAddress)]

busy = False
readTime = 0
writeTime = 0
clientList = {
}

def add_client(name: str, client:ModbusClient=None, host=None, port=None, highestAddress=1000, transferLimit=100):
    """Adds a handled client to the clientList.\nEither use already estabilished 'client' or fill out 'host', 'port'"""
    clientList[name] = LRLClient(client, name, host, port, highestAddress, transferLimit)
    clientList[name].setup_localRegisters()

def remove_client(name: str):
    clientList.pop(name)

"""def SetupLibrary(com, mes, maxTransfer:int=100):
    global highestAddress
    global transferSize
    global clientList
    global localRegisters
    global newRegisters

    if list(clientList.values()).count() == 0: raise Exception("LRLibrary: Client list is empty! Add client using 'add_client()'!")

    for client in list(clientList.values()):
        client.


    '''plc_server = com.plc_server
    highestAddress = max(com.regParameters) + mes.samplelenght'''

    i = 1
    transferSize = highestAddress
    while transferSize > maxTransfer:
        transferSize = ceil(highestAddress / i)
        i += 1
    localRegisters = [None for _ in range(highestAddress)]
    pass"""

def UpdateLibrary():
    """Updates the internal '_localRegisters' database of every 'LRLClient' in 'clientList'"""
    global busy
    while busy:
        continue
    busy = True
    #while newRegisters != localRegisters:

    for client in list(clientList.values()): # For every client in clientList
        while True:
            if WriteLibrary(client, True):
                client._newRegisters = []
                client._newRegisterSet = []
            else:
                print("Update: Failure ("+ client._name +")")
                if client._name == "MAIN":
                    busy = False
                    return False

            if ReadLibrary(client, True):
                pass
            else:
                print("Update: Failure ("+ client._name +")")
                if client._name == "MAIN":
                    busy = False
                    return False
            if len(client._newRegisters) == 0 or all([client._localRegisters[message[0]] == message[1] for message in client._newRegisters]):
                break
        client.get_client().close()
        client._newRegisters = []
        client._newRegisterSet = []
        print("Update: read-" + str(format(readTime,'.4f')) + ", write-" + str(format(writeTime,'.4f')) + " ("+ client._name +")")
    busy = False
    return True

def ReadLibrary(client:LRLClient, fromUpdate=False):
    global readTime
    start_time = time()

    registers = []
    i = 0
    t = 0
    timeout = 10
    while i < client._highestAddress and t < timeout:
        try:
            if not client.get_client().is_open():
                if not client.get_client().open():
                    return False
            registers.extend(client.get_client().read_holding_registers(i, client._transferSize))
        except:
            t += 1
        else:
            i += client._transferSize
            t = 0
    client._localRegisters = registers
    readTime = time() - start_time

    if not fromUpdate:
        client.get_client().close()

    if t < timeout:
        return True
    else:
        return False
    pass
def WriteLibrary(client:LRLClient, fromUpdate=False):
    start_time = time()
    t = 0
    timeout = 10
    while t < timeout:
        try:
            for reg in client._newRegisters:
                address, register = reg
                if not client.get_client().is_open():
                    if not client.get_client().open():
                        return False
                client.get_client().write_single_register(address, register)

            for regList in client._newRegisterSet:
                firstAddress, registers = regList
                if not client.get_client().is_open():
                    if not client.get_client().open():
                        return False
                client.get_client().write_multiple_registers(firstAddress, registers)
        except:
            t += 1
            continue
        else:
            break
    writeTime = time() - start_time

    if not fromUpdate:
        client._newRegisters = []
        client._newRegisterSet = []
    if t < timeout:
        return True
    else: return False