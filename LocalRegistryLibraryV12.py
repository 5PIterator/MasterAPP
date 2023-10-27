from time import time
from typing import Dict
import numpy, threading
from pyModbusTCP.client import ModbusClient
from concurrent.futures import ThreadPoolExecutor


class LRLClient():
    def __init__(self,
        client: ModbusClient = None,
        name:str = "MAIN",
        host:str = None,
        port:int = None,
        highestAddress:int = 1000,
        transferLimit:int = 125,
        HREG=False, IREG=False, DINP=False, COIL=False
        ):
        self._name = name
        self._host = host
        self._port = port
        self._client = client
        self._highestAddress = highestAddress
        self._transferLimit = transferLimit
        self._transferSize = 125

        self._localHoldingRegisters = []
        self._localInputRegisters = []
        self._localDiscreteInputs = []
        self._localCoils = []

        self._newRegisters = []
        self._newCoils = []
        self._newRegisterSet = []
        self._newCoilSet = []

        self._readHoldingRegisters = HREG
        self._readInputRegisters = IREG
        self._readDiscreteInputs = DINP
        self._readCoils = COIL

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
        self._transferSize = self._transferLimit
        self._localHoldingRegisters = [0 for _ in range(self._highestAddress)]
        self._localInputRegisters = [False for _ in range(self._highestAddress)]
        self._localDiscreteInputs = [0 for _ in range(self._highestAddress)]
        self._localCoils = [False for _ in range(self._highestAddress)]

busy = False
libTime = 0
clientList: Dict[str, LRLClient] = {}
threadpool = ThreadPoolExecutor(3)
def add_client(
    name: str,
    client:ModbusClient=None,
    host=None,
    port=502,
    highestAddress=1000,
    transferLimit=100,
    HReg=False, IReg=False, DInp=False, Coil=False
    ):
    """Adds/overwrites a handled client to the clientList.\nEither use already established 'ModbusTcpClient' or fill out 'host', 'port'\n
    decide which registers/bits you wish this client to operate with: default none"""
    if client is None:
        client = ModbusClient(host, port)
    clientList[name] = LRLClient(client, name, host, port, highestAddress, transferLimit, HReg, IReg, DInp, Coil)
    clientList[name].setup_localRegisters()

def remove_client(name: str):
    clientList.pop(name)

