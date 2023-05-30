import os, threading
from configparser import ConfigParser
from cryptography.fernet import Fernet
from PyQt5 import QtWidgets
from ToMainThreadV1 import FuncToMain


configFiles = {
    #'MAIN': (ConfigParser(), "configFiles/configMAIN"),
}
settingsDict = {}
_expressing = False

def addFile(name, filePath=None):
    '''Adds a file to managed configFiles. configFiles[name][0/1 - ConfigParser/filepath]'''
    global configFiles
    if filePath is None:
        filePath = "configFiles/config" + name
    configFiles[name] = (ConfigParser(), filePath)
def addSection(fileName, sectionName):
    '''Adds a section to the managed configFile. settingsDict[section]["FILE"] - configFiles'''
    global configFiles
    global settingsDict
    if fileName not in configFiles.keys():
        addFile(fileName)
    if sectionName not in settingsDict.keys():
        settingsDict[sectionName] = {}

    settingsDict[sectionName]["FILE"] = configFiles[fileName]
    pass
def addOption(sectionName, optionName, defValue=None, QtObject=None, encryption=None):
    '''Adds an option to a section of the managed configFile. settingsDict[section][option][0/1/2 - defValue/QtObject/byteKey]'''
    global configFiles
    global settingsDict

    if sectionName not in settingsDict.keys():
        addSection("MAIN", sectionName)
    settingsDict[sectionName][optionName] = [defValue, QtObject, encryption]

def loadSettings():
    print("loadSettings", "(Enter)")
    checkConfigFile()
    # Load Config
    for section in settingsDict.keys():
        for option in settingsDict[section].keys():
            if option == "FILE": continue
            widgetType = type(settingsDict[section][option][1])
            if widgetType == QtWidgets.QLineEdit or widgetType == QtWidgets.QLabel:
                settingsDict[section][option][0] = settingsDict[section]['FILE'][0].get(section, option)
            elif widgetType == QtWidgets.QSpinBox or widgetType == QtWidgets.QComboBox:
                settingsDict[section][option][0] = settingsDict[section]['FILE'][0].getint(section, option)
            elif widgetType == QtWidgets.QDoubleSpinBox:
                settingsDict[section][option][0] = settingsDict[section]['FILE'][0].getfloat(section, option)
            elif widgetType == QtWidgets.QCheckBox:
                settingsDict[section][option][0] = settingsDict[section]['FILE'][0].getboolean(section, option)

            if settingsDict[section][option][2] is not None: # of option is encrypted, decrypt with Fernet
                if settingsDict[section]['FILE'][0].get(section, option) == '':
                    settingsDict[section][option][0] =  settingsDict[section]['FILE'][0].get(section, option)
                else:
                    settingsDict[section][option][0] = Fernet(settingsDict[section][option][2]).decrypt(bytes(settingsDict[section]['FILE'][0].get(section, option) + '=', 'utf8')).decode('utf8')

    expressValues()
    print("loadSettings", "(FIN)")
def expressValues():
    '''Updates the QtObjects with settingsDict. !Processed in the MainThread!'''
    global _expressing
    if _expressing: return False
    _expressing = True

    if not isinstance(threading.current_thread(), threading._MainThread):
        FuncToMain(expressValues)
        return
    for section in settingsDict.keys():
        for option in settingsDict[section].keys():
            widgetType = type(settingsDict[section][option][1])
            if widgetType == QtWidgets.QLineEdit or widgetType == QtWidgets.QLabel:
                settingsDict[section][option][1].setText(str(settingsDict[section][option][0]))
            elif widgetType == QtWidgets.QSpinBox or widgetType == QtWidgets.QDoubleSpinBox:
                settingsDict[section][option][1].setValue(settingsDict[section][option][0])
            elif widgetType == QtWidgets.QComboBox:
                settingsDict[section][option][1].setCurrentIndex(int(settingsDict[section][option][0]))
            elif widgetType == QtWidgets.QCheckBox:
                settingsDict[section][option][1].setChecked(bool(settingsDict[section][option][0]))
    _expressing = False
    return True

def getValues(saveToFile=True, exprSettings=False):
    '''Updates the settingsDict from Qobjects. \n
    saveToFile -    If True, will automatically write into configFiles
    exprSettings -  If true, will update QtObjects
    '''
    if _expressing: return
    for section in settingsDict.keys():
        for option in settingsDict[section].keys():
            if option == "FILE": continue
            # synchronization
            widgetType = type(settingsDict[section][option][1])
            if widgetType == QtWidgets.QLineEdit:
                settingsDict[section][option][0] = str(settingsDict[section][option][1].text())
            elif widgetType == QtWidgets.QSpinBox:
                settingsDict[section][option][0] = int(settingsDict[section][option][1].value())
            elif widgetType == QtWidgets.QDoubleSpinBox:
                settingsDict[section][option][0] = float(settingsDict[section][option][1].value())
            elif widgetType == QtWidgets.QComboBox:
                settingsDict[section][option][0] = int(settingsDict[section][option][1].currentIndex())
            elif widgetType == QtWidgets.QCheckBox:
                settingsDict[section][option][0] = bool(settingsDict[section][option][1].isChecked())
    if exprSettings:
        expressValues()
    if saveToFile:
        saveToConfig()

def saveToConfig():
    # Prepare to write file
    if _expressing: return
    for section in settingsDict.keys():
        for option in settingsDict[section].keys():
            if option == "FILE": continue
            if settingsDict[section][option][2] is not None:
                settingsDict[section]['FILE'][0].set(section, option, Fernet(settingsDict[section][option][2]).encrypt(bytes(settingsDict[section][option][0], 'utf8')).decode('utf8'))
            else:
                settingsDict[section]['FILE'][0].set(section, option, str(settingsDict[section][option][0]))

    for file in configFiles.keys():
        with open(configFiles[file][1] + '.ini', 'w') as f:
            configFiles[file][0].write(f)
            f.close()

def checkConfigFile(overwrite = True):
    #check file
    for file in configFiles.keys():
        try:
            configFiles[file][0].read(configFiles[file][1] + '.ini')
        except:
            #printH("An error occurred while loading settings.")
            if not overwrite: return False

    for section in settingsDict.keys():
        if not settingsDict[section]['FILE'][0].has_section(section):
            #printH("A config file '" + settingsDict[section]['FILE'][1] + "' is missing section '" + section + "'")

            if not overwrite: return False
            settingsDict[section]['FILE'][0].add_section(section)
            for option in settingsDict[section].keys():
                if option == "FILE": continue
                settingsDict[section]['FILE'][0].set(section, option, str(settingsDict[section][option][0])),
            continue

        for option in settingsDict[section].keys():
            if option == "FILE": continue
            if not settingsDict[section]['FILE'][0].has_option(section, option):
                #printH("A config file '" + settingsDict[section]['FILE'][1] + "' is missing option '" + option + "' in section '" + section)

                if not overwrite: return False
                settingsDict[section]['FILE'][0].set(section, option, str(settingsDict[section][option][0])),

    for file in configFiles.keys():
        if not os.path.exists("configFiles"): # vytvori adresar pro data pokud neexistuje
            os.makedirs("configFiles")
        with open(configFiles[file][1] + '.ini', 'w') as f:
            configFiles[file][0].write(f)
            f.close()