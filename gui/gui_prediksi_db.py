# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_prediksi_db.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(818, 603)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Main/logo_unikom_kuning.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 2)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.judul = QtWidgets.QLabel(self.centralwidget)
        self.judul.setEnabled(True)
        self.judul.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.judul.setFont(font)
        self.judul.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.judul.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.judul.setLineWidth(0)
        self.judul.setTextFormat(QtCore.Qt.PlainText)
        self.judul.setScaledContents(False)
        self.judul.setAlignment(QtCore.Qt.AlignCenter)
        self.judul.setIndent(0)
        self.judul.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.judul.setObjectName("judul")
        self.verticalLayout.addWidget(self.judul)
        self.frame_4 = QtWidgets.QFrame(self.centralwidget)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout.setContentsMargins(9, 0, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(671, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pbKembali = QtWidgets.QPushButton(self.frame_4)
        self.pbKembali.setMinimumSize(QtCore.QSize(100, 0))
        self.pbKembali.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pbKembali.setObjectName("pbKembali")
        self.horizontalLayout.addWidget(self.pbKembali)
        self.verticalLayout.addWidget(self.frame_4)
        self.asd = QtWidgets.QGroupBox(self.centralwidget)
        self.asd.setTitle("")
        self.asd.setFlat(True)
        self.asd.setObjectName("asd")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.asd)
        self.horizontalLayout_2.setContentsMargins(9, 5, 9, 5)
        self.horizontalLayout_2.setSpacing(3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.DataLatih = QtWidgets.QGroupBox(self.asd)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DataLatih.sizePolicy().hasHeightForWidth())
        self.DataLatih.setSizePolicy(sizePolicy)
        self.DataLatih.setObjectName("DataLatih")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.DataLatih)
        self.verticalLayout_2.setContentsMargins(5, 1, 5, 1)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_3 = QtWidgets.QFrame(self.DataLatih)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.frame_3)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.leNim = QtWidgets.QLineEdit(self.frame_3)
        self.leNim.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.leNim.setText("")
        self.leNim.setObjectName("leNim")
        self.horizontalLayout_3.addWidget(self.leNim)
        self.pbCari = QtWidgets.QPushButton(self.frame_3)
        self.pbCari.setObjectName("pbCari")
        self.horizontalLayout_3.addWidget(self.pbCari)
        self.pbReset = QtWidgets.QPushButton(self.frame_3)
        self.pbReset.setObjectName("pbReset")
        self.horizontalLayout_3.addWidget(self.pbReset)
        spacerItem1 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.label_15 = QtWidgets.QLabel(self.frame_3)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_3.addWidget(self.label_15)
        self.leJml_2 = QtWidgets.QLineEdit(self.frame_3)
        self.leJml_2.setMaximumSize(QtCore.QSize(75, 16777215))
        self.leJml_2.setText("")
        self.leJml_2.setReadOnly(True)
        self.leJml_2.setObjectName("leJml_2")
        self.horizontalLayout_3.addWidget(self.leJml_2)
        self.verticalLayout_2.addWidget(self.frame_3)
        self.tbDataDB = QtWidgets.QTableWidget(self.DataLatih)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tbDataDB.sizePolicy().hasHeightForWidth())
        self.tbDataDB.setSizePolicy(sizePolicy)
        self.tbDataDB.setMinimumSize(QtCore.QSize(0, 170))
        self.tbDataDB.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tbDataDB.setAutoFillBackground(True)
        self.tbDataDB.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tbDataDB.setAlternatingRowColors(True)
        self.tbDataDB.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tbDataDB.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tbDataDB.setObjectName("tbDataDB")
        self.tbDataDB.setColumnCount(19)
        self.tbDataDB.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        item.setFont(font)
        self.tbDataDB.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tbDataDB.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tbDataDB.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tbDataDB.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tbDataDB.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tbDataDB.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tbDataDB.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tbDataDB.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tbDataDB.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tbDataDB.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tbDataDB.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tbDataDB.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tbDataDB.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tbDataDB.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tbDataDB.setHorizontalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tbDataDB.setHorizontalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tbDataDB.setHorizontalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tbDataDB.setHorizontalHeaderItem(17, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tbDataDB.setHorizontalHeaderItem(18, item)
        self.tbDataDB.horizontalHeader().setDefaultSectionSize(60)
        self.verticalLayout_2.addWidget(self.tbDataDB)
        self.horizontalLayout_2.addWidget(self.DataLatih)
        self.groupBox_3 = QtWidgets.QGroupBox(self.asd)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pbPilih = QtWidgets.QPushButton(self.groupBox_3)
        self.pbPilih.setDefault(False)
        self.pbPilih.setObjectName("pbPilih")
        self.verticalLayout_3.addWidget(self.pbPilih)
        self.pbPilihAll = QtWidgets.QPushButton(self.groupBox_3)
        self.pbPilihAll.setObjectName("pbPilihAll")
        self.verticalLayout_3.addWidget(self.pbPilihAll)
        self.line = QtWidgets.QFrame(self.groupBox_3)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(1)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.pbHapus = QtWidgets.QPushButton(self.groupBox_3)
        self.pbHapus.setObjectName("pbHapus")
        self.verticalLayout_3.addWidget(self.pbHapus)
        self.pbHapusAll = QtWidgets.QPushButton(self.groupBox_3)
        self.pbHapusAll.setObjectName("pbHapusAll")
        self.verticalLayout_3.addWidget(self.pbHapusAll)
        spacerItem2 = QtWidgets.QSpacerItem(20, 18, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.label_14 = QtWidgets.QLabel(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_3.addWidget(self.label_14)
        self.laJmlPil = QtWidgets.QLineEdit(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.laJmlPil.sizePolicy().hasHeightForWidth())
        self.laJmlPil.setSizePolicy(sizePolicy)
        self.laJmlPil.setMaximumSize(QtCore.QSize(90, 16777215))
        self.laJmlPil.setText("")
        self.laJmlPil.setAlignment(QtCore.Qt.AlignCenter)
        self.laJmlPil.setReadOnly(True)
        self.laJmlPil.setObjectName("laJmlPil")
        self.verticalLayout_3.addWidget(self.laJmlPil)
        self.pbProPre = QtWidgets.QPushButton(self.groupBox_3)
        self.pbProPre.setMinimumSize(QtCore.QSize(90, 50))
        self.pbProPre.setFlat(False)
        self.pbProPre.setObjectName("pbProPre")
        self.verticalLayout_3.addWidget(self.pbProPre)
        self.horizontalLayout_2.addWidget(self.groupBox_3)
        self.DataLatih_2 = QtWidgets.QGroupBox(self.asd)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DataLatih_2.sizePolicy().hasHeightForWidth())
        self.DataLatih_2.setSizePolicy(sizePolicy)
        self.DataLatih_2.setMinimumSize(QtCore.QSize(0, 0))
        self.DataLatih_2.setMaximumSize(QtCore.QSize(120, 16777215))
        self.DataLatih_2.setBaseSize(QtCore.QSize(0, 0))
        self.DataLatih_2.setObjectName("DataLatih_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.DataLatih_2)
        self.gridLayout_2.setContentsMargins(5, 5, 5, 1)
        self.gridLayout_2.setHorizontalSpacing(0)
        self.gridLayout_2.setVerticalSpacing(5)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tbDataPil = QtWidgets.QTableWidget(self.DataLatih_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tbDataPil.sizePolicy().hasHeightForWidth())
        self.tbDataPil.setSizePolicy(sizePolicy)
        self.tbDataPil.setMinimumSize(QtCore.QSize(0, 170))
        self.tbDataPil.setMaximumSize(QtCore.QSize(120, 16777215))
        self.tbDataPil.setBaseSize(QtCore.QSize(0, 0))
        self.tbDataPil.setAutoFillBackground(True)
        self.tbDataPil.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tbDataPil.setAlternatingRowColors(True)
        self.tbDataPil.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tbDataPil.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tbDataPil.setObjectName("tbDataPil")
        self.tbDataPil.setColumnCount(1)
        self.tbDataPil.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        item.setFont(font)
        self.tbDataPil.setHorizontalHeaderItem(0, item)
        self.tbDataPil.horizontalHeader().setDefaultSectionSize(60)
        self.gridLayout_2.addWidget(self.tbDataPil, 0, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.DataLatih_2)
        self.verticalLayout.addWidget(self.asd)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setFlat(True)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setContentsMargins(-1, 5, -1, 5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_2 = QtWidgets.QFrame(self.groupBox_2)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frame = QtWidgets.QFrame(self.frame_2)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_6.setContentsMargins(-1, 5, -1, 5)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_6.addWidget(self.label_2)
        self.leNim2 = QtWidgets.QLineEdit(self.frame)
        self.leNim2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.leNim2.setText("")
        self.leNim2.setObjectName("leNim2")
        self.horizontalLayout_6.addWidget(self.leNim2)
        self.pbCari2 = QtWidgets.QPushButton(self.frame)
        self.pbCari2.setMaximumSize(QtCore.QSize(125, 16777215))
        self.pbCari2.setObjectName("pbCari2")
        self.horizontalLayout_6.addWidget(self.pbCari2)
        self.pbReset2 = QtWidgets.QPushButton(self.frame)
        self.pbReset2.setMaximumSize(QtCore.QSize(125, 16777215))
        self.pbReset2.setObjectName("pbReset2")
        self.horizontalLayout_6.addWidget(self.pbReset2)
        self.horizontalLayout_4.addWidget(self.frame)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.label_12 = QtWidgets.QLabel(self.frame_2)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_4.addWidget(self.label_12)
        self.leWaktu = QtWidgets.QLineEdit(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leWaktu.sizePolicy().hasHeightForWidth())
        self.leWaktu.setSizePolicy(sizePolicy)
        self.leWaktu.setMaximumSize(QtCore.QSize(100, 16777215))
        self.leWaktu.setText("")
        self.leWaktu.setReadOnly(True)
        self.leWaktu.setObjectName("leWaktu")
        self.horizontalLayout_4.addWidget(self.leWaktu)
        spacerItem4 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.label_13 = QtWidgets.QLabel(self.frame_2)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_4.addWidget(self.label_13)
        self.leJml2 = QtWidgets.QLineEdit(self.frame_2)
        self.leJml2.setMaximumSize(QtCore.QSize(75, 16777215))
        self.leJml2.setText("")
        self.leJml2.setReadOnly(True)
        self.leJml2.setObjectName("leJml2")
        self.horizontalLayout_4.addWidget(self.leJml2)
        spacerItem5 = QtWidgets.QSpacerItem(25, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.verticalLayout_4.addWidget(self.frame_2)
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_5.setFlat(False)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.tbPrediksi = QtWidgets.QTableWidget(self.groupBox_5)
        self.tbPrediksi.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tbPrediksi.setAutoFillBackground(True)
        self.tbPrediksi.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tbPrediksi.setDragDropOverwriteMode(False)
        self.tbPrediksi.setAlternatingRowColors(True)
        self.tbPrediksi.setObjectName("tbPrediksi")
        self.tbPrediksi.setColumnCount(3)
        self.tbPrediksi.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tbPrediksi.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tbPrediksi.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.tbPrediksi.setHorizontalHeaderItem(2, item)
        self.tbPrediksi.horizontalHeader().setDefaultSectionSize(50)
        self.tbPrediksi.horizontalHeader().setMinimumSectionSize(25)
        self.verticalLayout_6.addWidget(self.tbPrediksi)
        self.verticalLayout_4.addWidget(self.groupBox_5)
        self.verticalLayout.addWidget(self.groupBox_2)
        MainWindow.setCentralWidget(self.centralwidget)
        regex = QtCore.QRegExp("[0-9_]+")
        validator = QtGui.QRegExpValidator(regex)
        self.leNim.setValidator(validator)
        self.leNim.setMaxLength(8)
        self.leNim2.setValidator(validator)
        self.leNim2.setMaxLength(8)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.judul.setText(_translate("MainWindow", "Menu Prediksi ANN Backpropagation Dari Database"))
        self.pbKembali.setToolTip(_translate("MainWindow", "Kembali ke menu utama"))
        self.pbKembali.setText(_translate("MainWindow", "Kembali"))
        self.DataLatih.setTitle(_translate("MainWindow", "Data akademik di database"))
        self.label.setText(_translate("MainWindow", "NIM"))
        self.leNim.setPlaceholderText(_translate("MainWindow", "NIM (102XXXXX)"))
        self.pbCari.setText(_translate("MainWindow", "Cari / Filter"))
        self.pbReset.setText(_translate("MainWindow", "Reset"))
        self.label_15.setText(_translate("MainWindow", "Jumlah Data"))
        self.leJml_2.setPlaceholderText(_translate("MainWindow", "0"))
        self.tbDataDB.setSortingEnabled(True)
        item = self.tbDataDB.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "NIM"))
        item = self.tbDataDB.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "IPS 1"))
        item = self.tbDataDB.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "IPS 2"))
        item = self.tbDataDB.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "IPS 3"))
        item = self.tbDataDB.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "IPS 4"))
        item = self.tbDataDB.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Fiska 1"))
        item = self.tbDataDB.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Matematika 1"))
        item = self.tbDataDB.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Fisika 2"))
        item = self.tbDataDB.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "Matematika 2"))
        item = self.tbDataDB.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow", "Algoritma Pemograman"))
        item = self.tbDataDB.horizontalHeaderItem(10)
        item.setText(_translate("MainWindow", "Elektronika 1"))
        item = self.tbDataDB.horizontalHeaderItem(11)
        item.setText(_translate("MainWindow", "Teori Sistem & Sinyal"))
        item = self.tbDataDB.horizontalHeaderItem(12)
        item.setText(_translate("MainWindow", "Organisasi & Arsitektur Komputer 1"))
        item = self.tbDataDB.horizontalHeaderItem(13)
        item.setText(_translate("MainWindow", "Sistem Digital"))
        item = self.tbDataDB.horizontalHeaderItem(14)
        item.setText(_translate("MainWindow", "Elektronika 2"))
        item = self.tbDataDB.horizontalHeaderItem(15)
        item.setText(_translate("MainWindow", "Struktur Data"))
        item = self.tbDataDB.horizontalHeaderItem(16)
        item.setText(_translate("MainWindow", "Matematika Diskrit"))
        item = self.tbDataDB.horizontalHeaderItem(17)
        item.setText(_translate("MainWindow", "Komunikasi Data"))
        item = self.tbDataDB.horizontalHeaderItem(18)
        item.setText(_translate("MainWindow", "Aljabar Linear"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Tools"))
        self.pbPilih.setToolTip(_translate("MainWindow", "Membaca data pengujian"))
        self.pbPilih.setText(_translate("MainWindow", "Pilih"))
        self.pbPilihAll.setText(_translate("MainWindow", "Pilih Semua"))
        self.pbHapus.setText(_translate("MainWindow", "Hapus"))
        self.pbHapusAll.setText(_translate("MainWindow", "Hapus Semua"))
        self.label_14.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Jumlah data<br/>yang dipilih:</p></body></html>"))
        self.laJmlPil.setPlaceholderText(_translate("MainWindow", "0"))
        self.pbProPre.setText(_translate("MainWindow", "Mulai Proses\n"
"Prediksi"))
        self.DataLatih_2.setTitle(_translate("MainWindow", "Data yang dipilih"))
        self.tbDataPil.setSortingEnabled(True)
        self.tbDataPil.setColumnWidth(0, 200)
        item = self.tbDataPil.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "NIM"))
        self.label_2.setText(_translate("MainWindow", "NIM"))
        self.leNim2.setPlaceholderText(_translate("MainWindow", "NIM (102XXXXX)"))
        self.pbCari2.setText(_translate("MainWindow", "Cari / Filter"))
        self.pbReset2.setText(_translate("MainWindow", "Reset"))
        self.label_12.setText(_translate("MainWindow", "Waktu Prediksi"))
        self.leWaktu.setPlaceholderText(_translate("MainWindow", "detik (second)"))
        self.label_13.setText(_translate("MainWindow", "Jumlah Data"))
        self.leJml2.setPlaceholderText(_translate("MainWindow", "0"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Hasil Prediksi"))
        self.tbPrediksi.setSortingEnabled(True)
        self.tbPrediksi.setColumnWidth(0, 60)
        item = self.tbPrediksi.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "NIM"))
        self.tbPrediksi.setColumnWidth(1, 100)
        item = self.tbPrediksi.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Hasil Prediksi IPK"))
        self.tbPrediksi.setColumnWidth(2, 1200)
        item = self.tbPrediksi.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Responsi"))
import gui.sourcesGambar_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())