def UpdateLibrary():
    """
    Updates the internal '_localRegisters' database of every 'LRLClient' in 'clientList'
    """
    global busy
    global libTime
    libTime = 0
    task_results = []
    def get_client_data(client: LRLClient):
        readTime = 0
        writeTime = 0

        if not client.get_client().is_open:
            if not client.get_client().open():
                task_results.append(False)
                return False

        start_time2 = time()
        t = 0
        timeout = 5
        while  t < timeout:
            # READING
            result = ReadLibrary(client, True)
            if result:
                readTime += result
            else:
                print("Update: Failure ("+ client._name +")")
                if client._name == "MAIN":
                    task_results.append(False)
                    return False
            # WRITING
            if (
                len(client._newRegisters) > 0 or
                len(client._newCoils) > 0 or
                len(client._newRegisterSet) > 0 or
                len(client._newCoilSet) > 0
                ):
                result = WriteLibrary(client, True)
                if result:
                    writeTime += result
                else:
                    print("Update: Failure ("+ client._name +")")
                    if client._name == "MAIN":
                        task_results.append(False)
                        return False
            if len(client._newRegisters) > 1:
                last_occurrences = {}
                for address, value, wordIndex in reversed(client._newRegisters):
                    if address in last_occurrences:
                        continue  # skip duplicates
                    last_occurrences[address] = (value, wordIndex)
                new_registers = [(addr, val, idx) for addr, (val, idx) in last_occurrences.items()]
                client._newRegisters = new_registers[::-1]
            if len(client._newCoils) > 1:
                last_occurrences = {}
                for address, value, wordIndex in reversed(client._newCoils):
                    if address in last_occurrences:
                        continue  # skip duplicates
                    last_occurrences[address] = (value, wordIndex)
                new_registers = [(addr, val, idx) for addr, (val, idx) in last_occurrences.items()]
                client._newCoils = new_registers[::-1]

            regSent = [client._localHoldingRegisters[message[0]] == message[1] for message in client._newRegisters]
            coilSent = [client._localCoils[message[0]] == message[1] for message in client._newCoils]

            if (all(regSent) and all(coilSent)): # check if message was sent
                break
            t += 1
        #client.get_client().close()
        client._newRegisters = []
        client._newRegisterSet = []
        clientTime = time() - start_time2
        print("clientTime: read-%fs, write-%fs, total-%fs (%s)" % (round(readTime,4), round(writeTime,4), round(clientTime,4), client._name))
        task_results.append(True)
        return True

    while busy:
        return False
    busy = True
    start_time = time()

    threads = []
    for client in list(clientList.values()):
        thread = threading.Thread(target=get_client_data, name=("lib"+client._name), args=(client,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    #current_tasks = [threadpool.submit(get_client_data, client) for client in list(clientList.values())] # For every client in clientList
    #task_results = [task.result() for task in current_tasks]

    libTime = time() - start_time
    print("libTime: total-%fs" % (round(libTime,2)))
    busy = False

    # check task result, if not all are True = error
    if not all(task_results):
        return False
    return True
def ReadLibrary(client:LRLClient, fromUpdate=False):
    start_time = time()

    holdingReg = []
    inputReg = []
    discreteIn = []
    coils = []
    i = 0
    t = 0
    timeout = 3
    reqLimit = 125
    hit_start = time()
    while t < timeout:
        try:
            for i in range(0, client._highestAddress + 1, reqLimit):
                if not client.get_client().is_open:
                    if not client.get_client().open():
                        return False
                if client._readHoldingRegisters: holdingReg.extend(client.get_client().read_holding_registers(i, reqLimit))
                if client._readInputRegisters: inputReg.extend(client.get_client().read_input_registers(i, reqLimit))
                if client._readDiscreteInputs: discreteIn.extend(client.get_client().read_discrete_inputs(i, reqLimit))
                if client._readCoils: coils.extend(client.get_client().read_coils(i, reqLimit))
        except:
            t += 1
        else:
            t = 0
            break
    hit_end = time() - hit_start

    if client._readHoldingRegisters: client._localHoldingRegisters = holdingReg
    if client._readInputRegisters: client._localInputRegisters = inputReg
    if client._readDiscreteInputs: client._localDiscreteInputs = discreteIn
    if client._readCoils: client._localCoils = coils
    if not fromUpdate:
        client.get_client().close()

    if t < timeout:
        return time() - start_time
    else:
        return False
def WriteLibrary(client:LRLClient, fromUpdate=False):
    result = 0
    t = 0
    timeout = 3
    while t < timeout:
        try:
            #register = None
            start_time = time()

            for i, reg in enumerate(client._newRegisters):
                address, value, wordIndex = reg
                if not client.get_client().is_open:
                    if not client.get_client().open():
                        return False

                if wordIndex is not None:
                    #if register is None or address != client._newRegisters[i-1][0]:
                    register = client._localHoldingRegisters[address]

                    if registerToWord(register, wordIndex) == str(value):
                        client._newRegisters[i] = (address, register, None)
                        continue

                    oldWord = registerToWord(register)
                    word = oldWord[:wordIndex] + str(value) + oldWord[wordIndex + 1:]
                    register = int(word[::-1], 2)
                    client._newRegisters[i] = (address, register, None)

                else:
                    register = value

                client.get_client().write_single_register(address, register)
                #client._localHoldingRegisters[address] = client.get_client().read_holding_registers(address, 1)[0]

            result = time() - start_time
            for regList in client._newRegisterSet:
                firstAddress, registers = regList
                if not client.get_client().is_open:
                    if not client.get_client().open():
                        return False
                client.get_client().write_multiple_registers(firstAddress, registers)

            for coi in client._newCoils:
                address, coil = coi
                if not client.get_client().is_open:
                    if not client.get_client().open():
                        return False
                client.get_client().write_single_coil(address, coil)

            for coilList in client._newCoilSet:
                firstAddress, coils = coilList
                if not client.get_client().is_open:
                    if not client.get_client().open():
                        return False
                client.get_client().write_multiple_coils(firstAddress, coils)
        except:
            t += 1
            continue
        else:
            t = 0
            break

    '''if not ReadLibrary(client, True):
        return False'''
    if not fromUpdate:
        client._newRegisters = []
        client._newRegisterSet = []
    if t < timeout:
        return result
    else: return False

def getRegisters(client:str, regType:str, address:int, amount:int=None):
    '''Gets a register from the LocalRegisterLibrary\n
    If 'amount' has value, returns list of registers\n
    register types:
    HREG - HoldingRegister
    IREG - InputRegister
    DINP - DiscreteInput
    COIL - Coils'''
    if regType != "HREG" and regType != "COIL" and regType != "IREG" and regType != "DINP":
        raise Exception("setRegister(): '"+ str(regType) + "' is not a valid register type")
    global busy

    client: LRLClient = clientList[client]

    while busy:
        continue
    busy = True
    localRegister = {
        "HREG": client._localHoldingRegisters,
        "IREG": client._localInputRegisters,
        "DINP": client._localDiscreteInputs,
        "COIL": client._localCoils,
    }

    if amount is None:
        """if debug:
            if slot == "L1P" or slot == "L1F":
                registers = AMP.GenerateNoise(slot, 1, (10000, 0))
            elif slot == "L2P" or slot == "L2F":
                registers = AMP.GenerateNoise(slot, 1, (10000, 0))
            elif slot == "R1P" or slot == "R1F":
                registers = AMP.GenerateNoise(slot, 1, (10000, 0))
            elif slot == "R2P" or slot == "R2F":
                registers = AMP.GenerateNoise(slot, 1, (10000, 0))
        else:
            if readServer:
                registers = DataBank.get_words(address)[0]
            else:
                registers = client._localRegisters[address]
            # registers = self.plc_server.read_holding_registers(address, 1)[0]
            registers = numpy.int16(registers)"""
        registers = localRegister[regType][address]
        if regType == "HREG" or regType == "IREG":
            registers = numpy.int16(registers)

    else:
        """if debug:
            if slot == "L1P" or slot == "L1F":
                registers = AMP.GenerateNoise(slot, amount, (10000, 0))
            elif slot == "L2P" or slot == "L2F":
                registers = AMP.Generate(slot, amount, (10000, 0))
            elif slot == "R1P" or slot == "R1F":
                registers = AMP.GenerateNoise(slot, amount, (10000, 0))
            elif slot == "R2P" or slot == "R2F":
                registers = AMP.GenerateNoise(slot, amount, (10000, 0))
        else:
            if readServer:
                registers = DataBank.get_words(address, amount)
            else:"""
        registers = localRegister[regType][address:address+amount]
        if regType == "HREG" or regType == "IREG":
            registers = [numpy.int16(value) for value in registers]

    busy = False
    return registers
def setRegister(clientName:str, regType:str, address:int, value, wordIndex:int=None, forceByWrite=False):
    '''Sets value of the target register to 'value' if 'wordIndex' is None\n
    Otherwise it will treat register as a word and sets target index of the word to 'value'\n
    register types:
    HREG - HoldingRegister
    COIL - Coils'''
    if regType != "HREG" and regType != "COIL":
        raise Exception("setRegister(): '"+ str(regType) + "' is not a valid register type")
    global busy
    client: LRLClient = clientList[clientName]

    #if not isinstance(threading.current_thread(), threading._MainThread) and not forceByWrite: # a check to ensure the mainThread isn't paused
    while busy :
        continue
    busy = True

    localRegister = {
        "HREG": client._localHoldingRegisters,
        "COIL": client._localCoils
    }
    newRegister = {
        "HREG": client._newRegisters,
        "COIL": client._newCoils
    }
    writtenReg = None
    register = None

    """if writeToServer:
        register = DataBank.get_words(address)[0]
    else:"""
    for i, reg in enumerate(newRegister[regType]): #Grab already written register
        if reg[0] == address:
            register = reg[1]
            writtenReg = i
            break
    if register is None: # if empty, update library and assign new register
        register = localRegister[regType][address]

    if regType == "HREG":
        if wordIndex is None:
            register = numpy.uint16(value)
        else:
            if forceByWrite: # continued by writeLibrary
                oldWord = registerToWord(register)
                word = oldWord[:wordIndex] + str(value) + oldWord[wordIndex + 1:]
                register = int(word[::-1], 2)
                wordIndex = None
            else:
                register = numpy.int16(value) # assign temporary value

    if wordIndex is not None: # if working with a word, send wordIndex and value
        client._newRegisters.append((address, register, wordIndex))
    elif writtenReg is None: # if grabbed from last read, create new register to send
        client._newRegisters.append((address, register, None))
    else: # if grabbed from written reg, overwrite
        newRegister[regType][writtenReg] = (address, register, None)

    #if not isinstance(threading.current_thread(), threading._MainThread) and not forceByWrite:
    busy = False
    return (address, register, wordIndex)
def setRegisters(client:str, regType:str, address:int, registers:list):
    '''Sets values of the target list of registers to 'registers'\n
    register types:
    HREG - HoldingRegister
    COIL - Coils'''
    if regType != "HREG" and regType != "COIL":
        raise Exception("setRegister(): '"+ str(regType) + "' is not a valid register type")
    global busy
    while busy:
        continue
    busy = True

    client: LRLClient = clientList[client]

    """localRegister = {
        "HREG": client._localHoldingRegisters,
        "COIL": client._localCoils
    }"""
    newRegister = {
        "HREG": client._newRegisterSet,
        "COIL": client._newCoilSet
    }
    if regType == "HREG":
        for i, reg in enumerate(registers):
            registers[i] = numpy.uint16(reg)


    '''if writeToServer:
        registers = DataBank.set_words(address, registers)
    else:'''
    writtenReg = None
    for i, set in enumerate(newRegister[regType]): #Grab written register_set
        if set[0] == address:
            registers = set[1]
            writtenReg = i
            break

    if writtenReg is None: # if there is no written registerSet, create new register_set to send
        newRegister[regType].append((address, registers))
    else: # if grabbed from written reg, overwrite
        newRegister[writtenReg] = (address, registers)
    busy = False

def registerToWord(register, wordIndex=None, length=12):
    '''Returns register as a word
    if 'wordIndex' has value, will return only value'''
    if wordIndex is None:
        word = bin(register)[2:].rjust(length, '0')[::-1]
    else:
        word = bin(register)[2:].rjust(length, '0')[::-1][wordIndex]
    return word
def wordToList(word:str):
    '''returns a word as an array of bool'''
    result = list(word)
    for i in range(len(result)):
        result[i] = bool(int(result[i]))
    return result