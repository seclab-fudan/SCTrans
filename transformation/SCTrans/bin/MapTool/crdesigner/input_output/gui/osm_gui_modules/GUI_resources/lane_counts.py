# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lane_counts.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(182, 425)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 5, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 6, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 4, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 7, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.frame)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 10, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.frame)
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 13, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.frame)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 11, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.frame)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 12, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 8, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.frame)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 9, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.frame)
        self.label_15.setObjectName("label_15")
        self.gridLayout_3.addWidget(self.label_15, 14, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.frame)
        self.label_16.setObjectName("label_16")
        self.gridLayout_3.addWidget(self.label_16, 15, 0, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.frame)
        self.label_17.setObjectName("label_17")
        self.gridLayout_3.addWidget(self.label_17, 16, 0, 1, 1)

        self.sb_motorway = QtWidgets.QSpinBox(self.frame)
        self.sb_motorway.setMaximum(1000000)
        self.sb_motorway.setObjectName("sb_motorway")
        self.gridLayout_3.addWidget(self.sb_motorway, 0, 1, 1, 1)
        self.sb_trunk = QtWidgets.QSpinBox(self.frame)
        self.sb_trunk.setMaximum(1000000)
        self.sb_trunk.setObjectName("sb_trunk")
        self.gridLayout_3.addWidget(self.sb_trunk, 1, 1, 1, 1)
        self.sb_primary = QtWidgets.QSpinBox(self.frame)
        self.sb_primary.setMaximum(1000000)
        self.sb_primary.setObjectName("sb_primary")
        self.gridLayout_3.addWidget(self.sb_primary, 2, 1, 1, 1)
        self.sb_secondary = QtWidgets.QSpinBox(self.frame)
        self.sb_secondary.setMaximum(1000000)
        self.sb_secondary.setObjectName("sb_secondary")
        self.gridLayout_3.addWidget(self.sb_secondary, 3, 1, 1, 1)
        self.sb_tertiary = QtWidgets.QSpinBox(self.frame)
        self.sb_tertiary.setMaximum(1000000)
        self.sb_tertiary.setObjectName("sb_tertiary")
        self.gridLayout_3.addWidget(self.sb_tertiary, 4, 1, 1, 1)
        self.sb_unclassified = QtWidgets.QSpinBox(self.frame)
        self.sb_unclassified.setMaximum(1000000)
        self.sb_unclassified.setObjectName("sb_unclassified")
        self.gridLayout_3.addWidget(self.sb_unclassified, 5, 1, 1, 1)
        self.sb_residential = QtWidgets.QSpinBox(self.frame)
        self.sb_residential.setMaximum(1000000)
        self.sb_residential.setObjectName("sb_residential")
        self.gridLayout_3.addWidget(self.sb_residential, 6, 1, 1, 1)
        self.sb_motorway_link = QtWidgets.QSpinBox(self.frame)
        self.sb_motorway_link.setMaximum(1000000)
        self.sb_motorway_link.setObjectName("sb_motorway_link")
        self.gridLayout_3.addWidget(self.sb_motorway_link, 7, 1, 1, 1)
        self.sb_trunk_link = QtWidgets.QSpinBox(self.frame)
        self.sb_trunk_link.setMaximum(1000000)
        self.sb_trunk_link.setObjectName("sb_trunk_link")
        self.gridLayout_3.addWidget(self.sb_trunk_link, 8, 1, 1, 1)
        self.sb_primary_link = QtWidgets.QSpinBox(self.frame)
        self.sb_primary_link.setMaximum(1000000)
        self.sb_primary_link.setObjectName("sb_primary_link")
        self.gridLayout_3.addWidget(self.sb_primary_link, 9, 1, 1, 1)
        self.sb_secondary_link = QtWidgets.QSpinBox(self.frame)
        self.sb_secondary_link.setMaximum(1000000)
        self.sb_secondary_link.setObjectName("sb_secondary_link")
        self.gridLayout_3.addWidget(self.sb_secondary_link, 10, 1, 1, 1)
        self.sb_tertiary_link = QtWidgets.QSpinBox(self.frame)
        self.sb_tertiary_link.setMaximum(1000000)
        self.sb_tertiary_link.setObjectName("sb_tertiary_link")
        self.gridLayout_3.addWidget(self.sb_tertiary_link, 11, 1, 1, 1)
        self.sb_living_street = QtWidgets.QSpinBox(self.frame)
        self.sb_living_street.setMaximum(1000000)
        self.sb_living_street.setObjectName("sb_living_street")
        self.gridLayout_3.addWidget(self.sb_living_street, 12, 1, 1, 1)
        self.sb_service = QtWidgets.QSpinBox(self.frame)
        self.sb_service.setMaximum(1000000)
        self.sb_service.setObjectName("sb_service")
        self.gridLayout_3.addWidget(self.sb_service, 13, 1, 1, 1)
        self.sb_path = QtWidgets.QSpinBox(self.frame)
        self.sb_path.setMaximum(1000000)
        self.sb_path.setObjectName("sb_path")
        self.gridLayout_3.addWidget(self.sb_path, 14, 1, 1, 1)
        self.sb_footway = QtWidgets.QSpinBox(self.frame)
        self.sb_footway.setMaximum(1000000)
        self.sb_footway.setObjectName("sb_footway")
        self.gridLayout_3.addWidget(self.sb_footway, 15, 1, 1, 1)
        self.sb_cycleway = QtWidgets.QSpinBox(self.frame)
        self.sb_cycleway.setMaximum(1000000)
        self.sb_cycleway.setObjectName("sb_cycleway")
        self.gridLayout_3.addWidget(self.sb_cycleway, 16, 1, 1, 1)

        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.accepted.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Edit Lane Count"))
        self.label.setText(_translate("Dialog", "motorway"))
        self.label_2.setText(_translate("Dialog", "trunk"))
        self.label_3.setText(_translate("Dialog", "primary"))
        self.label_4.setText(_translate("Dialog", "secondary"))
        self.label_5.setText(_translate("Dialog", "tertiary"))
        self.label_6.setText(_translate("Dialog", "unclassified"))
        self.label_7.setText(_translate("Dialog", "residential"))
        self.label_8.setText(_translate("Dialog", "motorway_link"))
        self.label_9.setText(_translate("Dialog", "trunk_link"))
        self.label_10.setText(_translate("Dialog", "primary_link"))
        self.label_11.setText(_translate("Dialog", "secondary_link"))
        self.label_12.setText(_translate("Dialog", "tertiary_link"))
        self.label_13.setText(_translate("Dialog", "living_street"))
        self.label_14.setText(_translate("Dialog", "service"))
        self.label_15.setText(_translate("Dialog", "path"))
        self.label_16.setText(_translate("Dialog", "footway"))
        self.label_17.setText(_translate("Dialog", "cycleway"))

