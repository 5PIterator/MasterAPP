from math import ceil
from time import time
import numpy, threading
from pyModbusTCP.client import ModbusClient
from ToMainThreadV2 import toMainThread


class LRLClient():
    def __init__(self,
        client: ModbusClient = None,
        name:str = "MAIN",
        host:str = None,
        port:int = None,
        highestAddress:int = 1000,
        transferLimit:int = 100,
        HREG=False, IREG=False, DINP=False, COIL=False
        ):
        self._name = name
        self._host = host
        self._port = port
        self._client = client
        self._highestAddress = highestAddress
        self._transferLimit = transferLimit
        self._transferSize = 100

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
        i = 1
        self._transferSize = self._highestAddress
        while self._transferSize > self._transferLimit:
            self._transferSize = ceil(self._highestAddress / i)
            i += 1
        self._localHoldingRegisters = [0 for _ in range(self._highestAddress)]
        self._localInputRegisters = [False for _ in range(self._highestAddress)]
        self._localDiscreteInputs = [0 for _ in range(self._highestAddress)]
        self._localCoils = [False for _ in range(self._highestAddress)]

busy = False
readTime = 0
writeTime = 0
clientList = {}

def add_client(
    name: str,
    client:ModbusClient=None,
    host=None,
    port=None,
    highestAddress=1000,
    transferLimit=100,
    HReg=False, IReg=False, DInp=False, Coil=False
    ):
    """Adds/overwrites a handled client to the clientList.\nEither use already estabilished 'ModbusClient' or fill out 'host', 'port'\n
    decide which registers/bits you wish this clien to operate with: default all"""
    if client is None:
        client = ModbusClient(host, port)
    clientList[name] = LRLClient(client, name, host, port, highestAddress, transferLimit, HReg, IReg, DInp, Coil)
    clientList[name].setup_localRegisters()

def remove_client(name: str):
    clientList.pop(name)

def UpdateLibrary():
    """Updates the internal '_localRegisters' database of every 'LRLClient' in 'clientList'"""
    global busy
    while busy:
        continue
    busy = True
    #while newRegisters != localRegisters:
    start_time = time()
    for client in list(clientList.values()): # For every client in clientList
        client: LRLClient
        client.get_client().open()

        t = 0
        timeout = 5
        while  t < timeout:
            if (
                len(client._newRegisters) > 0 or
                len(client._newCoils) > 0 or
                len(client._newRegisterSet) > 0 or
                len(client._newCoilSet) > 0
                ):
                if WriteLibrary(client, True):
                    pass
                    """client._newRegisters = []
                    client._newRegisterSet = []"""
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
        fin = time() - start_time
        client.get_client().close()
        client._newRegisters = []
        client._newRegisterSet = []
        print("Update: read-" + str(format(readTime,'.4f')) + ", write-" + str(format(writeTime,'.4f')) + " ("+ client._name +")")
    busy = False
    return True
def ReadLibrary(client:LRLClient, fromUpdate=False):
    global readTime
    start_time = time()

    holdingReg = []
    inputReg = []
    discreteIn = []
    coils = []
    i = 0
    t = 0
    timeout = 10
    while i < client._highestAddress and t < timeout:
        try:
            if not client.get_client().is_open():
                if not client.get_client().open():
                    return False
            if client._readHoldingRegisters: holdingReg.extend(client.get_client().read_holding_registers(i, client._transferSize))
            if client._readInputRegisters: inputReg.extend(client.get_client().read_discrete_inputs(i, client._transferSize))
            if client._readDiscreteInputs: discreteIn.extend(client.get_client().read_input_registers(i, client._transferSize))
            if client._readCoils: coils.extend(client.get_client().read_coils(i, client._transferSize))
        except:
            t += 1
        else:
            i += client._transferSize
            t = 0
    if client._readHoldingRegisters: client._localHoldingRegisters = holdingReg
    if client._readInputRegisters: client._localDiscreteInputs = inputReg
    if client._readDiscreteInputs: client._localInputRegisters = discreteIn
    if client._readCoils: client._localCoils = coils
    readTime = time() - start_time

    if not fromUpdate:
        client.get_client().close()

    if t < timeout:
        return True
    else:
        return False
def WriteLibrary(client:LRLClient, fromUpdate=False):
    start_time = time()
    t = 0
    timeout = 10

    if not ReadLibrary(client, True):
        return False

    while t < timeout:
        try:
            #register = None

            for i, reg in enumerate(client._newRegisters):
                address, value, wordIndex = reg
                if not client.get_client().is_open():
                    if not client.get_client().open():
                        return False
                    
                if wordIndex is not None:
                    #if register is None or address != client._newRegisters[i-1][0]: 
                    register = client._localHoldingRegisters[address]  

                    if registerToWord(register, wordIndex) == str(value):
                        continue

                    oldWord = registerToWord(register)
                    word = oldWord[:wordIndex] + str(value) + oldWord[wordIndex + 1:]
                    register = int(word[::-1], 2)
                    client._newRegisters[i] = (address, register, None)

                else:
                    register = value
                    
                client.get_client().write_single_register(address, register) 
                client._localHoldingRegisters[address] = register

            for regList in client._newRegisterSet:
                firstAddress, registers = regList
                if not client.get_client().is_open():
                    if not client.get_client().open():
                        return False
                client.get_client().write_multiple_registers(firstAddress, registers)

            for coi in client._newCoils:
                address, coil = coi
                if not client.get_client().is_open():
                    if not client.get_client().open():
                        return False
                client.get_client().write_single_coil(address, coil)

            for coilList in client._newCoilSet:
                firstAddress, coils = coilList
                if not client.get_client().is_open():
                    if not client.get_client().open():
                        return False
                client.get_client().write_multiple_coils(firstAddress, coils)
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
def setRegister(client:str, regType:str, address:int, value, wordIndex:int=None, forceByWrite=False):
    '''Sets value of the target register to 'value' if 'wordIndex' is None\n
    Otherwise it will treat register as a word and sets target index of the word to 'value'\n
    register types:
    HREG - HoldingRegister
    COIL - Coils'''
    if regType != "HREG" and regType != "COIL":
        raise Exception("setRegister(): '"+ str(regType) + "' is not a valid register type")
    global busy
    client: LRLClient = clientList[client]

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
    for i, set in enumerate(newRegister[regType]): #Grab written registerset
        if set[0] == address:
            registers = set[1]
            writtenReg = i
            break

    if writtenReg is None: # if there is no written registerSet, create new registerset to send
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
    word = list(word)
    for i in range(len(word)):
        word[i] = bool(int(word[i]))
    return word