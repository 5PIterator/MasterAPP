# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MasterAPPV7.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QAbstractSpinBox, QApplication, QCheckBox,
    QComboBox, QDoubleSpinBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QSpinBox, QSplitter,
    QTabWidget, QTableWidget, QTableWidgetItem, QTextEdit,
    QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget
import Images_rc
import Images_rc

class Ui_MasterAPP(object):
    def setupUi(self, MasterAPP):
        if not MasterAPP.objectName():
            MasterAPP.setObjectName(u"MasterAPP")
        MasterAPP.setWindowModality(Qt.WindowModal)
        MasterAPP.resize(1206, 709)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MasterAPP.sizePolicy().hasHeightForWidth())
        MasterAPP.setSizePolicy(sizePolicy)
        MasterAPP.setStyleSheet(u"QWidget#centralwidget\n"
"{\n"
"	background-image: url(:/img/Img/water.jpg);\n"
"}")
        MasterAPP.setTabShape(QTabWidget.Triangular)
        MasterAPP.setDockNestingEnabled(True)
        self.centralwidget = QWidget(MasterAPP)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.centralwidget.setStyleSheet(u"")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.masterScrollArea = QScrollArea(self.centralwidget)
        self.masterScrollArea.setObjectName(u"masterScrollArea")
        self.masterScrollArea.setMinimumSize(QSize(0, 598))
        self.masterScrollArea.setStyleSheet(u"QWidget#masterScrollAreaWidgetContents_2{\n"
" background-image: url(:/img/Img/water.jpg);\n"
"}")
        self.masterScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.masterScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.masterScrollArea.setWidgetResizable(True)
        self.masterScrollAreaWidgetContents_2 = QWidget()
        self.masterScrollAreaWidgetContents_2.setObjectName(u"masterScrollAreaWidgetContents_2")
        self.masterScrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 1204, 707))
        sizePolicy.setHeightForWidth(self.masterScrollAreaWidgetContents_2.sizePolicy().hasHeightForWidth())
        self.masterScrollAreaWidgetContents_2.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.masterScrollAreaWidgetContents_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.splitter = QSplitter(self.masterScrollAreaWidgetContents_2)
        self.splitter.setObjectName(u"splitter")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy2)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setHandleWidth(0)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.horizontalLayout_4 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.splitter_3 = QSplitter(self.layoutWidget)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Horizontal)
        self.splitter_3.setHandleWidth(0)
        self.frame = QFrame(self.splitter_3)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.tabWidget_2 = QTabWidget(self.frame)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        sizePolicy.setHeightForWidth(self.tabWidget_2.sizePolicy().hasHeightForWidth())
        self.tabWidget_2.setSizePolicy(sizePolicy)
        self.tabWidget_2.setMinimumSize(QSize(252, 0))
        self.tabWidget_2.setStyleSheet(u"QTabWidget::pane {\n"
"    background: transparent;\n"
"    border:0;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    background: rgba(0, 0, 0, 0);\n"
"}\n"
"\n"
"QTabBar::tab::selected {\n"
"    background: rgba(255, 255, 255, 150);\n"
"}")
        self.MainTab = QWidget()
        self.MainTab.setObjectName(u"MainTab")
        self.MainTab.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.gridLayout_11 = QGridLayout(self.MainTab)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, -1, -1, 25)
        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.logo_2 = QLabel(self.MainTab)
        self.logo_2.setObjectName(u"logo_2")
        self.logo_2.setMaximumSize(QSize(276, 16777215))
        self.logo_2.setPixmap(QPixmap(u":/img/Img/logo.png"))
        self.logo_2.setScaledContents(False)

        self.horizontalLayout_17.addWidget(self.logo_2)

        self.line_2 = QFrame(self.MainTab)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_17.addWidget(self.line_2)

        self.horizontalSpacer_26 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_26)

        self.groupBox_2 = QGroupBox(self.MainTab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy3)
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setAlignment(Qt.AlignCenter)
        self.groupBox_2.setFlat(True)
        self.groupBox_2.setCheckable(False)
        self.gridLayout_7 = QGridLayout(self.groupBox_2)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.t_label_4 = QLabel(self.groupBox_2)
        self.t_label_4.setObjectName(u"t_label_4")
        font1 = QFont()
        font1.setPointSize(16)
        self.t_label_4.setFont(font1)

        self.gridLayout_8.addWidget(self.t_label_4, 1, 1, 1, 1)

        self.t_label_3 = QLabel(self.groupBox_2)
        self.t_label_3.setObjectName(u"t_label_3")
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        self.t_label_3.setFont(font2)
        self.t_label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.t_label_3, 1, 0, 1, 1)

        self.t_label_1 = QLabel(self.groupBox_2)
        self.t_label_1.setObjectName(u"t_label_1")
        self.t_label_1.setFont(font2)
        self.t_label_1.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_8.addWidget(self.t_label_1, 0, 0, 1, 1)

        self.t_label_2 = QLabel(self.groupBox_2)
        self.t_label_2.setObjectName(u"t_label_2")
        self.t_label_2.setFont(font1)

        self.gridLayout_8.addWidget(self.t_label_2, 0, 1, 1, 1)


        self.verticalLayout_7.addLayout(self.gridLayout_8)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_4)


        self.gridLayout_7.addLayout(self.verticalLayout_7, 0, 0, 1, 1)


        self.horizontalLayout_17.addWidget(self.groupBox_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_17)

        self.tableWidget = QTableWidget(self.MainTab)
        if (self.tableWidget.columnCount() < 1):
            self.tableWidget.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignCenter);
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        if (self.tableWidget.rowCount() < 6):
            self.tableWidget.setRowCount(6)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem7.setFlags(Qt.ItemIsEnabled);
        self.tableWidget.setItem(0, 0, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem8.setFlags(Qt.ItemIsEnabled);
        self.tableWidget.setItem(1, 0, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem9.setFlags(Qt.ItemIsEnabled);
        self.tableWidget.setItem(2, 0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem10.setFlags(Qt.ItemIsEnabled);
        self.tableWidget.setItem(3, 0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem11.setFlags(Qt.ItemIsEnabled);
        self.tableWidget.setItem(4, 0, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        __qtablewidgetitem12.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem12.setFlags(Qt.ItemIsEnabled);
        self.tableWidget.setItem(5, 0, __qtablewidgetitem12)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMinimumSize(QSize(200, 362))
        self.tableWidget.setMaximumSize(QSize(16777215, 360))
        font3 = QFont()
        font3.setPointSize(18)
        font3.setBold(True)
        self.tableWidget.setFont(font3)
        self.tableWidget.setStyleSheet(u"background-color: rgba(255, 255, 255, 230);")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(200)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(260)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(True)
        self.tableWidget.verticalHeader().setMinimumSectionSize(60)
        self.tableWidget.verticalHeader().setDefaultSectionSize(60)
        self.tableWidget.verticalHeader().setHighlightSections(False)

        self.verticalLayout_4.addWidget(self.tableWidget)


        self.gridLayout_11.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.MainTab, "")
        self.HistoryTab = QWidget()
        self.HistoryTab.setObjectName(u"HistoryTab")
        self.gridLayout_10 = QGridLayout(self.HistoryTab)
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.historyScrollArea = QScrollArea(self.HistoryTab)
        self.historyScrollArea.setObjectName(u"historyScrollArea")
        self.historyScrollArea.setEnabled(True)
        self.historyScrollArea.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.historyScrollArea.setLineWidth(0)
        self.historyScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.historyScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.historyScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_8 = QWidget()
        self.scrollAreaWidgetContents_8.setObjectName(u"scrollAreaWidgetContents_8")
        self.scrollAreaWidgetContents_8.setGeometry(QRect(0, 0, 738, 659))
        self.gridLayout_4 = QGridLayout(self.scrollAreaWidgetContents_8)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.historyButtons = QFrame(self.scrollAreaWidgetContents_8)
        self.historyButtons.setObjectName(u"historyButtons")
        self.historyButtons.setMinimumSize(QSize(0, 0))
        self.historyButtons.setFrameShape(QFrame.StyledPanel)
        self.historyButtons.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.historyButtons)
        self.horizontalLayout_9.setSpacing(1)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.historyButton = QPushButton(self.historyButtons)
        self.historyButton.setObjectName(u"historyButton")
        font4 = QFont()
        font4.setFamilies([u"Segoe UI"])
        font4.setBold(True)
        self.historyButton.setFont(font4)
        self.historyButton.setStyleSheet(u"background-color: rgb(10, 10, 10);\n"
"color: rgb(0, 170, 0);")

        self.horizontalLayout_9.addWidget(self.historyButton)

        self.historyButton_2 = QPushButton(self.historyButtons)
        self.historyButton_2.setObjectName(u"historyButton_2")
        self.historyButton_2.setFont(font4)
        self.historyButton_2.setStyleSheet(u"background-color: rgb(10, 10, 10);\n"
"color: rgb(0, 170, 0);")

        self.horizontalLayout_9.addWidget(self.historyButton_2)


        self.gridLayout_4.addWidget(self.historyButtons, 2, 0, 1, 1)

        self.historyList = QTextEdit(self.scrollAreaWidgetContents_8)
        self.historyList.setObjectName(u"historyList")
        font5 = QFont()
        font5.setFamilies([u"Segoe UI"])
        font5.setPointSize(9)
        font5.setBold(True)
        self.historyList.setFont(font5)
        self.historyList.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color: rgb(0, 170, 0);\n"
"QHeaderView::section {\n"
"background-color: rgb(170, 0, 0);\n"
"color: rgb(0, 170, 0);\n"
"}\n"
"")
        self.historyList.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.historyList.setReadOnly(True)

        self.gridLayout_4.addWidget(self.historyList, 1, 0, 1, 1)

        self.historyScrollArea.setWidget(self.scrollAreaWidgetContents_8)

        self.gridLayout_10.addWidget(self.historyScrollArea, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.HistoryTab, "")
        self.SettingsTab = QWidget()
        self.SettingsTab.setObjectName(u"SettingsTab")
        self.gridLayout_12 = QGridLayout(self.SettingsTab)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.SettingsTab)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"background-color:transparent;\n"
"selection-color: rgb(0, 0, 0);\n"
"selection-background-color:transparent;\n"
"")
        self.scrollArea.setFrameShape(QFrame.Box)
        self.scrollArea.setFrameShadow(QFrame.Plain)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_4 = QWidget()
        self.scrollAreaWidgetContents_4.setObjectName(u"scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, 0, 738, 659))
        self.ServerGroupBox = QGroupBox(self.scrollAreaWidgetContents_4)
        self.ServerGroupBox.setObjectName(u"ServerGroupBox")
        self.ServerGroupBox.setGeometry(QRect(0, 210, 381, 111))
        font6 = QFont()
        font6.setBold(True)
        self.ServerGroupBox.setFont(font6)
        self.ServerGroupBox.setStyleSheet(u"background-color: rgba(255, 255, 255, 100);\n"
"border-color: rgb(255, 255, 255);")
        self.ServerGroupBox.setFlat(True)
        self.gridLayout_9 = QGridLayout(self.ServerGroupBox)
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(1)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.le_apiAddress = QLineEdit(self.ServerGroupBox)
        self.le_apiAddress.setObjectName(u"le_apiAddress")
        sizePolicy.setHeightForWidth(self.le_apiAddress.sizePolicy().hasHeightForWidth())
        self.le_apiAddress.setSizePolicy(sizePolicy)
        self.le_apiAddress.setMinimumSize(QSize(140, 21))
        self.le_apiAddress.setMaximumSize(QSize(140, 16777215))

        self.horizontalLayout_3.addWidget(self.le_apiAddress)

        self.label_4 = QLabel(self.ServerGroupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(3, 16777215))
        self.label_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_4)

        self.le_apiPort = QLineEdit(self.ServerGroupBox)
        self.le_apiPort.setObjectName(u"le_apiPort")
        sizePolicy.setHeightForWidth(self.le_apiPort.sizePolicy().hasHeightForWidth())
        self.le_apiPort.setSizePolicy(sizePolicy)
        self.le_apiPort.setMinimumSize(QSize(0, 21))
        self.le_apiPort.setMaximumSize(QSize(41, 16777215))
        self.le_apiPort.setMaxLength(4)
        self.le_apiPort.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.le_apiPort)


        self.gridLayout_9.addLayout(self.horizontalLayout_3, 0, 1, 1, 1)

        self.cb_apiAllowed = QCheckBox(self.ServerGroupBox)
        self.cb_apiAllowed.setObjectName(u"cb_apiAllowed")
        self.cb_apiAllowed.setEnabled(False)
        self.cb_apiAllowed.setMinimumSize(QSize(50, 0))
        self.cb_apiAllowed.setStyleSheet(u"background-color:transparent")
        self.cb_apiAllowed.setChecked(False)

        self.gridLayout_9.addWidget(self.cb_apiAllowed, 0, 2, 1, 1)

        self.label_2 = QLabel(self.ServerGroupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"background-color:transparent")

        self.gridLayout_9.addWidget(self.label_2, 0, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(1)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_4 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)

        self.le_plcAddress = QLineEdit(self.ServerGroupBox)
        self.le_plcAddress.setObjectName(u"le_plcAddress")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.le_plcAddress.sizePolicy().hasHeightForWidth())
        self.le_plcAddress.setSizePolicy(sizePolicy4)
        self.le_plcAddress.setMinimumSize(QSize(140, 21))
        self.le_plcAddress.setMaximumSize(QSize(140, 16777215))

        self.horizontalLayout_5.addWidget(self.le_plcAddress)

        self.label_5 = QLabel(self.ServerGroupBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(3, 16777215))
        self.label_5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label_5)

        self.le_plcPort = QLineEdit(self.ServerGroupBox)
        self.le_plcPort.setObjectName(u"le_plcPort")
        sizePolicy.setHeightForWidth(self.le_plcPort.sizePolicy().hasHeightForWidth())
        self.le_plcPort.setSizePolicy(sizePolicy)
        self.le_plcPort.setMinimumSize(QSize(0, 21))
        self.le_plcPort.setMaximumSize(QSize(41, 16777215))
        self.le_plcPort.setMaxLength(4)
        self.le_plcPort.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.le_plcPort)


        self.gridLayout_9.addLayout(self.horizontalLayout_5, 1, 1, 1, 1)

        self.label_3 = QLabel(self.ServerGroupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"background-color:transparent")

        self.gridLayout_9.addWidget(self.label_3, 1, 0, 1, 1)

        self.cb_plcAllowed = QCheckBox(self.ServerGroupBox)
        self.cb_plcAllowed.setObjectName(u"cb_plcAllowed")
        self.cb_plcAllowed.setMinimumSize(QSize(50, 0))
        self.cb_plcAllowed.setStyleSheet(u"background-color:transparent")
        self.cb_plcAllowed.setChecked(False)

        self.gridLayout_9.addWidget(self.cb_plcAllowed, 1, 2, 1, 1)

        self.label_9 = QLabel(self.ServerGroupBox)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setStyleSheet(u"background-color:transparent")

        self.gridLayout_9.addWidget(self.label_9, 2, 0, 1, 1)

        self.cb_axAllowed = QCheckBox(self.ServerGroupBox)
        self.cb_axAllowed.setObjectName(u"cb_axAllowed")
        self.cb_axAllowed.setEnabled(False)
        self.cb_axAllowed.setMinimumSize(QSize(50, 0))
        self.cb_axAllowed.setStyleSheet(u"background-color:transparent")
        self.cb_axAllowed.setChecked(False)

        self.gridLayout_9.addWidget(self.cb_axAllowed, 2, 2, 1, 1)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setSpacing(1)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_5 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_5)

        self.le_axAddress = QLineEdit(self.ServerGroupBox)
        self.le_axAddress.setObjectName(u"le_axAddress")
        sizePolicy4.setHeightForWidth(self.le_axAddress.sizePolicy().hasHeightForWidth())
        self.le_axAddress.setSizePolicy(sizePolicy4)
        self.le_axAddress.setMinimumSize(QSize(140, 21))
        self.le_axAddress.setMaximumSize(QSize(140, 16777215))

        self.horizontalLayout_10.addWidget(self.le_axAddress)

        self.label_10 = QLabel(self.ServerGroupBox)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMaximumSize(QSize(3, 16777215))
        self.label_10.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_10.addWidget(self.label_10)

        self.le_axPort = QLineEdit(self.ServerGroupBox)
        self.le_axPort.setObjectName(u"le_axPort")
        sizePolicy.setHeightForWidth(self.le_axPort.sizePolicy().hasHeightForWidth())
        self.le_axPort.setSizePolicy(sizePolicy)
        self.le_axPort.setMinimumSize(QSize(0, 21))
        self.le_axPort.setMaximumSize(QSize(41, 16777215))
        self.le_axPort.setMaxLength(5)
        self.le_axPort.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_10.addWidget(self.le_axPort)


        self.gridLayout_9.addLayout(self.horizontalLayout_10, 2, 1, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_7, 3, 0, 1, 1)

        self.IntervalGroup = QGroupBox(self.scrollAreaWidgetContents_4)
        self.IntervalGroup.setObjectName(u"IntervalGroup")
        self.IntervalGroup.setGeometry(QRect(0, 330, 381, 121))
        self.IntervalGroup.setFont(font6)
        self.IntervalGroup.setStyleSheet(u"background-color: rgba(255, 255, 255, 100);\n"
"border-color: rgb(255, 255, 255);")
        self.IntervalGroup.setFlat(True)
        self.gridLayout_14 = QGridLayout(self.IntervalGroup)
        self.gridLayout_14.setSpacing(0)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(-1, 0, -1, 0)
        self.dsb_apiInterval = QDoubleSpinBox(self.IntervalGroup)
        self.dsb_apiInterval.setObjectName(u"dsb_apiInterval")
        self.dsb_apiInterval.setEnabled(False)
        sizePolicy.setHeightForWidth(self.dsb_apiInterval.sizePolicy().hasHeightForWidth())
        self.dsb_apiInterval.setSizePolicy(sizePolicy)
        self.dsb_apiInterval.setMinimumSize(QSize(63, 0))
        self.dsb_apiInterval.setMaximumSize(QSize(56, 16777215))
        self.dsb_apiInterval.setStyleSheet(u"background-color:white")
        self.dsb_apiInterval.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.dsb_apiInterval.setDecimals(2)
        self.dsb_apiInterval.setMinimum(0.000000000000000)
        self.dsb_apiInterval.setMaximum(120.000000000000000)
        self.dsb_apiInterval.setSingleStep(1.000000000000000)
        self.dsb_apiInterval.setValue(5.000000000000000)

        self.gridLayout_14.addWidget(self.dsb_apiInterval, 1, 2, 1, 1)

        self.l_axInterval = QLabel(self.IntervalGroup)
        self.l_axInterval.setObjectName(u"l_axInterval")
        self.l_axInterval.setStyleSheet(u"background-color:transparent")
        self.l_axInterval.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_14.addWidget(self.l_axInterval, 2, 1, 1, 1)

        self.l_plcInterval = QLabel(self.IntervalGroup)
        self.l_plcInterval.setObjectName(u"l_plcInterval")
        self.l_plcInterval.setStyleSheet(u"background-color:transparent")
        self.l_plcInterval.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_14.addWidget(self.l_plcInterval, 3, 1, 1, 1)

        self.dsb_plcInterval = QDoubleSpinBox(self.IntervalGroup)
        self.dsb_plcInterval.setObjectName(u"dsb_plcInterval")
        sizePolicy.setHeightForWidth(self.dsb_plcInterval.sizePolicy().hasHeightForWidth())
        self.dsb_plcInterval.setSizePolicy(sizePolicy)
        self.dsb_plcInterval.setMinimumSize(QSize(63, 0))
        self.dsb_plcInterval.setMaximumSize(QSize(60, 16777215))
        self.dsb_plcInterval.setStyleSheet(u"background-color:white")
        self.dsb_plcInterval.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.dsb_plcInterval.setDecimals(0)
        self.dsb_plcInterval.setMinimum(1.000000000000000)
        self.dsb_plcInterval.setMaximum(60.000000000000000)
        self.dsb_plcInterval.setSingleStep(1.000000000000000)
        self.dsb_plcInterval.setValue(1.000000000000000)

        self.gridLayout_14.addWidget(self.dsb_plcInterval, 3, 2, 1, 1)

        self.dsb_axInterval = QDoubleSpinBox(self.IntervalGroup)
        self.dsb_axInterval.setObjectName(u"dsb_axInterval")
        self.dsb_axInterval.setEnabled(False)
        sizePolicy.setHeightForWidth(self.dsb_axInterval.sizePolicy().hasHeightForWidth())
        self.dsb_axInterval.setSizePolicy(sizePolicy)
        self.dsb_axInterval.setMinimumSize(QSize(63, 0))
        self.dsb_axInterval.setMaximumSize(QSize(60, 16777215))
        self.dsb_axInterval.setStyleSheet(u"background-color:white")
        self.dsb_axInterval.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.dsb_axInterval.setDecimals(2)
        self.dsb_axInterval.setMinimum(1.000000000000000)
        self.dsb_axInterval.setMaximum(60.000000000000000)
        self.dsb_axInterval.setSingleStep(1.000000000000000)
        self.dsb_axInterval.setValue(20.000000000000000)

        self.gridLayout_14.addWidget(self.dsb_axInterval, 2, 2, 1, 1)

        self.sb_retryInterval = QSpinBox(self.IntervalGroup)
        self.sb_retryInterval.setObjectName(u"sb_retryInterval")
        sizePolicy.setHeightForWidth(self.sb_retryInterval.sizePolicy().hasHeightForWidth())
        self.sb_retryInterval.setSizePolicy(sizePolicy)
        self.sb_retryInterval.setMinimumSize(QSize(63, 0))
        self.sb_retryInterval.setMaximumSize(QSize(60, 16777215))
        self.sb_retryInterval.setStyleSheet(u"background-color:white")
        self.sb_retryInterval.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_14.addWidget(self.sb_retryInterval, 0, 2, 1, 1)

        self.l_retryInterval = QLabel(self.IntervalGroup)
        self.l_retryInterval.setObjectName(u"l_retryInterval")
        self.l_retryInterval.setStyleSheet(u"background-color:transparent")
        self.l_retryInterval.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_14.addWidget(self.l_retryInterval, 0, 1, 1, 1)

        self.label = QLabel(self.IntervalGroup)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"background-color:transparent")

        self.gridLayout_14.addWidget(self.label, 0, 0, 1, 1)

        self.label_6 = QLabel(self.IntervalGroup)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"background-color:transparent")

        self.gridLayout_14.addWidget(self.label_6, 1, 0, 1, 1)

        self.label_14 = QLabel(self.IntervalGroup)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setStyleSheet(u"background-color:transparent")

        self.gridLayout_14.addWidget(self.label_14, 2, 0, 1, 1)

        self.label_22 = QLabel(self.IntervalGroup)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setStyleSheet(u"background-color:transparent")

        self.gridLayout_14.addWidget(self.label_22, 3, 0, 1, 1)

        self.l_apiInterval = QLabel(self.IntervalGroup)
        self.l_apiInterval.setObjectName(u"l_apiInterval")
        self.l_apiInterval.setStyleSheet(u"background-color:transparent")
        self.l_apiInterval.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_14.addWidget(self.l_apiInterval, 1, 1, 1, 1)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_14.addItem(self.verticalSpacer_8, 4, 0, 1, 1)

        self.groupBox = QGroupBox(self.scrollAreaWidgetContents_4)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(0, 0, 381, 201))
        self.groupBox.setFont(font6)
        self.groupBox.setStyleSheet(u"background-color: rgba(255, 255, 255, 100);\n"
"border-color: rgb(255, 255, 255);")
        self.groupBox.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.groupBox.setFlat(True)
        self.gridLayout_13 = QGridLayout(self.groupBox)
        self.gridLayout_13.setSpacing(0)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(-1, 0, -1, 0)
        self.pb_retry = QPushButton(self.groupBox)
        self.pb_retry.setObjectName(u"pb_retry")
        sizePolicy.setHeightForWidth(self.pb_retry.sizePolicy().hasHeightForWidth())
        self.pb_retry.setSizePolicy(sizePolicy)
        self.pb_retry.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.gridLayout_13.addWidget(self.pb_retry, 1, 2, 1, 1)

        self.line_3 = QFrame(self.groupBox)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout_13.addWidget(self.line_3, 5, 2, 1, 1)

        self.line_6 = QFrame(self.groupBox)
        self.line_6.setObjectName(u"line_6")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.line_6.sizePolicy().hasHeightForWidth())
        self.line_6.setSizePolicy(sizePolicy5)
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.gridLayout_13.addWidget(self.line_6, 5, 3, 1, 1)

        self.pb_changeDir = QPushButton(self.groupBox)
        self.pb_changeDir.setObjectName(u"pb_changeDir")
        sizePolicy.setHeightForWidth(self.pb_changeDir.sizePolicy().hasHeightForWidth())
        self.pb_changeDir.setSizePolicy(sizePolicy)
        self.pb_changeDir.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.gridLayout_13.addWidget(self.pb_changeDir, 6, 2, 1, 1)

        self.label_12 = QLabel(self.groupBox)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setStyleSheet(u"background-color:transparent")

        self.gridLayout_13.addWidget(self.label_12, 3, 0, 1, 1)

        self.cb_auto_retry = QCheckBox(self.groupBox)
        self.cb_auto_retry.setObjectName(u"cb_auto_retry")
        self.cb_auto_retry.setMinimumSize(QSize(50, 0))
        self.cb_auto_retry.setStyleSheet(u"background-color:transparent")
        self.cb_auto_retry.setChecked(False)

        self.gridLayout_13.addWidget(self.cb_auto_retry, 1, 3, 1, 1)

        self.label_16 = QLabel(self.groupBox)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setEnabled(False)
        self.label_16.setStyleSheet(u"background-color:transparent")

        self.gridLayout_13.addWidget(self.label_16, 4, 0, 1, 1)

        self.pb_updateCables = QPushButton(self.groupBox)
        self.pb_updateCables.setObjectName(u"pb_updateCables")
        sizePolicy.setHeightForWidth(self.pb_updateCables.sizePolicy().hasHeightForWidth())
        self.pb_updateCables.setSizePolicy(sizePolicy)
        self.pb_updateCables.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.gridLayout_13.addWidget(self.pb_updateCables, 3, 2, 1, 1)

        self.cb_auto_cableUpdate = QCheckBox(self.groupBox)
        self.cb_auto_cableUpdate.setObjectName(u"cb_auto_cableUpdate")
        self.cb_auto_cableUpdate.setMinimumSize(QSize(50, 0))
        self.cb_auto_cableUpdate.setStyleSheet(u"background-color:transparent")
        self.cb_auto_cableUpdate.setChecked(False)

        self.gridLayout_13.addWidget(self.cb_auto_cableUpdate, 3, 3, 1, 1)

        self.pb_stopClients = QPushButton(self.groupBox)
        self.pb_stopClients.setObjectName(u"pb_stopClients")
        sizePolicy.setHeightForWidth(self.pb_stopClients.sizePolicy().hasHeightForWidth())
        self.pb_stopClients.setSizePolicy(sizePolicy)
        self.pb_stopClients.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.gridLayout_13.addWidget(self.pb_stopClients, 2, 2, 1, 1)

        self.cb_auto_startClients = QCheckBox(self.groupBox)
        self.cb_auto_startClients.setObjectName(u"cb_auto_startClients")
        self.cb_auto_startClients.setMinimumSize(QSize(50, 0))
        self.cb_auto_startClients.setStyleSheet(u"background-color:transparent;")
        self.cb_auto_startClients.setChecked(False)

        self.gridLayout_13.addWidget(self.cb_auto_startClients, 0, 3, 1, 1)

        self.label_13 = QLabel(self.groupBox)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setStyleSheet(u"background-color:transparent")

        self.gridLayout_13.addWidget(self.label_13, 2, 0, 1, 1)

        self.label_20 = QLabel(self.groupBox)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setStyleSheet(u"background-color:transparent")

        self.gridLayout_13.addWidget(self.label_20, 6, 0, 1, 1)

        self.pb_startClients = QPushButton(self.groupBox)
        self.pb_startClients.setObjectName(u"pb_startClients")
        sizePolicy.setHeightForWidth(self.pb_startClients.sizePolicy().hasHeightForWidth())
        self.pb_startClients.setSizePolicy(sizePolicy)
        self.pb_startClients.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.gridLayout_13.addWidget(self.pb_startClients, 0, 2, 1, 1)

        self.cb_auto_cableCount = QCheckBox(self.groupBox)
        self.cb_auto_cableCount.setObjectName(u"cb_auto_cableCount")
        self.cb_auto_cableCount.setEnabled(False)
        self.cb_auto_cableCount.setMinimumSize(QSize(50, 0))
        self.cb_auto_cableCount.setStyleSheet(u"background-color:transparent")
        self.cb_auto_cableCount.setChecked(False)

        self.gridLayout_13.addWidget(self.cb_auto_cableCount, 4, 3, 1, 1)

        self.line = QFrame(self.groupBox)
        self.line.setObjectName(u"line")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy6)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_13.addWidget(self.line, 5, 1, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_13.addItem(self.verticalSpacer_6, 7, 0, 1, 1)

        self.line_4 = QFrame(self.groupBox)
        self.line_4.setObjectName(u"line_4")
        sizePolicy6.setHeightForWidth(self.line_4.sizePolicy().hasHeightForWidth())
        self.line_4.setSizePolicy(sizePolicy6)
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.gridLayout_13.addWidget(self.line_4, 5, 0, 1, 1)

        self.label_15 = QLabel(self.groupBox)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setStyleSheet(u"background-color:transparent")

        self.gridLayout_13.addWidget(self.label_15, 1, 0, 1, 1)

        self.label_11 = QLabel(self.groupBox)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setStyleSheet(u"background-color:transparent")

        self.gridLayout_13.addWidget(self.label_11, 0, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)

        self.sb_cableCount = QSpinBox(self.groupBox)
        self.sb_cableCount.setObjectName(u"sb_cableCount")
        self.sb_cableCount.setEnabled(False)
        sizePolicy6.setHeightForWidth(self.sb_cableCount.sizePolicy().hasHeightForWidth())
        self.sb_cableCount.setSizePolicy(sizePolicy6)
        self.sb_cableCount.setMaximumSize(QSize(20, 16777215))
        self.sb_cableCount.setStyleSheet(u"background-color:white")
        self.sb_cableCount.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.sb_cableCount.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.sb_cableCount.setValue(4)

        self.horizontalLayout_2.addWidget(self.sb_cableCount)


        self.gridLayout_13.addLayout(self.horizontalLayout_2, 4, 2, 1, 1)

        self.groupBox_3 = QGroupBox(self.scrollAreaWidgetContents_4)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(0, 460, 381, 111))
        self.groupBox_3.setFont(font6)
        self.groupBox_3.setStyleSheet(u"background-color: rgba(255, 255, 255, 100);\n"
"border-color: rgb(255, 255, 255);")
        self.groupBox_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.groupBox_3.setFlat(True)
        self.groupBox_3.setCheckable(False)
        self.gridLayout_15 = QGridLayout(self.groupBox_3)
        self.gridLayout_15.setSpacing(0)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(-1, 0, -1, 0)
        self.label_18 = QLabel(self.groupBox_3)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setStyleSheet(u"background-color:transparent")

        self.gridLayout_15.addWidget(self.label_18, 0, 0, 1, 1)

        self.label_17 = QLabel(self.groupBox_3)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setStyleSheet(u"background-color:transparent")

        self.gridLayout_15.addWidget(self.label_17, 1, 0, 1, 1)

        self.label_21 = QLabel(self.groupBox_3)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setStyleSheet(u"background-color:transparent")

        self.gridLayout_15.addWidget(self.label_21, 2, 0, 1, 1)

        self.pb_MMState = QSpinBox(self.groupBox_3)
        self.pb_MMState.setObjectName(u"pb_MMState")
        sizePolicy3.setHeightForWidth(self.pb_MMState.sizePolicy().hasHeightForWidth())
        self.pb_MMState.setSizePolicy(sizePolicy3)
        self.pb_MMState.setStyleSheet(u"background-color:white")
        self.pb_MMState.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.pb_MMState.setMinimum(1)
        self.pb_MMState.setMaximum(60)
        self.pb_MMState.setValue(2)

        self.gridLayout_15.addWidget(self.pb_MMState, 2, 3, 1, 1)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_15.addItem(self.verticalSpacer_9, 3, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_3, 0, 1, 1, 1)

        self.pb_SaveStateData = QPushButton(self.groupBox_3)
        self.pb_SaveStateData.setObjectName(u"pb_SaveStateData")
        sizePolicy.setHeightForWidth(self.pb_SaveStateData.sizePolicy().hasHeightForWidth())
        self.pb_SaveStateData.setSizePolicy(sizePolicy)
        self.pb_SaveStateData.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.gridLayout_15.addWidget(self.pb_SaveStateData, 1, 2, 1, 1)

        self.pb_changeDomain = QPushButton(self.groupBox_3)
        self.pb_changeDomain.setObjectName(u"pb_changeDomain")
        sizePolicy.setHeightForWidth(self.pb_changeDomain.sizePolicy().hasHeightForWidth())
        self.pb_changeDomain.setSizePolicy(sizePolicy)
        self.pb_changeDomain.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.gridLayout_15.addWidget(self.pb_changeDomain, 0, 2, 1, 1)

        self.cb_SaveStyle = QComboBox(self.groupBox_3)
        self.cb_SaveStyle.addItem("")
        self.cb_SaveStyle.addItem("")
        self.cb_SaveStyle.addItem("")
        self.cb_SaveStyle.addItem("")
        self.cb_SaveStyle.setObjectName(u"cb_SaveStyle")
        sizePolicy3.setHeightForWidth(self.cb_SaveStyle.sizePolicy().hasHeightForWidth())
        self.cb_SaveStyle.setSizePolicy(sizePolicy3)
        self.cb_SaveStyle.setStyleSheet(u"QComboBox QAbstractItemView {\n"
"background:white\n"
"}")
        self.cb_SaveStyle.setMaxVisibleItems(4)
        self.cb_SaveStyle.setMaxCount(4)
        self.cb_SaveStyle.setInsertPolicy(QComboBox.NoInsert)
        self.cb_SaveStyle.setIconSize(QSize(4, 4))
        self.cb_SaveStyle.setFrame(False)

        self.gridLayout_15.addWidget(self.cb_SaveStyle, 1, 3, 1, 1)

        self.l_domainHost = QLabel(self.groupBox_3)
        self.l_domainHost.setObjectName(u"l_domainHost")
        sizePolicy3.setHeightForWidth(self.l_domainHost.sizePolicy().hasHeightForWidth())
        self.l_domainHost.setSizePolicy(sizePolicy3)
        self.l_domainHost.setStyleSheet(u"background-color:transparent")
        self.l_domainHost.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_15.addWidget(self.l_domainHost, 0, 3, 1, 1)

        self.le_areal = QLineEdit(self.groupBox_3)
        self.le_areal.setObjectName(u"le_areal")
        self.le_areal.setMaximumSize(QSize(21, 16777215))
        self.le_areal.setMaxLength(2)
        self.le_areal.setFrame(True)
        self.le_areal.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)

        self.gridLayout_15.addWidget(self.le_areal, 0, 4, 1, 1)

        self.l_saveStateTimer = QLabel(self.groupBox_3)
        self.l_saveStateTimer.setObjectName(u"l_saveStateTimer")
        sizePolicy3.setHeightForWidth(self.l_saveStateTimer.sizePolicy().hasHeightForWidth())
        self.l_saveStateTimer.setSizePolicy(sizePolicy3)
        self.l_saveStateTimer.setMinimumSize(QSize(21, 0))
        self.l_saveStateTimer.setStyleSheet(u"background-color:transparent")
        self.l_saveStateTimer.setAlignment(Qt.AlignCenter)

        self.gridLayout_15.addWidget(self.l_saveStateTimer, 1, 4, 1, 1)

        self.l_workloadPath = QLabel(self.scrollAreaWidgetContents_4)
        self.l_workloadPath.setObjectName(u"l_workloadPath")
        self.l_workloadPath.setGeometry(QRect(10, 180, 471, 28))
        sizePolicy.setHeightForWidth(self.l_workloadPath.sizePolicy().hasHeightForWidth())
        self.l_workloadPath.setSizePolicy(sizePolicy)
        self.l_workloadPath.setStyleSheet(u"background-color:transparent")
        self.l_workloadPath.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_4)

        self.gridLayout_12.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.SettingsTab, "")
        self.graphTab = QWidget()
        self.graphTab.setObjectName(u"graphTab")
        self.graphTab.setStyleSheet(u"background-color: rgba(200, 200, 200, 20);")
        self.gridLayout = QGridLayout(self.graphTab)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_2 = QScrollArea(self.graphTab)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setStyleSheet(u"")
        self.scrollArea_2.setLineWidth(0)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 738, 659))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pg_workload_1 = PlotWidget(self.scrollAreaWidgetContents)
        self.pg_workload_1.setObjectName(u"pg_workload_1")
        sizePolicy3.setHeightForWidth(self.pg_workload_1.sizePolicy().hasHeightForWidth())
        self.pg_workload_1.setSizePolicy(sizePolicy3)
        self.pg_workload_1.setMinimumSize(QSize(0, 200))

        self.verticalLayout_2.addWidget(self.pg_workload_1)

        self.verticalSpacer = QSpacerItem(20, 542, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollArea_2, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.graphTab, "")

        self.gridLayout_5.addWidget(self.tabWidget_2, 0, 0, 1, 1)

        self.splitter_3.addWidget(self.frame)

        self.horizontalLayout_4.addWidget(self.splitter_3)

        self.splitter.addWidget(self.layoutWidget)
        self.layoutWidget1 = QWidget(self.splitter)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.CablelLayout = QVBoxLayout(self.layoutWidget1)
        self.CablelLayout.setSpacing(0)
        self.CablelLayout.setObjectName(u"CablelLayout")
        self.CablelLayout.setContentsMargins(0, 0, 0, 0)
        self.CableScrollArea = QScrollArea(self.layoutWidget1)
        self.CableScrollArea.setObjectName(u"CableScrollArea")
        sizePolicy7 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy7.setHorizontalStretch(255)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.CableScrollArea.sizePolicy().hasHeightForWidth())
        self.CableScrollArea.setSizePolicy(sizePolicy7)
        self.CableScrollArea.setMinimumSize(QSize(0, 0))
        self.CableScrollArea.setStyleSheet(u"QWidget#CableScrollAreaWidgetContents{\n"
"	background-image: url(:/img/Img/bamboo-texture_1136-248.jpg);\n"
"}")
        self.CableScrollArea.setFrameShape(QFrame.Box)
        self.CableScrollArea.setFrameShadow(QFrame.Sunken)
        self.CableScrollArea.setLineWidth(1)
        self.CableScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.CableScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.CableScrollArea.setWidgetResizable(True)
        self.CableScrollAreaWidgetContents = QWidget()
        self.CableScrollAreaWidgetContents.setObjectName(u"CableScrollAreaWidgetContents")
        self.CableScrollAreaWidgetContents.setGeometry(QRect(0, 0, 436, 662))
        sizePolicy8 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.CableScrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.CableScrollAreaWidgetContents.setSizePolicy(sizePolicy8)
        self.horizontalLayout = QHBoxLayout(self.CableScrollAreaWidgetContents)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 5, 9, 5)
        self.cableItem_1 = QFrame(self.CableScrollAreaWidgetContents)
        self.cableItem_1.setObjectName(u"cableItem_1")
        self.cableItem_1.setMaximumSize(QSize(251, 16777215))
        self.cableItem_1.setStyleSheet(u"background-color: rgba(255, 255, 255, 230);")
        self.verticalLayout = QVBoxLayout(self.cableItem_1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.cableLabel_1 = QLabel(self.cableItem_1)
        self.cableLabel_1.setObjectName(u"cableLabel_1")
        font7 = QFont()
        font7.setFamilies([u"Times New Roman"])
        font7.setPointSize(20)
        font7.setBold(True)
        self.cableLabel_1.setFont(font7)
        self.cableLabel_1.setStyleSheet(u"background-color:transparent")
        self.cableLabel_1.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.cableLabel_1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.statusImage_1 = QLabel(self.cableItem_1)
        self.statusImage_1.setObjectName(u"statusImage_1")
        sizePolicy6.setHeightForWidth(self.statusImage_1.sizePolicy().hasHeightForWidth())
        self.statusImage_1.setSizePolicy(sizePolicy6)
        self.statusImage_1.setStyleSheet(u"background-color:transparent")
        self.statusImage_1.setPixmap(QPixmap(u":/img/Img/YellowLight.png"))
        self.statusImage_1.setScaledContents(False)
        self.statusImage_1.setAlignment(Qt.AlignCenter)
        self.statusImage_1.setWordWrap(True)

        self.verticalLayout.addWidget(self.statusImage_1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.tableWidget_1 = QTableWidget(self.cableItem_1)
        if (self.tableWidget_1.columnCount() < 1):
            self.tableWidget_1.setColumnCount(1)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget_1.setHorizontalHeaderItem(0, __qtablewidgetitem13)
        if (self.tableWidget_1.rowCount() < 6):
            self.tableWidget_1.setRowCount(6)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget_1.setVerticalHeaderItem(0, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget_1.setVerticalHeaderItem(1, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget_1.setVerticalHeaderItem(2, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget_1.setVerticalHeaderItem(3, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableWidget_1.setVerticalHeaderItem(4, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableWidget_1.setVerticalHeaderItem(5, __qtablewidgetitem19)
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.NoBrush)
        __qtablewidgetitem20 = QTableWidgetItem()
        __qtablewidgetitem20.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem20.setFont(font6);
        __qtablewidgetitem20.setBackground(brush);
        __qtablewidgetitem20.setFlags(Qt.ItemIsEnabled);
        self.tableWidget_1.setItem(0, 0, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        __qtablewidgetitem21.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem21.setFlags(Qt.ItemIsEnabled);
        self.tableWidget_1.setItem(1, 0, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        __qtablewidgetitem22.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem22.setFont(font6);
        __qtablewidgetitem22.setFlags(Qt.ItemIsEnabled);
        self.tableWidget_1.setItem(2, 0, __qtablewidgetitem22)
        font8 = QFont()
        font8.setBold(False)
        __qtablewidgetitem23 = QTableWidgetItem()
        __qtablewidgetitem23.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem23.setFont(font8);
        __qtablewidgetitem23.setFlags(Qt.ItemIsEnabled);
        self.tableWidget_1.setItem(3, 0, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        __qtablewidgetitem24.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem24.setFont(font8);
        __qtablewidgetitem24.setFlags(Qt.ItemIsEnabled);
        self.tableWidget_1.setItem(4, 0, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        __qtablewidgetitem25.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem25.setFont(font8);
        __qtablewidgetitem25.setFlags(Qt.ItemIsEnabled);
        self.tableWidget_1.setItem(5, 0, __qtablewidgetitem25)
        self.tableWidget_1.setObjectName(u"tableWidget_1")
        sizePolicy.setHeightForWidth(self.tableWidget_1.sizePolicy().hasHeightForWidth())
        self.tableWidget_1.setSizePolicy(sizePolicy)
        self.tableWidget_1.setMinimumSize(QSize(250, 362))
        font9 = QFont()
        font9.setPointSize(18)
        font9.setBold(False)
        self.tableWidget_1.setFont(font9)
        self.tableWidget_1.setStyleSheet(u"background-color:transparent")
        self.tableWidget_1.horizontalHeader().setVisible(False)
        self.tableWidget_1.horizontalHeader().setMinimumSectionSize(200)
        self.tableWidget_1.horizontalHeader().setDefaultSectionSize(250)
        self.tableWidget_1.verticalHeader().setVisible(False)
        self.tableWidget_1.verticalHeader().setMinimumSectionSize(50)
        self.tableWidget_1.verticalHeader().setDefaultSectionSize(60)

        self.verticalLayout.addWidget(self.tableWidget_1)


        self.horizontalLayout.addWidget(self.cableItem_1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.CableScrollArea.setWidget(self.CableScrollAreaWidgetContents)

        self.CablelLayout.addWidget(self.CableScrollArea)

        self.splitter.addWidget(self.layoutWidget1)

        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)

        self.masterScrollArea.setWidget(self.masterScrollAreaWidgetContents_2)

        self.gridLayout_3.addWidget(self.masterScrollArea, 0, 0, 1, 1)

        MasterAPP.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.tabWidget_2, self.historyScrollArea)
        QWidget.setTabOrder(self.historyScrollArea, self.historyList)
        QWidget.setTabOrder(self.historyList, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.scrollArea_2)
        QWidget.setTabOrder(self.scrollArea_2, self.tableWidget)
        QWidget.setTabOrder(self.tableWidget, self.CableScrollArea)
        QWidget.setTabOrder(self.CableScrollArea, self.tableWidget_1)
        QWidget.setTabOrder(self.tableWidget_1, self.historyButton)
        QWidget.setTabOrder(self.historyButton, self.historyButton_2)
        QWidget.setTabOrder(self.historyButton_2, self.pb_startClients)
        QWidget.setTabOrder(self.pb_startClients, self.cb_auto_startClients)
        QWidget.setTabOrder(self.cb_auto_startClients, self.pb_retry)
        QWidget.setTabOrder(self.pb_retry, self.cb_auto_retry)
        QWidget.setTabOrder(self.cb_auto_retry, self.pb_stopClients)
        QWidget.setTabOrder(self.pb_stopClients, self.pb_updateCables)
        QWidget.setTabOrder(self.pb_updateCables, self.cb_auto_cableUpdate)
        QWidget.setTabOrder(self.cb_auto_cableUpdate, self.sb_cableCount)
        QWidget.setTabOrder(self.sb_cableCount, self.cb_auto_cableCount)
        QWidget.setTabOrder(self.cb_auto_cableCount, self.pb_changeDir)
        QWidget.setTabOrder(self.pb_changeDir, self.le_apiAddress)
        QWidget.setTabOrder(self.le_apiAddress, self.le_apiPort)
        QWidget.setTabOrder(self.le_apiPort, self.cb_apiAllowed)
        QWidget.setTabOrder(self.cb_apiAllowed, self.le_plcAddress)
        QWidget.setTabOrder(self.le_plcAddress, self.le_plcPort)
        QWidget.setTabOrder(self.le_plcPort, self.cb_plcAllowed)
        QWidget.setTabOrder(self.cb_plcAllowed, self.le_axAddress)
        QWidget.setTabOrder(self.le_axAddress, self.le_axPort)
        QWidget.setTabOrder(self.le_axPort, self.cb_axAllowed)
        QWidget.setTabOrder(self.cb_axAllowed, self.sb_retryInterval)
        QWidget.setTabOrder(self.sb_retryInterval, self.dsb_apiInterval)
        QWidget.setTabOrder(self.dsb_apiInterval, self.dsb_axInterval)
        QWidget.setTabOrder(self.dsb_axInterval, self.dsb_plcInterval)
        QWidget.setTabOrder(self.dsb_plcInterval, self.pb_changeDomain)
        QWidget.setTabOrder(self.pb_changeDomain, self.le_areal)
        QWidget.setTabOrder(self.le_areal, self.pb_SaveStateData)
        QWidget.setTabOrder(self.pb_SaveStateData, self.cb_SaveStyle)
        QWidget.setTabOrder(self.cb_SaveStyle, self.pb_MMState)
        QWidget.setTabOrder(self.pb_MMState, self.masterScrollArea)

        self.retranslateUi(MasterAPP)

        self.tabWidget_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MasterAPP)
    # setupUi

    def retranslateUi(self, MasterAPP):
        MasterAPP.setWindowTitle(QCoreApplication.translate("MasterAPP", u"MasterAPP", None))
        self.logo_2.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("MasterAPP", u"External Temperatures", None))
        self.t_label_4.setText(QCoreApplication.translate("MasterAPP", u"N/A", None))
        self.t_label_3.setText(QCoreApplication.translate("MasterAPP", u"Air:", None))
        self.t_label_1.setText(QCoreApplication.translate("MasterAPP", u"Water:", None))
        self.t_label_2.setText(QCoreApplication.translate("MasterAPP", u"N/A", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MasterAPP", u"test", None));
        ___qtablewidgetitem1 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MasterAPP", u"State Cable", None));
        ___qtablewidgetitem2 = self.tableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MasterAPP", u"State Rider", None));
        ___qtablewidgetitem3 = self.tableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MasterAPP", u"ID Rider", None));
        ___qtablewidgetitem4 = self.tableWidget.verticalHeaderItem(3)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MasterAPP", u"Position [m]", None));
        ___qtablewidgetitem5 = self.tableWidget.verticalHeaderItem(4)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MasterAPP", u"Speed [km/h]", None));
        ___qtablewidgetitem6 = self.tableWidget.verticalHeaderItem(5)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MasterAPP", u"Alarm/Faul", None));

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        ___qtablewidgetitem7 = self.tableWidget.item(0, 0)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MasterAPP", u"Cable State", None));
        ___qtablewidgetitem8 = self.tableWidget.item(1, 0)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MasterAPP", u"Rider State", None));
        ___qtablewidgetitem9 = self.tableWidget.item(2, 0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MasterAPP", u"Rider ID", None));
        ___qtablewidgetitem10 = self.tableWidget.item(3, 0)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MasterAPP", u"Position [m]", None));
        ___qtablewidgetitem11 = self.tableWidget.item(4, 0)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MasterAPP", u"Speed [km/h]", None));
        ___qtablewidgetitem12 = self.tableWidget.item(5, 0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MasterAPP", u"Alarm/Faul", None));
        self.tableWidget.setSortingEnabled(__sortingEnabled)

        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.MainTab), QCoreApplication.translate("MasterAPP", u"Main", None))
#if QT_CONFIG(tooltip)
        self.historyButton.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This button clears the entire history list, excluding time of MasterAPP launch.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.historyButton.setText(QCoreApplication.translate("MasterAPP", u"Clear", None))
#if QT_CONFIG(tooltip)
        self.historyButton_2.setToolTip(QCoreApplication.translate("MasterAPP", u"This variable exports history as a text file.", None))
#endif // QT_CONFIG(tooltip)
        self.historyButton_2.setText(QCoreApplication.translate("MasterAPP", u"Export", None))
        self.historyList.setHtml(QCoreApplication.translate("MasterAPP", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.HistoryTab), QCoreApplication.translate("MasterAPP", u"History", None))
        self.ServerGroupBox.setTitle(QCoreApplication.translate("MasterAPP", u"External Servers", None))
        self.le_apiAddress.setInputMask("")
        self.le_apiAddress.setPlaceholderText(QCoreApplication.translate("MasterAPP", u"0.0.0.0 (This Machine)", None))
        self.label_4.setText(QCoreApplication.translate("MasterAPP", u":", None))
        self.le_apiPort.setPlaceholderText(QCoreApplication.translate("MasterAPP", u"1000", None))
#if QT_CONFIG(tooltip)
        self.cb_apiAllowed.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable disables or enables the MasterAPP API client.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.cb_apiAllowed.setText(QCoreApplication.translate("MasterAPP", u"Enabled", None))
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable controls the host and port of the API server MasterAPP API client will connect to.</p><p>Default address - This machine:1000</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("MasterAPP", u"API Address: ", None))
        self.le_plcAddress.setInputMask("")
        self.le_plcAddress.setPlaceholderText(QCoreApplication.translate("MasterAPP", u"0.0.0.0 (This Machine)", None))
        self.label_5.setText(QCoreApplication.translate("MasterAPP", u":", None))
        self.le_plcPort.setPlaceholderText(QCoreApplication.translate("MasterAPP", u"502", None))
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable controls the host and port of the PLC server MasterAPP PLC client will connect to..</p><p>Default address - This machine:1001</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("MasterAPP", u"PLC Address: ", None))
#if QT_CONFIG(tooltip)
        self.cb_plcAllowed.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable disables or enables the MasterAPP PLC client.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.cb_plcAllowed.setText(QCoreApplication.translate("MasterAPP", u"Enabled", None))
#if QT_CONFIG(tooltip)
        self.label_9.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable controls the address and port of the AX-DOOR terminal MasterAPP AX server will listen to.</p><p>Default address - 192.168.11.50:11854</p><p>AX-DOOR backup address - 192.168.1.240:80</p><p>! The AX-DOOR backup address is the address of default settings of the AX-DOOR terminal. Only use the backup address if you have problems with the given default address and if dip-6 on the AX-DOOR is set to ON</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_9.setText(QCoreApplication.translate("MasterAPP", u"AX Address: ", None))
#if QT_CONFIG(tooltip)
        self.cb_axAllowed.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable disables or enables the MasterAPP AX server.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.cb_axAllowed.setText(QCoreApplication.translate("MasterAPP", u"Enabled", None))
        self.le_axAddress.setInputMask("")
        self.le_axAddress.setPlaceholderText(QCoreApplication.translate("MasterAPP", u"192.168.11.50", None))
        self.label_10.setText(QCoreApplication.translate("MasterAPP", u":", None))
        self.le_axPort.setPlaceholderText(QCoreApplication.translate("MasterAPP", u"11854", None))
        self.IntervalGroup.setTitle(QCoreApplication.translate("MasterAPP", u"Intervals", None))
#if QT_CONFIG(tooltip)
        self.dsb_apiInterval.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>The interval between attempts at communicating with API and PLC servers. If fails once, connection is lost.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.dsb_apiInterval.setSuffix(QCoreApplication.translate("MasterAPP", u"s", None))
#if QT_CONFIG(tooltip)
        self.l_axInterval.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable shows in how long does AX-Door sends a request.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.l_axInterval.setText(QCoreApplication.translate("MasterAPP", u"00", None))
#if QT_CONFIG(tooltip)
        self.l_plcInterval.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable shows in how long does MasterAPP executes GetCables.</p><p><br/></p><p>First execution always synchronizes to a minute.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.l_plcInterval.setText(QCoreApplication.translate("MasterAPP", u"00", None))
#if QT_CONFIG(tooltip)
        self.dsb_plcInterval.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>The interval between attempts at updating the cable information.</p><p>If fails once, connection is lost.</p><p>Cannot be changed during update Loop.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.dsb_plcInterval.setSuffix(QCoreApplication.translate("MasterAPP", u"s", None))
#if QT_CONFIG(tooltip)
        self.dsb_axInterval.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>The interval between attempts at communicating with API and PLC servers. If fails once, connection is lost.</p><p>Will be updated on the next request interval.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.dsb_axInterval.setSuffix(QCoreApplication.translate("MasterAPP", u"s", None))
        self.sb_retryInterval.setSuffix(QCoreApplication.translate("MasterAPP", u"s", None))
#if QT_CONFIG(tooltip)
        self.l_retryInterval.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable shows in how long does MasterAPP executes Retry.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.l_retryInterval.setText(QCoreApplication.translate("MasterAPP", u"00", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable controls the interval between individual attempts at connection to API and PLC servers.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("MasterAPP", u"Retry Interval:", None))
#if QT_CONFIG(tooltip)
        self.label_6.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable controls the interval between Idle messages to API.</p><p>MasterAPP periodically sends a http GET request on which API responds in case of an update.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("MasterAPP", u"API Idle Message Interval:", None))
#if QT_CONFIG(tooltip)
        self.label_14.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable controls the interval between keepAlive messages from AX-DOOR.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_14.setText(QCoreApplication.translate("MasterAPP", u"AX Request Interval:", None))
#if QT_CONFIG(tooltip)
        self.label_22.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable controls the interval between updating Cable information from both API and PLC.</p><p>MasterAPP periodically sends a request on which API responds with Rider information, then sends the same for PLC which responds with Cable information</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_22.setText(QCoreApplication.translate("MasterAPP", u"PLC Cable Update Interval:", None))
#if QT_CONFIG(tooltip)
        self.l_apiInterval.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable shows in how long does MasterAPP sends an Idle Message</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.l_apiInterval.setText(QCoreApplication.translate("MasterAPP", u"00", None))
        self.groupBox.setTitle(QCoreApplication.translate("MasterAPP", u"MasterAPP", None))
#if QT_CONFIG(tooltip)
        self.pb_retry.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This button manually restarts the MasterApp Clients during runtime.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_retry.setText(QCoreApplication.translate("MasterAPP", u"Retry", None))
#if QT_CONFIG(tooltip)
        self.pb_changeDir.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This button opens option to set new directory.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_changeDir.setText(QCoreApplication.translate("MasterAPP", u"Change Directory", None))
#if QT_CONFIG(tooltip)
        self.label_12.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_12.setText(QCoreApplication.translate("MasterAPP", u"Cable Update", None))
#if QT_CONFIG(tooltip)
        self.cb_auto_retry.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable automatically restarts the MasterApp Clients after losing connections with servers.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.cb_auto_retry.setText(QCoreApplication.translate("MasterAPP", u"Auto", None))
#if QT_CONFIG(tooltip)
        self.label_16.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable controls the number of Cables that will be loaded from the servers.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_16.setText(QCoreApplication.translate("MasterAPP", u"Cable Count:", None))
#if QT_CONFIG(tooltip)
        self.pb_updateCables.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This button manually updates cables, or triggers the automatic PLC Cable update</p><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_updateCables.setText(QCoreApplication.translate("MasterAPP", u"GetCables", None))
#if QT_CONFIG(tooltip)
        self.cb_auto_cableUpdate.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable decides if GetCable triggers update loop, or only sends a single request for cable update. Also, automatically triggers during start if enabled.</p><p>!First activation delays the update to the next minute!</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.cb_auto_cableUpdate.setText(QCoreApplication.translate("MasterAPP", u"Auto", None))
#if QT_CONFIG(tooltip)
        self.pb_stopClients.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This button interrupts retry and disables listeners and update loop.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_stopClients.setText(QCoreApplication.translate("MasterAPP", u"Stop", None))
#if QT_CONFIG(tooltip)
        self.cb_auto_startClients.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable automatically starts the MasterApp Clients after MasterAPP startup.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.cb_auto_startClients.setText(QCoreApplication.translate("MasterAPP", u"Auto", None))
#if QT_CONFIG(tooltip)
        self.label_13.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_13.setText(QCoreApplication.translate("MasterAPP", u"Stop Servers:", None))
#if QT_CONFIG(tooltip)
        self.label_20.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable controls where the state data will be saved.</p><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_20.setText(QCoreApplication.translate("MasterAPP", u"Save Directory:", None))
#if QT_CONFIG(tooltip)
        self.pb_startClients.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This button manually starts the MasterApp Clients.</p><p>1. Tests connection for enabled addresses</p><p>2. Starts listeners</p><p>3. Updates cables from enabled servers</p><p>4. PLC update loop, and listens for API updates</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_startClients.setText(QCoreApplication.translate("MasterAPP", u"Start", None))
#if QT_CONFIG(tooltip)
        self.cb_auto_cableCount.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable automatically gets the max amount of Cables from the servers after successful connection.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.cb_auto_cableCount.setText(QCoreApplication.translate("MasterAPP", u"Auto", None))
#if QT_CONFIG(tooltip)
        self.label_15.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_15.setText(QCoreApplication.translate("MasterAPP", u"Restart Clients:", None))
#if QT_CONFIG(tooltip)
        self.label_11.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_11.setText(QCoreApplication.translate("MasterAPP", u"Start Clients:", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MasterAPP", u"External Domain", None))
#if QT_CONFIG(tooltip)
        self.label_18.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable controls the address and port of the domain where MasterAPP will send data of the state of the cables.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_18.setText(QCoreApplication.translate("MasterAPP", u"Domain:", None))
#if QT_CONFIG(tooltip)
        self.label_17.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable controls whether and how new data will be sent to the selected domain. </p><p>This is performed automatically by Update function.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_17.setText(QCoreApplication.translate("MasterAPP", u"Save State of Quido:", None))
#if QT_CONFIG(tooltip)
        self.label_21.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_21.setText(QCoreApplication.translate("MasterAPP", u"Minimal Minute State:", None))
#if QT_CONFIG(tooltip)
        self.pb_MMState.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable affects how MasterAPP evaluates whether Cable was running in a minute. (True)</p><p>1/60s - MasterAPP will evaluate True if it was ON a single second</p><p>60/60s - MasterAPP will only evaluate True if it was ON the whole minute</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_MMState.setSuffix(QCoreApplication.translate("MasterAPP", u"/60s", None))
        self.pb_MMState.setPrefix("")
#if QT_CONFIG(tooltip)
        self.pb_SaveStateData.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This button manually triggers save function.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_SaveStateData.setText(QCoreApplication.translate("MasterAPP", u"SaveStateData", None))
        self.pb_changeDomain.setText(QCoreApplication.translate("MasterAPP", u"Change Domain", None))
        self.cb_SaveStyle.setItemText(0, QCoreApplication.translate("MasterAPP", u"Don't save", None))
        self.cb_SaveStyle.setItemText(1, QCoreApplication.translate("MasterAPP", u"Only save", None))
        self.cb_SaveStyle.setItemText(2, QCoreApplication.translate("MasterAPP", u"Send one", None))
        self.cb_SaveStyle.setItemText(3, QCoreApplication.translate("MasterAPP", u"Send all", None))

#if QT_CONFIG(tooltip)
        self.cb_SaveStyle.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>Don't save - Will never save new data from quido</p><p>Only save - Will only save data from quido</p><p>Save and send one - Will save data from quido and send new to selected domain</p><p>Save and send all - Will save data from quido and send all to selected domain (in case data is not synchronized)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.cb_SaveStyle.setCurrentText(QCoreApplication.translate("MasterAPP", u"Don't save", None))
#if QT_CONFIG(tooltip)
        self.l_domainHost.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable controls the address and port of the domain where MasterAPP will send data of the state of the cables.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.l_domainHost.setText(QCoreApplication.translate("MasterAPP", u"wakearealy.cz", None))
        self.le_areal.setText("")
        self.le_areal.setPlaceholderText("")
#if QT_CONFIG(tooltip)
        self.l_saveStateTimer.setToolTip(QCoreApplication.translate("MasterAPP", u"<html><head/><body><p>This variable shows when MasterAPP executes SaveStateData</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.l_saveStateTimer.setText(QCoreApplication.translate("MasterAPP", u"00", None))
        self.l_workloadPath.setText(QCoreApplication.translate("MasterAPP", u"/Workload", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.SettingsTab), QCoreApplication.translate("MasterAPP", u"Settings", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.graphTab), QCoreApplication.translate("MasterAPP", u"Workload", None))
        self.cableLabel_1.setText(QCoreApplication.translate("MasterAPP", u"Cable0", None))
        self.statusImage_1.setText("")
        ___qtablewidgetitem13 = self.tableWidget_1.horizontalHeaderItem(0)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MasterAPP", u"New Column", None));
        ___qtablewidgetitem14 = self.tableWidget_1.verticalHeaderItem(0)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MasterAPP", u"CableState", None));
        ___qtablewidgetitem15 = self.tableWidget_1.verticalHeaderItem(1)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MasterAPP", u"RiderState", None));
        ___qtablewidgetitem16 = self.tableWidget_1.verticalHeaderItem(2)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MasterAPP", u"RiderID", None));
        ___qtablewidgetitem17 = self.tableWidget_1.verticalHeaderItem(3)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MasterAPP", u"Position", None));
        ___qtablewidgetitem18 = self.tableWidget_1.verticalHeaderItem(4)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MasterAPP", u"Speed", None));
        ___qtablewidgetitem19 = self.tableWidget_1.verticalHeaderItem(5)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MasterAPP", u"Error", None));

        __sortingEnabled1 = self.tableWidget_1.isSortingEnabled()
        self.tableWidget_1.setSortingEnabled(False)
        ___qtablewidgetitem20 = self.tableWidget_1.item(0, 0)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MasterAPP", u"0,1,2,4", None));
        ___qtablewidgetitem21 = self.tableWidget_1.item(1, 0)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MasterAPP", u"0,1,2", None));
        ___qtablewidgetitem22 = self.tableWidget_1.item(2, 0)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MasterAPP", u"####", None));
        ___qtablewidgetitem23 = self.tableWidget_1.item(3, 0)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MasterAPP", u"m", None));
        ___qtablewidgetitem24 = self.tableWidget_1.item(4, 0)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MasterAPP", u"m/s", None));
        ___qtablewidgetitem25 = self.tableWidget_1.item(5, 0)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MasterAPP", u"X 0000", None));
        self.tableWidget_1.setSortingEnabled(__sortingEnabled1)

    # retranslateUi

